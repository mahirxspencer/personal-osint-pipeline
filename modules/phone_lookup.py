"""Optional phone-number validation using Numverify."""

import os
from typing import Any, Dict

import requests


def lookup_phone(phone_number: str, api_key: str | None = None) -> Dict[str, Any]:
    api_key = api_key or os.getenv("NUMVERIFY_API_KEY")
    if not api_key:
        return {"error": "Missing NUMVERIFY_API_KEY"}

    print(f"[+] Looking up phone number: {phone_number}")
    url = "http://apilayer.net/api/validate"
    params = {"access_key": api_key, "number": phone_number}

    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("[+] Valid phone number" if data.get("valid") else "[!] Invalid phone number")
            return data
        print(f"[!] API error: {response.status_code}")
        return {"error": f"HTTP {response.status_code}"}
    except requests.RequestException as exc:
        print(f"[!] Exception in phone lookup: {exc}")
        return {"error": str(exc)}
