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

wc2026-dashboard/

│

├── wc2026_dashboard.py     # Main Streamlit dashboard

├── requirements.txt        # Dependencies

├── README.md               # Project documentation

├── .gitignore              # Ignores secrets file

└── .streamlit/

└── secrets.toml        # API keys (local only, never pushed)

---

## 💡 Insights

- Live scores refresh every 60 seconds automatically
- Group standings update in real-time as matches are played
- AI predictor uses current tournament form and stats for each prediction
- Venue map covers all 16 stadiums across 3 host nations
- Goals per group chart dynamically highlights the most exciting group

---

## 🎓 Technical Highlights

This project demonstrates end-to-end data engineering and visualization:

- **Live API integration** with caching for performance optimization
- **Real-time data transformation** from raw JSON to structured dashboard components
- **AI integration** using Anthropic Claude for natural language match analysis
- **Interactive visualizations** with Plotly including geo maps, bar charts and donut charts
- **Custom CSS theming** with animations, flip cards and pulsing live indicators

Ideal for demonstrating practical data analytics skills including API integration, real-time data handling, and AI-powered insights.

---

## 🌐 Future Enhancements

- Add knockout bracket visualizer as tournament progresses
- Integrate player-level stats and heatmaps
- Add historical World Cup data for deeper comparisons
- Mobile-optimized responsive layout
- Push notifications for live match alerts

---

## ✨ Author

**Shubham Acharya**
Data Analyst | Power BI | SQL | Python | Streamlit
📍 Based in India | Open to opportunities in Spain
📫 [LinkedIn](https://www.linkedin.com/in/shubhamacharyaanalyst/) • [Portfolio](https://shubhamac20.github.io/portfolio) • [GitHub](https://github.com/ShubhamAC20)

---

## 🏁 License

This project is open source under the MIT License — free to use, modify, and share with attribution.
