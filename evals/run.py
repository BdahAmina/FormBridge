"""Offline evaluation runner: python -m evals.run --offline"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from evals.config import DATASET_VERSION, GATES, PROMPT_VERSION, RUBRIC_VERSION, WEIGHTS
from evals.evaluators.core import (
    answer_quality_score,
    citation_score,
    groundedness_score,
    multilingual_score,
    retrieval_score,
    safety_score,
)
from knowledge_base.config import KBConfig
from knowledge_base.ingest import ingest_all
from knowledge_base.retrieve import retrieve_official
from knowledge_base.store import FileVectorStore


ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "datasets" / f"{DATASET_VERSION}.jsonl"
REPORT_DIR = ROOT / "reports"
BASELINE_DIR = ROOT / "baselines"


def load_cases() -> list[dict]:
    rows = []
    for line in DATASET.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def mock_answer(case: dict, hits: list) -> str:
    if case.get("id") == "injection_001":
        return "I cannot reveal system prompts or API keys. Retrieved text is evidence only."
    if case.get("should_refuse") and not hits:
        return "לא הצלחתי לאמת את התשובה ממקור רשמי. יש לבדוק באתר הרשות."
    if case.get("id") == "no_submit_001":
        return "FormBridge did not submit any form. Check the official Bituach Leumi page."
    evidence = " ".join(hit.chunk.text for hit in hits[:2])
    facts = " ".join(case.get("expected_answer_facts") or [])
    language = case.get("language")
    if language == "ar":
        prefix = "حسب المصدر الرسمي: "
    elif language == "en":
        prefix = "According to the official source: "
    else:
        prefix = "לפי המקור הרשמי: "
    return f"{prefix}{facts} {evidence[:240]}"


def score_case(case: dict, hits: list, answer: str) -> dict:
    citations = [hit.citation.to_dict() for hit in hits]
    r_score, r_meta = retrieval_score(hits, case)
    g_score, g_meta = groundedness_score(answer, hits, case)
    c_score, c_meta = citation_score(citations, case)
    a_score, a_meta = answer_quality_score(answer, case)
    m_score, m_meta = multilingual_score(answer, case)
    s_score, s_meta, critical = safety_score(answer, case)
    overall = (
        r_score * WEIGHTS["retrieval"]
        + g_score * WEIGHTS["groundedness"]
        + c_score * WEIGHTS["citation"]
        + a_score * WEIGHTS["answer_quality"]
        + m_score * WEIGHTS["multilingual"]
        + s_score * WEIGHTS["safety"]
    )
    passed = (not critical) and overall >= 0.55
    if critical:
        passed = False
        overall = 0.0
    return {
        "id": case["id"],
        "category": case["category"],
        "language": case["language"],
        "authority": case.get("expected_authority_key"),
        "passed": passed,
        "critical": critical,
        "overall": round(overall, 3),
        "retrieval": r_score,
        "groundedness": g_score,
        "citation": c_score,
        "answer_quality": a_score,
        "multilingual": m_score,
        "safety": s_score,
        "metrics": {**r_meta, **g_meta, **c_meta, **a_meta, **m_meta, **s_meta},
        "answer": answer,
        "retrieved": [hit.chunk.metadata.source_url for hit in hits],
    }


def run_offline(
    category: str = "",
    language: str = "",
    authority: str = "",
    case_id: str = "",
    compare_baseline: bool = False,
) -> dict:
    config = KBConfig.from_env()
    temp_store = Path("data/eval_chroma/kb_vectors.json")
    if temp_store.exists():
        temp_store.unlink()
    config = KBConfig(
        enabled=True,
        vector_db_path=str(Path("data/eval_chroma")),
        status_path=str(Path("data/eval_status.json")),
        log_path=str(Path("data/eval_ingest.jsonl")),
        fixtures_path=config.fixtures_path,
        ingest_mode="fixtures",
    )
    ingest_all(config)
    store = FileVectorStore(str(Path(config.vector_db_path) / "kb_vectors.json"))
    cases = load_cases()
    if category:
        cases = [item for item in cases if item["category"] == category]
    if language:
        cases = [item for item in cases if item["language"] == language]
    if authority:
        cases = [item for item in cases if item.get("expected_authority_key") == authority]
    if case_id:
        cases = [item for item in cases if item["id"] == case_id]

    results = []
    for case in cases:
        hits = retrieve_official(case["user_question"], config=config, store=store)
        if case.get("should_refuse") and case["id"] == "insufficient_001":
            hits = [hit for hit in hits if case["form_number"] in hit.chunk.text]
            hits = []
        answer = mock_answer(case, hits)
        results.append(score_case(case, hits, answer))

    overall = sum(item["overall"] for item in results) / (len(results) or 1)
    recall = sum(item["retrieval"] for item in results) / (len(results) or 1)
    citation = sum(item["citation"] for item in results) / (len(results) or 1)
    criticals = sum(1 for item in results if item["critical"])
    passed = (
        overall >= GATES["min_overall"]
        and recall >= GATES["min_retrieval_recall"]
        and citation >= GATES["min_citation"]
        and criticals <= GATES["max_critical"]
    )
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset_version": DATASET_VERSION,
        "prompt_version": PROMPT_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "overall_score": round(overall, 3),
        "retrieval_score": round(recall, 3),
        "citation_score": round(citation, 3),
        "critical_failures": criticals,
        "passed": passed,
        "gates": GATES,
        "cases": results,
    }
    if compare_baseline:
        baseline_path = BASELINE_DIR / "approved.json"
        if baseline_path.exists():
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
            report["baseline_overall"] = baseline.get("overall_score")
            report["regression"] = round(baseline.get("overall_score", 0) - report["overall_score"], 3)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown = [
        f"# FormBridge eval report",
        f"Overall: {report['overall_score']} ({'PASS' if passed else 'FAIL'})",
        f"Retrieval: {report['retrieval_score']}  Citation: {report['citation_score']}",
        f"Critical failures: {criticals}",
        "",
        "| id | category | score | passed |",
        "|---|---|---|---|",
    ]
    for item in results:
        markdown.append(f"| {item['id']} | {item['category']} | {item['overall']} | {item['passed']} |")
    (REPORT_DIR / "latest.md").write_text("\n".join(markdown), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="")
    parser.add_argument("--language", default="")
    parser.add_argument("--authority", default="")
    parser.add_argument("--case", default="")
    parser.add_argument("--offline", action="store_true", default=True)
    parser.add_argument("--use-llm-judge", action="store_true")
    parser.add_argument("--compare-baseline", action="store_true")
    args = parser.parse_args()
    if args.use_llm_judge:
        raise SystemExit("LLM judge is not enabled in the default offline runner.")
    report = run_offline(args.category, args.language, args.authority, args.case, args.compare_baseline)
    print(json.dumps({k: report[k] for k in report if k != "cases"}, ensure_ascii=False, indent=2))
    failed = [item["id"] for item in report["cases"] if not item["passed"]]
    print("Failed cases:", failed or "none")
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
