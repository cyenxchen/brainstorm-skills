#!/usr/bin/env python3
"""Assert that Claude AskUserQuestion calls expose one recommended first option."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Iterator


LOGGER = logging.getLogger("brainstorm.claude-recommendation")
RECOMMENDED_SUFFIX = " (Recommended)"


def iter_ask_user_question_inputs(session_path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    """Yield AskUserQuestion inputs from a Claude Code JSONL transcript."""

    with session_path.open(encoding="utf-8") as session_file:
        for line_number, raw_line in enumerate(session_file, start=1):
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON on line {line_number}: {error}") from error

            content = event.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if (
                    isinstance(block, dict)
                    and block.get("type") == "tool_use"
                    and block.get("name") == "AskUserQuestion"
                ):
                    tool_input = block.get("input")
                    if not isinstance(tool_input, dict):
                        raise ValueError(
                            f"AskUserQuestion on line {line_number} has no object input"
                        )
                    yield line_number, tool_input


def validate_session(session_path: Path) -> list[str]:
    """Return all recommendation-contract violations in one transcript."""

    violations: list[str] = []
    call_count = 0

    for line_number, tool_input in iter_ask_user_question_inputs(session_path):
        call_count += 1
        questions = tool_input.get("questions")
        if not isinstance(questions, list) or not questions:
            violations.append(f"line {line_number}: questions must be a non-empty array")
            continue

        for question_index, question in enumerate(questions, start=1):
            options = question.get("options") if isinstance(question, dict) else None
            if not isinstance(options, list) or not options:
                violations.append(
                    f"line {line_number}, question {question_index}: options must be non-empty"
                )
                continue

            labels = [
                option.get("label", "") if isinstance(option, dict) else ""
                for option in options
            ]
            recommended_indexes = [
                index for index, label in enumerate(labels) if label.endswith(RECOMMENDED_SUFFIX)
            ]

            # Claude Code has no separate recommendation field: the first label
            # must carry the literal suffix so the native picker can render it.
            if recommended_indexes != [0]:
                violations.append(
                    f"line {line_number}, question {question_index}: expected exactly one "
                    f"recommended first option, got labels={labels!r}"
                )

    if call_count == 0:
        violations.append("no AskUserQuestion calls found")

    LOGGER.info("checked %d AskUserQuestion call(s) in %s", call_count, session_path)
    return violations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Brainstorm's Claude AskUserQuestion recommendation contract."
    )
    parser.add_argument("session", type=Path, help="Claude Code JSONL session transcript")
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = parse_args()

    try:
        violations = validate_session(args.session)
    except (OSError, ValueError) as error:
        LOGGER.error("could not validate session: %s", error)
        return 2

    if violations:
        for violation in violations:
            LOGGER.error("%s", violation)
        return 1

    LOGGER.info("recommendation contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
