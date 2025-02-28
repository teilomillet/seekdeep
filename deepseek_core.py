import chromadb
import requests
import json
import time
from typing import List, Dict, Any, Tuple
from deepseek_data import *

def setup_db(name="research_collection"):
    return chromadb.Client().create_collection(name=name)

def add_docs(collection, texts, ids=None, metadatas=None):
    if ids is None: ids = [f"doc_{i}" for i in range(len(texts))]
    if metadatas is None: metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    collection.add(documents=texts, metadatas=metadatas, ids=ids)
    return collection

def search(collection, query, n_results=3):
    results = collection.query(query_texts=[query], n_results=n_results)
    return [{"text": doc, "metadata": meta, "id": id} for doc, meta, id in 
            zip(results["documents"][0], results["metadatas"][0], results["ids"][0])]

def generate(prompt, model="deepseek-r1:1.5b", base_url="http://localhost:11434/api"):
    response = requests.post(f"{base_url}/generate",
                            json={"model": model, "prompt": prompt, "stream": False})
    return response.json().get("response", "") if response.status_code == 200 else ""

def process_llm_calls(question, context=None, answer=None, mode="decompose"):
    prompts = {"decompose": DECOMPOSE_PROMPT.format(question=question),
              "expand": EXPAND_PROMPT.format(query=question),
              "answer": ANSWER_PROMPT.format(question=question, context=context),
              "evaluate": EVALUATE_PROMPT.format(question=question, answer=answer),
              "beast": BEAST_MODE_PROMPT.format(question=question, full_context=context, 
                                               search_history=answer)}
    result = generate(prompts[mode])
    
    if mode == "decompose":
        return [q.strip() for q in result.split("\n") if q.strip() and "?" in q][:3]
    elif mode == "evaluate":
        passes = all([f"{c}: PASS" in result for c in ["Relevance", "Completeness", "Accuracy", "Clarity"]])
        needs_more = "more research is needed" in result.lower()
        suggested = question
        for line in result.split("\n"):
            if "suggest" in line.lower() and ":" in line:
                suggested = line.split(":", 1)[1].strip()
                break
        return {"passes": passes, "needs_more": needs_more, "suggested": suggested}
    return result

def deep_research(question, collection, max_iterations=3):
    iterations, memory = 0, {"sub_questions": [], "answer_attempts": []}
    search_history, current_query = [], question
    
    # Break down question into sub-questions
    if max_iterations > 1:
        memory["sub_questions"] = process_llm_calls(question, mode="decompose")
    
    while iterations < max_iterations:
        # Expand query if not first iteration
        if iterations > 0 and current_query != question:
            current_query = process_llm_calls(current_query, mode="expand")
            
        # Search phase
        results = search(collection, current_query)
        search_history.append({"query": current_query, "results": results})
        
        # Generate answer
        context_str = "\n".join([f"Doc {i+1}: {doc['text']}" for i, doc in enumerate(results)])
        answer = process_llm_calls(question, context_str, mode="answer")
        memory["answer_attempts"].append({"query": current_query, "answer": answer})
        
        # Check if last iteration - use beast mode
        if iterations == max_iterations - 1:
            history_str = "\n".join([f"Query: {h['query']}" for h in search_history])
            return {"answer": process_llm_calls(question, context_str, history_str, "beast"), 
                    "iterations": iterations + 1, "memory": memory, "beast_mode": True}
        
        # Evaluate answer
        eval_result = process_llm_calls(question, answer=answer, mode="evaluate")
        if not eval_result["needs_more"]:
            return {"answer": answer, "iterations": iterations + 1, "memory": memory}
        
        # Set next query
        if memory["sub_questions"] and iterations < len(memory["sub_questions"]):
            current_query = memory["sub_questions"][iterations]
        else:
            current_query = eval_result["suggested"]
        
        iterations += 1
        time.sleep(1)  # Prevent rate limiting
    
    return {"answer": answer, "iterations": max_iterations, "memory": memory} 