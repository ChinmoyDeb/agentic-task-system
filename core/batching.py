def create_batches(tasks):
    """
    Manually groups tasks into execution batches.

    Dependency order:
    1. Retriever tasks run first.
    2. Analyzer tasks run second.
    3. Writer tasks run last.

    This avoids using any black-box workflow abstraction.
    """

    batches = []

    retriever_tasks = [task for task in tasks if task.agent == "retriever"]
    analyzer_tasks = [task for task in tasks if task.agent == "analyzer"]
    writer_tasks = [task for task in tasks if task.agent == "writer"]

    if retriever_tasks:
        batches.append(retriever_tasks)

    if analyzer_tasks:
        batches.append(analyzer_tasks)

    if writer_tasks:
        batches.append(writer_tasks)

    return batches
