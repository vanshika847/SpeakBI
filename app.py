import os
import sqlite3
import tempfile
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from database.schema_loader import ensure_schema, get_schema_description
from modules.chart_selector import select_chart
from modules.data_health_checker import data_health_report
from modules.insight_generator import generate_insights
from modules.intent_parser import parse_intent
from modules.sql_generator import generate_sql
from modules.sql_validator import validate_sql
from modules.story_generator import build_story
from utils.data_loader import load_csv_to_sqlite
# ── DB path — avoids OneDrive locking ────────────────────
_default_db = "database/database.db"
try:
    _test = sqlite3.connect(_default_db)
    _test.execute("SELECT 1")
    _test.close()
    DB_PATH = _default_db
except Exception:
    DB_PATH = os.path.join(tempfile.gettempdir(), "speakbi_database.db")
# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="SpeakBI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: white;
        border: 2px solid #4a9eff;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    .chat-user {
        background: #1e3a5f;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-ai {
        background: #1e2130;
        color: #a0cfff;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 5px 0;
        max-width: 80%;
        border-left: 3px solid #4a9eff;
    }
    .stButton > button {
        background: linear-gradient(90deg, #4a9eff, #0066cc);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
# ── Session state ─────────────────────────────────────────
for key, default in {
    "conversation_history": [],
    "chat_bubbles":         [],
    "last_intent":          None,
    "query_text":           "",
    "df_current":           None,
    "schema_desc":          None,
    "db_ready":             False,
    "show_sql":             False,
}.items():
    st.session_state.setdefault(key, default)
# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/48/combo-chart.png", width=48)
    st.title("SpeakBI")
    st.caption("Ask analytics questions in plain English")
    st.markdown("---")
    st.subheader("Data Source")
    uploaded_file = st.file_uploader(
        "Upload your own CSV",
        type=["csv"],
        help="Upload any CSV. SpeakBI will auto-detect columns."
    )
    if uploaded_file:
        with st.spinner("Loading your data..."):
            try:
                df_upload = pd.read_csv(uploaded_file)
                df_upload.columns = (
                    df_upload.columns
                    .str.strip()
                    .str.lower()
                    .str.replace(" ", "_")
                )
                for col in df_upload.columns:
                    if "timestamp" in col or "date" in col or "time" in col:
                        df_upload[col] = pd.to_datetime(
                            df_upload[col], errors="coerce"
                        )
                ensure_schema(DB_PATH, df_upload)
                for attempt in range(3):
                    try:
                        with sqlite3.connect(DB_PATH, timeout=10) as conn:
                            df_upload.to_sql(
                                "sales", conn,
                                if_exists="replace", index=False
                            )
                        break
                    except sqlite3.OperationalError:
                        import time
                        time.sleep(1)
                st.session_state["schema_desc"] = get_schema_description(DB_PATH)
                st.session_state["db_ready"]    = True
                st.session_state["last_intent"] = None
                st.session_state["conversation_history"] = []
                st.success(f"Loaded {len(df_upload):,} rows")
                st.caption(f"Columns: {', '.join(df_upload.columns.tolist())}")
            except Exception as e:
                st.error(f"Failed to load CSV: {e}")
    else:
        try:
            load_csv_to_sqlite("sample_data_clean.csv", DB_PATH)

            ensure_schema(DB_PATH)
            st.session_state["schema_desc"] = get_schema_description(DB_PATH)
            st.session_state["db_ready"]    = True
            st.info("Using hackathon dataset")
        except Exception as e:
            st.error(f"Failed to load data: {e}")
    st.markdown("---")
    st.subheader("Goal Tracker")
    goal_views = st.number_input(
        "Target Views", value=1000000, step=50000, format="%d"
    )
    st.markdown("---")
    st.subheader("Date Range")
    col_s, col_e = st.columns(2)
    start_date = col_s.date_input("From", value=datetime(2024, 1, 1))
    end_date   = col_e.date_input("To",   value=datetime(2025, 12, 31))
    st.markdown("---")
    st.subheader("Try asking...")
    examples = [
        "Show total views by category",
        "Which region has the most likes?",
        "Compare views across languages",
        "Show sentiment score by category",
        "Which category gets the most shares?",
        "Show views trend over time",
        "Compare ads enabled vs disabled views",
        "Show me top performing regions",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state["query_text"] = ex
            st.rerun()
    st.markdown("---")
    st.session_state["show_sql"] = st.checkbox(
        "Show SQL (Developer Mode)", value=False
    )
# ── Header ────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#4a9eff;'>"
    "SpeakBI — Ask Your Data Anything</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#888;font-size:16px;'>"
    "Type a business question below. No SQL. No chart config. "
    "Just plain English.</p>",
    unsafe_allow_html=True
)
# ── Query input ───────────────────────────────────────────
query = st.text_input(
    label="Your question",
    value=st.session_state["query_text"],
    placeholder='"Show total views by category for 2024"',
    label_visibility="collapsed",
    key="main_query_input"
)
run_col, clear_col = st.columns([5, 1])
with run_col:
    run_btn = st.button("Analyse", use_container_width=True, type="primary")
with clear_col:
    if st.button("Clear", use_container_width=True):
        st.session_state["conversation_history"] = []
        st.session_state["chat_bubbles"]         = []
        st.session_state["query_text"]           = ""
        st.rerun()
if not query or not run_btn:
    st.markdown(
        "<div style='text-align:center;color:#555;margin-top:60px;"
        "font-size:14px;'>"
        "Enter a question above and click Analyse to generate your dashboard."
        "</div>",
        unsafe_allow_html=True
    )
    st.stop()
# ── Pipeline ──────────────────────────────────────────────
with st.spinner("Analysing your question..."):
    context = st.session_state["conversation_history"]
    context.append(query)
    st.session_state["conversation_history"] = context[-10:]
    schema_desc = st.session_state.get("schema_desc", "")
    intent = parse_intent(
        query,
        context,
        st.session_state.get("last_intent"),
        schema_desc
    )
    st.session_state["last_intent"] = intent
    sql = generate_sql(
        intent,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
# ── Developer SQL ─────────────────────────────────────────
if st.session_state.get("show_sql"):
    with st.expander("Generated SQL", expanded=False):
        st.code(sql, language="sql")
# ── Hallucination guard ───────────────────────────────────
if intent.get("intent") == "unavailable":
    st.warning(
        "This question references data not available in your dataset. "
        "Please rephrase or upload a CSV with the relevant columns."
    )
    st.info(f"Available schema:\n{schema_desc}")
    st.stop()
# ── Validate SQL ──────────────────────────────────────────
try:
    validate_sql(sql)
except ValueError as exc:
    st.error(f"Could not generate a safe query: {exc}")
    st.info("Try rephrasing your question.")
    st.stop()
# ── Run query ─────────────────────────────────────────────
try:
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        df = pd.read_sql_query(sql, conn)
except Exception as e:
    st.error(f"Query failed: {e}")
    st.info(
        "The AI may have used a column that does not exist. "
        "Try rephrasing."
    )
    st.stop()
if df.empty:
    st.warning(
        "No data found. Try adjusting your date range or rephrasing."
    )
    st.stop()
st.session_state["df_current"] = df
# ── KPI calculations ──────────────────────────────────────
views     = df["views"].sum()     if "views"     in df.columns else 0
likes     = df["likes"].sum()     if "likes"     in df.columns else 0
comments  = df["comments"].sum()  if "comments"  in df.columns else 0
shares    = df["shares"].sum()    if "shares"    in df.columns else 0
sentiment = df["sentiment_score"].mean() if "sentiment_score" in df.columns else 0
engagement = (likes / views) if views else 0
growth = (
    float(df["views"].pct_change().fillna(0).iloc[-1])
    if "views" in df.columns and len(df) >= 2
    else 0.0
)
# ── Mood banner ───────────────────────────────────────────
st.markdown("---")
mood       = "Growth Mode" if growth >= 0 else "Alert Mode"
mood_color = "#0f9d58"     if growth >= 0 else "#d93025"
st.markdown(
    f"<div style='background:{mood_color};color:white;padding:10px 20px;"
    f"border-radius:10px;text-align:center;font-size:18px;"
    f"font-weight:bold;margin-bottom:16px;'>"
    f"{mood} — Period change: {growth:+.1%}</div>",
    unsafe_allow_html=True
)
# ── KPI cards ─────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Views",      f"{views:,.0f}",      delta=f"{growth:+.1%}")
k2.metric("Total Likes",      f"{likes:,.0f}")
k3.metric("Engagement Rate",  f"{engagement:.2%}")
k4.metric("Avg Sentiment",    f"{sentiment:.3f}")
goal_pct = min(views / goal_views, 1.0) if goal_views else 0
st.progress(
    goal_pct,
    text=f"View Goal: {views:,.0f} of {goal_views:,.0f} ({goal_pct:.0%})"
)
# ── Chart ─────────────────────────────────────────────────
st.markdown("---")
st.subheader("Interactive Dashboard")
chart     = select_chart(intent, df)
x_col     = chart.get("x")
y_col     = chart.get("y")
color_col = chart.get("color")
missing   = [c for c in [x_col, y_col] if c and c not in df.columns]
if missing:
    st.warning(
        f"Chart columns not found: {missing}. "
        f"Available: {list(df.columns)}"
    )
    st.dataframe(df, use_container_width=True)
else:
    color_val   = color_col if (color_col and color_col in df.columns) else None
    forecast_df = None
    fig         = None
    if chart["type"] == "forecast":
        try:
            from modules.forecast_engine import build_forecast
            forecast_df = build_forecast(
                df, periods=intent.get("forecast_months", 6)
            )
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_df["timestamp"],
                y=forecast_df["views"],
                name="Forecast",
                line=dict(color="#4a9eff", width=2)
            ))
            if "yhat_upper" in forecast_df.columns:
                fig.add_trace(go.Scatter(
                    x=forecast_df["timestamp"],
                    y=forecast_df["yhat_upper"],
                    fill=None,
                    line=dict(color="rgba(74,158,255,0.2)"),
                    name="Upper bound"
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_df["timestamp"],
                    y=forecast_df["yhat_lower"],
                    fill="tonexty",
                    line=dict(color="rgba(74,158,255,0.2)"),
                    name="Lower bound"
                ))
            fig.update_layout(
                template="plotly_dark", title="Views Forecast"
            )
        except Exception as e:
            st.warning(f"Forecast unavailable: {e}")
            fig = px.bar(
                df, x=x_col, y=y_col,
                template="plotly_dark", title=query
            )
    elif chart["type"] == "line":
        fig = px.line(
            df, x=x_col, y=y_col, color=color_val,
            template="plotly_dark", title=query
        )
    elif chart["type"] == "pie":
        fig = px.pie(
            df, names=x_col, values=y_col,
            template="plotly_dark", title=query
        )
    elif chart["type"] == "scatter":
        fig = px.scatter(
            df, x=x_col, y=y_col, color=color_val,
            template="plotly_dark", title=query
        )
    else:
        fig = px.bar(
            df, x=x_col, y=y_col, color=color_val,
            template="plotly_dark", title=query,
            barmode="group"
        )
    if fig:
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            hoverlabel=dict(bgcolor="#1e2130", font_size=13),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig, use_container_width=True)
# ── Raw data ──────────────────────────────────────────────
with st.expander("View Raw Data"):
    st.dataframe(df, use_container_width=True)
    csv_out = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV", csv_out,
        file_name="speakbi_result.csv",
        mime="text/csv"
    )
# ── Insights ──────────────────────────────────────────────
st.markdown("---")
st.subheader("AI Insights")
col_ins, col_health = st.columns(2)
with col_ins:
    st.markdown("**Key Findings**")
    for line in generate_insights(df).split("\n"):
        if line.strip():
            st.markdown(f"- {line.strip()}")
with col_health:
    st.markdown("**Data Health**")
    health = data_health_report(df)
    if "good" in health.lower():
        st.success(health)
    else:
        st.warning(health)
# ── Executive story ───────────────────────────────────────
st.markdown("---")
st.subheader("Executive Summary")
story = build_story(
    intent, df, None,
    st.session_state["conversation_history"]
)
with st.expander("Full Story", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Overview**\n\n{story.get('overview', 'N/A')}")
        st.markdown(f"**Opportunities**\n\n{story.get('opportunities', 'N/A')}")
    with c2:
        st.markdown(f"**Risks**\n\n{story.get('risks', 'N/A')}")
        st.markdown(f"**Forecast**\n\n{story.get('forecast', 'N/A')}")
    st.markdown("**Recommended Actions**")
    for action in story.get("next_actions", []):
        st.markdown(f"- {action}")
# ── Chat with dashboard ───────────────────────────────────
st.markdown("---")
st.subheader("Chat with your Dashboard")
st.caption(
    "Ask follow-up questions like: "
    "'Now filter to only region PK' or "
    "'Show only Gaming category'"
)
st.session_state["chat_bubbles"].append(
    {"role": "user", "text": query}
)
st.session_state["chat_bubbles"].append(
    {"role": "ai", "text": story.get("overview", "Analysis complete.")}
)
for bubble in st.session_state["chat_bubbles"][-8:]:
    if bubble["role"] == "user":
        st.markdown(
            f"<div class='chat-user'>"
            f"<strong>You:</strong> {bubble['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-ai'>"
            f"<strong>SpeakBI:</strong> {bubble['text']}</div>",
            unsafe_allow_html=True
        )