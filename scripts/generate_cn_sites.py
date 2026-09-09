#!/usr/bin/env python3
"""Generate cnSites.yaml from v2fly's domain-list-community release.

For each TARGET in TARGETS, the matching list is located inside
dlc.dat_plain.yml. App-specific sections that do not have their own list are
read from the upstream geolocation-cn source file. `domain:` rules are
prefixed with `+.` (wildcard), and `full:` rules have no prefix (exact match).
Entries tagged with the `@!cn` attribute (overseas-only) are dropped, any
remaining attributes are stripped. Sections are separated by `# <TARGET>`
comment headers.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

import yaml

LIST_URL = "https://github.com/v2fly/domain-list-community/releases/latest/download/dlc.dat_plain.yml"
GEOLOCATION_CN_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/geolocation-cn"

TARGETS = [
    "bytedance",
    "xiaohongshu",
    "bilibili",
    "tencent",
    "oppo",
    "xiaomi",
    "alibaba",
    "zhihu",
    "meituan",
    
    # categories
    "category-ai-cn",
    "category-bank-cn",
    "category-cdn-cn",
    "category-food-cn",
    "category-media-cn",
    "category-netdisk-cn",
    "category-ntp-cn",
    "category-social-media-cn",
    
    # cloud services
    "aliyun",
    "huaweicloud",
    
    # scholar-cn
    "cas",
    "cnki",
    "chaoxing",
    "wanfang"
]

# App groups found in data/geolocation-cn but not published as standalone lists.
# Map the output section name to the upstream level-two heading.
APP_SECTIONS = {
    "umetrip": "航旅纵横",
}


def fetch_text(url: str, description: str) -> str:
    print(f"Fetching {description} from {url}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return response.read().decode()
    except urllib.error.URLError as e:
        print(f"Error fetching {description}: {e}")
        sys.exit(1)


def fetch_dlc() -> dict[str, Any]:
    return yaml.safe_load(fetch_text(LIST_URL, "DLC YAML"))


def find_list(data: dict[str, Any], name: str) -> Optional[list[str]]:
    for entry in data.get("lists") or []:
        if entry.get("name") == name:
            return list(entry.get("rules") or [])
    return None


def find_source_section(source: str, heading: str) -> Optional[list[str]]:
    """Return rules under a `## heading` until the next level-two heading."""
    marker = f"## {heading}"
    in_section = False
    rules: list[str] = []

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if in_section:
                break
            in_section = line == marker
        elif in_section and line and not line.startswith("#"):
            rules.append(line)

    return rules if in_section else None


def extract_domains(rules: list[str]) -> list[str]:
    domains: list[str] = []
    for rule in rules:
        if rule.startswith("domain:"):
            prefix = "+."
            body = rule[len("domain:"):]
        elif rule.startswith("full:"):
            prefix = ""
            body = rule[len("full:"):]
        else:
            continue

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
            domains.append(f"{prefix}{domain_part}")
    return domains


def extract_source_domains(rules: list[str]) -> list[str]:
    """Convert domain-list-community source rules to Clash domain rules."""
    domains: list[str] = []
    for rule in rules:
        parts = rule.split()
        body = parts[0]
        attrs = {part.lstrip("@") for part in parts[1:] if part.startswith("@")}
        if "!cn" in attrs:
            continue

        if body.startswith("full:"):
            prefix = ""
            domain = body[len("full:"):]
        elif body.startswith("domain:"):
            prefix = "+."
            domain = body[len("domain:"):]
        elif body.startswith(("include:", "keyword:", "regexp:")):
            continue
        else:
            prefix = "+."
            domain = body

        if domain:
            domains.append(f"{prefix}{domain}")
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
                f.write(f"  - '{domain}'\n")
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

    geolocation_cn = fetch_text(GEOLOCATION_CN_URL, "geolocation-cn source")
    for app, heading in APP_SECTIONS.items():
        rules = find_source_section(geolocation_cn, heading)
        if rules is None:
            print(f"Warning: app section '{heading}' not found in source.")
            continue
        domains = extract_source_domains(rules)
        print(f"  {app}: {len(domains)} domains")
        sections.append((app, domains))

    output = Path(__file__).resolve().parent.parent / "cnSites.yaml"
    write_cn_sites(output, sections)


if __name__ == "__main__":
    main()
