#!/usr/bin/env python3
"""Validate Brainstorm's one-question-at-a-time continuation contract."""

from __future__ import annotations

import logging
from pathlib import Path


LOGGER = logging.getLogger("brainstorm.question-progression")
SKILL_PATH = Path(__file__).parents[1] / "skills" / "brainstorm" / "SKILL.md"


def validate_contract(skill_text: str) -> list[str]:
    """Return wording defects that can reintroduce premature turn completion."""

    violations: list[str] = []

    # A native picker can return a valid answer while the agent turn stays active.
    if "each tool call and each conversational turn" in skill_text:
        violations.append("question limit must not be tied to the conversational turn")

    required_clauses = (
        "Keep at most one unanswered question at a time.",
        "After a valid answer returns, continue the active turn",
        "Do not emit a final answer merely because one question was answered.",
    )
    for clause in required_clauses:
        if clause not in skill_text:
            violations.append(f"missing continuation clause: {clause}")

    return violations


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    violations = validate_contract(skill_text)

    if violations:
        for violation in violations:
            LOGGER.error("%s", violation)
        return 1

    LOGGER.info("question progression contract passed for %s", SKILL_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
