"""CLI entry point for the Personal OSINT Pipeline.

Use only for authorized security assessments, education, and personal exposure reviews.
"""

import argparse
from pathlib import Path

from modules.analyze_risk import analyze
from modules.enrich_social import enrich_social
from modules.enumerate_identity import enumerate_identity
from modules.report import generate_report


def run_pipeline(
    name: str,
    username: str,
    email: str,
    output_dir: str = "output",
    use_breach_api: bool = False,
):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("\n[1/4] Enumerating identity")
    enumerate_identity(
        name=name, username=username, email=email, output_dir=output_path
    )

    print("\n[2/4] Enriching social profiles")
    enrich_social(username=username, output_dir=output_path)

    print("\n[3/4] Analyzing risk")
    analyze(output_dir=output_path, use_breach_api=use_breach_api)

    print("\n[4/4] Generating report")
    return generate_report(output_dir=output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Personal OSINT Pipeline")
    parser.add_argument(
        "--name", required=True, help="Full name of the authorized subject"
    )
    parser.add_argument("--username", required=True, help="Username to scan")
    parser.add_argument("--email", required=True, help="Email address to check")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for generated JSON/HTML/PDF files",
    )
    parser.add_argument(
        "--use-breach-api",
        action="store_true",
        help="Enable optional BreachDirectory check. Requires RAPIDAPI_KEY in the environment.",
    )

    args = parser.parse_args()
    run_pipeline(
        name=args.name,
        username=args.username,
        email=args.email,
        output_dir=args.output_dir,
        use_breach_api=args.use_breach_api,
    )
