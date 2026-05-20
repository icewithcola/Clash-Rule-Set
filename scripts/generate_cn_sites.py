#!/usr/bin/env python3
"""Generate cnSites.yaml from v2fly's domain-list-community release.

For each TARGET in TARGETS, the matching list is located inside
dlc.dat_plain.yml. Only `domain:` rules are kept, entries tagged with the
`@!cn` attribute (overseas-only) are dropped, any remaining `:@xxx`
attribute suffix is stripped, and the bare domain is emitted as
`'+.<domain>'`. Sections are separated by `# <TARGET>` comment headers.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

import yaml

LIST_URL = "https://github.com/v2fly/domain-list-community/releases/latest/download/dlc.dat_plain.yml"

TARGETS = [
    "bytedance",
    "xiaohongshu",
    "bilibili",
    "tencent"
]


def fetch_dlc() -> dict[str, Any]:
    print(f"Fetching DLC YAML from {LIST_URL}...")
    try:
        req = urllib.request.Request(
            LIST_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return yaml.safe_load(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching DLC YAML: {e}")
        sys.exit(1)


def find_list(data: dict[str, Any], name: str) -> Optional[list[str]]:
    for entry in data.get("lists") or []:
        if entry.get("name") == name:
            return list(entry.get("rules") or [])
    return None


def extract_domains(rules: list[str]) -> list[str]:
    domains: list[str] = []
    for rule in rules:
        # Only `domain:` rules map cleanly to clash's `+.` suffix wildcard.
        # `full:` is exact-match, `regexp:` is a pattern -- both skipped.
        if not rule.startswith("domain:"):
            continue

        body = rule[len("domain:"):]

        # Body may carry attributes after `:@`, e.g. `foo.com:@!cn,@ads`.
        if ":@" in body:
            domain_part, attrs = body.split(":@", 1)
            attr_set = {
                a.strip().lstrip("@")
                for a in attrs.split(",")
                if a.strip()
            }
            # Drop overseas-only entries -- they do not belong in cnSites.
            if "!cn" in attr_set:
                continue
        else:
            domain_part = body

        domain_part = domain_part.strip()
        if domain_part:
            domains.append(domain_part)
    return domains


def write_cn_sites(path: Path, sections: list[tuple[str, list[str]]]) -> None:
    total = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write("payload:\n")
        for idx, (name, domains) in enumerate(sections):
            if idx > 0:
                f.write("\n")
            f.write(f"# {name}\n")
            for domain in domains:
                f.write(f"  - '+.{domain}'\n")
                total += 1
    print(f"Successfully wrote {total} domains to {path}.")


def main() -> None:
    data = fetch_dlc()

    sections: list[tuple[str, list[str]]] = []
    for target in TARGETS:
        rules = find_list(data, target)
        if rules is None:
            print(f"Warning: list '{target}' not found in source.")
            continue
        domains = extract_domains(rules)
        print(f"  {target}: {len(domains)} domains")
        sections.append((target, domains))

    output = Path(__file__).resolve().parent.parent / "cnSites.yaml"
    write_cn_sites(output, sections)


if __name__ == "__main__":
    main()
