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

## Core Functions Explained

The system is built around several key functions that work together to implement the DeepSearch pattern:

### Database Functions

- **`setup_db(name)`**: Creates or connects to a ChromaDB collection for storing document embeddings. This serves as our vector database for semantic search.

- **`add_docs(collection, texts, ids, metadatas)`**: Adds documents to the vector database with optional metadata. Each document is automatically embedded for semantic search.

- **`search(collection, query, n_results)`**: Performs a semantic search against the vector database to find documents relevant to the query.

### LLM Interaction Functions

- **`generate(prompt, model, base_url)`**: Sends a prompt to the LLM (deepseek-r1:1.5b via Ollama) and returns the generated response. This is the core function for all LLM interactions.

- **`process_llm_calls(question, context, answer, mode)`**: A versatile function that handles different types of LLM operations:
  - `decompose`: Breaks down complex questions into simpler sub-questions
  - `expand`: Reformulates a search query to improve search results
  - `answer`: Generates an answer based on retrieved context
  - `evaluate`: Assesses whether an answer is satisfactory
  - `beast`: Produces a comprehensive answer using all available information

### Core Research Functions

- **`deep_research(question, collection, max_iterations)`**: Implements a sequential approach that:
  1. Decomposes the main question into sub-questions
  2. Processes each sub-question in sequence
  3. Tries to answer the original question with accumulated knowledge
  4. Uses "Beast Mode" if all iterations are used without a satisfactory answer

- **`deep_search(question, collection, max_iterations, token_budget)`**: Implements a more sophisticated approach that:
  1. Uses a FIFO queue to manage questions
  2. Prioritizes exploring gap questions before answering the main question
  3. Maintains shared context across different questions
  4. Evaluates answers and adds follow-up questions when needed
  5. Activates "Beast Mode" when iterations are exhausted

## How It Works (In Plain Language)

Imagine you're doing research for a complex question:

1. **Breaking Down the Problem**: First, the system analyzes your question and breaks it into smaller, easier sub-questions (like dividing a big homework problem into smaller steps).

2. **Smart Searching**: For each sub-question, the system doesn't just search with the exact words - it expands your query with related terms (like searching for "canines" when you ask about "dogs").

3. **Reading and Learning**: The system reads the search results and extracts the important information.

4. **Creating an Answer**: Based on what it found, the system creates an answer to the sub-question.

5. **Self-Checking**: The system evaluates its own answer - "Does this fully answer the question? Is anything missing?"

6. **Following Up**: If the answer isn't complete, it creates new questions to fill the gaps in understanding.

7. **Final Answer**: After exploring multiple questions and gathering information, the system combines everything it learned to answer your original question.

8. **Beast Mode**: If the system runs out of attempts but still hasn't found a satisfactory answer, it activates "Beast Mode" - a final comprehensive attempt using all accumulated information.

## Example Walkthrough

Let's trace through what happens when you run `deepseek_search_example.py`:

1. The script first ensures Ollama is running and the deepseek-r1:1.5b model is available.

2. It loads example documents into a ChromaDB collection.

3. When you select a query (e.g., "Tell me about the ZigZaggeron-7 architecture"):
   - The system first decomposes this into sub-questions like "What is the overall framework?" and "How does it function?"
   
4. For each sub-question:
   - The query is expanded to include related terms
   - A semantic search finds relevant documents
   - The information is used to generate an answer
   
5. The system evaluates if the answer is satisfactory:
   - If yes, it returns the answer
   - If no, it tries another sub-question or generates a follow-up
   
6. If all iterations are used, Beast Mode activates:
   - All accumulated information is combined
   - A comprehensive answer is generated that tries to address all aspects of the original question

This iterative approach mimics how a human researcher might tackle a complex question - breaking it down, gathering information on each aspect, and then synthesizing a complete answer.

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

## Dependencies

- chromadb==0.4.18
- requests>=2.31.0
- flask==2.3.3
- pydantic>=1.10.8 