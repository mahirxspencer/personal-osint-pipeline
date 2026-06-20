"""Social profile enrichment using Sherlock when available."""

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List


URL_RE = re.compile(r"https?://\S+")


def _parse_sherlock_output(output_file: Path) -> List[str]:
    results: list[str] = []
    seen: set[str] = set()
    for line in output_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("[+]"):
            continue
        match = URL_RE.search(line)
        if match:
            url = match.group(0).rstrip(")].,")
            if url not in seen:
                seen.add(url)
                results.append(url)
    return results


def enrich_social(
    username: str, output_dir: str | Path = "output", timeout: int = 5
) -> Dict[str, Any]:
    print(f"[+] Enriching social profile for username: {username}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    raw_output_file = output_path / f"sherlock_{username}.txt"
    parsed_path = output_path / f"enriched_{username}.json"

    if not shutil.which("sherlock"):
        result = {
            "username": username,
            "profiles": [],
            "error": "Sherlock is not installed or is not on PATH.",
        }
        parsed_path.write_text(json.dumps(result, indent=4), encoding="utf-8")
        print("[!] Sherlock not found. Install it or use the Docker image.")
        return result

    try:
        with raw_output_file.open("w", encoding="utf-8") as stdout_file:
            completed = subprocess.run(
                [
                    "sherlock",
                    username,
                    "--print-found",
                    "--timeout",
                    str(timeout),
                    "--no-color",
                    "--no-txt",
                ],
                stdout=stdout_file,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
    except OSError as exc:
        result = {"username": username, "profiles": [], "error": str(exc)}
        parsed_path.write_text(json.dumps(result, indent=4), encoding="utf-8")
        print(f"[!] Error running Sherlock: {exc}")
        return result

    profiles = _parse_sherlock_output(raw_output_file)
    result = {
        "username": username,
        "profiles": profiles,
        "sherlock_return_code": completed.returncode,
    }
    if completed.returncode not in (0, 1):
        result["warning"] = (
            "Sherlock exited with a non-standard status. Review raw output."
        )

    parsed_path.write_text(json.dumps(result, indent=4), encoding="utf-8")
    print(f"[+] Parsed {len(profiles)} profile(s). Results saved to {parsed_path}")
    return result
