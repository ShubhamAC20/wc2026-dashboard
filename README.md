# ⚽ FIFA World Cup 2026 Live Dashboard

🏆 **FIFA World Cup 2026 Live Dashboard**

A real-time, interactive football analytics dashboard built with Python, Plotly, and Streamlit, powered by live API data from football-data.org and AI-driven match predictions using Claude (Anthropic). The dashboard tracks live scores, group standings, match schedules, top scorers, and delivers AI-powered match predictions for the biggest sporting event on the planet.

---

## 📊 Features

- **Live Match Scores** – Real-time results and live match tracking via football-data.org API
- **Group Standings** – All 12 groups with form indicators, points progress bars, and gold/silver/bronze glow for top teams
- **Match Timeline** – Full schedule of all 104 matches grouped by date with status badges
- **AI Score Predictor** – Claude-powered match predictions with analysis, confidence rating, key factors and one to watch
- **Title Contenders** – Interactive flip cards for top 8 nations with stats on the back
- **Top Scorers** – Live leaderboard of tournament top scorers
- **Countdown Timer** – Live countdown to the next upcoming match
- **Goals Per Group Chart** – Visual comparison of which group is most exciting
- **Tournament Venue Map** – Interactive geo map of all 16 stadiums across USA, Canada & Mexico
- **Personal Branding** – Built-in LinkedIn and portfolio links

---

## 🧠 Tech Stack

| Category | Tools |
|---|---|
| Programming | Python 3.12 |
| Libraries | Pandas, Plotly, Requests |
| Dashboard Framework | Streamlit |
| Live Data | football-data.org API |
| AI Predictions | Anthropic Claude API (claude-sonnet-4-6) |
| Version Control | Git & GitHub |

---

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ShubhamAC20/wc2026-dashboard.git
cd wc2026-dashboard
pip install -r requirements.txt
```

Or manually install key libraries:

```bash
pip install streamlit pandas plotly requests anthropic
```

Set up your API keys in `.streamlit/secrets.toml`:

```toml
FOOTBALL_API_KEY = "your_football_data_token"
ANTHROPIC_KEY = "your_anthropic_key"
```

Run the app locally:

```bash
python -m streamlit run wc2026_dashboard.py
```

Then open the link shown in your terminal (usually http://localhost:8501).

---

## 📁 Project Structure
