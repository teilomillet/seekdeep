# DeepSearch Observability Implementation Targets

This document identifies specific components and functions in the DeepSearch codebase that should be instrumented for observability.

## Core Functions to Instrument

- [ ] `deep_search` - Main entry point function
- [ ] `deep_research` - Core research iteration loop
- [ ] `setup_db` - Database initialization
- [ ] `add_docs` - Document ingestion process
- [ ] `process_llm_call` - LLM interaction handler
- [ ] `search` - Vector search operation
- [ ] `_decompose_main_question` - Question breakdown
- [ ] `_expand_query` - Query enhancement 
- [ ] `_generate_answer` - Answer creation
- [ ] `_evaluate_answer` - Answer assessment
- [ ] `_perform_beast_mode` - Accelerated answer generation

## Trace Points

- [ ] Research iteration boundaries
- [ ] LLM call entry and exit
- [ ] Vector search operations
- [ ] Document retrieval
- [ ] Query parsing
- [ ] Answer generation
- [ ] Evaluation steps

## Metrics to Collect

### Counter Metrics
- [ ] Total research iterations
- [ ] LLM API calls made
- [ ] Tokens consumed (input)
- [ ] Tokens generated (output)
- [ ] Vector searches performed
- [ ] Documents retrieved
- [ ] Beast mode activations
- [ ] Early stopping events
- [ ] Hallucination detections

### Gauge Metrics
- [ ] Average search latency
- [ ] Current token consumption rate
- [ ] Vector DB response time
- [ ] LLM response time
- [ ] Question complexity score
- [ ] Running search count

### Histogram Metrics
- [ ] LLM latency distribution
- [ ] Token count distribution
- [ ] Vector search latency distribution
- [ ] Answer quality score distribution
- [ ] Iteration count distribution

## Log Points

- [ ] Research start/completion
- [ ] Question decomposition results
- [ ] Query expansion results
- [ ] Vector search queries and results
- [ ] LLM prompts and responses
- [ ] Answer evaluation details
- [ ] Beast mode triggers
- [ ] Hallucination detection events

## Custom Attributes for Spans

- [ ] Question complexity
- [ ] Token counts
- [ ] Answer quality metrics
- [ ] Research iteration number
- [ ] Search query parameters
- [ ] Document relevance scores
- [ ] LLM model identifier
- [ ] Prompt template used

## Visualization Requirements

- [ ] Research journey flowchart
- [ ] Token usage timeline
- [ ] Latency breakdown by component
- [ ] Answer quality progression
- [ ] Question decomposition tree
- [ ] Vector search effectiveness
- [ ] LLM performance metrics

## Database Instrumentation

- [ ] ChromaDB query operations
- [ ] Document embedding generation
- [ ] Similarity search latency
- [ ] Index statistics 

## Error and Exception Tracking

- [ ] LLM API failures
- [ ] Token limit exceeded events
- [ ] Database connectivity issues
- [ ] Malformed queries
- [ ] Timeout events 