class WriterAgent:
    """
    Writer Agent

    Produces a generic executive report using the analyzed
    information provided by previous agents.
    """

    async def run(self, task, context):
        themes = context.get("themes", [])
        risks = context.get("risks", [])
        findings = context.get("findings", [])
        top_keywords = context.get("top_keywords", [])

        if not themes and not findings:
            return {
                "final_answer": (
                    "I could not find enough information to generate a meaningful report."
                )
            }

        output = []
        output.append("EXECUTIVE REPORT")
        output.append("=" * 60)
        output.append("")

        output.append("Summary")
        output.append("-" * 60)

        output.append(
            "The available documents were retrieved, analyzed, and summarized "
            "using a transparent rule-based agent pipeline. The following "
            "sections highlight the primary findings, recurring themes, "
            "potential risks, and important keywords."
        )

        output.append("")

        if themes:
            output.append("Key Themes")
            output.append("-" * 60)

            for index, theme in enumerate(themes, start=1):
                output.append(f"{index}. {theme}")

            output.append("")

        if findings:
            output.append("Key Findings")
            output.append("-" * 60)

            for index, finding in enumerate(findings, start=1):
                output.append(f"{index}. {finding}")

            output.append("")

        if top_keywords:
            output.append("Top Keywords")
            output.append("-" * 60)

            output.append(", ".join(top_keywords))
            output.append("")

        if risks:
            output.append("Risks / Considerations")
            output.append("-" * 60)

            for index, risk in enumerate(risks, start=1):
                output.append(f"{index}. {risk}")

            output.append("")
        else:
            output.append("Risks / Considerations")
            output.append("-" * 60)
            output.append("No explicit risks were identified in the retrieved documents.")
            output.append("")

        output.append("Recommendation")
        output.append("-" * 60)

        output.append(
            "Decision-makers should review the identified themes and findings "
            "before taking action. Any potential risks should be evaluated "
            "alongside the available evidence to support informed decisions."
        )

        output.append("")
        output.append("=" * 60)
        output.append("End of Report")

        return {
            "final_answer": "\n".join(output)
        }
