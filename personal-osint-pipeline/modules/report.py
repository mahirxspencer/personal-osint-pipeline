"""HTML and optional PDF report generation."""

import json
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pdfkit


def generate_report(output_dir: str | Path = "output", templates_dir: str | Path = "templates") -> Optional[str]:
    print("[+] Generating report...")

    output_path = Path(output_dir)
    analysis_path = output_path / "analysis_result.json"
    try:
        data = json.loads(analysis_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[!] Failed to load analysis data: {exc}")
        return None

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report_template.html")

    score = int(data.get("risk_score", 0) or 0)
    data["risk_color"] = "red" if score >= 3 else "orange" if score >= 1 else "green"

    rendered = template.render(**data)
    output_path.mkdir(parents=True, exist_ok=True)
    html_path = output_path / f"report_{data.get('username', 'subject')}.html"
    html_path.write_text(rendered, encoding="utf-8")
    print(f"[+] HTML report written to: {html_path}")

    pdf_path = html_path.with_suffix(".pdf")
    try:
        pdfkit.from_file(str(html_path), str(pdf_path))
        print(f"[+] PDF report written to: {pdf_path}")
        return str(pdf_path)
    except Exception as exc:
        print(f"[!] PDF generation failed: {exc}")
        print("[+] HTML report is still available.")
        return str(html_path)


if __name__ == "__main__":
    generate_report()
