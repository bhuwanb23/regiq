#!/usr/bin/env python3
"""
REGIQ AI/ML - Q&A Module (Gemini 2.5 Flash)
Builds a simple Q&A system with context retrieval placeholder and confidence scoring.
"""

from pathlib import Path
import sys
from typing import Any, Dict, Optional

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.llm.gemini_client import GeminiClient, GeminiClientConfig, GeminiHelpers


class QASystem:
	def __init__(self, client: Optional[GeminiClient] = None) -> None:
		self.client = client or GeminiClient(GeminiClientConfig())
		self.helpers = GeminiHelpers(self.client)

	def answer(self, question: str, context: str) -> Dict[str, Any]:
		return self.helpers.answer(question, context)

	def answer_with_retrieval(self, question: str, retrieve_context_fn) -> Dict[str, Any]:
		"""Perform retrieval (provided function) then answer.
		retrieve_context_fn: Callable[[str], str] that returns textual context
		"""
		ctx = retrieve_context_fn(question)
		return self.answer(question, ctx)


def main():  # simple manual test
	print("🧪 Testing QASystem")
	qa = QASystem()
	question = "What is the SEC deadline?"
	context = "The SEC requires disclosures by Q4 2025. Deadline: December 31, 2025."
	try:
		ans = qa.answer(question, context)
		print("✅ QA answer:", ans)
	except Exception as e:
		print("❌ QA failed:", e)


if __name__ == "__main__":
	main()
