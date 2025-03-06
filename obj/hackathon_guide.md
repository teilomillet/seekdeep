# DeepSearch Observability Challenge Guide

## Overview

This 3-hour challenge invites participants to implement observability for the DeepSearch system using OpenTelemetry Protocol (OTLP). The focus is on deriving meaningful insights about system behavior rather than completing a prescribed set of tasks.

## Participant Preparation

Participants will benefit from:
- **LLM Knowledge**: Understanding of large language models and their orchestration
- **Observability Skills**: Experience with monitoring, metrics, tracing, and visualization

Participants work in teams, bringing together complementary skills to create more comprehensive solutions.

## Challenge Structure

### Philosophy

We're looking for solutions that:
- Illuminate system behavior in surprising ways
- Create connections between seemingly unrelated metrics
- Provide actionable intelligence for system improvement
- Demonstrate creative approaches to complex monitoring challenges

## Focus Areas

### Foundation Implementation
Creating a solid observability foundation:
- Proper instrumentation of key system components
- Effective collection and processing of telemetry data
- Reliable data pipeline from collection to presentation

### Insight Development
Uncovering meaningful information about the system:
- Patterns in token usage across different operations
- Performance bottlenecks in the research process
- Factors that trigger beast mode activation
- Error propagation and failure modes

### Interactive Capabilities
Building ways to explore the observability data:
- Real-time alerts for important conditions (like keyword detection in prompts)
- Visual tools to explore system behavior
- Export mechanisms for deeper analysis
- Comparative analysis between different runs

### Alerting and Monitoring
Implementing practical monitoring scenarios:
- Setting up keyword detection for sensitive terms in prompts
- Creating token budget threshold alerts
- Detecting excessive iteration counts
- Monitoring LLM latency patterns
- Tracking answer quality trends

## Evaluation Criteria

Solutions will be evaluated on:

1. **Foundation Quality** 
   - How well basic observability is implemented
   - Completeness of the instrumentation
   - Reliability of the data pipeline

2. **Insight Value** 
   - What the solution reveals about the system
   - How actionable and meaningful the findings are
   - Unexpected discoveries that drive understanding

3. **Communication Effectiveness** 
   - Clarity of information presentation
   - Ability to communicate complex patterns
   - Effectiveness of visualizations and explanations

4. **Technical Creativity** 
   - Novel approaches to observability challenges
   - Elegant solutions to difficult monitoring problems
   - Innovative ways to correlate information

## Getting Started

1. Review the observability_tasks.md document for detailed guidance
2. Start by setting up the OpenTelemetry SDK and export pipeline
3. Instrument key system components (deep_search, LLM calls, vector search)
4. Focus on areas you believe will yield the most valuable insights
5. Develop at least one interactive capability
6. Implement at least one alerting scenario

## Enriching Spans with Context

Consider adding these attributes to your spans to provide richer context:
- Research process attributes (iteration number, question type)
- LLM operation details (token counts, prompt templates used)
- Search operation information (original vs. expanded queries)
- Answer generation context (completion status, question being answered)

This additional context can dramatically increase the value of your traces for debugging and analysis.

## Presentation Guidelines

Your 5-minute presentation should include:
1. A brief overview of your instrumentation approach
2. A meaningful insight you discovered about the system
3. A demonstration of at least one interactive capability
4. An example of an alerting scenario you implemented
5. A reflection on what your findings mean for the system

The goal is to demonstrate how your observability solution helps understand and improve the system, not just showing technical implementation details. Focus on the "why" as much as the "how". 