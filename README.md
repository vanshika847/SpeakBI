# 🧠 SpeakBI — Where Data Speaks Your Language
> *"The goal is to turn data into information, and information into insight."*
> — Carly Fiorina, Former CEO of HP
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange?logo=google&logoColor=white)](https://aistudio.google.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Prophet](https://img.shields.io/badge/Prophet-Forecasting-00A6ED)](https://facebook.github.io/prophet)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%26%20Gemini-red)](https://aistudio.google.com)
---
## 📖 Table of Contents
- [The Problem Nobody Talks About](#-the-problem-nobody-talks-about)
- [What Makes SpeakBI Different](#-what-makes-speakbi-different)
- [Live Demo](#-live-demo)
- [Architecture](#-architecture--flow)
- [Features](#-features)
- [Use Cases](#-use-cases)
- [Interactivity and UX](#-interactivity--ux)
- [Dataset](#-dataset)
- [Setup Instructions](#-setup-instructions)
- [Example Queries](#-example-queries)
- [Hallucination Handling](#-hallucination-handling)
- [Cost Analysis](#-cost-analysis)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Evaluation Coverage](#-evaluation-coverage)
- [Future Enhancements](#-future-enhancements)
- [Team](#-team)
---
## 🎯 The Problem Nobody Talks About
Every company has data. Very few people can actually use it.
A CEO wants to know *"Which content category is driving growth in Pakistan?"*
But between them and the answer stands a queue of SQL queries, a confused
analyst, a three-day wait, and a chart that answers the wrong question.
> *"Data is the new oil. But like oil, it is only valuable once refined —
> and most people are standing in front of a refinery they cannot operate."*
This is not a data problem. It is an **access problem**.
SpeakBI eliminates that gap entirely. It is a conversational Business
Intelligence platform that lets **anyone** — regardless of technical skill —
generate fully interactive, AI-powered dashboards by simply typing what
they want to know.
No SQL. No chart settings. No analyst required. No waiting. Just a question.
> *"The most profound technologies are those that disappear. They weave
> themselves into the fabric of everyday life until they are
> indistinguishable from it."* — Mark Weiser
SpeakBI is what happens when AI disappears into the dashboard —
and all that remains is the insight.
---
## ✨ What Makes SpeakBI Different
> *"Innovation is seeing what everybody has seen and thinking
> what nobody has thought."* — Dr. Albert Szent-Györgyi
| The Old Way | The SpeakBI Way |
|---|---|
| Write SQL queries manually | Type plain English naturally |
| Wait days for a data analyst | Get a dashboard in under 3 seconds |
| Static PDF reports | Live interactive Plotly dashboards |
| One question = one support ticket | Follow-up in the same conversation |
| Fixed hardcoded data sources | Upload any CSV and start querying instantly |
| Guess which chart type to use | AI picks the contextually correct chart |
| Made-up numbers when data is missing | Honest transparent "I don't have that data" |
| Everyone needs SQL training | Everyone just needs to know their question |
---
## 🚀 Live Demo
> *"A picture is worth a thousand words.
> An interactive dashboard is worth a thousand meetings."*
**[▶ Launch SpeakBI Live App →](https://your-app-name.streamlit.app)**
**[📁 View GitHub Repository →](https://github.com/YOUR_USERNAME/SpeakBI)**
**[🎥 Watch 10-Minute Demo Video →](https://your-demo-video-link.com)**
---
## 🗺️ Architecture & Flow
> *"Simplicity is the ultimate sophistication."* — Leonardo da Vinci
**[🔗 View Full Interactive Architecture Diagram →](https://your-diagram-link.com)**
> To update this diagram: export from [draw.io](https://draw.io),
> [Miro](https://miro.com), or [Eraser.io](https://eraser.io),
> save as `docs/architecture.png` in this repo,
> and replace the link above with your public share URL.
![SpeakBI Architecture Diagram](docs/architecture.png)
### The 7-Layer Intelligence Pipeline
| Layer | Module | What It Does |
|---|---|---|
| 1️⃣ Intent Parser | `intent_parser.py` | Gemini reads your question + real schema and returns structured JSON |
| 2️⃣ SQL Generator | `sql_generator.py` | Jinja2 converts intent JSON into a precise parameterised SQL query |
| 3️⃣ SQL Validator | `sql_validator.py` | Blocks DROP, DELETE, INSERT — only SELECT queries reach the database |
| 4️⃣ Hallucination Guard | `app.py` | Stops pipeline if data does not exist — no fake numbers ever |
| 5️⃣ Query Engine | SQLite | Runs validated SQL against 1M+ rows and returns a pandas DataFrame |
| 6️⃣ Chart Selector | `chart_selector.py` | Picks line / bar / pie / grouped / forecast based on intent and data shape |
| 7️⃣ Dashboard Render | Streamlit + Plotly | Interactive chart, KPI cards, data health, and AI executive story |
---
## 🌟 Features
> *"The best interface is no interface."* — Golden Krishna
### Core Intelligence
| Feature | Description |
|---|---|
| 🗣️ **Natural Language to SQL** | Schema-grounded Gemini prompts generate SQL using only real column names — never invented ones |
| 📊 **Smart Chart Selection** | Intent-aware: time data → line chart, categories → bar, proportions → pie, future → forecast |
| 🧠 **Conversational Memory** | 10-message rolling context window so follow-ups like "now filter to PK only" work naturally |
| 🔮 **Forecasting Engine** | Meta Prophet generates multi-month forecasts with upper and lower confidence band shading |
| 📝 **Executive AI Summary** | Gemini writes a board-ready narrative: overview, opportunities, risks, forecast, and 3 next actions |
| 🛡️ **Hallucination Guard** | Detects unavailable data and stops the pipeline cleanly — never invents an answer |
### Dashboard and UX
| Feature | Description |
|---|---|
| 📈 **Interactive Plotly Charts** | Hover tooltips, zoom, pan, legend toggle to isolate a series, and PNG export on every chart |
| 🎯 **Live KPI Cards** | Views, likes, engagement rate, avg sentiment — recalculated fresh on every single query |
| 🟢 **Growth / Alert Mood Banner** | Full-width colour banner: green for positive trend, red for decline — readable at a glance |
| 🎯 **Goal Progress Tracker** | Set a target view count and a live progress bar tracks actuals vs goal as a percentage |
| 💬 **Chat Timeline** | Scrollable conversation history showing every question and every AI response in the session |
| 🏥 **Data Health Report** | Detects missing values, duplicate rows, negative metrics, and out-of-range sentiment scores |
| 📥 **Raw Data and Export** | Expandable table showing full query results with a one-click CSV download button |
### Power Features
| Feature | Description |
|---|---|
| 📂 **Data Format Agnostic** | Upload any CSV — SpeakBI auto-normalises columns, parses dates, and starts answering immediately |
| 🔍 **Developer SQL Mode** | Checkbox toggle reveals the exact SQL generated for full technical transparency |
| ⚡ **Example Query Shortcuts** | One-click sidebar buttons pre-loaded with the most common CXO questions |
| 🎙️ **Voice Input** | Optional microphone query input via Google Speech Recognition |
| 🔄 **Retry Logic** | Exponential backoff on Gemini 429 rate limits — the app never crashes mid-demo |
| 💾 **Data Caching** | Streamlit `@st.cache_data` prevents 1M-row CSV from reloading on every page interaction |
---
## 💼 Use Cases
> *"If we have data, let us look at data.
> If all we have are opinions, let us go with mine."*
> — Jim Barksdale, Former CEO of Netscape
---
### 🎬 Use Case 1 — Content Strategy Executive
*You need to know what is working before the next quarterly review.*
**Question a CXO actually asks:**
> "Which video category drives the most engagement across all our markets?"
**What SpeakBI delivers:**
- Queries 1M+ rows instantly
- Calculates engagement rate per category
- Renders ranked bar chart with exact hover values
- Writes AI recommendation on where to increase production budget
---
### 🌍 Use Case 2 — Regional Marketing VP
*You are presenting to the board in 20 minutes and need regional data now.*
**Question:**
> "Compare total views and shares across all regions"
**What SpeakBI delivers:**
- Grouped bar chart: PK, IN, US, UK, BR side by side
- KPI cards showing top and bottom performing regions
- AI summary flagging which region needs immediate attention
---
### 💰 Use Case 3 — Monetisation Lead
*You need to justify the ads strategy with real numbers.*
**Question:**
> "Compare views for ads enabled vs ads disabled content"
**What SpeakBI delivers:**
- Pie chart showing the split with percentage labels on hover
- AI insight on whether monetised content is over or underperforming
- Recommended action on optimising the ads-to-organic content ratio
---
### 💙 Use Case 4 — Brand and Sentiment Manager
*You want to know how audiences feel before launching a campaign.*
**Question:**
> "Show average sentiment score by category"
**What SpeakBI delivers:**
- Colour-coded bar chart ranked from most positive to most negative
- Executive risk flags on categories scoring below neutral
- AI narrative on what is driving negative sentiment patterns
---
### 🌐 Use Case 5 — Localisation and Language Team
*You are deciding which language to prioritise for next quarter.*
**Question:**
> "Which language gets the most comments and shares?"
**What SpeakBI delivers:**
- Grouped bar chart: comments vs shares per language side by side
- Gemini recommendation identifying the top 2 languages to invest in
- Engagement breakdown to justify localisation budget decisions
---
### 📅 Use Case 6 — Long-Term Planning Committee
*You need a forward view, not just historical data.*
**Question:**
> "Forecast the next 6 months of views"
**What SpeakBI delivers:**
- Prophet forecast line chart with upper and lower confidence band shading
- AI narrative on momentum direction and risk range
- Downloadable CSV of forecast values for further offline planning
---
### 📂 Use Case 7 — Any Team With New Data
*Your team just exported a fresh dataset and needs answers immediately.*
**Action and question:**
> Drag any CSV into the sidebar uploader
> "What are the top performing segments by total reach?"
**What SpeakBI delivers:**
- Reads your columns automatically with zero configuration
- Normalises names and builds the database schema in seconds
- Answers correctly with the right chart type — no manual setup required
---
### 💬 Use Case 8 — Conversational Drill-Down
*The real power: asking follow-up questions like a real analyst 