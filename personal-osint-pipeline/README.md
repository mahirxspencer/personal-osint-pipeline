# Personal OSINT Automation Pipeline

A modular Python OSINT pipeline for **authorized** personal exposure reviews, security education, and research. It combines email reputation checks, public username discovery, simple exposure scoring, and HTML/PDF report generation.

## Ethical and legal usage

Use this only when you have authorization, such as reviewing your own public footprint or helping someone who gave permission.

Do not use this for stalking, harassment, doxxing, unauthorized surveillance, or collecting private data. Follow the laws, terms of service, and rate limits for every service you use.

## Features

- Email reputation check through EmailRep
- Username discovery through Sherlock
- Optional breach summary check through BreachDirectory/RapidAPI
- Optional Hunter.io and Numverify helper modules
- Risk scoring based on username reuse, suspicious email reputation, and breach summary
- HTML report generation with optional PDF export
- Docker support

## Project structure

```text
personal-osint-pipeline/
├── modules/
│   ├── analyze_risk.py
│   ├── check_breaches.py
│   ├── email_finder.py
│   ├── enrich_social.py
│   ├── enumerate_identity.py
│   ├── phone_lookup.py
│   ├── report.py
│   └── socialscan_lookup.py
├── templates/
│   └── report_template.html
├── run_pipeline.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── .gitignore
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
```

Sherlock must also be installed and available on your PATH for username discovery:

```bash
pipx install git+https://github.com/sherlock-project/sherlock.git
```

## Environment variables

Copy `.env.example` to `.env` and fill in only the keys you need. Never commit real keys.

```bash
RAPIDAPI_KEY=your_rapidapi_key_here
NUMVERIFY_API_KEY=your_numverify_key_here
HUNTER_API_KEY=your_hunter_key_here
```

## Run the pipeline

```bash
python run_pipeline.py --name "Jane Doe" --username janedoe123 --email janedoe@example.com
```

Optional breach summary check:

```bash
python run_pipeline.py --name "Jane Doe" --username janedoe123 --email janedoe@example.com --use-breach-api
```

Custom output directory:

```bash
python run_pipeline.py --name "Jane Doe" --username janedoe123 --email janedoe@example.com --output-dir reports/janedoe
```

## Docker

Build:

```bash
docker build -t personal-osint-pipeline .
```

Run:

```bash
docker run --rm -v "$PWD/output:/app/output" personal-osint-pipeline --name "Jane Doe" --username janedoe123 --email janedoe@example.com
```

With optional breach API:

```bash
docker run --rm -e RAPIDAPI_KEY="$RAPIDAPI_KEY" -v "$PWD/output:/app/output" personal-osint-pipeline --name "Jane Doe" --username janedoe123 --email janedoe@example.com --use-breach-api
```

## Output

Generated files are written to `output/` by default:

- `enumeration_result.json`
- `enriched_<username>.json`
- `analysis_result.json`
- `report_<username>.html`
- `report_<username>.pdf` when wkhtmltopdf is installed and working

The report intentionally summarizes breach exposure only. It does not store or display leaked passwords.

## Recommended workflow

1. Run the pipeline on yourself or an explicitly authorized subject.
2. Manually verify each returned profile URL before treating it as a true match.
3. Use the report to identify cleanup actions: reduce username reuse, remove stale profiles, strengthen MFA, and rotate exposed credentials.
4. Keep generated output private and do not commit it to GitHub.
