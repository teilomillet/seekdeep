# Compact DeepSearch Implementation

A minimal, functional implementation of the DeepSearch/DeepResearch concept using a local vector database (ChromaDB) and the deepseek-r1:1.5b reasoning model via Ollama. This implementation follows a functional programming approach and stays under 100 lines of core code while providing an iterative research system.

## What is DeepSearch/DeepResearch?

DeepSearch is a new approach to information retrieval that runs through an iterative loop of searching, reading, and reasoning until finding the optimal answer. Unlike traditional RAG systems that typically perform a single search-generate pass, DeepSearch performs multiple iterations, continuously refining its approach until it finds a satisfactory answer.

## Features

- Uses ChromaDB for vector storage and similarity search
- Implements an iterative search-read-reason loop
- Evaluates answers and determines if more research is needed
- Uses the deepseek-r1:1.5b model via Ollama
- Follows functional programming principles for a cleaner implementation

### Key DeepSearch Features Implemented

Based on the Jina AI article ["A Practical Guide to Implementing DeepSearch/DeepResearch"](https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch/), this implementation includes:

- **Question Decomposition**: Breaking down complex questions into sub-questions
- **Advanced Evaluation**: Multi-criteria evaluation of answers
- **Budget Forcing ("Beast Mode")**: Ensuring the system delivers an answer before budget expiration
- **Memory Management**: Keeping track of what's been tried and learned
- **Query Expansion**: Sophisticated query reformulation with synonyms and related terms

## Implementation

This repository uses a minimal and efficient approach:

1. **`deepseek_core.py`** - Core functionality in under 100 lines (90 lines total)
2. **`deepseek_data.py`** - All prompts and data templates
3. **`deepseek_example.py`** - Example usage script

## Installation

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the deepseek-r1:1.5b model:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```python
from deepseek_core import setup_db, add_docs, deep_research

# Setup vector database
collection = setup_db("my_collection")

# Add documents
documents = [
    "Artificial intelligence (AI) is intelligence demonstrated by machines.",
    "Machine learning is a subset of AI focused on data-based prediction.",
    # Add more documents...
]
collection = add_docs(collection, documents)

# Perform research
result = deep_research(
    "What is the relationship between deep learning and neural networks?",
    collection,
    max_iterations=3
)

# Access results
print(f"Answer: {result['answer']}")
print(f"Total iterations: {result['iterations']}")
print(f"Sub-questions used: {len(result['memory']['sub_questions'])}")
```

## Running the Example

```bash
# Make sure Ollama is running
ollama serve

# Run the example
python deepseek_example.py
```

## How It Works

The system follows the iterative DeepSearch process:

1. **Decompose**: Break down complex questions into simpler sub-questions
2. **Search**: Query the vector database to find relevant documents
3. **Read**: Process and extract information from the retrieved documents
4. **Generate**: Create an answer based on the retrieved information
5. **Evaluate**: Assess if the answer is satisfactory using multiple criteria
6. **Refine**: If needed, refine the query and repeat the process
7. **Beast Mode**: If reaching the maximum iterations, provide a comprehensive answer using all accumulated context

## Dependencies

- chromadb==0.4.18
- requests>=2.28.0
- pydantic>=1.10.8 