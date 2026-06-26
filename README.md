\# Agentic AI Multi-Step Task System



\## Overview



This project is a lightweight agentic AI system that accepts a complex user request, decomposes it into ordered subtasks, assigns those subtasks to specialized agents, streams progress while running, and handles failures gracefully.



The project intentionally avoids black-box agent frameworks. Planning, routing, batching, streaming, retries, and failure handling are implemented manually.



\## Features



\- Accepts complex multi-part user requests

\- Decomposes requests into ordered subtasks

\- Uses specialized agents:

&#x20; - Planner Agent

&#x20; - Retriever Agent

&#x20; - Analyzer Agent

&#x20; - Writer Agent

\- Executes through an async pipeline

\- Streams partial progress updates

\- Implements manual batching logic

\- Retries failed tasks

\- Stops safely when required tasks fail



\## How to Run



Install dependencies:



```bash

pip install -r requirements.txt

