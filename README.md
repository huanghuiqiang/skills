# skills

[简体中文](./README.zh-CN.md)

A small collection of Codex skills, organized in a single repository.

This repo is for practical, reusable skills that can be installed into a local Codex setup and invoked explicitly or implicitly when the task matches.

## Features

- Multiple skills in one repository, one skill per directory
- Lightweight structure that is easy to inspect and maintain
- Script-backed skills when deterministic behavior is useful
- Focus on practical workflows rather than large frameworks

## Included skills

- `web-fetcher`: fetches a URL through markdown mirrors with fallback and returns readable markdown or text for downstream summarization, extraction, or analysis

## Repository layout

```text
skills/
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
└── web-fetcher/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── scripts/
        └── fetch.py
```

Each skill should normally contain:

- `SKILL.md`: the skill definition and operating instructions
- `agents/openai.yaml`: UI-facing metadata such as display name and default prompt
- `scripts/`, `references/`, `assets/`: optional support files when needed

## Skill: `web-fetcher`

Use `web-fetcher` when the main problem is extracting readable text from a URL before a later step such as summarization, extraction, or analysis.

Typical use cases:

- articles
- documentation pages
- blog posts
- X status links
- pages that should be converted into readable markdown or text before further work

What it does:

- tries multiple fetch strategies in sequence
- prefers markdown-oriented mirrors first
- rejects obvious error pages and login walls
- treats HTTP 4xx and 5xx responses as failures
- converts raw HTML to readable text only as a last resort

Current fallback order:

1. `r.jina.ai`
2. `defuddle.md`
3. `markdown.new`
4. raw HTML converted to text

## Installation

Install the skill into Codex from this repository using the GitHub installer flow supported by your setup.

Repository:

```text
huanghuiqiang/skills
```

Skill path:

```text
web-fetcher
```

If your environment supports installation from a GitHub repo path, use the repository above and point to the skill directory inside it.

## Local usage

Run the fetcher directly:

```bash
python3 web-fetcher/scripts/fetch.py https://example.com/article
```

Save the output to a file:

```bash
python3 web-fetcher/scripts/fetch.py https://example.com/article -o output.md
```

You can also pass a URL without a scheme. It will be normalized to `https://`.

```bash
python3 web-fetcher/scripts/fetch.py example.com/article
```

## Behavior

Success criteria:

- content must not be trivially short
- content must contain real body text, not only metadata
- content must not look like an obvious login wall or generic fetch error

Failure categories surfaced by the script:

- mirror unavailable
- login or error page returned instead of page content
- unsupported page type
- page did not yield enough readable content to trust

## Limitations

- Mirror availability can change over time.
- Some sites intentionally block automated fetchers.
- `x.com/i/article/...` pages are currently unreliable across mirrors.
- The raw HTML fallback is best-effort text extraction, not a full readability engine.
- This repo does not currently include automated tests for mirror behavior.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

The short version:

- keep each skill focused on one bounded problem
- keep `SKILL.md` concise
- move implementation detail into scripts or references when appropriate
- avoid unnecessary extra files inside a skill directory

## License

No license file has been added yet. If you plan to open this repo for external reuse, choose and add a license explicitly.

## Status

This repository is intentionally small. The goal is to keep each skill easy to inspect, install, and evolve.
