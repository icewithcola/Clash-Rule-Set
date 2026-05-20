#!/usr/bin/env python3
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

URL = "https://controlplane.tailscale.com/derpmap/default"


def get_derp_map() -> dict[str, Any]:
    print(f"Fetching DERP map from {URL}...")
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching DERP map: {e}")
        sys.exit(1)


def write_yaml(filename: Path, items: list[str]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("payload:\n")
        for item in items:
            f.write(f"  - '{item}'\n")
    print(f"Successfully wrote {len(items)} items to {filename}.")


def generate_files(data: dict[str, Any]) -> None:
    print("Generating rule providers...")
    domains: list[str] = []
    ips: list[str] = []

    regions = data.get("Regions", {})

    for region in regions.values():
        nodes = region.get("Nodes", [])
        for node in nodes:
            hostname = node.get("HostName")
            ipv4 = node.get("IPv4")
            ipv6 = node.get("IPv6")

            if hostname:
                domains.append(hostname)
            if ipv4:
                ips.append(f"{ipv4}/32")
            if ipv6:
                ips.append(f"{ipv6}/128")

    # Get script directory to make paths relative to script
    script_dir = Path(__file__).parent

    write_yaml(script_dir / "tailscale-domain.yaml", domains)
    write_yaml(script_dir / "tailscale-ip.yaml", ips)


if __name__ == "__main__":
    data = get_derp_map()
    generate_files(data)
