import asyncio

from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.analyzer import AnalyzerAgent
from agents.writer import WriterAgent
from core.task import Task
from core.batching import create_batches


class Orchestrator:
    """
    Coordinates the full agentic workflow.

    Responsibilities:
    - Accept the user request
    - Ask planner to create subtasks
    - Convert plan into Task objects
    - Batch tasks manually
    - Route each task to the correct agent
    - Stream progress to the user
    - Retry failed tasks
    - Stop safely when required tasks fail
    """

    def __init__(self):
        self.planner = PlannerAgent()

        self.agents = {
            "retriever": RetrieverAgent(),
            "analyzer": AnalyzerAgent(),
            "writer": WriterAgent()
        }

    async def stream(self, message):
        print(message)
        await asyncio.sleep(0.2)

    async def execute_task(self, task, context):
        agent = self.agents[task.agent]
        max_retries = 2

        for attempt in range(max_retries + 1):
            try:
                task.status = "running"

                await self.stream(
                    f"[Task {task.id}] Starting {task.agent}: {task.description}"
                )

                result = await agent.run(task, context)

                task.status = "completed"
                task.result = result
                task.error = None

                context.update(result)

                await self.stream(
                    f"[Task {task.id}] Completed successfully."
                )

                return task

            except Exception as error:
                task.status = "failed"
                task.error = str(error)

                await self.stream(
                    f"[Task {task.id}] Failed attempt {attempt + 1}: {error}"
                )

                if attempt < max_retries:
                    await self.stream(f"[Task {task.id}] Retrying...")
                    await asyncio.sleep(0.5)
                else:
                    await self.stream(
                        f"[Task {task.id}] Failed permanently. Continuing safely."
                    )
                    return task

    async def run(self, user_request):
        context = {
            "user_request": user_request
        }

        await self.stream("Planning task...")

        plan = self.planner.plan(user_request)

        tasks = [
            Task(
                id=step["id"],
                agent=step["agent"],
                description=step["description"]
            )
            for step in plan
        ]

        await self.stream(f"Created {len(tasks)} task(s).")

        batches = create_batches(tasks)

        for batch_index, batch in enumerate(batches, start=1):
            await self.stream(f"\nExecuting batch {batch_index}...")

            results = await asyncio.gather(
                *[self.execute_task(task, context) for task in batch]
            )

            failed_required_tasks = [
                task for task in results
                if task.status == "failed" and task.agent == "retriever"
            ]

            if failed_required_tasks:
                await self.stream(
                    "A required retrieval task failed. Stopping pipeline gracefully."
                )
                break

        await self.stream("\nPipeline finished.")

        if "final_answer" not in context:context["final_answer"] = (
        "The requested task could not be completed because the retriever "
        "was unable to find relevant information after multiple retry attempts. "
        "The pipeline terminated gracefully to avoid producing an inaccurate report."
    )

        return context
