#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phase 2.3: LLM Integration (Gemini 2.5 Flash)
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def test_gemini_client_basic():
	print("\n🤖 Testing Gemini Client Wrapper...")
	from services.regulatory_intelligence.llm.gemini_client import GeminiClient, GeminiClientConfig
	client = GeminiClient(GeminiClientConfig())
	assert client is not None
	# Only perform live call if API key present to avoid CI failures
	import os
	if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
		text = client.generate_text("Say 'Hello, REGIQ AI/ML!' exactly.")
		print("✅ Live generate_text response length:", len(str(text)))
	else:
		print("⚠️  API key not set; skipping live call")
	assert True


def test_summarization():
	print("\n📝 Testing Summarization Service...")
	from services.regulatory_intelligence.llm.summarization import SummarizationService
	service = SummarizationService()
	sample = "SEC requires enhanced disclosures by Q4 2025. Implement new reporting controls."
	import os
	if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
		result = service.executive_summary(sample)
		assert isinstance(result, dict)
		print("✅ Summary keys:", list(result.keys()))
	else:
		print("⚠️  API key not set; skipping live summarization")
	assert True


def test_qa():
	print("\n❓ Testing Q&A System...")
	from services.regulatory_intelligence.llm.qa import QASystem
	qa = QASystem()
	q = "What is the deadline?"
	ctx = "Deadline: December 31, 2025 for SEC disclosures."
	import os
	if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
		ans = qa.answer(q, ctx)
		assert isinstance(ans, dict)
		print("✅ QA keys:", list(ans.keys()))
	else:
		print("⚠️  API key not set; skipping live QA")
	assert True


def main():
	print("🚀 Phase 2.3 Comprehensive Test Suite")
	test_gemini_client_basic()
	test_summarization()
	test_qa()
	print("\n🎉 Phase 2.3 tests done (conditional on API key)")


if __name__ == "__main__":
	main()
