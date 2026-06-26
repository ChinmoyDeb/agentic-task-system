class PlannerAgent:
    """
    Planner Agent

    Converts a complex user request into ordered subtasks.
    This implementation is intentionally rule-based and transparent.
    """

    def plan(self, user_request: str):
        request = user_request.lower()
        steps = []

        if any(word in request for word in ["research", "find", "gather", "retrieve"]):
            steps.append({
                "id": len(steps) + 1,
                "agent": "retriever",
                "description": "Retrieve relevant information from the knowledge base"
            })

        if any(word in request for word in ["analyze", "compare", "summarize", "extract", "benefits", "risks"]):
            steps.append({
                "id": len(steps) + 1,
                "agent": "analyzer",
                "description": "Analyze retrieved information and extract themes and risks"
            })

        steps.append({
            "id": len(steps) + 1,
            "agent": "writer",
            "description": "Generate the final response"
        })

        return steps
