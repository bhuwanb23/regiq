#!/usr/bin/env python3
"""
REGIQ AI/ML - Gemini Client Wrapper
Provides a robust wrapper around Google Gemini API (gemini-2.5-flash) with:
- Exponential retry/backoff
- Simple rate limiting
- Structured output helpers
- Error handling and logging

Reference: https://ai.google.dev/gemini-api/docs
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass

# Official SDK per docs
# https://ai.google.dev/gemini-api/docs
try:
	from google import genai
except Exception as _e:  # pragma: no cover
	genai = None  # Allow import without SDK installed for non-API tests

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from config.env_config import get_env_config


@dataclass
class GeminiClientConfig:
	model: str = "gemini-2.5-flash"
	max_retries: int = 3
	initial_backoff_seconds: float = 1.5
	rate_limit_rpm: int = 60  # requests per minute
	timeout_seconds: int = 60
	# Optionally allow passing API key directly; otherwise use env
	api_key_env_var: str = "GEMINI_API_KEY"  # as shown in docs curl uses x-goog-api-key


class RateLimiter:
	"""Simple fixed-window RPM rate limiter."""
	def __init__(self, requests_per_minute: int) -> None:
		self.requests_per_minute = max(1, requests_per_minute)
		self.window_start = time.time()
		self.request_count = 0

	def acquire(self) -> None:
		window = 60.0
		now = time.time()
		elapsed = now - self.window_start
		if elapsed >= window:
			self.window_start = now
			self.request_count = 0
		self.request_count += 1
		if self.request_count > self.requests_per_minute:
			# sleep until next window
			sleep_for = window - elapsed
			time.sleep(max(0.0, sleep_for))
			self.window_start = time.time()
			self.request_count = 1


class GeminiClient:
	"""High-level Gemini client focused on text operations."""
	def __init__(self, config: Optional[GeminiClientConfig] = None) -> None:
		self.config = config or GeminiClientConfig()
		self.logger = self._setup_logger()
		self.env_config = get_env_config()
		self._rate_limiter = RateLimiter(self.config.rate_limit_rpm)
		self._client = self._init_client()

	def _setup_logger(self) -> logging.Logger:
		logger = logging.getLogger("gemini_client")
		logger.setLevel(logging.INFO)
		if not logger.handlers:
			h = logging.StreamHandler()
			h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
			logger.addHandler(h)
		return logger

	def _init_client(self):
		if genai is None:
			self.logger.warning("google-genai SDK not available; install google-genai to enable API calls")
			return None
		# The SDK picks API key from environment automatically. Ensure it's present.
		api_key = os.getenv(self.config.api_key_env_var) or os.getenv("GOOGLE_API_KEY")
		if not api_key:
			self.logger.warning("Gemini API key not found in environment; API calls will fail until configured")
		# Construct client (per docs example)
		try:
			client = genai.Client()
			return client
		except Exception as e:  # pragma: no cover
			self.logger.error(f"Failed to init Gemini client: {e}")
			return None

	def _retry_loop(self, func: Callable[[], Any]) -> Any:
		attempt = 0
		backoff = self.config.initial_backoff_seconds
		while True:
			try:
				self._rate_limiter.acquire()
				return func()
			except Exception as e:
				attempt += 1
				# Simple heuristic: retry on 429/5xx or transient errors in message
				msg = str(e)
				is_retriable = any(tok in msg for tok in ["429", "Rate limit", "timeout", "temporar", "unavailable", "5", "deadline"])
				if attempt >= self.config.max_retries or not is_retriable:
					self.logger.error(f"Gemini call failed (attempt {attempt}): {e}")
					raise
				self.logger.warning(f"Retrying Gemini call (attempt {attempt}) after error: {e}")
				time.sleep(backoff)
				backoff *= 2

	def generate_text(self, prompt: str, model: Optional[str] = None, safety_settings: Optional[Dict[str, Any]] = None) -> str:
		"""Generate free-form text from a prompt using gemini-2.5-flash by default."""
		if self._client is None:
			raise RuntimeError("Gemini client not initialized")
		use_model = model or self.config.model
		def _call():
			resp = self._client.models.generate_content(
				model=use_model,
				contents=prompt,
			)
			return getattr(resp, "text", None) or getattr(resp, "output_text", None) or str(resp)
		return self._retry_loop(_call)

	def generate_structured_json(self, prompt: str, schema_hint: Optional[Dict[str, Any]] = None, model: Optional[str] = None) -> Dict[str, Any]:
		"""Ask Gemini to return JSON; best-effort coercion with fallback parsing."""
		text = self.generate_text(self._json_prompt(prompt, schema_hint), model=model)
		# try parse json from text; tolerate fenced blocks
		clean = text.strip()
		if clean.startswith("```"):
			clean = clean.strip('`')
			# After stripping fences, attempt to find JSON braces
		start = clean.find('{')
		end = clean.rfind('}')
		if start != -1 and end != -1 and end > start:
			clean = clean[start:end+1]
		try:
			return json.loads(clean)
		except Exception:
			return {"raw": text}

	def _json_prompt(self, user_prompt: str, schema_hint: Optional[Dict[str, Any]]) -> str:
		parts = [
			"You are to respond ONLY with valid JSON. Do not include explanations.",
			"If you cannot produce the requested structure, return an empty JSON object {}.",
		]
		if schema_hint:
			parts.append("JSON schema hint: " + json.dumps(schema_hint))
		parts.append("Task: " + user_prompt)
		return "\n\n".join(parts)


# Convenience helpers tailored to project
class GeminiHelpers:
	def __init__(self, client: GeminiClient) -> None:
		self.client = client

	def summarize(self, text: str, style: str = "executive", max_bullets: int = 6) -> Dict[str, Any]:
		prompt = (
			"Summarize the following regulatory document.\n"
			f"Style: {style} summary.\n"
			f"Include: overview, key points (<= {max_bullets}), risks, deadlines, required actions.\n"
			"Return JSON with keys: overview, key_points (array), risks, deadlines, actions.\n\n"
			"DOCUMENT:\n" + text
		)
		schema = {
			"overview": "string",
			"key_points": ["string"],
			"risks": "string",
			"deadlines": "string",
			"actions": "string",
		}
		return self.client.generate_structured_json(prompt, schema)

	def key_points(self, text: str, max_points: int = 8) -> List[str]:
		prompt = (
			f"Extract up to {max_points} concise, actionable key points from the document.\n"
			"Return JSON array of strings only.\n\nDOCUMENT:\n" + text
		)
		data = self.client.generate_structured_json(prompt, {"items": "string"})
		if isinstance(data, list):
			return data
		return data.get("key_points") or data.get("items") or data.get("raw", [])

	def answer(self, question: str, context: str) -> Dict[str, Any]:
		prompt = (
			"You are a compliance and regulatory assistant.\n"
			"Answer the QUESTION using only the CONTEXT. If uncertain, say 'insufficient context'.\n"
			"Return JSON with keys: answer, confidence (0-1), citations (array of quoted snippets).\n\n"
			"CONTEXT:\n" + context + "\n\nQUESTION: " + question
		)
		schema = {"answer": "string", "confidence": "number", "citations": ["string"]}
		return self.client.generate_structured_json(prompt, schema)
