# DeepSearch System Components for Observability

This document provides an overview of key components in the DeepSearch system that could be instrumented for observability. Rather than a checklist of required implementations, consider this a guide to help you identify valuable areas for instrumentation.

## Key Functions in the System

The DeepSearch system includes these important functions that play crucial roles in the research process:

`deep_search` - Main entry point function that orchestrates the entire research process
`deep_research` - Core research iteration loop handling the exploration
`setup_db` - Database initialization for storing and retrieving documents
`add_docs` - Document ingestion process that adds knowledge to the system
`process_llm_call` - LLM interaction handler for various reasoning tasks
`search` - Vector search operation that finds relevant documents
`_decompose_main_question` - Function that breaks down complex questions
`_expand_query` - Query enhancement to improve search results
`_generate_answer` - Answer creation based on retrieved context
`_evaluate_answer` - Quality assessment of generated answers
`_activate_beast_mode` - Comprehensive synthesis of accumulated knowledge

## Potential Trace Points

Consider instrumenting these key transition points in the system, they are not exhaustive:

**Process Boundaries**
- Research iteration start/end
- LLM call entry and exit
- Vector search operations
- Document retrieval

**Reasoning Steps**
- Query parsing and expansion
- Answer generation
- Answer evaluation
- Beast mode activation

## Valuable Metrics to Consider

### Performance Metrics
- Total execution time per research request
- LLM API call latency
- Token consumption (input and output)
- Vector search performance
- Documents retrieved per query
- Time spent in each research phase

### Quality and Process Metrics
- Answer completion status (complete vs. incomplete)
- Number of follow-up questions generated
- Sub-question count from question decomposition
- Beast mode activation frequency
- Early completion events (when satisfactory answers are found)
- Total research iteration count per query
- Gap questions explored during research
- Context size used for each answer generation

### Resource Metrics
- Token usage efficiency
- Memory consumption during research
- LLM API rate limits and usage
- Database connection pool usage

## Useful Context for Spans

These attributes can add valuable context to your trace spans:

### Research Process Attributes
- Current iteration number within the research process
- Question type (original, decomposed, follow-up)
- Current token budget remaining
- Whether beast mode is active
- Evaluation result status (complete/incomplete)
- Number of gap questions in the queue
- Position in the research flow (decomposition, search, answer, evaluate)

### LLM Operation Attributes
- Token counts (input, output, total)
- Prompt template used (decompose, expand, answer, evaluate, beast)
- Estimated token overhead for prompt templates
- LLM model identifier and parameters

### Search Operation Attributes
- Original query text
- Expanded query text
- Query length (character and estimated token count)
- Number of search results returned
- Context size compiled from search results
- Whether context was truncated to fit budget

### Answer Generation Attributes
- Question being answered
- Context size used for generation
- Answer length (character and token count)
- Whether the answer passed evaluation
- Suggested follow-up question if incomplete

## Alerting and Monitoring Examples

Here are some practical alerting and monitoring scenarios you might implement:

- **Keyword Detection in Prompts**: Set up an alert when specific sensitive or problematic words appear in prompts (e.g., detect inappropriate content or potential prompt injection attempts)
- **Token Budget Thresholds**: Create alerts when a research query exceeds 80% of its token budget, allowing for intervention before limits are reached
- **Excessive Iterations**: Monitor when research processes exceed expected iteration counts, which might indicate circular reasoning or unsuccessful searches
- **LLM Latency Spikes**: Alert when LLM response times exceed normal thresholds, which could indicate service degradation
- **Answer Quality Trends**: Track patterns of incomplete answers for certain question types to identify systematic weaknesses
- **Beast Mode Frequency**: Monitor unusual patterns in beast mode activation that might indicate inefficient question handling
- **Database Performance**: Alert on vector search operations taking longer than expected

## Visualization Considerations

When designing visualizations, consider these aspects:

- Research journey visualization showing the path through questions
- Token usage breakdown across different operations
- Latency attribution by component
- Quality metrics over time or iterations
- Question decomposition visualization
- Vector search effectiveness indicators
- LLM performance comparisons

## Error Scenarios to Monitor

Pay attention to these potential error conditions:

- LLM API failures or timeouts
- Token limit exceeded events
- Database connectivity issues
- Malformed queries or prompts
- Research timeout events
- Quality threshold failures

Remember that the most valuable observability doesn't come from covering everything, but from instrumenting the aspects that provide the most meaningful insights into system behavior and performance. 