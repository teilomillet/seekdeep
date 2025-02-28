"""
Prompts and data structures for the DeepSearch implementation using deepseek-r1.
This file contains all the text templates needed for the compact core implementation.
"""

# Prompt for decomposing questions into sub-questions
DECOMPOSE_PROMPT = """
You are a research assistant breaking down complex questions.
Given a research question, identify 2-3 sub-questions that would help answer the main question.
Keep the sub-questions specific, relevant, and phrased as questions.

Original question: {question}

Output 2-3 sub-questions as a numbered list, one per line.
"""

# Prompt for expanding queries with synonyms and related terms
EXPAND_PROMPT = """
You are a search query optimizer. Expand the given query with synonyms and related terms to improve search results.
Create a more comprehensive search query by adding related concepts, alternative terminology, or specific terms.

Query: {query}

Expanded query (maintain brevity):
"""

# Prompt for generating an answer based on context
ANSWER_PROMPT = """
You are a knowledgeable assistant answering questions based on retrieved context.
Use the provided context to answer the question accurately and comprehensively.
Only use information from the context provided.

Question: {question}

Context:
{context}

Answer:
"""

# Prompt for comprehensive answer evaluation
EVALUATE_PROMPT = """
You are evaluating the quality of an answer to a research question.
Assess whether the answer satisfies the following criteria:
1. Relevance: Does the answer directly address the question?
2. Completeness: Does the answer cover all key aspects of the question?
3. Accuracy: Is the information provided correct, based on your knowledge?
4. Clarity: Is the answer clear, well-organized, and easy to understand?

Question: {question}

Answer: {answer}

For each criterion, output:
- PASS or FAIL
- Brief reason for the decision
- Whether further research is needed

Then conclude with an overall assessment:
- If more research is needed, suggest a better query.
- If no more research is needed, state that the answer is satisfactory.
"""

# Prompt for beast mode (using all available information)
BEAST_MODE_PROMPT = """
You are a research specialist tasked with providing the best possible answer based on all available information.
Review all search results and previous attempts to construct a comprehensive answer to the original question.
Use all available context to provide the most complete answer possible.

Original Question: {question}

All Available Context:
{full_context}

Search History:
{search_history}

Provide a comprehensive, authoritative answer to the original question:
""" 