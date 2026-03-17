import json
import os
from typing import Dict, List
from google import genai
_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
def _build_prompt(
    user_input: str,
    history: List[str],
    schema_desc: str = ""
) -> str:
    convo = "\n".join(history[-5:])
    return f"""
You are an AI analyst for a YouTube video analytics dashboard.
DATABASE SCHEMA:
{schema_desc}
IMPORTANT RULES:
- Only use column names that exist in the schema above.
- The main numeric metrics are: views, likes, comments, shares, duration_sec, sentiment_score.
- The main grouping columns are: category, language, region, ads_enabled.
- The time column is: timestamp.
- If the user asks about something not in the schema, set intent to "unavailable".
- Return ONLY valid JSON, no markdown, no explanation, no code fences.
JSON keys required:
  metrics         (list)    - SQL expressions e.g. ["SUM(views) AS views", "AVG(sentiment_score) AS sentiment_score"]
  group_by        (list)    - column names to GROUP BY e.g. ["category"]
  filters         (dict)    - column: value pairs e.g. {{"region": "PK"}}
  time_grain      (string)  - day / month / quarter / year
  forecast_months (integer) - 0 if no forecast
  intent          (string)  - trend / breakdown / forecast / comparison / summary / unavailable
Conversation so far:
{convo}
New question: {user_input}
Return JSON only.
"""
def _call_gemini(prompt: str) -> Dict:
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY not set in .env")
    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    text = response.text.strip()
    if "```" in text:
        parts = text.split("```")
        text  = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())
def merge_intents(base: Dict, override: Dict) -> Dict:
    merged  = {**base}
    filters = merged.get("filters", {}).copy()
    filters.update(override.get("filters", {}))
    merged.update(override)
    merged["filters"] = filters
    return merged
def _default_intent(query: str) -> Dict:
    return {
        "metrics":         ["SUM(views) AS views"],
        "group_by":        ["category"],
        "filters":         {},
        "time_grain":      "month",
        "forecast_months": 0,
        "intent":          "summary",
        "original_query":  query,
    }
def parse_intent(
    user_input: str,
    history: List[str],
    last_intent: Dict = None,
    schema_desc: str  = ""
) -> Dict:
    if not user_input.strip():
        return _default_intent(user_input)
    try:
        prompt = _build_prompt(user_input, history, schema_desc)
        parsed = _call_gemini(prompt)
    except Exception as e:
        print(f"[intent_parser] Gemini failed: {e}")
        parsed = {}
    if parsed.get("intent") == "unavailable":
        return {
            "metrics":         [],
            "group_by":        [],
            "filters":         {},
            "time_grain":      "month",
            "forecast_months": 0,
            "intent":          "unavailable",
            "original_query":  user_input,
        }
    intent = _default_intent(user_input)
    intent.update({
        "metrics":         parsed.get("metrics",         intent["metrics"]),
        "group_by":        parsed.get("group_by",        intent["group_by"]),
        "filters":         parsed.get("filters",         {}),
        "time_grain":      parsed.get("time_grain",      "month"),
        "forecast_months": parsed.get("forecast_months", 0),
        "intent":          parsed.get("intent",          "summary"),
    })
    if last_intent:
        intent = merge_intents(last_intent, intent)
    return intent