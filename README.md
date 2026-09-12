# brainstorm-skills

Claude Code and Codex skills published by [@cyenxchen](https://github.com/cyenxchen).

## Skills

### `brainstorm` — Standalone staged brainstorming

Classifies an idea as a feasibility spike, bounded change, or architectural design and scales the ceremony accordingly. Spike and bounded paths stop after their result. Architectural work can hand off to implementation only after the document is approved and the user separately confirms starting.

**Install for Claude Code:**

```bash
npx skills add cyenxchen/brainstorm-skills --skill brainstorm --agent claude-code --global
```

**Install for Codex:**

```bash
npx skills add cyenxchen/brainstorm-skills --skill brainstorm --agent codex --global
```

To install the same skill for both hosts:

```bash
npx skills add cyenxchen/brainstorm-skills --skill brainstorm --agent claude-code codex --global
```

These commands install at user scope. Omit `--global` to install only in the current project.

**What it does:**

- Classifies each request as spike, bounded, or architectural and lets you override the classification
- Asks one question at a time to clarify your idea
- Routes text choices through permitted Claude Code or Codex question tools, including async; follows host policy for plain-text approvals and unanswered questions
- Uses optional native feedback throughout design and document review; preserves user-required approvals and actual permission boundaries
- Returns a recommendation for spikes, an in-chat design for bounded changes, or a local `docs/brainstorm/YYYY-MM-DD-<topic>-design.md` draft for architectural work; commits only when authorized
- **Architectural only:** an explicit keep changes `Status: Draft` to `Status: Approved`; after verifying that write, the skill asks separately whether to implement now
- Starts implementation in the same active task only after an explicit yes; No stops, cancellation/empty/timeout never starts work, and an async delivery acknowledgement remains pending

Tool availability does not guarantee a popup. See [question routing and version notes](skills/brainstorm/README.md#native-question-ui) for the observed Codex Default-mode restrictions.

**When to use:**

When you want to explore feasibility or design a change before implementation,
while keeping document approval and implementation authorization distinct.

## Credits

The `brainstorm` skill is extracted from [obra/superpowers](https://github.com/obra/superpowers) (MIT licensed) and modified to:

- Stop after spike and bounded results, and after Draft or declined architectural outcomes
- Add an explicit architectural Draft-to-Approved state transition and separate same-task implementation handoff
- Remove cross-skill dependencies that don't exist outside the full Superpowers plugin
- Rename to `brainstorm` to distinguish it from the original `brainstorming` skill

Original author: Jesse Vincent ([@obra](https://github.com/obra)). The Superpowers methodology this skill comes from is documented in his [original release announcement](https://blog.fsck.com/2025/10/09/superpowers/).

## License

MIT — see [LICENSE](./LICENSE).
