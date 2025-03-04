# Function Reference for SeekDeep

This document provides a comprehensive reference for all functions and types defined in `seekdeep_core.py`.

## Type Definitions

### SearchResult
```python
class SearchResult(TypedDict):
    """Type for search result item"""
    text: str
    metadata: Dict[str, Any]
    id: str
```

A dictionary type for representing individual search results from the vector database:
- `text`: The document content
- `metadata`: Associated metadata for the document
- `id`: The unique identifier of the document

### EvaluationResult
```python
class EvaluationResult(TypedDict):
    """Type for evaluation result"""
    status: str
    suggested: Optional[str]
```

A dictionary type for representing the evaluation of an answer:
- `status`: Either "complete" or "incomplete"
- `suggested`: An optional follow-up question if the answer is incomplete

### DeepResearchResult
```python
class DeepResearchResult(TypedDict):
    """Type for deep_research result"""
    answer: str
    iterations: int
    memory: Dict[str, Any]
    beast_mode: Optional[bool]
```

A dictionary type for the result of the `deep_research` function:
- `answer`: The final answer generated
- `iterations`: Number of iterations performed
- `memory`: Research memory containing sub-questions, search history, and answer attempts
- `beast_mode`: Flag indicating if beast mode was activated for final answer

### DeepSearchResult
```python
class DeepSearchResult(TypedDict):
    """Type for deep_search result"""
    answer: str
    iterations: int
    gap_questions: List[str]
    search_history: List[Dict[str, Any]]
    research_trail: List[Dict[str, Any]]
    beast_mode: Optional[bool]
```

A dictionary type for the result of the `deep_search` function:
- `answer`: The final answer generated
- `iterations`: Number of iterations performed
- `gap_questions`: Questions explored during the research process
- `search_history`: Record of all searches performed
- `research_trail`: Detailed record of the research process
- `beast_mode`: Flag indicating if beast mode was activated for final answer

## Utility Functions

### estimate_tokens
```python
def estimate_tokens(text: str) -> int
```

Estimates the number of tokens in a text string using the typical token-to-character ratio in English text (approximately 4 characters per token).

**Parameters:**
- `text (str)`: The text to estimate token count for

**Returns:**
- `int`: Estimated number of tokens in the text

### trim_context_to_budget
```python
def trim_context_to_budget(context_items: List[Dict[str, str]], token_budget: int) -> str
```

Trims a list of context items to fit within a specified token budget, prioritizing more recent items.

**Parameters:**
- `context_items (List[Dict[str, str]])`: List of context dictionaries with "question" and "context" keys
- `token_budget (int)`: Maximum number of tokens to include

**Returns:**
- `str`: Combined context string that fits within the token budget

## Database Functions

### setup_db
```python
def setup_db(name: str = "research_collection") -> Collection
```

Creates and initializes a new ChromaDB collection for document storage.

**Parameters:**
- `name (str)`: The name to give the collection. Defaults to "research_collection"

**Returns:**
- `Collection`: A ChromaDB collection object

### add_docs
```python
def add_docs(collection: Collection, texts: List[str], ids: Optional[List[str]] = None, metadatas: Optional[List[Dict[str, Any]]] = None) -> Collection
```

Adds documents to a ChromaDB collection with optional custom IDs and metadata.

**Parameters:**
- `collection`: The ChromaDB collection where documents will be stored
- `texts (list)`: List of text strings to add to the collection
- `ids (list, optional)`: List of unique IDs for each document
- `metadatas (list, optional)`: List of metadata dictionaries for each document

**Returns:**
- `Collection`: The updated ChromaDB collection

### search
```python
def search(collection: Collection, query: str, n_results: int = 3) -> List[SearchResult]
```

Performs a semantic search on the ChromaDB collection to find relevant documents.

**Parameters:**
- `collection`: ChromaDB collection to search
- `query (str)`: Search query string
- `n_results (int)`: Number of most relevant results to return (default: 3)

**Returns:**
- `list`: List of SearchResult dictionaries containing text, metadata, and id

## LLM Interaction Functions

### generate
```python
def generate(prompt: str, model: str = "deepseek-r1:1.5b", base_url: str = "http://localhost:11434/api") -> str
```

Generates text using a Large Language Model via API.

**Parameters:**
- `prompt (str)`: The text prompt to send to the language model
- `model (str)`: The model identifier to use for generation (default: "deepseek-r1:1.5b")
- `base_url (str)`: The base URL of the API endpoint (default: "http://localhost:11434/api")

**Returns:**
- `str`: The generated text response from the model

### process_llm_calls
```python
def process_llm_calls(question: str, context: Optional[str] = None, answer: Optional[str] = None, mode: str = "decompose") -> Union[List[str], str, EvaluationResult]
```

Processes LLM calls for different modes of research operation.

**Parameters:**
- `question (str)`: The question or query to process
- `context (str, optional)`: Contextual information for answer generation
- `answer (str, optional)`: An answer to evaluate, used only in evaluate mode
- `mode (str)`: The operation mode - one of: "decompose", "expand", "answer", "evaluate", or "beast" (default: "decompose")

**Returns:**
- `varies`: 
  - decompose mode: list of sub-questions
  - expand mode: str containing enhanced query
  - answer/beast mode: str containing the generated answer
  - evaluate mode: EvaluationResult dict with status and suggested follow-up

## Helper Functions

### _decompose_main_question
```python
def _decompose_main_question(question: str) -> Tuple[List[str], int]
```

Extracts sub-questions from the main question for exploration.

**Parameters:**
- `question (str)`: The main research question

**Returns:**
- `Tuple[List[str], int]`: A tuple containing the list of sub-questions and the token usage

### _expand_search_query
```python
def _expand_search_query(question: str) -> Tuple[str, int]
```

Expands the search query for better retrieval.

**Parameters:**
- `question (str)`: The question to expand

**Returns:**
- `Tuple[str, int]`: A tuple containing the expanded query and the token usage

### _perform_search
```python
def _perform_search(collection: Collection, query: str, token_budget: int) -> Tuple[List[SearchResult], str, int]
```

Performs semantic search and prepares context within budget.

**Parameters:**
- `collection (Collection)`: The ChromaDB collection to search
- `query (str)`: The search query
- `token_budget (int)`: Maximum number of tokens to include

**Returns:**
- `Tuple[List[SearchResult], str, int]`: A tuple containing search results, context string, and token usage

### _generate_and_evaluate
```python
def _generate_and_evaluate(question: str, current_question: str, context_str: str) -> Tuple[str, Dict[str, Any], int]
```

Generates an answer and evaluates its completeness.

**Parameters:**
- `question (str)`: The main research question
- `current_question (str)`: The current sub-question being processed
- `context_str (str)`: Retrieved context for answer generation

**Returns:**
- `Tuple[str, Dict[str, Any], int]`: A tuple containing the answer, evaluation result, and token usage

### _activate_beast_mode
```python
def _activate_beast_mode(question: str, knowledge: List[Dict[str, str]], token_budget: int, current_usage: int) -> Tuple[str, int]
```

Generates a comprehensive answer in beast mode.

**Parameters:**
- `question (str)`: The main research question
- `knowledge (List[Dict[str, str]])`: Accumulated knowledge from research
- `token_budget (int)`: Maximum token budget
- `current_usage (int)`: Current token usage

**Returns:**
- `Tuple[str, int]`: A tuple containing the beast mode answer and token usage

### _select_next_question
```python
def _select_next_question(sub_questions: List[str], current_iteration: int, eval_result: Dict[str, Any], original_question: str) -> str
```

Selects the next question to process based on iteration and evaluation.

**Parameters:**
- `sub_questions (List[str])`: List of sub-questions
- `current_iteration (int)`: Current iteration index
- `eval_result (Dict[str, Any])`: Evaluation result of the current answer
- `original_question (str)`: The original research question

**Returns:**
- `str`: The next question to process

### _process_research_step
```python
def _process_research_step(current_query: str, collection: Collection, memory: Dict[str, List[Any]], main_question: str) -> Tuple[str, Dict[str, Any], bool]
```

Processes a single research step and returns the answer, evaluation result, and completion status.

**Parameters:**
- `current_query (str)`: The current question being processed
- `collection (Collection)`: The ChromaDB collection to search
- `memory (Dict[str, List[Any]])`: Research memory
- `main_question (str)`: The main research question

**Returns:**
- `Tuple[str, Dict[str, Any], bool]`: A tuple containing the answer, evaluation result, and completion status

### _generate_beast_mode_answer
```python
def _generate_beast_mode_answer(question: str, context: str, memory: Dict[str, List[Any]]) -> str
```

Generates a comprehensive answer using beast mode.

**Parameters:**
- `question (str)`: The main research question
- `context (str)`: The context for answer generation
- `memory (Dict[str, List[Any]])`: Research memory

**Returns:**
- `str`: The comprehensive beast mode answer

## Core Research Functions

### deep_research
```python
def deep_research(question: str, collection: Collection, max_iterations: int = 3) -> DeepResearchResult
```

Performs an in-depth research process on a question using iterative decomposition and refinement.

**Parameters:**
- `question (str)`: The main research question to investigate
- `collection (Collection)`: ChromaDB collection containing the knowledge documents to search
- `max_iterations (int)`: Maximum number of research iterations before forced completion (default: 3)

**Returns:**
- `DeepResearchResult`: A dictionary containing answer, iterations, and research data

### deep_search
```python
def deep_search(question: str, collection: Collection, max_iterations: int = 3, token_budget: int = 5000, progress_callback: Optional[Callable[[], None]] = None) -> DeepSearchResult
```

Performs a breadth-first search-based research approach to answer complex questions.

**Parameters:**
- `question (str)`: The main research question to investigate
- `collection (Collection)`: ChromaDB collection containing the knowledge documents to search
- `max_iterations (int)`: Maximum number of iterations before forced completion (default: 3)
- `token_budget (int)`: Approximate maximum token count to use for context (default: 5000)
- `progress_callback (function)`: Optional callback function to report progress

**Returns:**
- `DeepSearchResult`: A dictionary containing answer, iterations, and research data 