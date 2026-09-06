# Complete-design and document feedback validation — 2026-09-06

This is a model-based instruction-contract regression, not a live CLI UI test.
It extends the earlier section-only evaluation in
`section_feedback_validation.md`; that earlier report describes the previous
candidate's retained final approval gates, not the current behavior.

## Frozen candidates

- Before SKILL.md SHA-256:
  `0f81dfa0039eb99f87c7ab94344e00080aaf44007f8e304c0f9ea62a9080a91d`
- After SKILL.md SHA-256:
  `0fed2bc56547888088c29e92e82255405a27cc880785f44284a0cc17b5627e46`
- Unchanged test fixture SHA-256:
  `ec4c4403466aa6f783be492789a82739db64b146d348794a650922eb1166ede3`

The fixture added complete-design, written-spec, and bounded native-feedback
cases before any skill edit. The existing cancelled-spec case now explicitly
requests approval, so it checks preservation of a user-required gate rather
than the removed default gate. Acceptance criteria were updated before testing.

Each evaluator used gpt-6-astra, xhigh reasoning, and fresh context (`none`).
Evaluators received the candidate and fixture, not earlier conclusions or the
acceptance oracle. The main agent independently compared their traces with
`question_routing_acceptance.md` and inspected the resulting diff.

## Sequential red/green results

| Evaluator | Scope | Result |
| --- | --- | --- |
| final_red_1 | Three new cases | All FAIL |
| final_red_2 | Three new cases | All FAIL |
| final_red_3 | Three new cases | All FAIL |
| final_green_1 | All 12 cases | All PASS |
| final_green_2 | All 12 cases | All PASS |
| final_green_3 | All 12 cases | All PASS |

All red runs preceded the skill edit. They independently identified the same
conflicts: old lines 99/237 required approval before writing, 100/258 required
a commit, 270–276 required final approval before delivery, and 40–44/91–92
required approval for bounded delivery. A host-priority-compliant assistant
could override those instructions, but the written contract was contradictory.

All green runs used the same revised skill and unchanged fixture. Their traces
agreed on these observable transitions:

- Complete design: optional native feedback → empty → provisional local draft
  and self-review → native document feedback → keep → uncommitted delivery.
- Written spec: native feedback → custom recovery clarification → edit and
  self-review → delivery, without a renewed approval request.
- Bounded design: native feedback → empty → provisional in-chat delivery.
- Section feedback: answer → next section/question in the same active flow;
  empty next answer → continued provisional drafting.
- User-required approvals: preserve the gate, choose the permitted native
  tool or required plain-text route, and wait for an explicit answer.
- Async acknowledgement and automatic continuations: retain one pending
  question; a custom answer advances to the next question, not a duplicate.
- Cancelled user-required approval: one plain-text fallback when control
  returns; later explicit approval permits delivery, not implementation.

## Other verification

Passed once each: question-progression assertion, real HTTP standalone-branding
test, skill format validation in the repo and installed directory, and
`git diff --check`. `diff -qr` confirmed the installed skill directory matched
the repo. Claude Code's skill path links to the same installed directory.

No current Claude transcript was supplied, so transcript recommendation
validation was not run. Live CLI picker rendering, interaction with the
original session after re-reading, and real model compliance remain unverified.
No commit or push was performed during this correction.
