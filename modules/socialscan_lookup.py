"""Optional SocialScan lookup helper."""

from typing import Any, Dict, List

try:
    from socialscan.util import Platforms, sync_execute_queries
except ImportError:  # pragma: no cover
    Platforms = None
    sync_execute_queries = None


def socialscan_lookup(username: str) -> List[Dict[str, Any]]:
    if Platforms is None or sync_execute_queries is None:
        print("[!] socialscan is not installed. Run: pip install socialscan")
        return []

    print(f"[+] Running SocialScan for: {username}")
    platforms = list(Platforms)
    results = sync_execute_queries([username], platforms)

    found_accounts = []
    for result in results:
        if result.success and not result.available:
            found_accounts.append(
                {
                    "platform": result.platform.name,
                    "input": result.query,
                    "valid": result.valid,
                    "available": result.available,
                    "detected": result.success,
                }
            )

    print(f"[+] Found {len(found_accounts)} accounts via SocialScan")
    return found_accounts
