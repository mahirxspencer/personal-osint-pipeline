"""Risk analysis for authorized personal exposure review."""

import json
from pathlib import Path
from typing import Any, Dict

from modules.check_breaches import check_breachdirectory


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def analyze(
    output_dir: str | Path = "output", use_breach_api: bool = False
) -> Dict[str, Any] | None:
    print("[+] Analyzing identity exposure...")

    output_path = Path(output_dir)
    enumeration_path = output_path / "enumeration_result.json"

    try:
        identity = _load_json(enumeration_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[!] Failed to load enumeration data: {exc}")
        return None

    subject_input = identity.get("input", {})
    username = subject_input.get("username", "")
    email = subject_input.get("email", "")

    enriched_path = output_path / f"enriched_{username}.json"
    try:
        enriched = _load_json(enriched_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[!] Failed to load enriched social data: {exc}")
        return None

    profiles = enriched.get("profiles", []) or []
    platform_count = len(profiles)
    reused = platform_count >= 5

    breach_found = False
    breach_count = 0
    email_breached: str | bool = "Not checked"

    if use_breach_api:
        breach_result = check_breachdirectory(email)
        breach_found = bool(breach_result.get("found"))
        breach_count = int(breach_result.get("breach_count", 0) or 0)
        email_breached = breach_found
        if breach_result.get("error"):
            email_breached = f"Check failed: {breach_result['error']}"
    else:
        print("[!] Skipping BreachDirectory API check")

    email_rep = identity.get("email_analysis", {}) or {}
    suspicious_email = bool(email_rep.get("suspicious"))

    score = 0
    score += 1 if reused else 0
    score += 1 if suspicious_email else 0
    score += 2 if breach_found else 0

    result = {
        "username": username,
        "email": email,
        "platforms_found": platform_count,
        "reused_across_platforms": reused,
        "email_reputation": email_rep.get("reputation", "unknown"),
        "email_suspicious": suspicious_email,
        "email_breached": email_breached,
        "breach_count": breach_count,
        "risk_score": score,
        "flag": (
            "High Risk" if score >= 3 else "Moderate Risk" if score >= 1 else "Low Risk"
        ),
        "profile_urls": profiles,
        "notes": [
            "Breach details are summarized only; leaked passwords are intentionally not stored or displayed.",
            "Treat profile matches as leads, not proof of account ownership.",
        ],
    }

    analysis_path = output_path / "analysis_result.json"
    analysis_path.write_text(json.dumps(result, indent=4), encoding="utf-8")

    print(f"[+] Risk analysis complete. Score: {score} -> {result['flag']}")
    print(f"[+] Saved to {analysis_path}")
    return result


if __name__ == "__main__":
    analyze()
