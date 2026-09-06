# Section feedback regression evidence — 2026-09-06

These results are independent model-based instruction evaluations, not live
Codex CLI or Claude Code UI tests. The evaluator read the candidate skill and
scenario fixture without prior evaluations or the acceptance oracle. The main
agent checked the reported transitions against `question_routing_acceptance.md`.

## Frozen inputs

- Fixture: `question_routing_scenarios.json`, SHA-256
  `185ca1ba94e8ea1c80c4ff5f6da6744027b1729e9187904df3d8479163bd29e7`.
- Before: `skills/brainstorm/SKILL.md`, SHA-256
  `3e0fb5bf013328afbbf592a0ec1c5f2c572dd547c60b008c2d714b2db1f12ed5`.
- After: `skills/brainstorm/SKILL.md`, SHA-256
  `0f81dfa0039eb99f87c7ab94344e00080aaf44007f8e304c0f9ea62a9080a91d`.

## Sequential target evaluations

All evaluators used `gpt-6-astra`, reasoning `xhigh`, fresh context (`none`).
The unchanged target was `section_feedback_continues_default`.

| Evaluator | Result | Observed instruction behavior |
| --- | --- | --- |
| `routing_red_1` | FAIL | Line 99 mandates section approval; lines 175–180 classify it as required input, forcing text despite optional-feedback intent. |
| `routing_red_2` | FAIL | Answer continuation and optional-empty fallback exist, but mandatory section approval conflicts with the requested flow. |
| `routing_red_3` | FAIL | Lines 99 and 231 lack the distinction between optional section refinement and complete-design approval. |
| `routing_green_1` | PASS | Native keep/adjust feedback → answer advances to configuration → empty answer retains provisional defaults and continues. |
| `routing_green_2` | PASS | Same event sequence; neither feedback nor an empty answer opens complete-design or written-spec approval. |
| `routing_green_3` | PASS | Same event sequence; no mandatory section gate or premature final response, complete-design approval remains separate. |

All three failures were obtained before editing the skill. All three passes
used the same revised skill and unchanged fixture. The failing evaluations
identified a contradictory instruction contract, not a recorded UI failure:
an assistant honoring the user's override could already choose the right route.

## Related regression

`routing_green_1` also evaluated all eight pre-existing cases, all PASS:

- Required approval in constrained Default: plain text, wait with gate closed.
- Empty optional Default question: provisional default, continue without retry.
- Async retention: both timed continuations retain one pending question; custom
  60-day answer advances to reader roles, whose acknowledgement stays pending.
- Async-only bounded approval: explicit answer permits delivery, then STOP.
- Sync-allowed bounded approval: native schema, explicit answer, delivery, STOP.
- Claude clarification: native Claude schema, custom answer, next question.
- No question tool: plain-text required approval, no invented tool or approval.
- Cancelled spec approval: one text fallback, later explicit approval, STOP.

Executable checks passed once each:

- `python3 tests/assert_question_progression_contract.py`
- `node tests/assert_standalone_branding.js` (real local HTTP server)
- `python3 /Users/cyenx/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/brainstorm`
- The same format validator against the active installed skill.

The active install at `/Users/cyenx/.agents/skills/brainstorm` matches the repo
skill directory (`diff -qr` produced no differences). Claude Code's skill path
is a symlink to that install. No valid Claude transcript was supplied, so
`assert_claude_recommendation.py` was not run. Live picker rendering and an old
session re-reading the updated instructions remain unverified. During the
evaluations, Git reported `bad object HEAD`, so status/history checks were
unavailable. Before committing, missing objects were restored from a verified
GitHub mirror; `git fsck --full` passed, and the index, HEAD, and working files
were verified unchanged by the repair.
