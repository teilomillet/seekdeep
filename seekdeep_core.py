import chromadb
import requests
import time
import re
from typing import List, Dict, Any, Optional, Union, Callable, TypedDict, Tuple
from chromadb.api.models.Collection import Collection
from seekdeep_data import (
    DECOMPOSE_PROMPT,
    EXPAND_PROMPT,
    ANSWER_PROMPT,
    EVALUATE_PROMPT,
    BEAST_MODE_PROMPT
)

# Type definitions
class SearchResult(TypedDict):
    """Type for search result item"""
    text: str
    metadata: Dict[str, Any]
    id: str

class EvaluationResult(TypedDict):
    """Type for evaluation result"""
    status: str
    suggested: Optional[str]

class DeepResearchResult(TypedDict):
    """Type for deep_research result"""
    answer: str
    iterations: int
    memory: Dict[str, Any]
    beast_mode: Optional[bool]

class DeepSearchResult(TypedDict):
    """Type for deep_search result"""
    answer: str
    iterations: int
    gap_questions: List[str]
    search_history: List[Dict[str, Any]]
    research_trail: List[Dict[str, Any]]
    beast_mode: Optional[bool]

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    
    This function provides a rough estimate of token count based on the 
    typical token-to-character ratio in English text. More accurate counts
    would require using the specific tokenizer of the target LLM.
    
    Args:
        text (str): The text to estimate token count for
        
    Returns:
        int: Estimated number of tokens in the text
    """
    # A common approximation is 4 characters per token for English text
    # This is a rough estimate - true tokenization depends on the specific model
    return len(text) // 4 + 1  # +1 to avoid returning 0 for very short strings

def trim_context_to_budget(context_items: List[Dict[str, str]], token_budget: int) -> str:
    """
    Trim a list of context items to fit within a token budget.
    
    This function prioritizes more recent items (assumes the list is in 
    chronological order) and includes as many as possible while staying
    within the token budget.
    
    Args:
        context_items (List[Dict[str, str]]): List of context dictionaries
                                             with "question" and "context" keys
        token_budget (int): Maximum number of tokens to include
        
    Returns:
        str: Combined context string that fits within the token budget
    """
    # Reserve some tokens for the prompts and other text (headers, etc.)
    reserved_tokens = 500
    available_budget = max(token_budget - reserved_tokens, 500)  # Ensure minimum context size
    
    # Start with more recent items (reverse the list)
    prioritized_items = list(reversed(context_items))
    
    included_contexts = []
    current_token_count = 0
    
    # Add context items until we hit the budget
    for item in prioritized_items:
        context = item["context"]
        question = item["question"]
        
        # Create a formatted context entry with the question
        formatted_entry = f"Question: {question}\nContext: {context}"
        entry_tokens = estimate_tokens(formatted_entry)
        
        # Check if adding this item would exceed our budget
        if current_token_count + entry_tokens <= available_budget:
            included_contexts.append(formatted_entry)
            current_token_count += entry_tokens
        else:
            # If the item is too large, we could try to truncate it, but for simplicity
            # we'll just skip it in this implementation
            continue
    
    # Combine the included contexts (restore original order)
    return "\n\n".join(reversed(included_contexts))

def setup_db(name: str = "research_collection") -> Collection:
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

def add_docs(collection: Collection, 
             texts: List[str], 
             ids: Optional[List[str]] = None, 
             metadatas: Optional[List[Dict[str, Any]]] = None) -> Collection:
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

def search(collection: Collection, query: str, n_results: int = 3) -> List[SearchResult]:
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

def generate(prompt: str, 
             model: str = "deepseek-r1:1.5b", 
             base_url: str = "http://localhost:11434/api") -> str:
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

def process_llm_calls(question: str, 
                     context: Optional[str] = None, 
                     answer: Optional[str] = None, 
                     mode: str = "decompose") -> Union[List[str], str, EvaluationResult]:
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
        "answer": ANSWER_PROMPT.format(question=question, context=context or "No relevant information found."),
        "evaluate": EVALUATE_PROMPT.format(question=question, answer=answer),
        "beast": BEAST_MODE_PROMPT.format(
            question=question, 
            full_context=context or "No relevant information found.", 
            search_history=answer or ""
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
        eval_result: EvaluationResult = {
            "status": "complete" if is_complete else "incomplete",
            "suggested": suggested
        }        
        return eval_result
    
    else:  # answer or beast mode
        # Simply return the generated text as the answer
        return result

def _decompose_main_question(question: str) -> Tuple[List[str], int]:
    """Extract sub-questions from the main question for exploration."""
    sub_questions = process_llm_calls(question, mode="decompose")
    if not isinstance(sub_questions, list):
        # Type safety: ensure we have a list of questions
        sub_questions = [question]
    
    # Estimate token usage for question decomposition
    token_usage = estimate_tokens(str(sub_questions)) + 200  # Add overhead for prompt
    
    return sub_questions, token_usage

def _expand_search_query(question: str) -> Tuple[str, int]:
    """Expand the search query for better retrieval."""
    search_query = process_llm_calls(question, mode="expand")
    if not isinstance(search_query, str):
        # Type safety: ensure we have a string query
        search_query = question
    
    # Estimate token usage for query expansion
    token_usage = estimate_tokens(search_query) + 100  # Add overhead for prompt
    
    return search_query, token_usage

def _perform_search(collection: Collection, query: str, token_budget: int) -> Tuple[List[SearchResult], str, int]:
    """Perform semantic search and prepare context within budget."""
    # Perform semantic search to find relevant documents
    search_results = search(collection, query)
    
    # Build context by combining all retrieved documents
    context_str = "\n\n".join([r["text"] for r in search_results])
    
    # Check if context exceeds our token budget
    context_tokens = estimate_tokens(context_str)
    if context_tokens > token_budget // 2:  # Use half budget for individual answers
        # Truncate to fit within half the token budget (save space for the answer)
        context_str = context_str[:token_budget // 2 * 4]  # Convert tokens to approx char count
        context_tokens = token_budget // 2
        print(f"Context truncated to fit within token budget ({token_budget // 2} tokens)")
    
    return search_results, context_str, context_tokens

def _generate_and_evaluate(question: str, current_question: str, context_str: str) -> Tuple[str, Dict[str, Any], int]:
    """Generate an answer and evaluate its completeness."""
    # Generate an answer based on the search results
    answer_result = process_llm_calls(current_question, context_str, mode="answer")
    if not isinstance(answer_result, str):
        # Type safety: ensure we have a string answer
        answer_result = "Unable to generate an answer."
    answer = answer_result
    
    # Track token usage for answer generation
    token_usage = estimate_tokens(answer) + 150  # Add overhead for prompt
    
    # Evaluate if the answer satisfactorily addresses the original question
    eval_result = process_llm_calls(question, answer=answer, mode="evaluate")
    if not isinstance(eval_result, dict):
        # Type safety: handle unexpected result
        eval_result = {"status": "incomplete", "suggested": None}
    
    # Add token usage for evaluation
    token_usage += estimate_tokens(str(eval_result)) + 100  # Add overhead for prompt
    
    return answer, eval_result, token_usage

def _activate_beast_mode(question: str, knowledge: List[Dict[str, str]], token_budget: int, current_usage: int) -> Tuple[str, int]:
    """Generate a comprehensive answer in beast mode."""
    print("\n--- Activating Beast Mode ---")
    print(f"Token usage before beast mode: ~{current_usage} tokens")
    
    if knowledge:
        # Calculate remaining token budget for context
        remaining_budget = max(token_budget - current_usage, 1000)  # Ensure at least 1000 tokens
        
        # Use the token budget management function to create context within budget
        full_context = trim_context_to_budget(knowledge, remaining_budget)
        context_tokens = estimate_tokens(full_context)
        token_usage = context_tokens
        print(f"Beast mode context size: ~{context_tokens} tokens")
    else:
        full_context = "No relevant information found."
        token_usage = 0
    
    # Create a summary of all the queries we've explored
    history_str = "\n".join([f"Question explored: {item['question']}" for item in knowledge])
    
    # Generate a final comprehensive answer using all accumulated knowledge
    beast_result = process_llm_calls(question, full_context, history_str, "beast")
    if not isinstance(beast_result, str):
        # Type safety: ensure we have a string answer
        beast_result = "Unable to generate a comprehensive answer."
    
    # Add token usage for beast mode answer
    token_usage += estimate_tokens(beast_result) + 200  # Add overhead for beast mode prompt
    
    return beast_result, token_usage

def _select_next_question(sub_questions: List[str], current_iteration: int, eval_result: Dict[str, Any], original_question: str) -> str:
    """Select the next question to process based on iteration and evaluation."""
    if current_iteration < len(sub_questions):
        # If there are more sub-questions in our decomposition, use the next one
        return sub_questions[current_iteration]
    else:
        # Otherwise, use the suggested follow-up or fall back to the original question
        return eval_result.get("suggested", "") if eval_result.get("suggested") else original_question

def _process_research_step(current_query: str, 
                         collection: Collection, 
                         memory: Dict[str, List[Any]],
                         main_question: str) -> Tuple[str, Dict[str, Any], bool]:
    """Process a single research step and return the answer, evaluation result, and completion status."""
    # Expand the query for better search results
    search_query, _ = _expand_search_query(current_query)
    
    # Perform the search
    search_results = search(collection, search_query)
    
    # Build context from search results
    context_str = "\n\n".join([r["text"] for r in search_results])
    
    # Record search in memory
    memory["search_history"].append({"query": current_query, "results": search_results})
    
    # Generate an answer
    answer = process_llm_calls(current_query, context_str, mode="answer")
    if not isinstance(answer, str):
        answer = "Unable to generate a proper answer."
    
    # Add answer to memory
    memory["answer_attempts"].append({"query": current_query, "answer": answer})
    
    # Evaluate the answer
    eval_result = process_llm_calls(main_question, answer=answer, mode="evaluate")
    if not isinstance(eval_result, dict):
        eval_result = {"status": "incomplete", "suggested": None}
    
    # Check if answer is complete
    is_complete = eval_result.get("status") == "complete"
    
    return answer, eval_result, is_complete

def _generate_beast_mode_answer(question: str, 
                              context: str, 
                              memory: Dict[str, List[Any]]) -> str:
    """Generate a comprehensive answer using beast mode."""
    # Create a history string summarizing all queries performed
    history_str = "\n".join([f"Query: {h['query']}" for h in memory["search_history"]])
    
    # Generate a comprehensive answer using beast mode
    beast_answer = process_llm_calls(question, context, history_str, "beast")
    if not isinstance(beast_answer, str):
        beast_answer = "Unable to generate a comprehensive answer."
    
    return beast_answer

def deep_research(question: str, 
                 collection: Collection, 
                 max_iterations: int = 3) -> DeepResearchResult:
    """
    Perform an in-depth research process on a question using iterative decomposition and refinement.
    
    Uses a functional approach with smaller, focused helper functions to:
    1. Decompose a complex question into simpler sub-questions
    2. Process each sub-question sequentially
    3. Evaluate answers and select the next question to explore
    4. Fall back to "beast mode" for comprehensive synthesis if needed
    
    Args:
        question (str): The main research question to investigate
        collection: ChromaDB collection containing the knowledge documents to search
        max_iterations (int): Maximum number of research iterations before forced completion
        
    Returns:
        DeepResearchResult: A dictionary containing answer, iterations, and research data
    """
    # Initialize research memory
    memory = {
        "sub_questions": [],
        "search_history": [],
        "answer_attempts": []
    }
    
    # Decompose the main question
    sub_questions, _ = _decompose_main_question(question)
    memory["sub_questions"] = sub_questions
    
    # Select the first question to process
    current_query = sub_questions[0] if sub_questions else question
    
    # Track current iteration
    iteration = 0
    latest_answer = ""
    
    # Main research loop
    while iteration < max_iterations:
        print(f"\n--- Step {iteration + 1} ---")
        print(f"Current question: {current_query}")
        
        # Process this research step
        answer, eval_result, is_complete = _process_research_step(
            current_query, collection, memory, question
        )
        
        # Store the latest answer for potential return
        latest_answer = answer
        
        # Handle final iteration - use beast mode
        if iteration == max_iterations - 1:
            # Get the most recent context
            last_context = ""
            if memory["search_history"]:
                last_results = memory["search_history"][-1]["results"]
                last_context = "\n\n".join([r["text"] for r in last_results])
            
            # Generate beast mode answer
            beast_answer = _generate_beast_mode_answer(question, last_context, memory)
            
            # Return final result with beast mode
            return {
                "answer": beast_answer,
                "iterations": iteration + 1,
                "memory": memory,
                "beast_mode": True
            }
        
        # If we have a complete answer, return it
        if is_complete:
            return {
                "answer": answer,
                "iterations": iteration + 1,
                "memory": memory,
                "beast_mode": None
            }
        
        # Prepare for next iteration
        iteration += 1
        
        # Select the next question to process
        current_query = _select_next_question(sub_questions, iteration, eval_result, question)
        
        # Add a small delay to prevent API rate limiting
        time.sleep(1)
    
    # If we've exhausted all iterations, return the latest answer
    return {
        "answer": latest_answer,
        "iterations": max_iterations,
        "memory": memory,
        "beast_mode": None
    }

def deep_search(question: str, 
               collection: Collection, 
               max_iterations: int = 3, 
               token_budget: int = 5000, 
               progress_callback: Optional[Callable[[], None]] = None) -> DeepSearchResult:
    """
    Perform a breadth-first search-based research approach to answer complex questions.
    
    Uses a functional approach with smaller, focused helper functions to:
    1. Decompose the main question into sub-questions
    2. Process each question using breadth-first search 
    3. Maintain a knowledge base of search results
    4. Evaluate answers for completeness
    5. Fall back to "beast mode" for comprehensive synthesis if needed
    
    Args:
        question (str): The main research question to investigate
        collection: ChromaDB collection containing the knowledge documents to search
        max_iterations (int): Maximum number of iterations before forced completion
        token_budget (int): Approximate maximum token count to use for context
        progress_callback (function): Optional callback function to report progress
        
    Returns:
        DeepSearchResult: A dictionary containing answer, iterations, and research data
    """
    # Initialize tracking structures
    step = 0
    visited_queries: List[str] = []
    search_history: List[Dict[str, Any]] = []
    knowledge: List[Dict[str, str]] = []
    research_trail: List[Dict[str, Any]] = []
    current_token_usage = 0
    
    # Initialize a FIFO queue with the original question as the first gap to fill
    gaps: List[str] = [question]
    
    # Main reasoning loop - continue until we run out of questions or hit max iterations
    while gaps and step < max_iterations:
        # Get the next question from the queue (breadth-first approach)
        current_question = gaps.pop(0)
        visited_queries.append(current_question)
        
        # Log the current step
        print(f"\n--- Step {step + 1} ---")
        print(f"Current question: {current_question}")
        
        # Call progress callback if provided
        if progress_callback:
            progress_callback()
            
        step += 1
        
        # Special handling for the first iteration - decompose the main question
        if step == 1:
            sub_questions, decomp_tokens = _decompose_main_question(current_question)
            current_token_usage += decomp_tokens
            
            # Add each new sub-question to our queue if we haven't seen it before
            for q in sub_questions:
                if q not in visited_queries and q not in gaps:
                    gaps.append(q)
            
            # Make sure the original question is revisited at the end (for synthesis)
            # but only if we have other questions to process first
            if gaps and question not in gaps:
                gaps.append(question)
        
        # Expand the search query for better results
        expanded_query, expand_tokens = _expand_search_query(current_question)
        current_token_usage += expand_tokens
        
        # Perform search and prepare context
        search_results, context_str, context_tokens = _perform_search(
            collection, expanded_query, token_budget
        )
        current_token_usage += context_tokens
        
        # Record search history and knowledge
        search_history.append({"query": current_question, "results": search_results})
        knowledge.append({"question": current_question, "context": context_str})
        
        # Generate and evaluate an answer, but only after the first step
        if step > 1:
            # Generate answer and evaluate its completeness
            answer, eval_result, answer_tokens = _generate_and_evaluate(
                question, current_question, context_str
            )
            current_token_usage += answer_tokens
            
            # Add to research trail for tracking
            research_trail.append({
                "question": current_question,
                "expanded_query": expanded_query,
                "search_results": search_results,
                "answer": answer
            })
            
            # Display current token usage for monitoring
            print(f"Current token usage: ~{current_token_usage} tokens (budget: {token_budget})")
            
            # If we have a satisfactory answer, return it immediately
            if eval_result.get("status") == "complete":
                return {
                    "answer": answer,
                    "iterations": step,
                    "gap_questions": visited_queries,
                    "search_history": search_history,
                    "research_trail": research_trail,
                    "beast_mode": None
                }
            
            # If the answer is incomplete, add the suggested follow-up question
            # to our queue of knowledge gaps (if it's new)
            if eval_result.get("suggested") and eval_result.get("suggested") not in visited_queries and eval_result.get("suggested") not in gaps:
                gaps.append(eval_result.get("suggested", ""))
        
        # Add a small delay to prevent API rate limiting
        time.sleep(1)
    
    # If no satisfactory answer, use "beast mode" to synthesize everything
    final_answer, beast_tokens = _activate_beast_mode(
        question, knowledge, token_budget, current_token_usage
    )
    current_token_usage += beast_tokens
    print(f"Final total token usage: ~{current_token_usage} tokens")
    
    # Return the beast mode answer along with the research process data
    return {
        "answer": final_answer,
        "iterations": step,
        "gap_questions": visited_queries,
        "search_history": search_history,
        "research_trail": research_trail,
        "beast_mode": True
    } 