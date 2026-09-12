#!/usr/bin/env python3
"""Validate the architectural document approval and implementation handoff."""

from __future__ import annotations

import json
import logging
from pathlib import Path


LOGGER = logging.getLogger("brainstorm.architectural-handoff")
ROOT = Path(__file__).parents[1]
SKILL_PATH = ROOT / "skills" / "brainstorm" / "SKILL.md"
ROOT_README_PATH = ROOT / "README.md"
SKILL_README_PATH = ROOT / "skills" / "brainstorm" / "README.md"
AGENTS_PATH = ROOT / "AGENTS.md"
SCENARIOS_PATH = ROOT / "tests" / "question_routing_scenarios.json"
ACCEPTANCE_PATH = ROOT / "tests" / "question_routing_acceptance.md"


def validate_contract() -> list[str]:
    """Return defects in the approved-document implementation handoff contract."""

    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    root_readme = ROOT_README_PATH.read_text(encoding="utf-8")
    skill_readme = SKILL_README_PATH.read_text(encoding="utf-8")
    agents_text = AGENTS_PATH.read_text(encoding="utf-8")
    acceptance_text = ACCEPTANCE_PATH.read_text(encoding="utf-8")
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    violations: list[str] = []

    required_skill_clauses = (
        "Write every architectural design document with `**Status:** Draft`.",
        "change the document to `**Status:** Approved`",
        "Verify that the Approved status is persisted before asking the implementation question.",
        "Ask one final required question: whether to start implementing the approved design now.",
        "Only an explicit yes to that final question authorizes implementation.",
        "A no, cancellation, empty answer, timeout, or delivery acknowledgement leaves implementation unauthorized",
        "continue the same active task through the host's normal skill selection and repository instructions",
        "does not authorize commit, push, pull-request creation, publication, deployment, or production changes.",
    )
    for clause in required_skill_clauses:
        if clause not in skill_text:
            violations.append(f"missing skill contract: {clause}")

    if "Does not implement or auto-chain to another skill." in skill_text:
        violations.append("frontmatter still forbids the approved architectural handoff")

    documentation_clauses = (
        (root_readme, "Architectural only:"),
        (skill_readme, "`Status: Approved`"),
        (agents_text, "architectural implementation handoff"),
    )
    for text, clause in documentation_clauses:
        if clause not in text:
            violations.append(f"missing synchronized documentation: {clause}")

    expected_ids = {
        "architectural_keep_start_default",
        "architectural_keep_stop_claude",
        "architectural_status_write_failure",
        "architectural_skipped_feedback_draft_stop",
    }
    cases = {case["id"]: case for case in scenarios["cases"]}
    for case_id in expected_ids:
        if case_id not in cases:
            violations.append(f"missing routing scenario: {case_id}")
        if f"`{case_id}`" not in acceptance_text:
            violations.append(f"missing acceptance criterion: {case_id}")

    start_case = cases.get("architectural_keep_start_default")
    if start_case:
        event_order = [event["when"] for event in start_case["events"]]
        expected_order = [
            "written-spec feedback is answered with Keep current design",
            "the document status update completes and is verified",
            "the final implementation question is asked",
            "the user explicitly answers yes",
        ]
        if event_order != expected_order:
            violations.append("architectural start scenario does not preserve handoff ordering")

    return violations


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    violations = validate_contract()

    if violations:
        for violation in violations:
            LOGGER.error("%s", violation)
        return 1

    LOGGER.info("architectural handoff contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
