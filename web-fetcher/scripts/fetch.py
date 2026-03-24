#!/usr/bin/env python3
"""Fetch page content as markdown/text with a mirror fallback chain."""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import re
import subprocess
import sys
from urllib.parse import urlparse


UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

BAD_PATTERNS = [
    re.compile(r"Something went wrong, but don.?t fret", re.I),
    re.compile(r"Some privacy related extensions may cause issues on x\.com", re.I),
    re.compile(r"Don.?t miss what.?s happening", re.I),
    re.compile(r"This page is not supported\.", re.I),
    re.compile(r'"error"\s*:\s*"Failed to fetch', re.I),
]


class FetchError(RuntimeError):
    """Raised when a fetch strategy returns unusable content."""


class HTMLTextExtractor(HTMLParser):
    """Best-effort HTML to text conversion for last-resort fallback."""

    BLOCK_TAGS = {
        "article",
        "aside",
        "blockquote",
        "br",
        "div",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "tr",
        "ul",
    }
    SKIP_TAGS = {"script", "style", "svg", "noscript", "iframe"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth == 0 and tag in self.BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if self._skip_depth == 0 and tag in self.BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0 and data.strip():
            self._chunks.append(data)

    def get_text(self) -> str:
        text = html.unescape(" ".join(self._chunks))
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text.strip()


def normalize_url(url: str) -> str:
    if not re.match(r"^https?://", url, re.I):
        return "https://" + url
    return url


def fetch_url(url: str, headers: dict[str, str] | None = None, timeout: int = 30) -> str:
    cmd = ["curl", "-L", "-sS", "--fail-with-body", "--max-time", str(timeout), "-A", UA]
    if headers:
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise FetchError(result.stderr.strip() or f"curl exited with {result.returncode}")
    return result.stdout


def looks_like_bad_page(content: str) -> str | None:
    lowered = content.lower()
    if "log in" in lowered and "sign up" in lowered:
        if "don’t miss what's happening" in lowered or "don't miss what's happening" in lowered:
            return "x_login_wall"
        if "privacy related extensions may cause issues on x.com" in lowered:
            return "x_login_wall"

    for pattern in BAD_PATTERNS:
        if pattern.search(content):
            return pattern.pattern
    return None


def strip_frontmatter(content: str) -> str:
    if content.startswith("---\n"):
        parts = content.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1].strip()
    return content.strip()


def html_to_text(content: str) -> str:
    extractor = HTMLTextExtractor()
    extractor.feed(content)
    extractor.close()
    return extractor.get_text()


def validate_content(content: str, target: str, strategy: str) -> str:
    if not content or len(content.strip()) < 80:
        raise FetchError(f"{strategy} returned too little content")

    body = strip_frontmatter(content)
    if len(body) < 80:
        raise FetchError(f"{strategy} returned metadata without real body content")

    bad_match = looks_like_bad_page(content)
    if bad_match:
        raise FetchError(f"{strategy} returned an error/login page matching `{bad_match}`")

    parsed = urlparse(target)
    if parsed.netloc in {"x.com", "twitter.com", "www.x.com", "www.twitter.com"}:
        if "/i/article/" in parsed.path and "This page is not supported." in content:
            raise FetchError(f"{strategy} does not support X article pages")

    return content


def fetch_via_jina(target: str) -> str:
    return fetch_url(f"https://r.jina.ai/{target}", headers={"Accept": "text/markdown"})


def fetch_via_defuddle(target: str) -> str:
    return fetch_url(f"https://defuddle.md/{target}")


def fetch_via_markdown_new(target: str) -> str:
    return fetch_url(f"https://markdown.new/{target}")


def fetch_raw(target: str) -> str:
    content = fetch_url(target)
    if "<html" in content.lower() or "<body" in content.lower():
        text = html_to_text(content)
        if len(text) < 80:
            raise FetchError("Raw HTML could not be converted into readable text")
        return text
    return content


STRATEGIES = [
    ("Jina Reader", fetch_via_jina),
    ("defuddle.md", fetch_via_defuddle),
    ("markdown.new", fetch_via_markdown_new),
    ("Raw HTML", fetch_raw),
]


def fetch(target: str) -> str:
    errors: list[tuple[str, str]] = []
    for name, fn in STRATEGIES:
        try:
            print(f"[{name}] Fetching...", file=sys.stderr)
            content = fn(target)
            content = validate_content(content, target, name)
            print(f"[{name}] Success ({len(content)} chars)", file=sys.stderr)
            return content
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[{name}] Failed: {exc}", file=sys.stderr)
            errors.append((name, str(exc)))

    raise RuntimeError(
        "All strategies failed:\n" + "\n".join(f"  - {name}: {err}" for name, err in errors)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch web page content as markdown/text")
    parser.add_argument("url", help="Target URL to fetch")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    target = normalize_url(args.url)
    content = fetch(target)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(content)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
