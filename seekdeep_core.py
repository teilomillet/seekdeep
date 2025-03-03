import chromadb
import requests
import time
import re
from seekdeep_data import (
    DECOMPOSE_PROMPT,
    EXPAND_PROMPT,
    ANSWER_PROMPT,
    EVALUATE_PROMPT,
    BEAST_MODE_PROMPT
)

def setup_db(name="research_collection"):
    """
    Creates and initializes a new ChromaDB collection for document storage.
    
    ChromaDB is a vector database that allows for semantic search operations.
    This function connects to a local ChromaDB instance and creates a new collection
    that will store document embeddings.
    
    Args:
        name (str): The name to give the collection. Defaults to "research_collection".
            Using different names allows for multiple separate collections.
            
    Returns:
        Collection: A ChromaDB collection object that can be used to add documents 
        and perform searches.
    """
    return chromadb.Client().create_collection(name=name)

def add_docs(collection, texts, ids=None, metadatas=None):
    """
    Adds documents to a ChromaDB collection with optional custom IDs and metadata.
    
    This function takes a list of text documents and adds them to the specified
    ChromaDB collection. The documents will be automatically converted to vector
    embeddings by ChromaDB for later semantic search operations.
    
    Args:
        collection: The ChromaDB collection where documents will be stored
        texts (list): List of text strings to add to the collection
        ids (list, optional): List of unique IDs for each document. If not provided,
            IDs will be automatically generated in the format "doc_0", "doc_1", etc.
        metadatas (list, optional): List of metadata dictionaries for each document.
            If not provided, default metadata with source information will be created.
            
    Returns:
        Collection: The updated ChromaDB collection with the new documents added.
    """
    # Generate default IDs if none provided
    if ids is None:
        ids = [f"doc_{i}" for i in range(len(texts))]
    # Generate default metadata if none provided
    if metadatas is None:
        metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    # Add the documents, metadata, and IDs to the collection
    collection.add(documents=texts, metadatas=metadatas, ids=ids)
    return collection

def search(collection, query, n_results=3):
    """
    Perform a semantic search on the ChromaDB collection to find relevant documents.
    
    This function uses vector similarity search to find documents in the collection
    that are semantically similar to the input query. The search is based on the
    vector embeddings of both the query and the stored documents.
    
    Args:
        collection: ChromaDB collection to search - must be previously populated with documents
        query (str): Search query string that will be converted to a vector embedding
        n_results (int): Number of most relevant results to return (default: 3)
        
    Returns:
        list: A list of dictionaries, each containing:
            - "text": The document content
            - "metadata": Associated metadata for the document
            - "id": The unique identifier of the document
    """
    # Perform the semantic search - this converts the query to a vector 
    # and finds the most similar document vectors
    results = collection.query(query_texts=[query], n_results=n_results)
    
    # Format the results as a list of dictionaries for easier access
    # ChromaDB returns results in separate lists that we combine here
    search_results = [
        {
            "text": doc,  # The actual document text
            "metadata": meta,  # Any metadata associated with this document
            "id": id  # The unique ID of this document
        } 
        for doc, meta, id in zip(
            results["documents"][0],  # List of document texts
            results["metadatas"][0],  # List of document metadata dictionaries
            results["ids"][0]  # List of document IDs
        )
    ]
    
    return search_results

def generate(prompt, model="deepseek-r1:1.5b", base_url="http://localhost:11434/api"):
    """
    Generate text using a Large Language Model (LLM) via API.
    
    This function sends a text generation request to an LLM API endpoint 
    and returns the model's response. It uses a local API server (by default)
    that should be running the specified model.
    
    Args:
        prompt (str): The text prompt to send to the language model
        model (str): The model identifier to use for generation
                     Default is "deepseek-r1:1.5b"
        base_url (str): The base URL of the API endpoint
                        Default is "http://localhost:11434/api" (local Ollama server)
                        
    Returns:
        str: The generated text response from the model, or an empty string if the request fails
    """
    # Send the API request to the LLM server
    response = requests.post(f"{base_url}/generate",
                           json={"model": model, "prompt": prompt, "stream": False})
    
    # Return the response text if successful, otherwise return empty string
    return response.json().get("response", "") if response.status_code == 200 else ""

def process_llm_calls(question, context=None, answer=None, mode="decompose"):
    """
    Process LLM calls for different modes of research operation.
    
    This function is the central hub for different types of LLM operations needed
    during the research process. It handles several different "modes" of operation:
    
    - decompose: Break down a complex question into simpler sub-questions
    - expand: Enhance a query to improve search results
    - answer: Generate an answer based on a question and relevant context
    - evaluate: Assess whether an answer is complete or needs more research
    - beast: Generate a comprehensive answer using all available information
    
    Args:
        question (str): The question or query to process
        context (str, optional): Contextual information for answer generation,
                                usually search results from the database
        answer (str, optional): An answer to evaluate, used only in evaluate mode
        mode (str): The operation mode - one of: "decompose", "expand", "answer", 
                    "evaluate", or "beast". Default is "decompose".
        
    Returns:
        varies: 
            - decompose mode: list of sub-questions
            - expand mode: str containing enhanced query
            - answer/beast mode: str containing the generated answer
            - evaluate mode: dict with status ("complete" or "incomplete") and 
                           suggested follow-up query if incomplete
    """
    # Select the appropriate prompt template based on the mode
    # Each prompt is filled with the relevant information
    prompts = {
        "decompose": DECOMPOSE_PROMPT.format(question=question),
        "expand": EXPAND_PROMPT.format(query=question),
        "answer": ANSWER_PROMPT.format(question=question, context=context),
        "evaluate": EVALUATE_PROMPT.format(question=question, answer=answer),
        "beast": BEAST_MODE_PROMPT.format(
            question=question, 
            full_context=context, 
            search_history=answer
        )
    }
    
    # Generate response from the LLM using the selected prompt
    result = generate(prompts[mode])
    
    # Remove thinking tags if they exist (some LLM responses include these)
    if "<think>" in result and "</think>" in result:
        result = result.split("</think>", 1)[1].strip()
    
    # Process the result differently based on the mode
    if mode == "decompose":
        # Extract sub-questions from the LLM output
        # We're looking for numbered items or sentences with question marks
        lines = [line.strip() for line in result.split('\n') if line.strip()]
        questions = []
        for line in lines:
            # Match lines that start with a number + period (like "1.") 
            # or lines containing a question mark that are long enough to be real questions
            if re.match(r'^\d+\.', line) or ('?' in line and len(line) > 10):
                questions.append(line)
        
        # If no questions were found, just use the original question
        return questions if questions else [question]
    
    elif mode == "expand":
        # Simply return the expanded query as generated by the LLM
        return result
    
    elif mode == "evaluate":
        # Determine if the answer is satisfactory by looking for specific words
        is_complete = "satisfactory" in result.lower() or "PASS" in result
        
        # If the answer is incomplete, try to extract a suggested follow-up query
        suggested = None
        if not is_complete:
            # First look for lines containing "suggest" and a colon
            for line in result.split('\n'):
                if "suggest" in line.lower() and ":" in line:
                    suggested = line.split(":", 1)[1].strip()
                    break
            
            # If that didn't work, look for lines with question marks
            if not suggested:
                for line in result.split('\n'):
                    if '?' in line and len(line) > 15:
                        suggested = line.strip()
                        break
            
            # If still no suggestion, create a default one
            if not suggested:
                suggested = f"more details about {question}"
        
        # Return a dictionary with status and suggested follow-up (if needed)        
        return {
            "status": "complete" if is_complete else "incomplete",
            "suggested": suggested
        }
    
    else:  # answer or beast mode
        # Simply return the generated text as the answer
        return result

def deep_research(question, collection, max_iterations=3):
    """
    Perform an in-depth research process on a question using iterative decomposition and refinement.
    
    This function implements a research methodology that:
    1. Decomposes a complex question into simpler sub-questions
    2. Processes each sub-question sequentially 
    3. For each sub-question:
       - Expands the query to improve search relevance
       - Searches for relevant documents
       - Generates an answer based on the search results
       - Evaluates if the answer is complete
    4. If all iterations are used, creates a comprehensive "beast mode" answer
       using all the gathered information
    
    Args:
        question (str): The main research question to investigate
        collection: ChromaDB collection containing the knowledge documents to search
        max_iterations (int): Maximum number of research iterations before forced completion
                             (default: 3)
        
    Returns:
        dict: A dictionary containing:
            - "answer" (str): The final answer text
            - "iterations" (int): Number of iterations performed
            - "memory" (dict): Research process data including:
                - "sub_questions": List of decomposed questions
                - "search_history": Search queries and results
                - "answer_attempts": Generated answers for each step
            - "beast_mode" (bool): Whether the answer was generated in beast mode
                                  (only present if beast mode was used)
    """
    # Initialize tracking variables to store the research process
    iterations = 0
    memory = {
        "sub_questions": [],  # Will store the decomposed questions
        "search_history": [],  # Will store search queries and results
        "answer_attempts": []  # Will store answers for each question
    }
    
    # Step 1: Decompose the main question into simpler sub-questions
    # This helps break down complex questions into manageable parts
    sub_questions = process_llm_calls(question, mode="decompose")
    memory["sub_questions"] = sub_questions
    
    # Start with the first sub-question (or the original if decomposition failed)
    current_query = sub_questions[0] if sub_questions else question
    
    # Main research loop - continue until max iterations or satisfactory answer
    while iterations < max_iterations:
        print(f"\n--- Step {iterations + 1} ---")
        print(f"Current question: {current_query}")
        
        # Step 2: Search for relevant information
        # First expand the query to enhance search relevance
        search_query = process_llm_calls(current_query, mode="expand")
        
        # Perform semantic search in the document collection
        search_results = search(collection, search_query)
        
        # Combine all retrieved documents into a single context string
        context_str = "\n\n".join([r["text"] for r in search_results])
        
        # Keep track of search history for later analysis
        memory["search_history"].append({"query": current_query, "results": search_results})
        
        # Step 3: Generate an answer using the retrieved information
        answer = process_llm_calls(current_query, context_str, mode="answer")
        memory["answer_attempts"].append({"query": current_query, "answer": answer})
        
        # Step 4: Special handling for the final iteration
        # If we're on the last iteration, use "beast mode" to create a comprehensive answer
        # that incorporates all the information gathered throughout the process
        if iterations == max_iterations - 1:
            # Create a history string summarizing all queries performed
            history_str = "\n".join([f"Query: {h['query']}" for h in memory["search_history"]])
            
            # Generate a comprehensive answer using beast mode
            beast_answer = process_llm_calls(question, context_str, history_str, "beast")
            
            # Return the final result with all tracking information
            return {
                "answer": beast_answer,
                "iterations": iterations + 1,
                "memory": memory,
                "beast_mode": True  # Flag indicating beast mode was used
            }
        
        # Step 5: Evaluate the current answer
        # Check if the answer is satisfactory or if more research is needed
        eval_result = process_llm_calls(question, answer=answer, mode="evaluate")
        
        # If the answer is complete, return it
        if eval_result["status"] == "complete":
            return {
                "answer": answer,
                "iterations": iterations + 1,
                "memory": memory
            }
        
        # Step 6: Prepare for the next iteration
        iterations += 1
        
        # Select the next question:
        # - If there are more sub-questions, use the next one
        # - Otherwise, use the suggested follow-up from the evaluation
        if iterations < len(sub_questions):
            current_query = sub_questions[iterations]
        else:
            current_query = eval_result["suggested"] if eval_result["suggested"] else question
        
        # Add a small delay to prevent API rate limiting
        time.sleep(1)
    
    # If we've exhausted all iterations and still don't have a complete answer,
    # return the most recent answer with the tracking information
    return {
        "answer": answer,
        "iterations": max_iterations,
        "memory": memory
    }

def deep_search(question, collection, max_iterations=3, token_budget=5000):
    """
    Perform a breadth-first search-based research approach to answer complex questions.
    
    Unlike deep_research which processes sub-questions sequentially, this function:
    1. Maintains a queue of questions (knowledge gaps) to investigate
    2. Uses breadth-first-search to explore the question space
    3. Dynamically adds new questions based on evaluation results
    4. Builds a comprehensive knowledge base from search results
    5. Falls back to "beast mode" if no satisfactory answer is found within iterations
    
    This approach is particularly effective for questions requiring exploration of
    multiple related angles before synthesis into a final answer.
    
    Args:
        question (str): The main research question to investigate
        collection: ChromaDB collection containing the knowledge documents to search
        max_iterations (int): Maximum number of iterations before forced completion
                             (default: 3)
        token_budget (int): Approximate maximum token count to use for context
                           (default: 5000, helps prevent context overflows)
        
    Returns:
        dict: A dictionary containing:
            - "answer" (str): The final answer text
            - "iterations" (int): Number of iterations performed  
            - "gap_questions" (list): All questions investigated during the process
            - "search_history" (list): Search queries and results for each step
            - "beast_mode" (bool): Whether the answer was generated in beast mode
                                  (only present if beast mode was used)
    """
    # Initialize iteration counter
    step = 0
    
    # Initialize tracking data structures
    visited_queries = []  # Questions we've already processed
    search_history = []   # History of all searches performed
    knowledge = []        # Accumulated knowledge from all searches
    
    # Initialize a FIFO queue with the original question as the first gap to fill
    # This queue tracks all the "knowledge gaps" we need to address
    gaps = [question]
    
    # Main reasoning loop - continue until we run out of questions or hit max iterations
    while gaps and step < max_iterations:
        # Get the next question from the queue (breadth-first approach)
        current_question = gaps.pop(0)
        visited_queries.append(current_question)
        
        # Log the current step for monitoring
        print(f"\n--- Step {step + 1} ---")
        print(f"Current question: {current_question}")
        step += 1
        
        # Special handling for the first iteration only
        # Decompose the main question into sub-questions to populate our queue
        if step == 1:
            # Break down the question into sub-questions
            sub_questions = process_llm_calls(current_question, mode="decompose")
            
            # Add each new sub-question to our queue if we haven't seen it before
            for q in sub_questions:
                if q not in visited_queries and q not in gaps:
                    gaps.append(q)
            
            # Make sure the original question is revisited at the end (for synthesis)
            # but only if we have other questions to process first
            if gaps and question not in gaps:
                gaps.append(question)
        
        # Search phase - expand and enrich the search query for better results
        search_query = process_llm_calls(current_question, mode="expand")
        
        # Perform semantic search to find relevant documents
        search_results = search(collection, search_query)
        
        # Record search history for later analysis and use in beast mode
        search_history.append({"query": current_question, "results": search_results})
        
        # Build context by combining all retrieved documents
        context_str = "\n\n".join([r["text"] for r in search_results])
        
        # Add to our accumulated knowledge base
        knowledge.append({"question": current_question, "context": context_str})
        
        # Generate and evaluate an answer, but only after the first step
        # (The first step is just for decomposition and gathering initial info)
        if step > 1:
            # Generate an answer based on the search results
            answer = process_llm_calls(current_question, context_str, mode="answer")
            
            # Evaluate if the answer satisfactorily addresses the original question
            eval_result = process_llm_calls(question, answer=answer, mode="evaluate")
            
            # If we have a satisfactory answer, return it immediately
            if eval_result["status"] == "complete":
                return {
                    "answer": answer,
                    "iterations": step,
                    "gap_questions": visited_queries,
                    "search_history": search_history
                }
            
            # If the answer is incomplete, add the suggested follow-up question
            # to our queue of knowledge gaps (if it's new)
            if eval_result["suggested"] and eval_result["suggested"] not in visited_queries and eval_result["suggested"] not in gaps:
                gaps.append(eval_result["suggested"])
        
        # Add a small delay to prevent API rate limiting
        time.sleep(1)
    
    # If we've reached max iterations or run out of questions without a satisfactory answer,
    # use "beast mode" to synthesize everything we've learned
    print("\n--- Activating Beast Mode ---")
    
    # Combine all gathered knowledge into a comprehensive context
    full_context = "\n\n".join([k["context"] for k in knowledge])
    
    # Create a summary of all the queries we've explored
    history_str = "\n".join([f"Query: {h['query']}" for h in search_history])
    
    # Generate a final comprehensive answer using all accumulated knowledge
    final_answer = process_llm_calls(question, full_context, history_str, "beast")
    
    # Return the beast mode answer along with the research process data
    return {
        "answer": final_answer,
        "iterations": step,
        "gap_questions": visited_queries,
        "search_history": search_history,
        "beast_mode": True
    } 