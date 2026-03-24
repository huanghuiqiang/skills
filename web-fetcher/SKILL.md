---
name: web-fetcher
description: Use this skill when the user provides a URL and wants clean page text or markdown before summarizing, extracting, or analyzing it. It fetches through markdown mirrors with fallback, rejects obvious error or login-wall pages, and converts raw HTML to readable text only as a last resort.
---

# Web Fetcher

Use this skill when the main problem is extracting readable text from a URL before a later step such as summarization, extraction, or analysis.

Typical inputs:

- article URLs
- docs pages
- blog posts
- X status links
- pages that should be converted to markdown before analysis

Do not use this skill when:

- the user already pasted the source text
- the task is only about a local file
- browsing is needed for current facts and the problem is not page extraction

## Default Workflow

1. Run the fetch script with the target URL.
2. If it succeeds, use the returned markdown/text as the source input for the next step.
3. If it fails, tell the user whether the failure is:
   - mirror unavailable
   - extracted content is actually a login/error page
   - page type is not supported by the mirrors
   - the page returned too little readable content to trust

## Commands

Fetch to stdout:

```bash
python3 <skill-path>/scripts/fetch.py <url>
```

Save to file:

```bash
python3 <skill-path>/scripts/fetch.py <url> -o output.md
```

## Notes

- Default strategy order is `r.jina.ai` -> `defuddle.md` -> `markdown.new` -> raw HTML converted to readable text.
- The script treats HTTP 4xx/5xx responses, obvious X login walls, unsupported pages, and generic error pages as failures.
- For normal `x.com/.../status/...` links, `r.jina.ai` is usually the best first path.
- For `x.com/i/article/...` pages, current mirrors are unreliable. If all strategies fail, report that page type clearly instead of pretending extraction succeeded.
- The raw HTML path is only a last resort. It should return extracted readable text, not untouched HTML markup.

## Common Pairing

When the user wants understanding rather than raw extraction:

1. Use `$web-fetcher` to get clean source text.
2. Feed the result into `$i2i`.
