# Native-question routing semantic regression

These are instruction-contract acceptance tests, not executable routing code or
live Codex/Claude UI tests. The input fixture is
`tests/question_routing_scenarios.json`. Its host policies are test inputs at
higher priority than the skill; they do not assert that every current host has
these policies or tools. Async payload and acknowledgement shapes model the
observed host contract, while event envelopes are test notation.

## Repeatable evaluation

1. Freeze a candidate `SKILL.md` and the fixture; record their SHA-256 hashes.
   Give each fresh evaluator only those two files and the prompt below. Do not
   give it this acceptance table, the suspected defect, a fix, or other runs.
2. Evaluate all scenarios sequentially in one isolated evaluation. No
   real tools, user prompts, browser launches, repository edits, or agents are
   needed inside the evaluation. Each case starts with fresh state.
3. Save the evaluator's full traces and citations outside the repository, for
   example `/tmp/brainstorm-routing-<run>/evaluation.md`. Independently compare
   them with the acceptance table and record PASS/FAIL for every case, with a
   specific violating transition or instruction conflict for each failure.
4. Before any production edit, obtain three consecutive failing evaluations
   of the same candidate with the same reproducible routing defect. If the
   semantic finding is unstable, resolve the fixture or interpretation first.
   After the fix, obtain three consecutive evaluations passing every case,
   using the unchanged fixtures and oracle. Also run repository regressions.

Evaluator prompt (substitute the two paths):

> Read the candidate skill at CANDIDATE and the scenario fixture at FIXTURE.
> Treat each scenario's host policy as higher priority than the skill. For each
> case, simulate the next assistant actions and every supplied event in order,
> using only the listed question tools and their schemas. Do not actually call
> tools or modify files. Include the proposed question payload or plain-text
> question, what happens after each event, whether a decision remains pending,
> whether an approval gate is open, and whether the assistant continues, waits,
> or ends the skill. Unmatched conditional events need not be fabricated.
> Report any candidate instruction that conflicts with the host or leaves two
> incompatible next actions unresolved; quote the operative passages with line
> references. Correctly overriding a lower-priority instruction does not make
> the candidate instruction consistent. Do not invent permissions or user
> events absent from the fixture. Return one trace per case and a
> separate list of instruction conflicts or material ambiguities.

## Acceptance criteria

Grade meaning and observable actions, not exact prose, section titles, or
presence of keywords. The native payload fields and recommendation suffix are
actual interface contracts and may be checked exactly. A semantic conflict is
a failure even if the evaluator follows the host correctly: cite the specific
candidate requirement and the incompatible host requirement. Do not fail for
missing explanatory wording when the instructions already determine a correct
route. A material ambiguity must identify two plausible incompatible actions
and the text that permits them; stylistic alternatives are not ambiguities.

All cases must preserve one unanswered decision at a time and no implementation
before the architectural document is Approved plus a separate explicit start
decision. Spike and bounded paths stop after their deliverable. Approval to a
bounded design never authorizes retained implementation within this skill.
Recommended options and elapsed time are never user approval.

| Case | Expected observable outcome |
| --- | --- |
| `complete_design_native_default` | Use optional native design feedback; an empty answer retains provisional assumptions and permits writing the requested local Draft and self-review. Ask optional native written-spec feedback. The explicit keep approves the document only: persist and verify Approved, then ask the separate required implementation question through the host's plain-text route. The explicit no stops without implementation or Git changes. |
| `written_spec_native_default` | Ask optional native document feedback, accept the custom change, revise the Draft and self-review. Any empty optional follow-up leaves it Draft and continues to delivery without an implementation question. Do not commit or implement. |
| `bounded_native_default` | Ask optional native feedback; an empty answer keeps provisional recommendations and permits delivering the in-chat design and stopping. No spec, mandatory design approval, commit, or implementation. |
| `section_feedback_continues_default` | Present the first section as a provisional draft and use a permitted native question for optional feedback, with meaningful keep/revise choices and custom input. The answer leads to the next section and its native question in the same active turn. The empty second answer retains a stated provisional recommendation and continues drafting; it is not approval. Do not impose section or final approval gates absent a user requirement, or treat feedback as implementation approval. |
| `required_approval_default` | Ask one concise plain-text approval question and wait. Neither sync nor async may bypass this host's required-input route. Do not print a textual multiple-choice menu or claim approval. An unconditional candidate command to use an exposed picker for this approval is a conflict, even if overridden. |
| `optional_empty_default` | It is permissible to omit the optional question and draft using the existing default, or send one correctly formed optional sync question. If sent and empty, continue using a stated provisional assumption; do not re-ask the preference or block on it. Do not invent a mandatory approval before delivering the design. General async guidance may also permit one optional async question, but it must not hold up the requested draft. |
| `async_pending_then_custom_answer` | Prefer one async retention question. Use only `title` and optional string `options` inside its question item, not the sync schema. `{accepted:true}` and both automatic continuations leave that same question pending. Independent document reading is allowed; do not repeat in plain text, send another question, infer an answer, or end the flow with a duplicate question. When “60 days” arrives, accept it as a custom answer and ask the reader-role question during the same active flow. The new acknowledgement leaves only that second question pending. |
| `async_only_bounded_approval` | Use the available and permitted async tool; do not declare it unsupported merely because sync is absent. Delivery leaves the gate closed. Explicit “Approved” opens the design gate; deliver the approved in-chat design and stop without code, a plan document, or another skill. |
| `sync_allowed_bounded_approval` | Use one synchronous question because this host allows it for approval. Its single question has stable `snake_case` `id`, `question`, `header`, and object `options`; no `multiSelect`. The explicit answer permits delivering the design and stopping. Do not impose a universal ban on synchronous approvals. |
| `claude_clarification_continues` | Use one `AskUserQuestion` with `question`, `header`, `multiSelect:false`, and object `options`; no `id` or Codex tool. Accept the custom 60-day answer, then ask the role question without prematurely ending the flow. |
| `no_tool_required_approval` | Ask one concise plain-text approval question, wait with the gate closed, and invent no unavailable tool. The absence of a picker does not waive approval. |
| `cancelled_spec_approval` | Ask via the permitted synchronous tool. Cancellation is not approval. When control returns, state that an answer is still needed, ask the same question once in plain text, and wait; no automatic retry loop or implementation. The later explicit approval permits changing the document to Approved. Verify the write, ask the separate implementation question through the permitted native route, and stop on No. |
| `architectural_keep_start_default` | Accept Keep current design as document approval only. Change Draft to Approved and verify that write before asking one required implementation question through the constrained host's plain-text route. The later explicit yes ends the brainstorm phase and continues the same active task through normal implementation routing. It does not authorize commit, push, PR creation, publication, deployment, or production changes. |
| `architectural_keep_stop_claude` | Use Claude's permitted native feedback route. Keep approves the document but not implementation; persist and verify Approved before asking the separate implementation question. The No answer stops after reporting the approved path, with no implementation or Git changes. |
| `architectural_status_write_failure` | Report the status-write failure, keep implementation unauthorized, and do not ask the final implementation question. |
| `architectural_skipped_feedback_draft_stop` | An empty optional document-feedback result leaves Status: Draft. Deliver the draft and stop without asking the implementation question or changing implementation files. |

For every structured question, send exactly one question with 2–3 meaningful,
mutually exclusive options when appropriate, exactly one recommended option
first with the literal ` (Recommended)` suffix, and no added `Other` option.
Apply header and option-label limits to schemas that have those fields; do not
invent absent async fields to satisfy sync formatting rules. The async string
options carry the recommendation in the string itself.

## Evidence limits

A passing evaluation establishes agreement between the candidate's written
instructions and these host scenarios. It does not establish real UI rendering,
event delivery, model compliance in a live session, or current feature-flag
availability. Report those as untested unless separate live evidence exists.
Existing exact-clause tests are supplementary checks, not the red/green proof
for this routing defect. Transcript validators need an actual supplied
transcript; synthetic traces must not be presented as recorded host sessions.
