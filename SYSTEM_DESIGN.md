# System Design Document

## Agentic AI Multi-Step Task System

---

## 1. Introduction

### Objective

The objective of this project is to build a transparent Agentic AI system capable of processing complex user requests by decomposing them into multiple ordered subtasks, assigning those subtasks to specialized agents, executing them asynchronously, streaming intermediate progress, and handling failures gracefully.

Unlike many modern AI systems that rely on orchestration frameworks such as LangChain, CrewAI, AutoGen, or LangGraph, this implementation intentionally builds every stage manually to demonstrate an understanding of the underlying execution process.

---

# 2. System Goals

The system was designed to satisfy the following requirements:

* Accept complex multi-step user requests.
* Decompose requests into ordered subtasks.
* Assign subtasks to specialized agents.
* Execute tasks using an asynchronous pipeline.
* Stream intermediate execution updates.
* Handle failures through retries and graceful termination.
* Perform manual batching without external orchestration frameworks.

---

# 3. High-Level Architecture

```text
                         User
                           │
                           ▼
                  User Request Input
                           │
                           ▼
                   Planner Agent
              (Task Decomposition)
                           │
                           ▼
                    Task Objects
                           │
                           ▼
                 Manual Batch Builder
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Retriever Agent     Analyzer Agent     Writer Agent
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    Shared Context
                           │
                           ▼
                    Final Response
```

---

# 4. System Components

## 4.1 Main Application

**File**

```
main.py
```

Responsibilities

* Accept user input.
* Create the orchestrator.
* Start asynchronous execution.
* Display the final output.

---

## 4.2 Planner Agent

**File**

```
agents/planner.py
```

Purpose

The Planner Agent converts a natural language request into a sequence of executable tasks.

Example

Input

```
Research remote work benefits,
analyze the risks,
generate a report.
```

Generated Plan

```
Task 1 → Retriever

Task 2 → Analyzer

Task 3 → Writer
```

Planning is completely rule-based and deterministic.

No LLM is involved.

---

## 4.3 Task Objects

**File**

```
core/task.py
```

Each planned step becomes a Task object.

Each task stores

* Task ID
* Assigned Agent
* Description
* Status
* Result
* Error Message

Task Lifecycle

```
Pending

↓

Running

↓

Completed
```

or

```
Pending

↓

Running

↓

Failed

↓

Retry

↓

Failed Permanently
```

---

## 4.4 Manual Batch Builder

**File**

```
core/batching.py
```

The batch builder groups tasks according to execution dependencies.

Current dependency order

```
Retriever

↓

Analyzer

↓

Writer
```

Each batch executes only after the previous batch completes successfully.

This batching mechanism is implemented manually without workflow engines.

---

## 4.5 Retriever Agent

**File**

```
agents/retriever.py
```

Responsibilities

* Load local knowledge base.
* Tokenize user query.
* Remove stop words.
* Compare keywords.
* Rank documents.
* Return best matching documents.

Retrieval Pipeline

```
User Query

↓

Tokenization

↓

Stop-word Removal

↓

Keyword Matching

↓

Ranking

↓

Retrieved Documents
```

The retrieval process is transparent and entirely rule-based.

---

## 4.6 Analyzer Agent

**File**

```
agents/analyzer.py
```

Responsibilities

* Read retrieved documents.
* Extract document themes.
* Detect potential risks.
* Generate findings.
* Compute frequently occurring keywords.

Outputs

* Themes
* Findings
* Risks
* Top Keywords

The Analyzer performs deterministic analysis without using machine learning or language models.

---

## 4.7 Writer Agent

**File**

```
agents/writer.py
```

Responsibilities

* Generate the executive report.
* Organize findings.
* Present risks.
* Summarize important keywords.
* Produce recommendations.

Output Structure

* Executive Summary
* Key Themes
* Findings
* Top Keywords
* Risks
* Recommendation

The Writer consumes information produced by previous agents through the shared context.

---

## 4.8 Orchestrator

**File**

```
core/orchestrator.py
```

The orchestrator coordinates the entire workflow.

Responsibilities

* Receive user request.
* Invoke Planner.
* Create task objects.
* Perform manual batching.
* Execute batches asynchronously.
* Stream execution updates.
* Retry failed tasks.
* Maintain shared context.
* Return final report.

The orchestrator acts as the central controller of the system.

---

# 5. Shared Context

The agents communicate indirectly using a shared context dictionary.

Example

```python
context = {

"user_request": "...",

"retrieved_documents": [...],

"themes": [...],

"findings": [...],

"risks": [...],

"top_keywords": [...],

"final_answer": "..."
}
```

Each completed agent contributes new information to the context.

Subsequent agents consume only the information they require.

This design minimizes coupling between agents.

---

# 6. Execution Flow

```
User Input

↓

Planner

↓

Task Creation

↓

Manual Batching

↓

Retriever

↓

Analyzer

↓

Writer

↓

Final Report
```

Execution order is maintained through batching while allowing asynchronous execution inside each batch.

---

# 7. Data Flow

The following diagram illustrates how information moves through the system.

```
User Request
      │
      ▼
Planner
      │
      ▼
Task List
      │
      ▼
Retriever
      │
Retrieved Documents
      │
      ▼
Analyzer
      │
Themes
Findings
Risks
Keywords
      │
      ▼
Writer
      │
      ▼
Final Report
```

---

# 8. Asynchronous Execution

The project uses Python's asyncio library.

Execution inside a batch uses

```python
asyncio.gather(...)
```

Advantages

* Supports concurrent execution.
* Improves responsiveness.
* Preserves dependency ordering between batches.

---

# 9. Streaming

The orchestrator streams progress after every important step.

Example

```
Planning task...

Created 3 tasks...

Executing Batch 1...

Retriever Started...

Retriever Completed...

Executing Batch 2...

Analyzer Started...

Analyzer Completed...

Executing Batch 3...

Writer Started...

Writer Completed...

Pipeline Finished.
```

Streaming improves transparency and allows users to observe pipeline progress.

---

# 10. Failure Handling

Every task supports automatic retry.

Execution Model

```
Task

↓

Failure

↓

Retry

↓

Retry

↓

Permanent Failure
```

Critical retrieval failures terminate downstream execution.

Instead of crashing, the system returns a meaningful explanation to the user.

Example

```
The task could not be completed because no relevant information was found in the knowledge base. After multiple retry attempts, the retrieval step failed and the pipeline terminated gracefully.
```

---

# 11. Design Decisions

## Rule-Based Planning

A deterministic planner was selected because it keeps every planning decision transparent and explainable.

---

## Manual Batching

Manual batching demonstrates dependency management without hiding execution behind external frameworks.

---

## Shared Context

A shared context dictionary allows agents to communicate without depending directly on one another.

This improves modularity.

---

## Local Knowledge Base

A JSON knowledge base was chosen for simplicity and reproducibility.

It avoids requiring databases or external services.

---

## Async Execution

Python asyncio provides lightweight concurrency while keeping execution logic simple.

---

# 12. Scalability Considerations

Current Limitations

* Linear document search.
* Small local knowledge base.
* Rule-based planning.
* Single-machine execution.

Potential Improvements

* Inverted index.
* Vector database.
* Semantic retrieval.
* Dynamic dependency graph.
* Plugin-based agent registration.
* Distributed execution.
* Multiple concurrent retrieval agents.

---

# 13. Security Considerations

The current implementation executes only predefined internal agents.

No external code execution is performed.

The knowledge base is read-only and local to the project.

---

# 14. Conclusion

This project demonstrates a complete manually implemented Agentic AI workflow without relying on external orchestration frameworks.

The system includes task planning, manual batching, asynchronous execution, shared context management, streaming progress updates, retry logic, graceful failure handling, and specialized agents working together to solve multi-step user requests.

The architecture emphasizes transparency, modularity, and explainability while remaining simple enough to understand and extend.
