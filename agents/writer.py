class WriterAgent:
    """
    Writer Agent

    Produces the final user-facing answer from analyzed findings.
    """

    async def run(self, task, context):
        themes = context.get("themes") or []
        risks = context.get("risks") or []

        if not themes and not risks:
            return {
                "final_answer": "I could not find enough information to produce a detailed final answer."
            }

        output = "Executive Brief\n"
        output += "===============\n\n"

        output += "Summary:\n"
        output += (
            "Remote and hybrid work have become important operating models for modern organizations. "
            "The available information suggests that these models can create benefits when supported "
            "by strong communication, clear goals, and intentional collaboration practices.\n\n"
        )

        output += "Key Themes:\n"
        for theme in themes:
            output += f"- {theme}\n"

        output += "\nRisks and Considerations:\n"
        for risk in risks:
            output += f"- {risk}\n"

        output += "\nRecommendation:\n"
        output += (
            "Organizations should adopt a balanced approach that combines flexibility with clear "
            "communication norms, security practices, and support systems for employees."
        )

        return {
            "final_answer": output
        }