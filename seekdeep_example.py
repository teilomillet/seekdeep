import time
import subprocess
import requests
from seekdeep_core import setup_db, add_docs, deep_search
from seekdeep_documents import get_documents

# List of example research queries with varying complexity and relevance
# These demonstrate different types of questions the system can handle:
# - Factual questions about AI concepts
# - Simple explanatory queries
# - Questions about non-existent technology (to test handling of unknown topics)
queries = [
    "What is the relationship between deep learning and neural networks?",
    "How does machine learning relate to artificial intelligence?",
    "What are the applications of deep learning?",
    "Explain how neural networks work in simple terms",
    "What is the price of the latest AI training system?",
    "Tell me about the ZigZaggeron-7 architecture"  # Fictional architecture to test system behavior
]

# Default model to use
DEFAULT_MODEL = "deepseek-r1:1.5b"

def ensure_ollama_running():
    """
    Verify that the Ollama service is running and start it if needed.
    
    This function:
    1. Checks if the Ollama API is responding at the default port (11434)
    2. If not responding, attempts to start the Ollama service as a background process
    3. Waits briefly for the service to initialize
    4. Verifies the service is now running
    
    Returns:
        bool: True if Ollama is running (or was successfully started), False otherwise
    """
    try:
        # First, check if Ollama is already running by making a request to its API
        requests.get("http://localhost:11434/api/version", timeout=2)
        print("✅ Ollama is running")
        return True
    except requests.RequestException:
        # Ollama is not running, so we'll try to start it
        print("⚠️ Ollama is not running. Attempting to start...")
        try:
            # Start Ollama as a background process
            # stdout/stderr are piped to avoid cluttering the console
            subprocess.Popen(["ollama", "serve"], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
            
            # Wait a few seconds to give Ollama time to initialize
            time.sleep(3)
            
            # Check again if Ollama is now running
            try:
                requests.get("http://localhost:11434/api/version", timeout=2)
                print("✅ Ollama started successfully")
                return True
            except requests.RequestException:
                # Ollama still not running after our attempt to start it
                print("❌ Failed to start Ollama. Please start it manually with 'ollama serve'")
                return False
        except (subprocess.SubprocessError, FileNotFoundError):
            # Either the subprocess command failed or Ollama is not installed/not in PATH
            print("❌ Could not start Ollama. Please start it manually with 'ollama serve'")
            return False

def ensure_model_pulled(model=DEFAULT_MODEL):
    """
    Ensure the required language model is downloaded and available in Ollama.
    
    This function:
    1. Checks if the specified model is already available in Ollama
    2. If not, pulls (downloads) the model from Ollama's model hub
    3. Verifies the model was successfully downloaded
    
    Args:
        model (str): The name of the model to pull (default: DEFAULT_MODEL)
    
    Returns:
        bool: True if the model is available (or was successfully downloaded),
              False if the model could not be pulled or there was an error
    """
    try:
        # Get a list of all models currently available in Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get("models", [])
        
        # Check if our required model is in the list
        model_exists = any(m["name"] == model for m in models)
        
        if not model_exists:
            # Model isn't downloaded yet, so pull it now
            print(f"⚠️ Model {model} not found. Pulling now...")
            # This may take some time for larger models
            subprocess.run(["ollama", "pull", model], check=True)
            print(f"✅ Model {model} pulled successfully")
        else:
            # Model is already available locally
            print(f"✅ Model {model} is already available")
        return True
    except Exception as e:
        # Something went wrong - could be API issues, network problems, etc.
        print(f"❌ Error checking/pulling model: {str(e)}")
        return False

def run_example(model=DEFAULT_MODEL):
    """
    Run the complete DeepSearch example workflow.
    
    This function:
    1. Sets up a vector database collection
    2. Loads sample documents into the database
    3. Lets the user select a research query
    4. Configures and runs the deep_search algorithm
    5. Displays the results and performance statistics
    
    The function demonstrates the end-to-end usage of the DeepSearch system, from
    database setup to final answer generation.
    """
    # Display header to indicate what's running
    print("\n" + "="*80)
    print("RUNNING DEEPSEARCH WITH SEEKDEEP")
    print("Welcome to the SeekDeep Program.")
    print("="*80)
    
    # STEP 1: Initialize the vector database
    # Create a ChromaDB collection named "deepsearch_example_collection"
    # If a collection with this name already exists, it will be reused
    collection = setup_db("deepsearch_example_collection")
    
    # STEP 2: Populate the database with sample documents
    # The get_documents() function retrieves a set of text documents for demonstration
    documents = get_documents()
    print(f"Loading {len(documents)} documents...")
    # Add these documents to our collection with auto-generated IDs and metadata
    collection = add_docs(collection, documents)
    
    # STEP 3: Let the user select a query from the predefined list
    print("\nAvailable queries:")
    for i, q in enumerate(queries):
        print(f"{i+1}. {q}")
    
    # Get user input for query selection with error handling
    try:
        choice = int(input("\nChoose a query (1-6) or press Enter for default: ") or "1")
        # Ensure the choice is within valid range (1-6)
        query_idx = max(0, min(len(queries)-1, choice-1))
    except ValueError:
        # Default to the first query if input is invalid
        query_idx = 0
    
    # Get the selected query
    query = queries[query_idx]
    
    # Display the selected query
    print("\n" + "="*70)
    print(f"RESEARCHING: {query}")
    print("="*70)
    
    # STEP 4: Configure the research parameters
    # Let the user set the maximum number of iterations
    try:
        max_iterations = int(input("\nEnter maximum iterations (2-5) or press Enter for default (3): ") or "3")
        # Limit iterations to the range 2-5 for demonstration purposes
        max_iterations = max(2, min(5, max_iterations))
    except ValueError:
        # Default to 3 iterations if input is invalid
        max_iterations = 3
    
    # Display configuration information
    print(f"\nUsing model: {model}")
    print(f"Maximum iterations: {max_iterations}")
    
    # STEP 5: Run the deep search process
    # Start timing for performance measurement
    start_time = time.time()
    
    try:
        # Execute the deep_search algorithm with our parameters
        # This is the main research function that will:
        # - Break down the question into sub-questions
        # - Search for information on each sub-question
        # - Generate and evaluate answers
        # - Synthesize a final comprehensive answer
        result = deep_search(
            query,                   # The research question
            collection,              # The vector database collection
            max_iterations=max_iterations,  # Maximum search iterations
            token_budget=5000        # Limit on context size for LLM calls
        )
        
        # Calculate elapsed time for performance reporting
        elapsed_time = time.time() - start_time
        
        # STEP 6: Display the results
        # Print the final answer and statistics
        print("\n" + "="*50)
        print("===== FINAL RESULT =====")
        print("="*50)
        print(f"Answer: {result['answer']}")
        print(f"Total iterations: {result['iterations']}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        # Print detailed statistics about the research process
        print("\n===== RESEARCH STATS =====")
        print(f"Gap questions explored: {len(result['gap_questions'])}")
        if result['gap_questions']:
            for i, q in enumerate(result['gap_questions']):
                print(f"  {i+1}. {q}")
        
        # Indicate if the "beast mode" was activated (comprehensive final synthesis)
        if 'beast_mode' in result and result['beast_mode']:
            print("Beast Mode: Activated ✅")
            
    except Exception as e:
        # Handle any errors that occur during the research process
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Only run the example if the necessary services are available
    if ensure_ollama_running() and ensure_model_pulled():
        run_example()
    else:
        # Display helpful instructions if setup requirements aren't met
        print("Please ensure Ollama is installed and can be started.")
        print("Visit https://ollama.com for installation instructions.") 