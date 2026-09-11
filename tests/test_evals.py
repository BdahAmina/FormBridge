from evals.run import run_offline


def test_offline_evals_produce_report() -> None:
    report = run_offline()
    assert "overall_score" in report
    assert report["cases"]
    assert any(case["id"] == "injection_001" and case["passed"] for case in report["cases"])
    assert any(case["id"] == "insufficient_001" and case["passed"] for case in report["cases"])


def test_incorrect_answer_fails_groundedness() -> None:
    from evals.evaluators.core import groundedness_score

    score, meta = groundedness_score(
        "המועד האחרון הוא 12/12/2026",
        [],
        {
            "expected_answer_facts": ["לאמת"],
            "forbidden_claims": ["המועד האחרון הוא 12/12/2026"],
        },
    )
    assert score == 0.0
    assert meta["unsupported"] >= 1
