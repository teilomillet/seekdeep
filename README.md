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
- Includes hallucination detection for fictional topics
- Comprehensive inline documentation explaining both concepts and implementation details

### Key DeepSearch Features Implemented

Based on the Jina AI article ["A Practical Guide to Implementing DeepSearch/DeepResearch"](https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch/), this implementation includes:

- **Question Decomposition**: Breaking down complex questions into sub-questions
- **Advanced Evaluation**: Multi-criteria evaluation of answers
- **Budget Forcing ("Beast Mode")**: Ensuring the system delivers an answer before budget expiration
- **Memory Management**: Keeping track of what's been tried and learned
- **Query Expansion**: Sophisticated query reformulation with synonyms and related terms
- **Early Stopping**: Ending research when a satisfactory answer is found
- **Factuality Checks**: Detecting and handling fictional or non-existent topics

## Available Implementations

This repository includes a basic implementation of the DeepSearch concept:

**Basic Implementation** (`seekdeep_example.py`): A straightforward implementation that directly uses ChromaDB and the Ollama API.

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

## Code Documentation

The codebase features extensive inline documentation that serves as both educational material and implementation reference:

- **Conceptual Documentation**: Explains the DeepSearch approach and research methodologies
- **Function Documentation**: Detailed docstrings with parameters, return values, and examples
- **Implementation Notes**: Comments explaining design decisions and algorithm details
- **Section Headers**: Clear code organization with descriptive section markers

This documentation makes the code suitable for:
- Learning about DeepSearch implementations
- Exploring iterative research algorithms
- Seeing factuality checking in practice

## Getting Started

### Prerequisites

- Python 3.9+
- [ChromaDB](https://docs.trychroma.com/)
- [Ollama](https://ollama.ai/) with the deepseek-r1:1.5b model
- We recommend using uv to install the dependencies

### Installation

1. Clone this repository
2. Install the required packages:
```bash
uv sync
```
3. Make sure Ollama is installed and running
4. Pull the deepseek-r1:1.5b model:
```bash
ollama pull deepseek-r1:1.5b
```

### Running the Example

```bash
python seekdeep_example.py
```

This will start the example script that allows you to:
1. Select from sample research questions
2. Watch as the system decomposes and researches the question
3. View the final answer and research trail

## Documentation

Detailed documentation is available in the `docs` directory:

- [Example Walkthrough](docs/example_walkthrough.md): A step-by-step explanation of the example script
- [Implementation Details](docs/implementation_details.md): Deep dive into the core implementation
- [Function Reference](docs/function_reference.md): Comprehensive reference for all functions in seekdeep_core.py
- [Example Program Guide](docs/seekdeep_example_guide.md): User-friendly guide explaining how to use the example program
- [SeekDeep for Kids](docs/seekdeep_for_kids.md): Simple explanation of the concept for beginners and younger audiences

## Dependencies

- chromadb==0.4.18
- requests>=2.31.0
- flask==2.3.3
- pydantic>=1.10.8 