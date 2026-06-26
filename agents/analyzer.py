class AnalyzerAgent:
    """
    Analyzer Agent

    Reads retrieved documents and extracts simple structured findings.
    """

    async def run(self, task, context):
        documents = context.get("retrieved_documents", [])

        if not documents:
            raise ValueError("Analyzer received no documents.")

        themes = []
        risks = []

        for document in documents:
            content = document["content"].lower()

            if "productivity" in content:
                themes.append(
                    "Remote or hybrid work can improve productivity when supported by clear goals."
                )

            if "flexibility" in content:
                themes.append(
                    "Flexibility is a major benefit for employees and teams."
                )

            if "communication" in content:
                themes.append(
                    "Strong communication practices are important for distributed teams."
                )

            if "collaboration" in content:
                themes.append(
                    "Hybrid work can preserve collaboration while offering flexibility."
                )

            if "security" in content:
                risks.append(
                    "Security concerns must be managed carefully."
                )

            if "isolation" in content:
                risks.append(
                    "Employee isolation is a possible risk."
                )

            if "coordination" in content:
                risks.append(
                    "Coordination overhead can increase in remote environments."
                )

        return {
            "themes": list(set(themes)),
            "risks": list(set(risks))
        }
