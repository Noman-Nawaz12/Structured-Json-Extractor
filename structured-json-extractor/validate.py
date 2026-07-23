"""
Validator Script
-----------------
Loads recorded_responses.json (real outputs captured while designing the
prompt) and checks each one:
  1. Does it parse as valid JSON?
  2. Does the parsed object match our schema (correct fields + allowed values)?

This mirrors exactly what you'd do with live API responses -- the parsing
and validation logic is identical either way.
"""

import json
import os

VALID_ISSUE_TYPES = {"billing", "technical", "account", "other"}
VALID_URGENCY = {"low", "medium", "high"}


def validate_schema(obj: dict) -> list:
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


def run_case(label: str, case: dict):
    print(f"\n--- {label} ---")
    print(f"Input:  {case['input']}")
    raw = case["raw_output"]
    print(f"Output: {raw!r}")

    try:
        parsed = json.loads(raw)
        errors = validate_schema(parsed)
        if errors:
            print(f"❌ Parsed but SCHEMA INVALID -> {errors}")
            return False
        else:
            print(f"✅ PASS -> {parsed}")
            return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON PARSE FAILED -> {e}")
        return False


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "recorded_responses.json")
    with open(path) as f:
        cases = json.load(f)

    results = {}
    for label, case in cases.items():
        results[label] = run_case(label, case)

    print("\n============ SUMMARY ============")
    for label, passed in results.items():
        status = "PASS ✅" if passed else "FAIL ❌"
        print(f"{label:25s} -> {status}")

    total = len(results)
    passed_count = sum(results.values())
    print(f"\n{passed_count}/{total} test cases passed.")
