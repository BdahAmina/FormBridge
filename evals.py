"""Offline RAG evaluations for FormBridge (no Gemini API required)."""

from __future__ import annotations

from rag import build_knowledge_base, retrieve_passages


SAMPLE_DOCUMENT = """
עיריית באר שבע
הודעה לתשלום ארנונה

לכבוד: אחמד חסן
כתובת: רחוב הרצל 12, באר שבע

נשלחה הודעה זו כי חוב הארנונה לשנת 2026 טרם שולם.
סכום לתשלום: 1,240 ש"ח.
מועד אחרון לתשלום: 15/03/2026.

יש לצרף צילום תעודת זהות ואישור חשבון בנק.
לתשלום יש לפנות למחלקת הגבייה בטלפון 08-1234567.

אם לא תשולם יתרת החוב עד המועד, עלול להיפתח הליך גבייה.
"""


# Each case: question, a phrase that must appear in a top-3 retrieved chunk.
EVAL_CASES = [
    {
        "name": "deadline_hebrew",
        "question": "מה המועד האחרון לתשלום?",
        "must_contain": "15/03/2026",
    },
    {
        "name": "deadline_arabic",
        "question": "ما هو الموعد النهائي للدفع؟",
        "must_contain": "15/03/2026",
    },
    {
        "name": "payment_amount",
        "question": "כמה אני צריך לשלם?",
        "must_contain": "1,240",
    },
    {
        "name": "required_documents",
        "question": "אילו מסמכים צריך לצרף?",
        "must_contain": "תעודת זהות",
    },
    {
        "name": "recipient",
        "question": "למי נשלח המסמך?",
        "must_contain": "אחמד חסן",
    },
    {
        "name": "issuing_org",
        "question": "מי שלח את המסמך?",
        "must_contain": "עיריית באר שבע",
    },
]


def run_evals() -> dict:
    """Run retrieval tests and return a score report."""
    knowledge_base = build_knowledge_base(SAMPLE_DOCUMENT)
    results = []
    passed = 0

    for case in EVAL_CASES:
        passages = retrieve_passages(knowledge_base, case["question"], top_k=3)
        combined = "\n".join(item.text for item in passages)
        success = case["must_contain"] in combined
        passed += int(success)
        results.append(
            {
                "name": case["name"],
                "question": case["question"],
                "success": success,
                "retrieved": [item.text[:120] for item in passages],
            }
        )

    total = len(EVAL_CASES)
    score = round((passed / total) * 100)
    return {
        "metric": "Recall@3 — gold fact appears in the top 3 retrieved passages",
        "passed": passed,
        "total": total,
        "score": score,
        "results": results,
    }


def main() -> None:
    report = run_evals()
    print(f"FormBridge RAG evals: {report['passed']}/{report['total']} ({report['score']}%)")
    print(f"Metric: {report['metric']}")
    print()
    for item in report["results"]:
        mark = "PASS" if item["success"] else "FAIL"
        print(f"[{mark}] {item['name']}: {item['question']}")


if __name__ == "__main__":
    main()
