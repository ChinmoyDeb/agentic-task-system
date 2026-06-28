# Post-Mortem Document

## Agentic AI Multi-Step Task System

---

# 1. Project Overview

This project implements a transparent Agentic AI system capable of processing complex multi-step user requests through a manually orchestrated workflow.

Instead of relying on high-level orchestration frameworks, the project demonstrates the underlying mechanics of task decomposition, agent coordination, asynchronous execution, manual batching, streaming, retry logic, and graceful failure handling.

The final system consists of four specialized agents coordinated by a custom orchestrator:

* Planner Agent
* Retriever Agent
* Analyzer Agent
* Writer Agent

The project satisfies the assignment requirements while intentionally keeping the architecture simple, explainable, and easy to extend.

---

# 2. What Went Well

Several aspects of the implementation worked particularly well during development.

### Transparent Architecture

Building the orchestration manually provided complete control over task execution. Every planning and execution step is visible, making the workflow easy to debug and explain.

---

### Modular Agent Design

Each agent has a single responsibility.

* Planner performs task decomposition.
* Retriever searches the knowledge base.
* Analyzer extracts structured information.
* Writer generates the final report.

This separation of responsibilities made the project easier to develop and maintain.

---

### Asynchronous Execution

Using Python's asyncio simplified concurrent execution while preserving dependency ordering through manual batching.

Although the current pipeline contains only one task per batch, the architecture already supports executing multiple independent tasks concurrently in future extensions.

---

### Graceful Failure Handling

The retry mechanism and graceful pipeline termination behaved as expected.

Instead of crashing when information could not be retrieved, the system retries failed tasks before safely terminating with a meaningful user-facing explanation.

This behavior significantly improves reliability.

---

# 3. Scaling Issue

## Current Limitation

The largest scalability concern is the retrieval mechanism.

The Retriever Agent currently performs a linear search across every document stored inside the local JSON knowledge base.

Execution flow

```text id="8p2st4"
Load JSON

↓

Loop through every document

↓

Tokenize

↓

Compare keywords

↓

Rank documents
```

As the knowledge base grows, retrieval time increases linearly.

For a small demonstration dataset this is acceptable, but performance would degrade significantly with thousands or millions of documents.

---

## Future Improvement

To improve scalability, the retrieval layer could be redesigned using an inverted index or a vector database.

Possible improvements include

* Inverted index
* TF-IDF ranking
* Semantic embeddings
* Vector databases such as FAISS or Chroma
* Parallel document retrieval

These approaches would significantly reduce search time while improving retrieval quality.

---

# 4. Design Change I Would Make

If redesigning the system from scratch, I would replace the current fixed batch ordering with dependency-driven task scheduling.

Current implementation

```text id="8e29fq"
Retriever

↓

Analyzer

↓

Writer
```

Although this satisfies the assignment requirements, it assumes a fixed execution order.

Instead, each task could explicitly declare its dependencies.

Example

```text id="dwlvwd"
Task A

↓

Task C

Task B

↓

Task D
```

The orchestrator could automatically identify independent tasks and execute them concurrently.

Benefits

* Greater flexibility
* Improved scalability
* Easier addition of new agent types
* Better parallelism
* More generic workflow engine

---

# 5. Trade-Off 1

## Rule-Based Planning vs Intelligent Planning

The Planner Agent intentionally uses deterministic rule-based planning instead of a language model.

### Advantages

* Fully transparent execution.
* Easy to debug.
* Predictable behavior.
* No external dependencies.
* Fast execution.

### Disadvantages

* Limited understanding of natural language.
* Requires predefined keywords.
* Less adaptable to unfamiliar requests.

### Reasoning

The assignment explicitly requested avoiding black-box agent frameworks and demonstrating an understanding of internal execution.

A rule-based planner better supports those goals than an opaque language model.

---

# 6. Trade-Off 2

## Local Knowledge Base vs External Retrieval

The project stores information inside a local JSON file.

### Advantages

* Simple implementation.
* Completely offline.
* No API keys.
* Fast setup.
* Easy to reproduce.

### Disadvantages

* Limited amount of information.
* Manual updates required.
* Cannot answer arbitrary user queries.
* Retrieval quality depends entirely on available documents.

### Reasoning

Using a local knowledge base keeps the project deterministic and easy to evaluate while demonstrating retrieval logic without introducing external services or network dependencies.

---

# 7. Lessons Learned

Developing the system highlighted several important software engineering principles.

### Separation of Responsibilities

Breaking the workflow into specialized agents significantly simplified implementation.

Each component could be developed and tested independently.

---

### Shared Context Simplifies Communication

Using a shared context dictionary allowed agents to exchange information without directly depending on one another.

This reduced coupling and improved maintainability.

---

### Failure Handling Matters

A successful system must not only handle successful execution but also recover gracefully when failures occur.

Implementing retries and meaningful failure messages improved the overall robustness of the pipeline.

---

### Simplicity Improves Explainability

Although more sophisticated architectures exist, the manually implemented orchestrator clearly demonstrates how agentic workflows function internally.

This transparency aligns well with the educational objective of the assignment.

---

# 8. Future Improvements

If additional development time were available, the following improvements would be implemented.

* Dynamic dependency graph generation.
* Semantic document retrieval.
* Plugin-based agent registration.
* Multiple concurrent retriever agents.
* Persistent task queues.
* Configuration-driven workflow definitions.
* Distributed execution across multiple workers.
* Automatic task dependency detection.
* Rich terminal progress indicators.
* Support for multiple knowledge bases.

---

# 9. Final Reflection

This project successfully demonstrates the core concepts behind an Agentic AI system without relying on external orchestration frameworks.

The implementation includes transparent task planning, manual batching, asynchronous execution, streaming progress updates, retry logic, graceful failure handling, and modular specialized agents.

While the system intentionally favors simplicity over production-scale performance, the overall architecture provides a strong foundation that can be extended with more sophisticated planning, retrieval, and execution strategies in future iterations.

The project achieved its primary objective of demonstrating an understanding of how agentic systems operate internally while satisfying the functional requirements of the assignment.
