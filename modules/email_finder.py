"""Optional Hunter.io helper for authorized domain/company email discovery."""

import os
from typing import Any, Dict

import requests


def find_email_with_hunter(
    first_name: str,
    last_name: str,
    domain: str | None = None,
    company: str | None = None,
    api_key: str | None = None,
) -> Dict[str, Any]:
    api_key = api_key or os.getenv("HUNTER_API_KEY")
    if not api_key:
        return {"error": "Missing HUNTER_API_KEY"}

    if not domain and not company:
        return {"error": "Missing domain/company"}

    print(f"[+] Finding email using Hunter.io for: {first_name} {last_name}")
    params = {
        "api_key": api_key,
        "first_name": first_name,
        "last_name": last_name,
    }
    if domain:
        params["domain"] = domain
    if company:
        params["company"] = company

    try:
        res = requests.get(
            "https://api.hunter.io/v2/email-finder", params=params, timeout=15
        )
        if res.status_code == 200:
            return res.json()
        print(f"[!] Hunter API error: {res.status_code}")
        return {"error": f"Hunter error {res.status_code}"}
    except requests.RequestException as exc:
        print(f"[!] Exception during Hunter call: {exc}")
        return {"error": str(exc)}
