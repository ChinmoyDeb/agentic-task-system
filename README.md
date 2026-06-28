# Agentic AI Multi-Step Task System

A transparent, rule-based multi-agent AI system that accepts a complex user request, decomposes it into ordered subtasks, assigns each task to a specialized agent, executes the workflow asynchronously, streams intermediate progress, performs manual task batching, and gracefully handles failures.

---

# Project Objective

This project demonstrates the core concepts behind an **Agentic AI System** without relying on black-box agent orchestration frameworks.

Instead of using frameworks such as LangChain, CrewAI, AutoGen, or LangGraph, every stage of planning, task execution, batching, orchestration, and failure handling is implemented manually to clearly illustrate how an agentic pipeline works internally.

---

# Features

* Rule-based task planning
* Multiple specialized agents
* Transparent orchestration
* Manual task batching
* Asynchronous execution using asyncio
* Streaming progress updates
* Retry mechanism for failed tasks
* Graceful failure handling
* Shared execution context
* Local knowledge-base retrieval
* Topic-independent report generation

---

# Project Structure

```
.
├── agents
│   ├── analyzer.py
│   ├── planner.py
│   ├── retriever.py
│   └── writer.py
│
├── core
│   ├── batching.py
│   ├── orchestrator.py
│   └── task.py
│
├── data
│   └── knowledge_base.json
│
└── main.py
```

---

# System Architecture

```
                    User Request
                          │
                          ▼
                  Planner Agent
             (Task Decomposition)
                          │
                          ▼
                  Task Objects Created
                          │
                          ▼
                 Manual Task Batching
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   Retriever Agent   Analyzer Agent   Writer Agent
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  Shared Context Store
                          │
                          ▼
                 Final User Response
```

---

# Workflow

The execution pipeline follows these stages.

## 1. User Request

The application accepts a complex natural language request.

Example:

```
Research remote work benefits, analyze the risks,
and generate an executive report.
```

---

## 2. Planner Agent

The Planner Agent performs transparent rule-based planning.

Responsibilities:

* Read the user request
* Detect requested operations
* Create an ordered execution plan
* Assign specialized agents

Example output:

```
Task 1
Retriever Agent

↓

Task 2
Analyzer Agent

↓

Task 3
Writer Agent
```

Unlike LLM-based planners, every planning decision is fully deterministic and inspectable.

---

## 3. Task Creation

The planner output is converted into Task objects.

Each Task stores:

* task id
* assigned agent
* description
* execution status
* execution result
* error message

Example

```
Task(
    id=1,
    agent="retriever",
    description="Retrieve documents"
)
```

---

## 4. Manual Task Batching

Instead of relying on workflow libraries, batching is implemented manually.

Current dependency order:

```
Retriever

↓

Analyzer

↓

Writer
```

Each batch executes only after the previous dependency has completed.

This keeps the orchestration transparent while allowing parallel execution inside each batch.

---

## 5. Asynchronous Execution

Each execution batch runs using

```
asyncio.gather()
```

This allows independent tasks inside a batch to execute concurrently while preserving dependency ordering between batches.

---

## 6. Retriever Agent

Responsibilities

* Read local JSON knowledge base
* Tokenize user query
* Remove stop words
* Calculate keyword overlap
* Rank documents
* Return best matching documents

The retrieval algorithm is intentionally implemented from scratch.

No vector databases or embedding models are used.

---

# Retrieval Pipeline

```
User Query

↓

Tokenization

↓

Stop-word Removal

↓

Keyword Matching

↓

Document Ranking

↓

Top Documents
```

---

## 7. Analyzer Agent

The Analyzer Agent receives the retrieved documents.

Responsibilities

* Extract document themes
* Identify important findings
* Detect potential risks
* Generate keyword statistics

The implementation is completely rule-based and does not use any black-box NLP model.

Output includes

* themes
* findings
* risks
* top keywords

---

## 8. Writer Agent

The Writer Agent converts analyzed information into a structured report.

The report includes

* Executive Summary
* Key Themes
* Findings
* Top Keywords
* Risks
* Recommendation

Unlike the initial implementation, the final version is topic independent and can summarize any compatible knowledge base.

---

## 9. Shared Context

All agents communicate through a shared context dictionary.

Example

```
context = {

"user_request": ...,

"retrieved_documents": ...,

"themes": ...,

"risks": ...,

"findings": ...

}
```

Every completed agent contributes additional information that becomes available to later agents.

This avoids tight coupling between agents.

---

# Streaming Progress

Instead of waiting for the entire pipeline to complete, progress updates are streamed after every important step.

Example

```
Planning task...

Created 3 tasks.

Executing batch 1...

Retriever started...

Retriever completed.

Executing batch 2...

Analyzer started...

Analyzer completed.

Executing batch 3...

Writer started...

Writer completed.

Pipeline finished.
```

This improves transparency and user experience.

---

# Failure Handling

Every task includes retry logic.

If an exception occurs

```
Task Started

↓

Failure

↓

Retry

↓

Retry

↓

Permanent Failure
```

Each task is retried multiple times before being marked as failed.

If a critical retrieval task fails, the orchestrator safely terminates the remaining pipeline.

This prevents invalid downstream execution.

---

# Execution Flow

```
User Input

↓

Planner

↓

Execution Plan

↓

Task Objects

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

---

# Technologies Used

* Python 3
* asyncio
* dataclasses
* JSON
* Regular Expressions

No external AI orchestration framework is used.

---

# Design Decisions

## Why Rule-Based Planning?

A transparent planner demonstrates the internal mechanics of task decomposition.

This makes every planning decision explainable and reproducible.

---

## Why Manual Batching?

Manual batching clearly demonstrates dependency management.

It avoids hiding execution logic inside third-party workflow libraries.

---

## Why Shared Context?

Shared context allows loose coupling between agents.

Each agent contributes information without directly depending on another agent's implementation.

---

## Why Async Execution?

Async execution enables multiple independent tasks inside the same batch to run concurrently while preserving pipeline order.

---

# Example

Input

```
Research remote work benefits,
analyze the risks,
generate a report.
```

Pipeline

```
Planner

↓

Retriever

↓

Analyzer

↓

Writer
```

Output

```
Executive Report

Summary

Key Themes

Findings

Risks

Recommendation
```

---

# Future Improvements

Potential improvements include

* Semantic retrieval using embeddings
* Dependency graph generation
* Dynamic planner with additional agent types
* Vector database integration
* Plugin-based agent registration
* Parallel retrieval from multiple knowledge sources
* Automatic task dependency detection

---

# Assignment Requirements Mapping

| Requirement            | Implementation                     |
| ---------------------- | ---------------------------------- |
| Accept complex task    | Planner Agent                      |
| Task decomposition     | Rule-based Planner                 |
| Specialized agents     | Retriever, Analyzer, Writer        |
| Async execution        | asyncio.gather()                   |
| Streaming              | Progress updates during execution  |
| Failure handling       | Retry logic + graceful termination |
| Manual batching        | Custom batching module             |
| No black-box framework | Fully manual orchestration         |

---

# Conclusion

This project demonstrates the complete lifecycle of an Agentic AI workflow using transparent, manually implemented orchestration. Every stage—from planning and batching to execution, streaming, and failure handling—is explicitly implemented to showcase a clear understanding of agent coordination without relying on external orchestration frameworks.
