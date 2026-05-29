#!/usr/bin/env python3
"""Generate privacy.yaml from configurable DNS blocklist URLs.

Each URL in URLS is fetched as plain text, comment lines (`#`) and blank
lines are dropped, and each remaining bare domain is emitted as
`'<domain>'`. Sections are separated by `# Region: <url>` comment
headers so the source of every entry is preserved.

To add a new blocklist, append its raw URL to URLS below.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Configure the upstream blocklists here. Each URL must point to a
# plain-text file with one domain per line; lines starting with `#`
# and blank lines are ignored.
URLS = [
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/domains/native.oppo-realme.txt",  # noqa: E501
]


def fetch_text(url: str) -> str:
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return response.read().decode()
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)


def extract_domains(text: str) -> list[str]:
    domains: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        # Skip header/comment lines and blank lines. Hagezi files put
        # metadata in `#` comments before the domain list.
        if not line or line.startswith("#"):
            continue
        domains.append(line)
    return domains


def write_privacy(path: Path, sections: list[tuple[str, list[str]]]) -> None:
    total = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write("payload:\n")
        for idx, (url, domains) in enumerate(sections):
            if idx > 0:
                f.write("\n")
            f.write(f"# Region: {url}\n")
            for domain in domains:
                f.write(f"  - '{domain}'\n")
                total += 1
    print(f"Successfully wrote {total} domains to {path}.")


def main() -> None:
    sections: list[tuple[str, list[str]]] = []
    for url in URLS:
        text = fetch_text(url)
        domains = extract_domains(text)
        print(f"  {url}: {len(domains)} domains")
        sections.append((url, domains))

    output = Path(__file__).resolve().parent.parent / "privacy.yaml"
    write_privacy(output, sections)


if __name__ == "__main__":
    main()
