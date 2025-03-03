# Example Script Walkthrough

This document provides a detailed explanation of how the `deepseek_search_example.py` script works. We'll break down each part of the code and explain what it does in simple terms.

## Overview

The example script demonstrates the DeepSearch system in action. It:

1. Sets up the environment (making sure Ollama is running and the model is available)
2. Prepares test documents with unusual content
3. Allows the user to select a research question
4. Runs the DeepSearch algorithm to answer the question
5. Displays the results in a readable format

## Step-by-Step Explanation

### 1. Importing Dependencies

```python
import time
import subprocess
import requests
from deepseek_core import setup_db, add_docs, deep_search
from deepseek_documents import get_documents
```

This section imports the necessary libraries:
- `time`: For tracking execution time and adding delays
- `subprocess`: For running command-line operations (starting Ollama)
- `requests`: For making HTTP requests to the Ollama API
- Core functions from our DeepSearch implementation
- Example documents to search through

### 2. Example Research Queries

```python
queries = [
    "What is the relationship between deep learning and neural networks?",
    "How does machine learning relate to artificial intelligence?",
    "What are the applications of deep learning?",
    "Explain how neural networks work in simple terms",
    "What is the price of the latest AI training system?",
    "Tell me about the ZigZaggeron-7 architecture"
]
```

These pre-defined questions serve as examples for the user to choose from. The last two questions are specifically designed to match unusual content in our test documents (like specific prices and the made-up "ZigZaggeron-7" architecture).

### 3. Environment Setup Functions

```python
def ensure_ollama_running():
    """Check if Ollama is running and start it if needed."""
    try:
        requests.get("http://localhost:11434/api/version", timeout=2)
        print("✅ Ollama is running")
        return True
    except requests.RequestException:
        print("⚠️ Ollama is not running. Attempting to start...")
        # ... code to start Ollama ...
```

This function:
1. Checks if Ollama (the local LLM server) is already running by making a request to its API
2. If not running, tries to start it automatically
3. Verifies that it started successfully

Similarly, the `ensure_model_pulled` function makes sure the required model is downloaded and available:

```python
def ensure_model_pulled():
    """Ensure the deepseek model is pulled."""
    model = "deepseek-r1:1.5b"
    # ... code to check if model exists and pull it if needed ...
```

### 4. Main Example Function

The `run_example` function is the heart of the script:

```python
def run_example():
    print("\n" + "="*80)
    print("RUNNING DEEPSEARCH WITH DEEPSEEK-R1")
    print("Implements iterative search-read-reason loop with gap questions")
    print("="*80)
    
    # Setup the vector database
    collection = setup_db("deepsearch_example_collection")
    
    # Add documents to the database
    documents = get_documents()
    print(f"Loading {len(documents)} documents with unusual content...")
    collection = add_docs(collection, documents)
    
    # Let the user choose a query
    print("\nAvailable queries:")
    for i, q in enumerate(queries):
        print(f"{i+1}. {q}")
    
    try:
        choice = int(input("\nChoose a query (1-6) or press Enter for default: ") or "1")
        query_idx = max(0, min(len(queries)-1, choice-1))
    except ValueError:
        query_idx = 0
    
    query = queries[query_idx]
    
    print("\n" + "="*70)
    print(f"RESEARCHING: {query}")
    print("="*70)
    
    # Configure iterations
    try:
        max_iterations = int(input("\nEnter maximum iterations (2-5) or press Enter for default (3): ") or "3")
        max_iterations = max(2, min(5, max_iterations))
    except ValueError:
        max_iterations = 3
    
    print("\nUsing model: deepseek-r1:1.5b")
    print(f"Maximum iterations: {max_iterations}")
    
    # Start timer
    start_time = time.time()
    
    try:
        # Run the deep search
        result = deep_search(
            query,
            collection,
            max_iterations=max_iterations,
            token_budget=5000
        )
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*50)
        print("===== FINAL RESULT =====")
        print("="*50)
        print(f"Answer: {result['answer']}")
        print(f"Total iterations: {result['iterations']}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        # Print stats
        print("\n===== RESEARCH STATS =====")
        print(f"Gap questions explored: {len(result['gap_questions'])}")
        if result['gap_questions']:
            for i, q in enumerate(result['gap_questions']):
                print(f"  {i+1}. {q}")
        
        if 'beast_mode' in result and result['beast_mode']:
            print("Beast Mode: Activated ✅")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
```

Let's break this down into logical sections:

#### a. Setting Up the Vector Database

```python
# Setup the vector database
collection = setup_db("deepsearch_example_collection")

# Add documents to the database
documents = get_documents()
print(f"Loading {len(documents)} documents with unusual content...")
collection = add_docs(collection, documents)
```

This part:
1. Creates a ChromaDB collection for storing document embeddings
2. Loads example documents from `deepseek_documents.py`
3. Adds them to the collection for semantic search

#### b. User Input Collection

```python
# Let the user choose a query
print("\nAvailable queries:")
for i, q in enumerate(queries):
    print(f"{i+1}. {q}")

try:
    choice = int(input("\nChoose a query (1-6) or press Enter for default: ") or "1")
    query_idx = max(0, min(len(queries)-1, choice-1))
except ValueError:
    query_idx = 0

query = queries[query_idx]
```

This section:
1. Displays the available example queries
2. Lets the user select one (with input validation)
3. Uses the first query as default if no valid selection is made

Similarly, the script lets the user configure the maximum number of iterations:

```python
# Configure iterations
try:
    max_iterations = int(input("\nEnter maximum iterations (2-5) or press Enter for default (3): ") or "3")
    max_iterations = max(2, min(5, max_iterations))
except ValueError:
    max_iterations = 3
```

#### c. Running DeepSearch

```python
# Start timer
start_time = time.time()

try:
    # Run the deep search
    result = deep_search(
        query,
        collection,
        max_iterations=max_iterations,
        token_budget=5000
    )
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
```

This part:
1. Starts a timer to track execution time
2. Calls the `deep_search` function with the selected query and parameters
3. Records how long the process took

#### d. Displaying Results

```python
print("\n" + "="*50)
print("===== FINAL RESULT =====")
print("="*50)
print(f"Answer: {result['answer']}")
print(f"Total iterations: {result['iterations']}")
print(f"Time elapsed: {elapsed_time:.2f} seconds")

# Print stats
print("\n===== RESEARCH STATS =====")
print(f"Gap questions explored: {len(result['gap_questions'])}")
if result['gap_questions']:
    for i, q in enumerate(result['gap_questions']):
        print(f"  {i+1}. {q}")

if 'beast_mode' in result and result['beast_mode']:
    print("Beast Mode: Activated ✅")
```

This final section:
1. Displays the answer returned by the DeepSearch algorithm
2. Shows how many iterations were used
3. Reports the execution time
4. Lists all the questions that were explored during the process
5. Indicates whether "Beast Mode" was activated

### 5. Script Entry Point

```python
if __name__ == "__main__":
    if ensure_ollama_running() and ensure_model_pulled():
        run_example()
    else:
        print("Please ensure Ollama is installed and can be started.")
        print("Visit https://ollama.com for installation instructions.")
```

This final section:
1. Checks if Ollama is running and the model is available
2. If everything is ready, runs the main example function
3. If not, provides helpful installation instructions

## What Happens During Execution

When you run the script and select a query (e.g., "Tell me about the ZigZaggeron-7 architecture"), the following happens behind the scenes:

1. The query is sent to the `deep_search` function, which:
   - Decomposes it into sub-questions like "What is the ZigZaggeron-7 architecture?" and "How does it function?"
   - Sets up a queue with the original question first

2. For each question in the queue:
   - The query is expanded with related terms for better search results
   - A semantic search is performed against the document collection
   - Search results are collected and formatted for the LLM
   
3. After the first question, the system:
   - Generates an answer using the retrieved documents
   - Evaluates whether the answer is satisfactory
   - Determines follow-up questions if needed
   
4. This process continues for the specified number of iterations, or until a satisfactory answer is found

5. If no satisfactory answer is found after all iterations, "Beast Mode" activates:
   - All the information gathered so far is combined
   - A comprehensive final answer is generated
   
6. The final answer is returned along with statistics about the process

## Test Documents

The example uses a set of test documents from `deepseek_documents.py` that include unusual content specifically designed to be distinctive in search results:

- Documents with specific price tags (e.g., "$94,217.63")
- Unusual product names (e.g., "ZigZaggeron-7")
- Specific performance metrics (e.g., "96.37% accuracy")

This allows you to easily see when the system correctly identifies and includes specific details in the answers.

## Modifying the Example

Students can experiment with the example by:

1. Adding new documents to `deepseek_documents.py` 
2. Creating new research questions in the `queries` list
3. Adjusting the `max_iterations` to see how it affects the quality of results
4. Modifying the prompts in `deepseek_data.py` to change how questions are processed
5. Adding instrumentation to track the internal workings of the system

Each of these modifications provides an opportunity to observe different aspects of how DeepSearch works and how it can be improved. 