# brainstorm

Standalone staged-brainstorming skill. It classifies work as a feasibility
spike, bounded change, or architectural design; scales the artifact to that
path; refines drafts through native feedback; and stops before retained implementation.

See [SKILL.md](./SKILL.md) for the instructions read by Claude Code or Codex.

## Path outcomes

- **Spike:** investigate within the authorized scope, receive findings and a recommendation; any
  probe artifact remains explicitly throwaway.
- **Bounded:** refine a short in-chat design for an existing flow; no spec or
  implementation-plan document is created.
- **Architectural:** refine a sectioned design, then receive a local spec draft
  at `docs/brainstorm/YYYY-MM-DD-<topic>-design.md`.

Every path ends the skill. It does not implement the design, invoke
`writing-plans`, or auto-chain to another skill.

## Native question UI

Brainstorm follows the current host's question policy before selecting a tool.
Eligible text choices use Claude Code's `AskUserQuestion` or Codex's
`request_user_input` / `request_user_input_async` only when available and
permitted for that purpose, honoring the host's preference. Required input
uses plain text when the host requires it; async does not bypass that rule.
Each call asks one question, marks one recommendation, and accepts custom
answers. Visual choices continue to use the browser companion after consent.
Tool availability does not guarantee a popup in the client.

Section feedback, complete-design feedback, bounded-design feedback, and
written-spec review are optional draft refinement by default. Each uses a
permitted native question; an answer advances the same active flow. A skipped
optional synchronous question keeps recommendations provisional and does not
block writing or delivering the draft. The skill adds no complete-design or
final-spec approval gate. Genuinely blocking decisions and approvals explicitly
required by the user still follow the host's required-input route.

A design request includes its local draft, not automatic Git operations.
Commit only when already authorized; otherwise deliver the uncommitted draft
without adding a commit prompt. Feedback never authorizes implementation,
push, or publication, and an unreviewed draft must not be labeled approved.

An async delivery acknowledgement leaves the question pending until the user
answers. Brainstorm can do independent work while waiting, but does not repeat
the prompt or treat silence or automatic continuation as cancellation. After
an answer, it continues the remaining questions in the active flow. For an
optional empty result, host/user instructions to assume and continue take
precedence over re-asking; the assumption is provisional. Required approvals
remain explicit. A confirmed cancellation of a required question uses one
plain-text fallback when control returns, or after the user explicitly resumes
an interrupted turn.

In the observed Codex CLI 0.153.4 Default session, `request_user_input` was
limited to optional questions, excluded permission requests, and required
input had to use a concise plain-text question. An empty optional result
required continuing with best judgment. These are session-policy constraints;
other hosts can permit native approval questions.

Earlier local verification on Codex CLI 0.147.0 found that Default mode needed
`features.default_mode_request_user_input = true` to expose the synchronous
tool, while Plan mode did not. That experimental flag is version-specific;
check the current session's tools and policy instead of assuming it is still
required. On the earlier Claude Code 2.1.232 and Codex CLI 0.147.0 sessions,
Esc interrupted the turn before the model could retry. Async pending-state
handling is covered by instruction-contract scenarios, not a live UI test.

## Provenance

Extracted from [`brainstorming`](https://github.com/obra/superpowers/tree/main/skills/brainstorming)
in [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent).
The current migration tracks Superpowers v6.3.0 (`b36e082`), including its
three-path router and visual-companion hardening.

### Intentional differences from the original

1. **Standalone terminal states:** Superpowers implements bounded work after
   approval and hands architectural specs to `writing-plans`. This fork instead
   returns the path result and stops. A later user-directed turn owns
   planning or implementation.
2. **Name and trigger:** `brainstorming` is renamed to `brainstorm`, with
   frontmatter focused on explicit feasibility and design requests rather than
   forcing the skill before every creative edit.
3. **Spec path:** Architectural specs use `docs/brainstorm/` instead of
   `docs/superpowers/specs/`.
4. **No cross-plugin dependency:** The optional
   `elements-of-style:writing-clearly-and-concisely` handoff is omitted.
5. **Native structured questions:** Eligible text choices use permitted host
   tools, with host-policy routing and distinct optional, pending, and
   cancellation handling.
6. **Standalone branding fallback:** Selected-skill installs have no
   Superpowers package manifest, so the visual companion uses the unversioned
   `Superpowers Brainstorming` label instead of exposing `vunknown`.
7. **Optional design feedback:** Sections, complete designs, and written specs
   support continuous native dialogue without skill-imposed approval gates.
   User-required approvals remain explicit; Git operations need authorization.

### Migrated upstream behavior

- Spike / bounded / architectural classification, heavier-path fallback, and
  one-way upgrades when hidden complexity appears.
- Just-in-time visual-companion offering instead of an upfront blanket offer.
- Per-session HTTP/WebSocket authentication, security headers, bounded frame
  payloads, owner-safe shutdown, same-port restart, browser auto-open, live
  reconnect state, four-hour configurable idle timeout, and cross-platform
  launcher handling.
- Spec self-review, one-question-at-a-time dialogue,
  YAGNI, alternatives, isolation guidance, and targeted existing-code cleanup.

## License

MIT — see [LICENSE](../../LICENSE) at the repository root.
