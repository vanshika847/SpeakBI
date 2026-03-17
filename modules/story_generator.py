import json
import os
from typing import List, Optional
from google import genai
import pandas as pd
_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
PROMPT_TEMPLATE = """
You are an AI YouTube analytics coach.
Analyse the stats and conversation below.
Return ONLY valid JSON with these exact keys:
  overview      (string)
  opportunities (string)
  risks         (string)
  forecast      (string)
  next_actions  (list of 3 strings)
Conversation:
{context}
Stats:
{stats}
Return JSON only. No markdown. No explanation. No code fences.
"""
_FALLBACK = {
    "overview":      "Video analytics data has been loaded and analysed.",
    "opportunities": "Focus on the top-performing category to grow viewership.",
    "risks":         "Negative sentiment scores in some regions need attention.",
    "forecast":      "View trends appear stable based on current data.",
    "next_actions":  [
        "Increase content production in the top category.",
        "Target high-engagement regions with more uploads.",
        "Review and improve content in negative sentiment areas.",
    ],
}
def _format_stats(df: pd.DataFrame) -> dict:
    stats = {
        "total_views":   0,
        "total_likes":   0,
        "top_category":  "N/A",
        "top_region":    "N/A",
        "avg_sentiment": 0,
    }
    if "views" in df.columns:
        stats["total_views"] = int(df["views"].sum())
    if "likes" in df.columns:
        stats["total_likes"] = int(df["likes"].sum())
    if "category" in df.columns and "views" in df.columns:
        by_cat = df.groupby("category")["views"].sum()
        if not by_cat.empty:
            stats["top_category"] = str(by_cat.idxmax())
    if "region" in df.columns and "views" in df.columns:
        by_region = df.groupby("region")["views"].sum()
        if not by_region.empty:
            stats["top_region"] = str(by_region.idxmax())
    if "sentiment_score" in df.columns:
        stats["avg_sentiment"] = round(
            float(df["sentiment_score"].mean()), 3
        )
    return stats
def build_story(
    intent: dict,
    df: pd.DataFrame,
    forecast: Optional[pd.DataFrame] = None,
    conversation_history: Optional[List[str]] = None,
) -> dict:
    stats   = _format_stats(df)
    context = "\n".join(conversation_history[-6:]) if conversation_history else ""
    prompt  = PROMPT_TEMPLATE.format(
        context=context,
        stats=json.dumps(stats, indent=2)
    )
    try:
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
        story = json.loads(text.strip())
        for key in _FALLBACK:
            story.setdefault(key, _FALLBACK[key])
        return story
    except Exception as e:
        print(f"[story_generator] Gemini failed: {e}")
        return _FALLBACK