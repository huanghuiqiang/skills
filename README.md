# skills

A small collection of Codex skills, organized in a single repository.

This repo is intended for practical, reusable skills that can be installed into a local Codex setup and then invoked explicitly or implicitly by the agent when the task matches.

## What is in this repo

Currently included:

- `web-fetcher`: fetches a URL through markdown mirrors with fallback and returns readable markdown or text for downstream summarization, extraction, or analysis.

## Repository layout

```text
skills/
├── README.md
└── web-fetcher/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── scripts/
        └── fetch.py
```

Each skill lives in its own folder and should contain:

- `SKILL.md`: the skill definition and operating instructions
- `agents/openai.yaml`: UI-facing metadata such as display name and default prompt
- `scripts/`, `references/`, `assets/`: optional support files when needed

## Included skill

### `web-fetcher`

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

If your Codex environment supports installing from a GitHub repo path, install from:

```text
huanghuiqiang/skills
```

and use the skill path:

```text
web-fetcher
```

If your environment expects a direct repository path, point it at:

```text
web-fetcher
```

inside this repo.

## Local usage

The fetcher script can also be run directly.

Fetch to stdout:

```bash
python3 web-fetcher/scripts/fetch.py https://example.com/article
```

Save to a file:

```bash
python3 web-fetcher/scripts/fetch.py https://example.com/article -o output.md
```

You can also pass a URL without a scheme. The script will normalize it to `https://`.

```bash
python3 web-fetcher/scripts/fetch.py example.com/article
```

## How `web-fetcher` behaves

Success criteria:

- content must not be trivially short
- content must contain real body text, not only metadata
- content must not look like an obvious login wall or generic fetch error

Failure categories the skill is designed to surface clearly:

- mirror unavailable
- login or error page returned instead of page content
- unsupported page type
- page did not yield enough readable content to trust

## Known limitations

- Mirror availability can change over time.
- Some sites intentionally block automated fetchers.
- `x.com/i/article/...` pages are currently unreliable across mirrors.
- The raw HTML fallback is best-effort text extraction, not a full readability engine.
- This repo does not currently include automated tests for mirror behavior.

## When not to use `web-fetcher`

Do not use it when:

- the user already pasted the source text
- the task is only about a local file
- the task requires live web research rather than page extraction

## Contributing

A good skill in this repo should:

- solve one clearly bounded problem
- keep `SKILL.md` concise
- push implementation details into scripts or references when needed
- avoid adding extra project documentation inside the skill folder unless it is required by the skill system

Preferred structure for adding another skill:

```text
new-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
```

## Status

This repository is small by design. The goal is to keep each skill focused, easy to inspect, and easy to install.
