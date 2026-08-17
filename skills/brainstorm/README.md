# brainstorm

Standalone staged-brainstorming skill. It classifies work as a feasibility
spike, bounded change, or architectural design; scales the artifact to that
path; obtains explicit approval; and stops before retained implementation.

See [SKILL.md](./SKILL.md) for the instructions read by Claude Code or Codex.

## Path outcomes

- **Spike:** approve a small probe, receive findings and a recommendation; any
  probe artifact remains explicitly throwaway.
- **Bounded:** approve a short in-chat design for an existing flow; no spec or
  implementation-plan document is created.
- **Architectural:** approve a sectioned design, then receive a committed spec
  at `docs/brainstorm/YYYY-MM-DD-<topic>-design.md`.

Every path ends the skill. It does not implement the design, invoke
`writing-plans`, or auto-chain to another skill.

## Native question UI

In an interactive session, Brainstorm uses the host's native structured-question
tool for non-visual questions that have 2-3 meaningful, mutually exclusive
choices: Claude Code's `AskUserQuestion` or Codex's `request_user_input`. It
sends one single-select question per call, marks the recommended choice, and
relies on the native `Other` field for custom text. Genuinely open-ended
questions and sessions without a supported tool use plain text; visual choices
continue to use the browser companion.

An empty, cancelled, timed-out, or failed tool result never counts as a choice
or approval. When the host returns that result while keeping the turn active,
Brainstorm repeats the same question once in plain text and waits for an
explicit response. On the locally verified Claude Code 2.1.232 and Codex CLI
0.147.0, pressing Esc ends or interrupts the current turn before the model can
retry; the decision remains unanswered, and Brainstorm repeats it only after
the user explicitly resumes the same flow.

On the locally verified Codex CLI 0.147.0, Default mode exposes
`request_user_input` only when this under-development feature is enabled in
`~/.codex/config.toml`:

```toml
[features]
default_mode_request_user_input = true
```

Plan mode exposes the tool without this flag in that version. Restart the
active Codex session after changing the configuration, and re-check newer Codex
versions instead of assuming this experimental flag is still required.

## Provenance

Extracted from [`brainstorming`](https://github.com/obra/superpowers/tree/main/skills/brainstorming)
in [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent).
The current migration tracks Superpowers v6.3.0 (`b36e082`), including its
three-path router and visual-companion hardening.

### Intentional differences from the original

1. **Standalone terminal states:** Superpowers implements bounded work after
   approval and hands architectural specs to `writing-plans`. This fork instead
   returns the approved path result and stops. A later user-directed turn owns
   planning or implementation.
2. **Name and trigger:** `brainstorming` is renamed to `brainstorm`, with
   frontmatter focused on explicit feasibility and design requests rather than
   forcing the skill before every creative edit.
3. **Spec path:** Architectural specs use `docs/brainstorm/` instead of
   `docs/superpowers/specs/`.
4. **No cross-plugin dependency:** The optional
   `elements-of-style:writing-clearly-and-concisely` handoff is omitted.
5. **Native structured questions:** Eligible text choices use Claude Code's or
   Codex's native picker, including strict unanswered/cancellation handling.
6. **Standalone branding fallback:** Selected-skill installs have no
   Superpowers package manifest, so the visual companion uses the unversioned
   `Superpowers Brainstorming` label instead of exposing `vunknown`.

### Migrated upstream behavior

- Spike / bounded / architectural classification, heavier-path fallback, and
  one-way upgrades when hidden complexity appears.
- Just-in-time visual-companion offering instead of an upfront blanket offer.
- Per-session HTTP/WebSocket authentication, security headers, bounded frame
  payloads, owner-safe shutdown, same-port restart, browser auto-open, live
  reconnect state, four-hour configurable idle timeout, and cross-platform
  launcher handling.
- Spec self-review, one-question-at-a-time dialogue, incremental approval,
  YAGNI, alternatives, isolation guidance, and targeted existing-code cleanup.

## License

MIT — see [LICENSE](../../LICENSE) at the repository root.
