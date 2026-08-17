# brainstorm-skills

Claude Code and Codex skills published by [@cyenxchen](https://github.com/cyenxchen).

## Skills

### `brainstorm` — Standalone staged brainstorming

Classifies an idea as a feasibility spike, bounded change, or architectural design, scales the ceremony accordingly, and then stops. No auto-chaining to implementation planning and no surprise implementation.

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
- Uses Claude Code's `AskUserQuestion` or Codex's `request_user_input` UI for eligible text choices
- Requires explicit approval before every probe or proposed change
- Returns a recommendation for spikes, an approved in-chat design for bounded changes, or a committed `docs/brainstorm/YYYY-MM-DD-<topic>-design.md` spec for architectural work
- **Stops there.** You decide whether and how to continue in a later turn

**When to use:**

When you want to explore feasibility or design a change before implementation, while keeping the handoff back to you explicit.

## Credits

The `brainstorm` skill is extracted from [obra/superpowers](https://github.com/obra/superpowers) (MIT licensed) and modified to:

- Stop after delivering the path result — no auto-chaining to `writing-plans` or any other skill
- Adapt Superpowers' three-path router so every path stops before retained implementation
- Remove cross-skill dependencies that don't exist outside the full Superpowers plugin
- Rename to `brainstorm` to distinguish it from the original `brainstorming` skill

Original author: Jesse Vincent ([@obra](https://github.com/obra)). The Superpowers methodology this skill comes from is documented in his [original release announcement](https://blog.fsck.com/2025/10/09/superpowers/).

## License

MIT — see [LICENSE](./LICENSE).
