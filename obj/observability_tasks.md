# DeepSearch Observability Challenge

This document outlines our observability challenge for the DeepSearch system. Unlike typical implementation tasks, we want you to think creatively about what's worth monitoring and how to derive meaningful insights from system behavior.

## Challenge Philosophy

Observability is about answering questions you didn't know you'd need to ask. This challenge focuses on showing what matters by identifying meaningful system behaviors, communicating insights by making complex patterns understandable, enabling action by providing information that drives decisions and improvements, and revealing the invisible by surfacing hidden relationships between components.

## What We're Looking For

Rather than checking boxes on a rigid task list, we'll evaluate your solution based on how well it achieves these goals:

### Core Requirements

Your solution must use OpenTelemetry for instrumentation (no terminal logs), provide a working demonstration of your observability solution, and show meaningful insights into a system (DeepSearch's?) behavior.

### Evaluation Areas

We'll evaluate your solution across four main areas:

**1. Foundation Quality**
We'll assess how well you implemented basic observability, including proper instrumentation of key system components, effective collection and processing of telemetry data, and a reliable data pipeline from collection to presentation.

**2. Insight Value**
What did your solution reveal about the system? We value unexpected discoveries about system behavior, clear correlation between different metrics or events, information that helps understand why things happen, and insights that would lead to system improvements.

**3. Communication Effectiveness**
How well are insights communicated? We'll consider the clarity of information presentation, ability to surface important signals amid noise, logical organization of related information, and effective use of context to explain meaning.

**4. Technical Creativity**
How was your implementation? Points for novel approaches to monitoring complex operations, elegant solutions to difficult observability challenges, innovative ways to correlate disparate information, and creative instrumentation that reveals hidden patterns.

## Suggested Focus Areas

While you're free to explore what you find interesting, here are some areas that might yield valuable insights:

### System Behavior Understanding

Consider how question decomposition affects research quality, what patterns appear in token usage across different operations, how the system adapts to different query types, and what triggers beast mode activation and what are its effects.

### Operational Excellence

Look into where the performance bottlenecks are in the research process, how we can identify research queries that might struggle, what metrics predict successful vs. unsuccessful research, and how errors propagate through the system.

### Interactive Exploration

Think about how users might explore the question decomposition process, how we might compare multiple research runs, what would help debug a problematic search, and how we can export research artifacts for further analysis.

## Examples of Valuable Insights

Focus on achievable, practical insights that would be impossible to discover without proper observability tools. Here are examples of the types of insights we're looking for:

### Performance Analysis Insights

**Timing comparison:** "We identified that 70% of total execution time is spent in vector search operations, making it the clear optimization target."

**Simple metric comparison:** "By comparing runs with and without beast mode, we found that beast mode uses 3x more tokens but improves answer quality by only 15% for certain question types."

**Basic bottleneck identification:** "Our traces showed that query expansion takes longer than expected (40% of total time) despite using few tokens, revealing an unexpected bottleneck."

**Pipeline evaluation:** "We traced how changing one metric (context size) affected the entire pipeline performance, allowing us to find the optimal setting."

**Error source identification:** "By capturing spans for each operation, we pinpointed that 90% of failed searches originated from poor question decomposition, not from the vector search itself."

### Production Monitoring Insights

**Token budget alerts:** "We created alerts that trigger when a research query approaches 75% of its token budget (5000 tokens), allowing intervention before hitting context limitations."

**Beast mode activation monitoring:** "By tracking when beast mode activates at the end of iterations, we can proactively allocate more compute resources and notify users of potentially longer processing times."

**Answer evaluation tracking:** "Our monitoring shows when answers are marked 'incomplete' vs 'complete' by the evaluation function, helping identify patterns in question types that typically require multiple iterations."

**Question decomposition metrics:** "We discovered that questions decomposed into more than 4 sub-questions were 70% more likely to trigger beast mode, indicating a correlation between question complexity and research thoroughness."

**Iteration path visualization:** "By tracing the path through gap questions during research, we can now identify common exploration patterns and see which questions frequently lead to dead-ends versus useful insights."

Remember, we value insights that would be impossible to discover without proper observability tools, can directly lead to system improvements, are clear, specific, and actionable, and don't require extremely complex analysis to be valuable.

The best demonstrations will show how even simple observability implementations can reveal surprising and useful information about the system.

## Demonstration Elements

We expect your presentation to include these elements:

### 1. System Observability Infrastructure

Show your basic instrumentation and telemetry pipeline. Demonstrate how you collect, process and store observability data. Explain your approach to instrumentation.

*We choose to use X because Y, and we implemented Z to achieve W.*

### 2. Key Insights Demonstration

Present an explanation about the system behavior that would influence decisions or understanding.

*We discovered that X, and this helps us understand Y, which in turn allows us to improve Z.*

### 3. Interactive Capabilities

Demonstrate at least one interactive capability that allows deeper exploration of system behavior. This could take several forms:

**Real-time Alerts:** Show customizable alerts triggered by defined conditions such as token usage thresholds, unusual pattern detection, or performance degradation warnings. Demonstrate how these alerts provide actionable information.

**Interactive Exploration Tools:** Provide visual tools to inspect system behavior, such as tracing query decomposition visually, exploring research trails, or examining token usage patterns. Show how these tools reveal insights that static visualizations cannot.

**Artifact Exporting:** Demonstrate mechanisms to export telemetry data for external analysis, such as research trail exports, query pattern collections, or performance profiles. Show how these exports would enable deeper offline analysis.

**Correlation & Comparative Analysis:** Build interfaces allowing comparison between different executions, like side-by-side run comparisons, pattern detection across queries, or effectiveness metrics. Demonstrate how these comparisons reveal patterns not visible in single runs.

### 4. Technical Highlights

Briefly explain any particularly implementation details, showcase unique approaches you developed, and discuss challenges you overcame.

## What Makes a Successful Demo

A successful demonstration will clearly show:

1. **Complete Implementation:** A working end-to-end observability solution using OpenTelemetry
2. **Meaningful Insights:** At least an explanation about the system behavior that would influence decisions or understanding
3. **Interactive Capability:** At least one compelling way to interact with the observability data beyond static dashboards
4. **Technical Quality:** Clean implementation with thoughtful instrumentation choices
5. **Communication Clarity:** The ability to effectively explain what your solution reveals and why it matters

The goal is to demonstrate how your observability solution helps understand and improve the system, not just to show visualizations.

## Implementation Guidance

While we're not prescribing specific tasks, here's a suggested approach:

**First Hour:** Focus on building a solid foundation by setting up OpenTelemetry SDK and export pipeline, instrumenting key system components (deep_search, LLM calls, vector search), and verifying data collection and basic presentation.

**Second Hour:** Develop meaningful insights by identifying interesting patterns and relationships, creating ways to effectively communicate these findings, and beginning to build interactive capabilities.

**Final Hour:** Refine and prepare your demonstration by polishing your most valuable insights for presentation, ensuring clear communication of findings, and preparing to demonstrate key capabilities.

## Final Notes

Remember that observability is ultimately about understanding system behavior in ways that weren't anticipated during development. The most valuable solutions will be those that help us see DeepSearch in new ways and provide actionable insights for improvement.

We're excited to see your creative approaches to this challenge!

 