import re


class AnalyzerAgent:
    """
    Analyzer Agent

    Analyzes retrieved documents and extracts generic themes,
    risks, and key findings without relying on any black-box model.
    """

    RISK_KEYWORDS = {
        "risk", "risks", "issue", "issues", "problem", "problems",
        "challenge", "challenges", "concern", "concerns",
        "security", "isolation", "coordination", "failure",
        "overhead", "limitation", "limitations", "drawback",
        "drawbacks"
    }

    STOP_WORDS = {
        "the", "and", "for", "with", "that", "this", "from",
        "into", "about", "have", "has", "been", "being",
        "were", "was", "their", "there", "they", "them",
        "while", "which", "where", "when", "your", "our",
        "more", "less", "very", "many", "much", "also",
        "than", "into", "over", "under", "between"
    }

    def extract_keywords(self, text):
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())

        keywords = []

        for word in words:
            if word not in self.STOP_WORDS:
                keywords.append(word)

        return keywords

    async def run(self, task, context):
        documents = context.get("retrieved_documents", [])

        if not documents:
            raise ValueError("Analyzer received no documents.")

        themes = []
        risks = []
        findings = []
        keyword_frequency = {}

        for document in documents:
            title = document.get("title", "")
            content = document.get("content", "")

            findings.append(content)

            if title:
                themes.append(title)

            words = self.extract_keywords(content)

            for word in words:
                keyword_frequency[word] = keyword_frequency.get(word, 0) + 1

                if word in self.RISK_KEYWORDS:
                    risks.append(
                        f"Potential concern related to '{word}'."
                    )

        top_keywords = sorted(
            keyword_frequency.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]

        return {
            "themes": list(dict.fromkeys(themes)),
            "risks": list(dict.fromkeys(risks)),
            "findings": findings,
            "top_keywords": [word for word, _ in top_keywords]
        }
