# Contributing

This repository keeps skills intentionally small and inspectable.

## Principles

- One skill should solve one clearly bounded problem.
- Keep `SKILL.md` concise and procedural.
- Put deterministic logic into scripts when that is more reliable.
- Put detailed reference material into `references/` only when needed.
- Avoid extra documentation files inside a skill directory unless they are part of the skill system.

## Recommended structure

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
└── assets/
```

## Before opening a change

- Make sure the skill description matches its actual behavior.
- Keep naming simple and specific.
- Prefer small, reviewable changes.
- If a script is added, keep dependencies minimal when possible.
- If the skill depends on external services, document the limitation clearly.

## Notes

- This repo does not currently enforce a formal test harness for every skill.
- For legal clarity, add a `LICENSE` before encouraging broad third-party reuse.
