"""
Structured Outputs Test Script
--------------------------------
Sends 5 sample support messages + 1 tricky/messy message to Claude,
using a prompt that forces JSON-only output, then validates that
each response is parseable JSON matching our schema.
"""

import json
import os
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-6"

with open(os.path.join(os.path.dirname(__file__), "prompt_template.txt")) as f:
    PROMPT_TEMPLATE = f.read()

VALID_ISSUE_TYPES = {"billing", "technical", "account", "other"}
VALID_URGENCY = {"low", "medium", "high"}

TEST_MESSAGES = [
    "Hi, I'm Ahmed, ahmed@gmail.com. My app crashes every time I open it. Please help ASAP!",
    "You charged me twice this month, can someone check?",
    "I can't log into my account, forgot password isn't working.",
    "Just curious, do you guys have a dark mode planned?",
    "URGENT!! Sara here (sara99@yahoo.com) - payment failed and I'm locked out completely!!",
]

TRICKY_MESSAGE = (
    "idk my thing is broken lol also whats ur refund policy?? "
    "btw im [name redacted] pls call me at 03001234567"
)


def call_claude(message: str) -> str:
    prompt = PROMPT_TEMPLATE.replace("{MESSAGE}", message)
    payload = {
        "model": MODEL,
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    # Concatenate all text blocks
    return "".join(block.get("text", "") for block in data.get("content", []))


def validate_schema(obj: dict) -> list:
    """Return list of validation errors (empty list = valid)."""
    errors = []
    if "name" not in obj or not (obj["name"] is None or isinstance(obj["name"], str)):
        errors.append("`name` missing or wrong type")
    if "email" not in obj or not (obj["email"] is None or isinstance(obj["email"], str)):
        errors.append("`email` missing or wrong type")
    if obj.get("issue_type") not in VALID_ISSUE_TYPES:
        errors.append(f"`issue_type` invalid: {obj.get('issue_type')!r}")
    if obj.get("urgency") not in VALID_URGENCY:
        errors.append(f"`urgency` invalid: {obj.get('urgency')!r}")
    return errors


def run_test(label: str, message: str):
    print(f"\n--- {label} ---")
    print(f"Input: {message}")
    raw_output = call_claude(message)
    print(f"Raw model output: {raw_output!r}")

    try:
        parsed = json.loads(raw_output)
        errors = validate_schema(parsed)
        if errors:
            print(f"❌ Parsed but SCHEMA INVALID: {errors}")
        else:
            print(f"✅ Valid JSON matching schema: {parsed}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON PARSE FAILED: {e}")


if __name__ == "__main__":
    for i, msg in enumerate(TEST_MESSAGES, start=1):
        run_test(f"Test {i}", msg)

    run_test("Tricky/Messy Input", TRICKY_MESSAGE)
