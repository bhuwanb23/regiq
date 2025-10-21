#!/usr/bin/env python3
"""
REGIQ AI/ML - Summarization Module (Gemini 2.5 Flash)
Provides document summarization, executive summaries, and key points extraction.
"""

from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.llm.gemini_client import GeminiClient, GeminiClientConfig, GeminiHelpers


class SummarizationService:
	def __init__(self, client: Optional[GeminiClient] = None) -> None:
		self.client = client or GeminiClient(GeminiClientConfig())
		self.helpers = GeminiHelpers(self.client)

	def summarize_document(self, text: str, style: str = "executive", max_bullets: int = 6) -> Dict[str, Any]:
		return self.helpers.summarize(text, style=style, max_bullets=max_bullets)

	def executive_summary(self, text: str) -> Dict[str, Any]:
		return self.summarize_document(text, style="executive", max_bullets=6)

	def key_points(self, text: str, max_points: int = 8) -> List[str]:
		return self.helpers.key_points(text, max_points=max_points)


def main():  # simple manual test
	print("🧪 Testing SummarizationService")
	service = SummarizationService()
	sample = "Regulatory update: The SEC requires enhanced disclosures by Q4 2025. Institutions must implement new reporting controls."
	try:
		data = service.executive_summary(sample)
		print("✅ Executive summary:", data)
	except Exception as e:
		print("❌ Summarization failed:", e)


if __name__ == "__main__":
	main()
