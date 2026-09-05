# Repository Guidelines

## Project Structure & Module Organization

This repository distributes the standalone `brainstorm` skill for Claude Code and Codex.

- `skills/brainstorm/SKILL.md` defines routing, dialogue, approval, and completion behavior.
- `skills/brainstorm/README.md`, `visual-companion.md`, and `spec-document-reviewer-prompt.md` document usage and supporting workflows.
- `skills/brainstorm/scripts/` contains the Node.js server, browser helper, HTML frame, and Bash launchers.
- `tests/` contains standalone Python and JavaScript assertion scripts.
- `docs/brainstorm/` is ignored generated-design output; use `YYYY-MM-DD-<topic>-design.md` filenames.

## Build, Test, and Development Commands

Run from the repository root. Use Node.js, Python 3, and Bash; no package manifest, dependency installation, or build step is provided.

```bash
python3 tests/assert_question_progression_contract.py
node tests/assert_standalone_branding.js
python3 tests/assert_claude_recommendation.py /path/to/session.jsonl
```

These check dialogue wording, branding through a real local HTTP server, and recommendation labels in a Claude Code transcript, respectively. The transcript is supplied separately.

To preview the visual companion locally:

```bash
bash skills/brainstorm/scripts/start-server.sh --foreground
bash skills/brainstorm/scripts/stop-server.sh <session_dir>
```

Use the launcher's returned session directory for shutdown.

## Coding Style & Naming Conventions

Match surrounding files: four-space Python indentation, two-space JavaScript and Bash indentation, JavaScript semicolons and single quotes. Use `snake_case` for Python functions, `camelCase` for JavaScript functions, and uppercase shell configuration variables. Name assertion scripts `assert_<behavior>.py` or `assert_<behavior>.js`. Keep Markdown instructions direct and synchronize documented behavior with `SKILL.md`. No formatter or linter configuration is present.

## Testing Guidelines

Tests use Python standard-library checks and Node's built-in assertions; no coverage threshold is configured. Add focused regressions for changed contracts. For bug fixes, reproduce before editing business logic, confirm three consecutive failures, then fix and confirm three consecutive passes plus related full regression checks. Report any unavailable transcript validation explicitly.

## Commit & Pull Request Guidelines

Git history is currently unreadable (`bad object HEAD`), so an established commit convention cannot be verified. Use concise imperative subjects describing the changed behavior. PRs should explain the problem, affected skill paths, validation commands and results, and link relevant issues. Include screenshots for visual-companion changes. Preserve MIT attribution.

## Behavioral Boundaries

Preserve spike, bounded, and architectural outcomes, explicit approvals, and the stop before retained implementation. Ask the user to decide compatibility requirements when relevant.
