import os
import time
from deepseek_core import setup_db, add_docs, deep_research

# Example documents about AI topics
documents = [
    # General AI
    "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans.",
    "AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.",
    
    # Machine Learning
    "Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.",
    "Machine learning algorithms build mathematical models based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.",
    
    # Neural Networks
    "Neural networks are computing systems inspired by the biological neural networks that constitute animal brains.",
    "Neural networks learn to perform tasks by considering examples, generally without being programmed with task-specific rules.",
    "A neural network is based on a collection of connected units called artificial neurons, which loosely model the neurons in a biological brain.",
    
    # Deep Learning
    "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.",
    "Deep learning architectures such as deep neural networks, deep belief networks, recurrent neural networks, and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, and more.",
    "Deep learning uses multiple layers of neural networks to progressively extract higher-level features from raw input.",
    "The 'deep' in deep learning refers to the number of layers through which the data is transformed."
]

# Example research queries
queries = [
    "What is the relationship between deep learning and neural networks?",
    "How does machine learning relate to artificial intelligence?",
    "What are the applications of deep learning?",
    "Explain how neural networks work in simple terms"
]

def run_example():
    print("\n" + "="*80)
    print("RUNNING COMPACT DEEP RESEARCH WITH DEEPSEEK-R1")
    print("Implements all Jina AI DeepSearch features in under 100 lines of core code")
    print("="*80)
    
    # Setup the vector database
    collection = setup_db("deepseek_example_collection")
    
    # Add documents to the database
    collection = add_docs(collection, documents)
    
    # Let the user choose a query
    print("\nAvailable queries:")
    for i, q in enumerate(queries):
        print(f"{i+1}. {q}")
    
    try:
        choice = int(input("\nChoose a query (1-4) or press Enter for default: ") or "1")
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
    
    print(f"\nUsing model: deepseek-r1:1.5b")
    print(f"Maximum iterations: {max_iterations}")
    
    # Start timer
    start_time = time.time()
    
    try:
        # Run the deep research
        result = deep_research(
            query,
            collection,
            max_iterations=max_iterations
        )
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*50)
        print("===== FINAL RESULT =====")
        print("="*50)
        print(f"Answer: {result['answer']}")
        print(f"Total iterations: {result['iterations']}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        # Print stats from memory
        print("\n===== RESEARCH STATS =====")
        print(f"Sub-questions used: {len(result['memory']['sub_questions'])}")
        if result['memory']['sub_questions']:
            for i, q in enumerate(result['memory']['sub_questions']):
                print(f"  {i+1}. {q}")
        
        print(f"Answer attempts: {len(result['memory']['answer_attempts'])}")
        if 'beast_mode' in result and result['beast_mode']:
            print("Beast Mode: Activated ✅")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Check if Ollama is running
    import requests
    try:
        requests.get("http://localhost:11434/api/version")
        print("Ollama detected! Make sure you have pulled the deepseek-r1:1.5b model.")
        print("If you haven't, run: ollama pull deepseek-r1:1.5b")
    except:
        print("Warning: Ollama doesn't appear to be running. Please start Ollama first.")
        print("Run: ollama serve")
        exit(1)
    
    run_example() 