📄 Structured JSON Extractor
A prompt-engineering project that forces any LLM to return clean, predictable, schema-valid JSON from messy natural-language input — no extra text, no broken parsing. Upload a raw customer support message and get back structured ticket data ready to plug straight into an app.

🚀 Features
🎯 Enforced JSON-only output from any LLM prompt
📐 Custom-designed JSON schema for a real use case
🧪 Automated validation against the schema (type + enum checks)
💥 Deliberate "break testing" with messy/tricky input
🔧 Iterative prompt fixing based on real failures
✅ Repeatable test suite (5 clean cases + 1 tricky case, before/after fix)
📊 Clear PASS/FAIL summary report

🏗️ System Architecture
              Raw Customer Message
                      │
                      ▼
            Prompt Template Injection
           (schema + strict JSON rules)
                      │
                      ▼
                LLM (Claude API)
                      │
                      ▼
              Raw Model Output
                      │
                      ▼
             json.loads() Parse Check
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
      Parse Success        Parse Failure
            │                   │
            ▼                   ▼
    Schema Validation      ❌ FAIL (logged)
    (fields + enums)
            │
      ┌─────┴─────┐
      ▼           ▼
  ✅ PASS      ❌ FAIL
                (invalid field/enum)

📂 Project Structure
structured-json-extractor/
│
├── schema.json                  # Target JSON schema definition
├── prompt_template.txt          # Strict JSON-only prompt sent to the LLM
├── recorded_responses.json      # Test inputs + captured model outputs
├── validate.py                  # Parses & validates recorded responses (no API key needed)
├── test_structured_output.py    # Calls the live Anthropic API and validates output
└── README.md

🛠️ Tech Stack
Technology            Purpose
Python                Programming Language
Anthropic API         LLM Inference (Claude Sonnet)
json (stdlib)         Parsing & Validation
urllib                Lightweight HTTP calls to the API

🤖 Prompt Design
Core Rule
The model is instructed to respond with ONLY valid JSON — no explanation, no markdown fences, no preamble.

Schema Enforced
{
  "name": "string or null",
  "email": "string or null",
  "issue_type": "billing | technical | account | other",
  "urgency": "low | medium | high"
}

Purpose:

Extracts structured ticket data from free-form support messages
Guarantees every response is directly parseable as JSON
Forces issue_type and urgency to always resolve to a valid enum value, never null

⚙️ Installation
1. Clone / Download the Project
git clone https://github.com/yourusername/structured-json-extractor.git

cd structured-json-extractor

2. (Optional) Create Virtual Environment
Windows

python -m venv venv
venv\Scripts\activate

Linux / macOS

python3 -m venv venv
source venv/bin/activate

3. No extra dependencies needed for offline validation
validate.py uses only Python's built-in json module.

4. (Optional) Configure Anthropic API Key — for live testing
Windows

set ANTHROPIC_API_KEY=your_api_key_here

Linux / macOS

export ANTHROPIC_API_KEY=your_api_key_here

5. Run the Validator
python3 validate.py

Or run live against the real API:
python3 test_structured_output.py

💡 How It Works
Step 1
Write a JSON schema for the real-world use case (support ticket extraction).

↓

Step 2
Design a prompt that forces the LLM to return ONLY valid JSON matching that schema.

↓

Step 3
Send 5 different sample support messages through the prompt.

↓

Step 4
Parse each response with json.loads() and validate fields/enums.

↓

Step 5
Deliberately send a messy, tricky input designed to break the prompt.

↓

Step 6
Observe the failure — extra text ("Sure! Here's the JSON:") breaks parsing.

↓

Step 7
Fix the prompt with stricter formatting rules.

↓

Step 8
Re-test the tricky input — now passes.

📦 Dependencies
No third-party packages required for the offline validator. Only the live API test script needs:

Python 3.8+
Internet connection
ANTHROPIC_API_KEY environment variable

Everything else uses Python's standard library (json, os, urllib).

📊 Test Results
Test Case               Result
test_1 (technical)      ✅ PASS
test_2 (billing)        ✅ PASS
test_3 (account)        ✅ PASS
test_4 (other)          ✅ PASS
test_5 (billing, high)  ✅ PASS
tricky_before_fix       ❌ FAIL (extra text broke JSON parsing)
tricky_after_fix        ✅ PASS (fixed with stricter prompt rules)

Final Score: 6 / 7 passed (1 intentional failure demonstrated before the fix)

🎯 Use Cases
Customer support ticket automation
Chatbot-to-database data pipelines
Form-filling from unstructured text
Lead qualification from inbound messages
Email triage and categorization
Any app needing reliable LLM → JSON handoff

📈 Future Improvements
Use native JSON mode / tool-calling schema enforcement (stronger guarantee than prompt-only)
Add retry logic with self-correction on parse failure
Expand schema for multi-issue tickets
Add automated CI test runner
Support batch testing from a CSV of messages
Add confidence scoring per extracted field

👨‍💻 Author
[Noman Nawaz]

Learning Prompt Engineering & Structured Outputs

