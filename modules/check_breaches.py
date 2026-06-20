"""Optional breach exposure check.

This module intentionally does not print or save leaked passwords. It only returns
summary metadata so reports stay safer to share.
"""

import os
from typing import Any, Dict

import requests


BREACHDIRECTORY_URL = "https://breachdirectory.p.rapidapi.com/"


def check_breachdirectory(email: str, api_key: str | None = None) -> Dict[str, Any]:
    api_key = api_key or os.getenv("RAPIDAPI_KEY")
    if not api_key:
        return {"checked": False, "found": False, "error": "Missing RAPIDAPI_KEY"}

    querystring = {"func": "auto", "term": email}
    headers = {
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com",
        "X-RapidAPI-Key": api_key,
    }

    print(f"[+] Checking BreachDirectory for: {email}")
    try:
        response = requests.get(
            BREACHDIRECTORY_URL, headers=headers, params=querystring, timeout=15
        )
        if response.status_code == 200:
            data = response.json()

            # Defend against varying API response structures (dict vs list)
            if isinstance(data, dict):
                raw_results = data.get("result") or data.get("results") or []
                found_flag = bool(data.get("found"))
            elif isinstance(data, list):
                raw_results = data
                found_flag = False
            else:
                raw_results = []
                found_flag = False

            return {
                "checked": True,
                "found": found_flag or bool(raw_results),
                "breach_count": len(raw_results),
            }

        print(f"[!] BreachDirectory error: HTTP {response.status_code}")
        return {
            "checked": True,
            "found": False,
            "error": f"HTTP {response.status_code}",
        }
    except requests.RequestException as exc:
        print(f"[!] BreachDirectory exception: {exc}")
        return {"checked": True, "found": False, "error": str(exc)}
