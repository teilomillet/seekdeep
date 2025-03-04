# SeekDeep Example Program Guide

This guide explains how the `seekdeep_example.py` program works. The program demonstrates the DeepSearch concept by providing an interactive way to ask complex research questions and receive thoughtful, researched answers.

## Program Overview

The `seekdeep_example.py` program is a demonstration of the DeepSearch concept. It provides a simple interface where you can:

1. Select or enter a research question
2. Optionally provide your own documents for research
3. Watch as the system researches your question through multiple iterations
4. Receive a comprehensive answer with details about the research process

## Program Structure

The program is organized into clear, focused functions that each handle a specific part of the process:

### 1. Setup and Initialization

- **`ensure_ollama_running()`**: Makes sure the Ollama service (which provides the AI model) is running
- **`ensure_model_pulled()`**: Checks that the required AI model is downloaded and available
- **`main()`**: The entry point that coordinates the whole program

### 2. Document Management

- **`setup_database()`**: Creates and populates the vector database with documents
- **`read_custom_document()`**: Reads user-provided text files to use as research material

### 3. User Interaction

- **`select_query()`**: Shows sample questions and lets you choose one or enter your own
- **`is_valid_query()`**: Makes sure custom questions are specific enough to research
- **`configure_research_parameters()`**: Lets you set how thorough the research should be

### 4. Research Process

- **`run_example()`**: Coordinates the entire research workflow from start to finish
- **`progress_callback()`**: Shows progress indicators while research is happening
- **`display_results()`**: Shows the final answer and research statistics

## How It Works: Step by Step

When you run `seekdeep_example.py`, this is what happens:

1. **Initialization**:
   - The program checks if Ollama is running (starts it if needed)
   - It verifies the AI model is available (downloads it if needed)

2. **Setup**:
   - You're asked if you want to use your own documents
   - The system sets up a vector database with either your documents or the included samples

3. **Question Selection**:
   - You can choose from sample questions or enter your own research question
   - The system validates your question if you enter a custom one

4. **Research Configuration**:
   - You can set the maximum number of iterations (how thorough the research will be)
   - The program shows your selected settings

5. **Research Process**:
   - The DeepSearch algorithm starts working on your question
   - Progress indicators show activity as it works
   - Behind the scenes, it's:
     * Breaking down your question into sub-questions
     * Searching for relevant information
     * Evaluating the quality of answers
     * Asking follow-up questions as needed
     * Synthesizing a final answer

6. **Results**:
   - When finished, the program displays:
     * The complete answer to your question
     * How many iterations were performed
     * Which questions were explored
     * Whether "Beast Mode" was activated for complex questions
     * How much time the research took

## Special Features

### Custom Documents

You can use your own text files as research material:
1. When prompted, choose to use your own documents
2. Enter the path to your text file
3. The system will split the file into chunks and use them for research

### Custom Queries

You can ask your own research questions:
1. Select option #7 "Enter your own research question"
2. Type a specific, detailed question
3. The system will validate your question (it must be specific enough)

### Beast Mode

When a question is particularly complex or the system can't find a satisfactory answer within the set number of iterations, it activates "Beast Mode." This is a comprehensive synthesis approach that uses all gathered information to produce the best possible answer.

## Tips for Good Results

1. **Ask specific questions** - "What are the key differences between deep learning and traditional machine learning?" works better than "Tell me about AI"

2. **Provide relevant documents** if using your own - make sure your documents contain information related to your question

3. **Set appropriate iterations** - more complex questions benefit from more iterations (4-5), while simpler questions may need fewer (2-3)

4. **Be patient** - thorough research takes time, especially with more iterations

5. **Examine the research trail** - look at which questions were explored to understand how the system approached your query

## Exploring the Code

If you're interested in how the program works internally:

1. Each function has detailed comments explaining what it does
2. The main research algorithm is in `seekdeep_core.py`
3. Sample documents are provided by `seekdeep_documents.py`

The code is structured to be educational and demonstrate how you might implement your own DeepSearch system. 