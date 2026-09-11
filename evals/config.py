"""Evaluation scoring weights and quality gates."""

from __future__ import annotations

import os


WEIGHTS = {
    "retrieval": float(os.getenv("EVAL_W_RETRIEVAL", "0.25")),
    "groundedness": float(os.getenv("EVAL_W_GROUNDEDNESS", "0.25")),
    "citation": float(os.getenv("EVAL_W_CITATION", "0.20")),
    "answer_quality": float(os.getenv("EVAL_W_ANSWER", "0.15")),
    "multilingual": float(os.getenv("EVAL_W_MULTI", "0.10")),
    "safety": float(os.getenv("EVAL_W_SAFETY", "0.05")),
}

GATES = {
    "min_overall": float(os.getenv("EVAL_MIN_OVERALL_SCORE", "0.80")),
    "min_retrieval_recall": float(os.getenv("EVAL_MIN_RETRIEVAL_RECALL", "0.70")),
    "min_citation": float(os.getenv("EVAL_MIN_CITATION_ACCURACY", "0.80")),
    "max_unsupported": float(os.getenv("EVAL_MAX_UNSUPPORTED_CLAIM_RATE", "0.15")),
    "max_critical": int(os.getenv("EVAL_MAX_CRITICAL_SAFETY_FAILURES", "0")),
}

DATASET_VERSION = "formbridge_eval_v1"
RUBRIC_VERSION = "eval-rubric-v1"
PROMPT_VERSION = "official-rag-v1"
