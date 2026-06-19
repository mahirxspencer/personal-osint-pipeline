"""Identity enumeration helpers."""

import json
from pathlib import Path
from typing import Any, Dict

import requests


def check_emailrep(email: str) -> Dict[str, Any]:
    print(f"[+] Checking EmailRep for: {email}")
    try:
        response = requests.get(f"https://emailrep.io/{email}", timeout=15)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 429:
            print("[!] EmailRep rate limit hit (429). Returning limited data.")
            return {
                "email": email,
                "reputation": "unknown",
                "suspicious": None,
                "references": 0,
                "details": {"message": "Rate limit hit. Try again later."},
            }

        print(f"[!] EmailRep failed: {response.status_code}")
        return {"error": f"EmailRep request failed: HTTP {response.status_code}"}
    except requests.RequestException as exc:
        print(f"[!] EmailRep exception: {exc}")
        return {"error": str(exc)}


def enumerate_identity(name: str, username: str, email: str, output_dir: str | Path = "output") -> Dict[str, Any]:
    print(f"\n[+] Starting identity enumeration for: {name}, {username}, {email}")

    result: Dict[str, Any] = {
        "input": {"name": name, "username": username, "email": email},
        "email_analysis": {},
        "usernames": [],
    }

    if email:
        result["email_analysis"] = check_emailrep(email)

    if username:
        result["usernames"].append(username)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / "enumeration_result.json"
    file_path.write_text(json.dumps(result, indent=4), encoding="utf-8")

    print(f"[+] Enumeration complete. Results saved to {file_path}")
    return result
