class PlannerAgent:
    """
    Planner Agent

    Converts a user request into an ordered sequence of tasks
    using transparent rule-based planning.
    """

    RETRIEVAL_KEYWORDS = {
        "research", "find", "gather", "retrieve",
        "search", "lookup", "collect", "discover"
    }

    ANALYSIS_KEYWORDS = {
        "analyze", "analysis", "compare", "summarize",
        "summary", "extract", "evaluate", "review",
        "benefits", "risks", "advantages", "disadvantages",
        "insights", "findings"
    }

    REPORT_KEYWORDS = {
        "write", "generate", "report", "brief",
        "document", "response", "answer"
    }

    def contains_keyword(self, request, keywords):
        return any(keyword in request for keyword in keywords)

    def add_step(self, steps, agent, description):
        steps.append({
            "id": len(steps) + 1,
            "agent": agent,
            "description": description
        })

    def plan(self, user_request: str):
        request = user_request.lower()
        steps = []

        retrieval_needed = self.contains_keyword(
            request,
            self.RETRIEVAL_KEYWORDS
        )

        analysis_needed = self.contains_keyword(
            request,
            self.ANALYSIS_KEYWORDS
        )

        report_requested = self.contains_keyword(
            request,
            self.REPORT_KEYWORDS
        )

        if retrieval_needed:
            self.add_step(
                steps,
                "retriever",
                "Retrieve relevant documents from the knowledge base."
            )

        if retrieval_needed or analysis_needed:
            self.add_step(
                steps,
                "analyzer",
                "Analyze retrieved documents and extract findings."
            )

        if report_requested or not steps:
            self.add_step(
                steps,
                "writer",
                "Generate the final user-facing report."
            )
        else:
            self.add_step(
                steps,
                "writer",
                "Generate the final user-facing report."
            )

        return steps
