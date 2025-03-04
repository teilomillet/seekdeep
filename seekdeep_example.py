import time
import subprocess
import requests
import os
from seekdeep_core import setup_db, add_docs, deep_search
from seekdeep_documents import get_documents

# Default model to use
DEFAULT_MODEL = "deepseek-r1:1.5b"

# List of example research queries with varying complexity and relevance
# These demonstrate different types of questions the system can handle:
# - Factual questions about AI concepts
# - Simple explanatory queries
# - Questions about non-existent technology (to test handling of unknown topics)
SAMPLE_QUERIES = [
    "What is the relationship between deep learning and neural networks?",
    "How does machine learning relate to artificial intelligence?",
    "What are the applications of deep learning?",
    "Explain how neural networks work in simple terms",
    "What is the price of the latest AI training system?",
    "Tell me about the ZigZaggeron-7 architecture"  # Fictional architecture to test system behavior
]


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


def read_custom_document():
    """
    Prompt the user to enter a path to a custom document file.
    
    Returns:
        list: List of document strings from the file, or empty list if file cannot be read
    """
    filepath = input("\nEnter the path to your text file (or press Enter to skip): ")
    
    if not filepath.strip():
        print("No file provided. Using default documents.")
        return []
        
    try:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return []
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split the content into documents (one per paragraph or section)
        # This is a simple approach - could be more sophisticated
        documents = [doc.strip() for doc in content.split('\n\n') if doc.strip()]
        
        if not documents:
            print("No valid content found in file.")
            return []
            
        print(f"Successfully loaded {len(documents)} documents from file.")
        return documents
        
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []


def setup_database():
    """
    Initialize and populate the vector database with sample documents.
    
    Returns:
        Collection: The ChromaDB collection ready for searching
    """
    # Create a ChromaDB collection named "deepsearch_example_collection"
    collection = setup_db("deepsearch_example_collection")
    
    # Ask if the user wants to use a custom document
    use_custom = input("\nDo you want to use your own document? (y/n, default=n): ").lower().strip() == 'y'
    
    if use_custom:
        custom_docs = read_custom_document()
        if custom_docs:
            print(f"Loading {len(custom_docs)} custom documents...")
            collection = add_docs(collection, custom_docs)
        else:
            print("Using default documents instead.")
            documents = get_documents()
            print(f"Loading {len(documents)} default documents...")
            collection = add_docs(collection, documents)
    else:
        # The get_documents() function retrieves a set of text documents for demonstration
        documents = get_documents()
        print(f"Loading {len(documents)} default documents...")
        collection = add_docs(collection, documents)
    
    return collection


def is_valid_query(query):
    """
    Check if a custom query is valid (not too short or generic).
    
    Args:
        query (str): The custom query to validate
        
    Returns:
        bool: True if the query is valid, False otherwise
    """
    # Remove punctuation and convert to lowercase for comparison
    cleaned = query.lower().strip()
    
    # Check minimum length (at least 10 characters)
    if len(cleaned) < 10:
        return False
    
    # Check if query is too generic
    generic_phrases = ["help", "hello", "hi", "test", "what", "who", "where", "when", "why", "how"]
    if cleaned in generic_phrases:
        return False
        
    return True


def select_query():
    """
    Display sample queries and let the user select one or enter a custom query.
    
    Returns:
        str: The selected or custom query text
    """
    print("\nAvailable queries:")
    for i, q in enumerate(SAMPLE_QUERIES):
        print(f"{i+1}. {q}")
    print(f"{len(SAMPLE_QUERIES)+1}. Enter your own research question")
    
    # Get user input for query selection with error handling
    try:
        choice = int(input("\nChoose an option (1-7) or press Enter for default: ") or "1")
        
        # Check if user wants to enter a custom query
        if choice == len(SAMPLE_QUERIES) + 1:
            while True:
                custom_query = input("\nPlease enter your research question: ")
                if not custom_query.strip():
                    print("Empty query entered. Using default query instead.")
                    return SAMPLE_QUERIES[0]
                    
                if not is_valid_query(custom_query):
                    print("Please enter a more specific question (at least 10 characters).")
                    continue
                    
                print(f"Researching your question: \"{custom_query}\"")
                return custom_query
        else:
            # Ensure the choice is within valid range for sample queries
            query_idx = max(0, min(len(SAMPLE_QUERIES)-1, choice-1))
            return SAMPLE_QUERIES[query_idx]
    except ValueError:
        # Default to the first query if input is invalid
        print("Invalid input. Using default query instead.")
        return SAMPLE_QUERIES[0]


def configure_research_parameters():
    """
    Prompt the user for research parameters.
    
    Returns:
        int: Maximum number of iterations to perform
    """
    try:
        max_iterations = int(input("\nEnter maximum iterations (2-5) or press Enter for default (3): ") or "3")
        # Limit iterations to the range 2-5 for demonstration purposes
        max_iterations = max(2, min(5, max_iterations))
    except ValueError:
        # Default to 3 iterations if input is invalid
        max_iterations = 3
        
    return max_iterations


def display_results(result, elapsed_time):
    """
    Display the research results and statistics.
    
    Args:
        result (dict): The result dictionary from deep_search
        elapsed_time (float): Time taken to perform the research in seconds
    """
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


def progress_callback():
    """
    Callback function to show progress during research.
    Displays a simple animation to indicate the system is working.
    """
    print(".", end="", flush=True)


def run_example(model=DEFAULT_MODEL):
    """
    Run the complete DeepSearch example workflow.
    
    This function:
    1. Sets up a vector database collection
    2. Loads sample documents into the database
    3. Lets the user select a research query
    4. Configures and runs the deep_search algorithm
    5. Displays the results and performance statistics
    
    Args:
        model (str): The name of the model to use (default: DEFAULT_MODEL)
    """
    # Display header to indicate what's running
    print("\n" + "="*80)
    print("RUNNING DEEPSEARCH WITH SEEKDEEP")
    print("Welcome to the SeekDeep Program.")
    print("="*80)
    
    # STEP 1 & 2: Initialize and populate the vector database
    collection = setup_database()
    
    # STEP 3: Let the user select a query
    query = select_query()
    
    # Display the selected query
    print("\n" + "="*70)
    print(f"RESEARCHING: {query}")
    print("="*70)
    
    # STEP 4: Configure the research parameters
    max_iterations = configure_research_parameters()
    
    # Display configuration information
    print(f"\nUsing model: {model}")
    print(f"Maximum iterations: {max_iterations}")
    
    # STEP 5: Run the deep search process
    print("\nStarting research process. This may take a few minutes...")
    print("Working", end="", flush=True)
    
    # Start timing for performance measurement
    start_time = time.time()
    
    try:
        # Execute the deep_search algorithm with our parameters
        result = deep_search(
            query,                         # The research question
            collection,                    # The vector database collection
            max_iterations=max_iterations, # Maximum search iterations
            token_budget=7500,             # Limit on context size for LLM calls
            progress_callback=progress_callback  # Callback for progress indication
        )
        
        # Calculate elapsed time for performance reporting
        elapsed_time = time.time() - start_time
        
        # Add a newline after our progress dots
        print("\n")
        
        # STEP 6: Display the results
        display_results(result, elapsed_time)
            
    except Exception as e:
        # Add a newline after our progress dots
        print("\n")
        # Handle any errors that occur during the research process
        print(f"An error occurred: {str(e)}")
        
    print("\nResearch process complete. Thank you for using SeekDeep!")


def main():
    """
    Main entry point for the application.
    """
    # Only run the example if the necessary services are available
    if ensure_ollama_running() and ensure_model_pulled():
        run_example()
    else:
        # Display helpful instructions if setup requirements aren't met
        print("Please ensure Ollama is installed and can be started.")
        print("Visit https://ollama.com for installation instructions.")


if __name__ == "__main__":
    main() 