"""A dependency-free, schema-validating client for a MAX incident-triage server."""
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REQUIRED_FIELDS = {"summary", "severity", "probable_subsystem", "confidence", "evidence", "recommended_next_actions", "human_review_required"}


def build_prompt(incident: dict) -> str:
    evidence = json.dumps(incident, indent=2, sort_keys=True)
    return f"""You are an incident-triage assistant. Analyze only the supplied evidence.
Do not claim root cause as fact. Do not suggest destructive actions. A human must review all recommendations.
Return JSON only, with exactly: summary, severity (low|medium|high|critical), probable_subsystem,
confidence (0 to 1), evidence (array), recommended_next_actions (array), human_review_required (true).

Incident evidence:
{evidence}
"""


def validate_response(content: str) -> dict:
    try:
        result = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("Model response was not valid JSON.") from error
    if not isinstance(result, dict):
        raise ValueError("Model response must be a JSON object.")
    missing, unexpected = REQUIRED_FIELDS - result.keys(), result.keys() - REQUIRED_FIELDS
    if missing or unexpected:
        raise ValueError(f"Response schema mismatch; missing={sorted(missing)}, unexpected={sorted(unexpected)}")
    if result["severity"] not in {"low", "medium", "high", "critical"}:
        raise ValueError("Response severity is invalid.")
    if result["human_review_required"] is not True:
        raise ValueError("Response must require human review.")
    return result


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    incident = json.loads(Path(__file__).with_name("sample_incident.json").read_text())
    payload = {"model": os.environ.get("MAX_MODEL", "local-model"), "messages": [{"role": "user", "content": build_prompt(incident)}], "temperature": 0.0, "max_tokens": 700}
    if dry_run:
        print(json.dumps(payload, indent=2))
        return
    url = os.environ.get("MAX_URL", "http://127.0.0.1:8000") + "/v1/chat/completions"
    request = Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=90) as response:
            result = validate_response(json.load(response)["choices"][0]["message"]["content"])
    except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as error:
        raise SystemExit(f"Incident copilot did not produce a usable triage result: {error}") from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
