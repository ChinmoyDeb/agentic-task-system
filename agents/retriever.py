import json
import re


class RetrieverAgent:
    """
    Retriever Agent

    Performs simple manual keyword-based retrieval from a local JSON
    knowledge base. No black-box retrieval framework is used.
    """

    STOP_WORDS = {
        "the", "and", "for", "with", "that", "this", "from", "into",
        "about", "them", "then", "than", "have", "has", "are", "was",
        "were", "been", "being", "can", "could", "should", "would",
        "write", "generate", "create", "summarize", "summary",
        "research", "find", "gather", "retrieve", "analyze", "compare",
        "benefits", "risks", "brief", "executive"
    }

    def __init__(self, data_path="data/knowledge_base.json"):
        self.data_path = data_path

        with open(self.data_path, "r", encoding="utf-8") as file:
            self.knowledge_base = json.load(file)

        if not isinstance(self.knowledge_base, list):
            raise ValueError("Knowledge base must be a JSON list of documents.")

    def _tokenize(self, text: str):
        """
        Converts text into lowercase keyword tokens and removes common words.
        """
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

        return [
            word for word in words
            if word not in self.STOP_WORDS
        ]

    async def run(self, task, context):
        query = context.get("user_request", "")
        query_words = set(self._tokenize(query))

        if not query_words:
            raise ValueError("No meaningful query terms found.")

        results = []

        for document in self.knowledge_base:
            title = document.get("title", "")
            content = document.get("content", "")

            searchable_text = f"{title} {content}"
            document_words = set(self._tokenize(searchable_text))

            overlap = query_words.intersection(document_words)
            score = len(overlap)

            if score > 0:
                results.append({
                    "title": title,
                    "content": content,
                    "score": score,
                    "matched_terms": list(overlap)
                })

        results = sorted(results, key=lambda item: item["score"], reverse=True)

        if not results:
            raise ValueError("No relevant documents found.")

        return {
            "retrieved_documents": results[:3]
        }