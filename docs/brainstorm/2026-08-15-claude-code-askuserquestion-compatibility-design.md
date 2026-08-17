# Claude Code AskUserQuestion Compatibility Design

**Date:** 2026-08-15

**Status:** Approved

**Scope:** Add native structured-question support for Claude Code while preserving the existing Codex CLI behavior in one shared `brainstorm` skill.

## Context

The repository currently distributes one `skills/brainstorm/SKILL.md` to both Claude Code and Codex CLI. Commit `a6d46e8` added explicit Codex `request_user_input` guidance, but the skill has no corresponding Claude Code `AskUserQuestion` guidance.

The upstream `obra/superpowers` repository was checked at remote `main` commit `b36e082` (`v6.3.0`):

- The repository supports installation on both Claude Code and Codex CLI.
- Its current `brainstorming` skill uses platform-neutral conversational wording and does not name either native question tool.
- Historical commit `4d8db81` added explicit `AskUserQuestion` instructions.
- Historical commit `8e38ab8` deliberately removed those instructions as part of a broader simplification.
- No `request_user_input` guidance exists in the visible upstream `brainstorming` history.

Therefore upstream provides distribution compatibility, but it does not currently guarantee native structured-question behavior on either host. This change is a focused compatibility addition rather than a duplicate of current upstream behavior.

## Goals

- Keep one shared `SKILL.md` for Claude Code and Codex CLI.
- Require the host's native structured-question UI for eligible non-visual decisions when that tool is available.
- Preserve Brainstorm's one-question-at-a-time workflow.
- Give both hosts the same user-visible behavior despite their different tool schemas.
- Prevent cancellation, timeout, empty results, or tool errors from bypassing approval gates.
- Preserve Brainstorm's existing terminal state: write and commit the specification, deliver its path, and stop.

## Non-goals

- Do not create host-specific copies of `SKILL.md`.
- Do not add `allowed-tools` frontmatter.
- Do not enable Claude Code's multi-select capability.
- Do not adopt upstream's newer spike, bounded, and architectural routing.
- Do not modify the Visual Companion scripts or protocol.
- Do not add a new runtime-detection script, test framework, or version field.
- Do not change the design-document output path or chain into implementation planning.

## Chosen Approach

Replace the Codex-only question section with a host-neutral section named `Asking questions with native UI`. The section has one common behavioral contract followed by two small host adapters.

This keeps shared policy in one place while documenting only the schema differences that the model must not mix up. The skill selects from the tools actually exposed by the current harness; it does not inspect environment variables or execute detection code.

### Common contract

For every non-visual question that can be represented by meaningful choices:

- Use exactly one question per tool call and per conversational turn.
- Provide two or three mutually exclusive options.
- Put the recommended option first and append `(Recommended)` to its label.
- Use a header of at most 12 characters and concise option labels and descriptions.
- Do not add an `Other` option; both supported native interfaces provide free-form input.
- Treat custom text entered through `Other` as a valid user answer.
- Use plain text only when the question is genuinely open-ended or no supported native tool is available.
- Never call both native tools for the same question.

The common limit is deliberately two or three options even though Claude Code permits more. It matches the narrower Codex contract and keeps the experience consistent across hosts.

### Claude Code adapter

When `AskUserQuestion` is available, use it with one item in `questions`. The item contains:

- `question`
- `header`
- `multiSelect: false`
- `options`, each with `label` and `description`

Do not synthesize an `id` for Claude Code and do not omit `multiSelect: false`. The explicit value prevents the host's additional capability from changing Brainstorm's single-choice workflow.

### Codex adapter

When `request_user_input` is available, use it with one item in `questions`. The item contains:

- a short, stable `snake_case` `id`
- `question`
- `header`
- `options`, each with `label` and `description`

Do not send `multiSelect` to Codex. Retain the existing one-question-per-call rule even if the runtime accepts multiple questions.

### Tool selection

In normal supported sessions, only the host-native tool is exposed. Use `AskUserQuestion` when Claude Code exposes it, use `request_user_input` when Codex exposes it, and otherwise ask the same question and choices in plain text.

If both names unexpectedly appear, do not invoke both. Use the tool identified as native by the current harness; if the harness identity is unclear, fall back to plain text instead of guessing.

## Question Data Flow

1. Classify the next question as visual, open-ended, or structured.
2. Route visual content through the Visual Companion when enabled.
3. Route genuinely open-ended questions through plain conversation.
4. For a structured question, select exactly one available host adapter.
5. Construct a single-choice payload from the common contract.
6. Call the native tool and validate the result.
7. Continue only after receiving an explicit option selection or custom user text.

Visual Companion consent is itself a non-visual structured decision. Its consent prompt therefore uses the same native-question rules. Actual mockups, diagrams, and visual alternatives remain in the browser companion.

## Invalid and Unavailable Responses

The following do not constitute an answer:

- an empty answer map or empty response text;
- cancellation or dismissal;
- a result that explicitly indicates idle timeout or automatic continuation;
- a tool error or unavailable-tool result.

When the host returns any of these results while keeping the turn active:

1. Do not choose the recommended option.
2. Do not infer approval or continue through a design gate.
3. Briefly state that the structured question returned no valid answer.
4. Repeat the same question and options once in plain text.
5. End the turn and wait for the user's response.

Claude Code 2.1.232 and Codex CLI 0.147.0 both terminate the active turn when the user dismisses a native question with Esc, so the model cannot issue a same-turn fallback in that path. The decision remains unanswered. If the user explicitly resumes the same flow without supplying an answer, repeat the same question and options once in plain text before continuing.

There is no automatic retry loop. A recommendation is guidance only, never a default. Design-section approval, written-spec approval, and any implementation transition require an explicit affirmative answer.

## File Changes

### `skills/brainstorm/SKILL.md`

- Replace `Asking questions in Codex` with the common contract and two host adapters.
- Add invalid-result handling.
- Update Visual Companion consent wording to reuse the native-question rules.
- Leave the nine-step process, hard gate, output location, and stop-after-spec behavior unchanged.

### `skills/brainstorm/README.md`

- Rename `Codex question UI` to `Native question UI`.
- Describe `AskUserQuestion`, `request_user_input`, and the plain-text fallback.
- Link the official Claude Code tool reference.
- Keep Codex configuration guidance version-scoped and re-verify it against the installed Codex version before editing; do not present an observed feature flag as universal behavior.

### `README.md`

- State that Brainstorm uses native structured questions in both Claude Code and Codex CLI.
- Use the official `npx skills` agent identifiers `claude-code` and `codex`.
- Include an optional command that installs the same `brainstorm` skill to both hosts.

No other tracked files are in scope. The existing untracked `brainstorm-test/` directory must not be modified or committed.

## Validation Strategy

This repository has no existing automated behavior-test harness for Brainstorm. Adding a keyword-only shell test would prove that strings exist, not that either model calls the correct tool, so validation uses syntax checks, real installation, and host-level forward tests.

### 1. Format and discovery

- Run Codex's `quick_validate.py` against `skills/brainstorm`.
- Use the current `npx skills` CLI with the local repository as its source.
- Install `brainstorm` into a temporary project for both `claude-code` and `codex` with `--copy` and without `--global`.
- Verify both resolved installations contain identical copies of the intended `SKILL.md` and supporting files.

### 2. Static contract

Verify that:

- frontmatter remains unchanged and contains no `allowed-tools`;
- both native tool names are present;
- Claude guidance requires `multiSelect: false`;
- Codex guidance requires `id` and does not attach `multiSelect`;
- shared option, recommendation, fallback, and invalid-result rules are defined once;
- both README files match the implemented behavior.

### 3. Live host acceptance

Install the local working tree into isolated temporary projects and run the same scenarios in Claude Code and Codex CLI:

1. **Structured choice:** Ask Brainstorm to pose one non-visual question with three mutually exclusive options. Exactly one native question UI must appear.
2. **Open-ended input:** Ask for user-authored requirements that cannot be represented honestly by choices. The agent must use plain text.
3. **Cancellation:** Dismiss the native question. The agent must not select a recommendation or pass an approval gate. If the host keeps the turn active, the agent must repeat the question in plain text immediately. If the host aborts the turn, the decision must remain unanswered and the agent must repeat the question only after the user explicitly resumes the same flow.
4. **Codex regression:** Confirm the existing `request_user_input` behavior remains intact.

Run the core structured-choice scenario independently three times per host. Acceptance requires Claude Code to use `AskUserQuestion` in 3/3 runs and Codex CLI to use `request_user_input` in 3/3 runs. Capture terminal transcripts and tool-call results as delivery evidence without committing temporary logs.

## Acceptance Criteria

- A single installed `SKILL.md` works unchanged in Claude Code and Codex CLI.
- Eligible structured questions reliably invoke the host-native UI.
- Each call contains exactly one single-select question with two or three options.
- Claude and Codex payload fields are not mixed.
- Open-ended and visual questions retain their intended channels.
- Empty, cancelled, timed-out, and failed calls cannot imply a user decision.
- The Codex behavior added by `a6d46e8` remains operational.
- Documentation and installation examples agree with current official tooling.
- No unrelated upstream workflow changes or user-owned untracked files enter the commit.

## References

- [Claude Code tools reference](https://code.claude.com/docs/en/tools-reference)
- [Claude Code skills reference](https://code.claude.com/docs/en/skills)
- [Anthropic interactive command patterns](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/command-development/references/interactive-commands.md)
- [OpenAI skill documentation](https://developers.openai.com/codex/skills)
- [`npx skills` CLI documentation](https://github.com/vercel-labs/skills/blob/main/README.md)
