"""Optional Gemini judge. Disabled unless --use-llm-judge is passed."""

from __future__ import annotations


def judge_answer(_payload: dict) -> dict:
    raise RuntimeError("LLM judge is opt-in and was not requested in this offline run.")
