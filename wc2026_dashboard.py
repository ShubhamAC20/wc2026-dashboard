import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone
import requests

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FIFA World Cup 2026 ⚽",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  [data-testid="collapsedControl"] {display: flex !important;}
  section[data-testid="stSidebar"] {display: flex !important;}
</style>
""", unsafe_allow_html=True)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  #MainMenu {visibility: hidden;}
  header[data-testid="stHeader"] {visibility: hidden; height: 0;}
  .block-container {padding-top: 1rem !important;}
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #0a0e1a; color: #e8eaf0; }

  .hero-banner {
    background: linear-gradient(135deg, #0f1f3d 0%, #1a0a2e 40%, #0f3d1f 100%);
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 16px; padding: 32px 40px; margin-bottom: 24px;
    position: relative; overflow: hidden;
  }
  .hero-banner::before {
    content: "⚽"; position: absolute; right: 40px; top: 50%;
    transform: translateY(-50%); font-size: 96px; opacity: 0.08;
  }
  .hero-title {
    font-family: 'Bebas Neue', sans-serif; font-size: 52px; letter-spacing: 3px;
    background: linear-gradient(90deg, #FFD700, #FF6B35, #FFD700);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; margin: 0 0 6px 0;
  }
  .hero-sub { color: #8892a4; font-size: 14px; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; }
  .hero-stats { display: flex; gap: 32px; margin-top: 20px; }
  .hero-stat { text-align: center; }
  .hero-stat .num { font-family: 'Bebas Neue', sans-serif; font-size: 36px; color: #FFD700; line-height: 1; }
  .hero-stat .lbl { font-size: 11px; color: #6b7890; text-transform: uppercase; letter-spacing: 1px; }

  .metric-card {
    background: linear-gradient(145deg, #111827, #1a2035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 20px 24px; text-align: center; height: 100%;
  }
  .metric-card .icon { font-size: 28px; margin-bottom: 8px; }
  .metric-card .value { font-family: 'Bebas Neue', sans-serif; font-size: 38px; color: #FFD700; line-height: 1; }
  .metric-card .label { font-size: 12px; color: #6b7890; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

  .section-header {
    font-family: 'Bebas Neue', sans-serif; font-size: 22px; letter-spacing: 2px;
    color: #FFD700; border-left: 3px solid #FF6B35;
    padding-left: 12px; margin: 28px 0 16px 0;
  }

  .match-card {
    background: #111827; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; transition: all 0.2s;
  }
  .match-card:hover { border-color: rgba(255,215,0,0.25); background: #151d30; }
  .match-card.live { border-color: rgba(0,255,136,0.4); animation: pulse 2s infinite; }
  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,255,136,0.15); }
    50% { box-shadow: 0 0 0 6px rgba(0,255,136,0); }
  }
  .match-group { font-size: 10px; color: #FF6B35; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
  .match-teams { display: flex; align-items: center; justify-content: space-between; margin: 8px 0; }
  .match-team { font-weight: 600; font-size: 15px; flex: 1; }
  .match-team.right { text-align: right; }
  .match-score { font-family: 'Bebas Neue', sans-serif; font-size: 28px; color: #FFD700; letter-spacing: 3px; padding: 0 16px; }
  .match-meta { font-size: 11px; color: #4b5563; margin-top: 4px; }
  .live-badge { background: #00ff88; color: #000; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 20px; }
  .upcoming-badge { background: #2563eb; color: #fff; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 20px; }
  .ft-badge { background: #374151; color: #9ca3af; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 20px; }

  .standings-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .standings-table th {
    background: #1a2035; color: #6b7890; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1px; font-size: 11px;
    padding: 10px 12px; text-align: center;
  }
  .standings-table th:first-child { text-align: left; }
  .standings-table td { padding: 10px 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.04); }
  .standings-table td:first-child { text-align: left; }
  .standings-table tr:hover td { background: rgba(255,215,0,0.04); }
  .pos-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 50%;
    font-size: 12px; font-weight: 700; margin-right: 8px;
  }
  .pos-1 { background: #FFD700; color: #000; }
  .pos-2 { background: #C0C0C0; color: #000; }
  .pos-3 { background: #3b82f6; color: #fff; }
  .pos-4 { background: #374151; color: #9ca3af; }

  [data-testid="stSidebar"] { background: #0d1120 !important; }
  .stTabs [data-baseweb="tab-list"] { background: #111827; border-radius: 10px; padding: 4px; gap: 4px; }
  .stTabs [data-baseweb="tab"] { background: transparent; color: #6b7890; border-radius: 8px; font-weight: 600; font-size: 13px; }
  .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #1a2a4a, #1a3a2a) !important; color: #FFD700 !important; }

  .fun-fact {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;
  }
  .fun-fact .ff-label { font-size: 10px; color: #6366f1; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
  .fun-fact .ff-text { font-size: 14px; color: #d1d5db; line-height: 1.6; }

  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0e1a; }
  ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
  [data-testid="collapsedControl"] {display: none !important;}

  /* Animated counter */
  @keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .metric-card .value { animation: countUp 0.6s ease-out; }

  /* Gold/Silver/Bronze glow on standings rows */
  .glow-gold   { box-shadow: inset 3px 0 0 #FFD700; background: rgba(255,215,0,0.04) !important; }
  .glow-silver { box-shadow: inset 3px 0 0 #C0C0C0; background: rgba(192,192,192,0.04) !important; }
  .glow-bronze { box-shadow: inset 3px 0 0 #CD7F32; background: rgba(205,127,50,0.04) !important; }

  /* Progress bar in standings */
  .pts-bar-wrap { display: flex; align-items: center; gap: 8px; justify-content: center; }
  .pts-bar { height: 6px; border-radius: 3px; background: linear-gradient(90deg, #FF6B35, #FFD700); min-width: 4px; }

  /* Sparkline bar */
  .spark-wrap { display: flex; align-items: flex-end; gap: 2px; height: 20px; justify-content: center; }
  .spark-bar  { width: 6px; border-radius: 2px 2px 0 0; background: #3b82f6; min-height: 3px; }

  /* Flip cards */
  .flip-card { width: 100%; height: 220px; perspective: 1000px; cursor: pointer; margin-bottom: 12px; }
  .flip-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; }
  .flip-card:hover .flip-inner { transform: rotateY(180deg); }
  .flip-front, .flip-back {
    position: absolute; width: 100%; height: 100%; backface-visibility: hidden;
    border-radius: 12px; padding: 20px; box-sizing: border-box;
    border: 1px solid rgba(255,255,255,0.07);
  }
  .flip-front { background: #111827; text-align: center; }
  .flip-back  { background: linear-gradient(135deg, #1a2a4a, #0f3d1f); transform: rotateY(180deg); }

 ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }

  .stButton button {
    background: linear-gradient(135deg, #1a2a4a, #0f3d1f) !important;
    color: #FFD700 !important;
    border: 1px solid rgba(255,215,0,0.3) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
  }
  .stButton button:hover {
    border-color: #FFD700 !important;
    color: #FFD700 !important;
  }

</style>
""", unsafe_allow_html=True)

# ─── API CONFIG ───────────────────────────────────────────────────────────────
API_KEY = st.secrets["FOOTBALL_API_KEY"]  # Paste your football-data.org token here
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# ─── VENUE MAP ────────────────────────────────────────────────────────────────

VENUE_MAP = {
    # ── GROUP A ──────────────────────────────────────────────────────────────
    ("Mexico", "South Africa"):                   "Estadio Azteca, Mexico City",
    ("South Korea", "Czechia"):                   "SoFi Stadium, Los Angeles",
    ("Mexico", "South Korea"):                    "Lumen Field, Seattle",
    ("Czechia", "South Africa"):                  "Hard Rock Stadium, Miami",
    ("South Africa", "South Korea"):              "Estadio Akron, Guadalajara",
    ("Czechia", "Mexico"):                        "AT&T Stadium, Dallas",
    # ── GROUP B ──────────────────────────────────────────────────────────────
    ("Canada", "Bosnia-Herzegovina"):         "BC Place, Vancouver",
    ("Qatar", "Switzerland"):                     "AT&T Stadium, Dallas",
    ("Switzerland", "Bosnia-Herzegovina"):    "Lincoln Financial Field, Philadelphia",
    ("Canada", "Qatar"):                          "BMO Field, Toronto",
    ("Bosnia-Herzegovina", "Qatar"):          "Levi's Stadium, San Francisco",
    ("Switzerland", "Canada"):                    "BC Place, Vancouver",
    # ── GROUP C ──────────────────────────────────────────────────────────────
    ("Brazil", "Morocco"):                        "MetLife Stadium, New York/NJ",
    ("Haiti", "Scotland"):                        "Levi's Stadium, San Francisco",
    ("Scotland", "Morocco"):                      "NRG Stadium, Houston",
    ("Brazil", "Haiti"):                          "SoFi Stadium, Los Angeles",
    ("Scotland", "Brazil"):                       "MetLife Stadium, New York/NJ",
    ("Morocco", "Haiti"):                         "Gillette Stadium, Boston",
    # ── GROUP D ──────────────────────────────────────────────────────────────
    ("United States", "Paraguay"):                "Arrowhead Stadium, Kansas City",
    ("Australia", "Turkey"):                      "Rose Bowl, Los Angeles",
    ("United States", "Australia"):               "Mercedes-Benz Stadium, Atlanta",
    ("Turkey", "Paraguay"):                       "Estadio Azteca, Mexico City",
    ("Turkey", "United States"):                  "AT&T Stadium, Dallas",
    ("Paraguay", "Australia"):                    "Hard Rock Stadium, Miami",
    # ── GROUP E ──────────────────────────────────────────────────────────────
    ("Spain", "Cape Verde"):                      "Mercedes-Benz Stadium, Atlanta",
    ("Saudi Arabia", "Uruguay"):                  "NRG Stadium, Houston",
    ("Spain", "Saudi Arabia"):                    "Gillette Stadium, Boston",
    ("Uruguay", "Cape Verde"):                    "Lincoln Financial Field, Philadelphia",
    ("Cape Verde", "Saudi Arabia"):               "Levi's Stadium, San Francisco",
    ("Uruguay", "Spain"):                         "MetLife Stadium, New York/NJ",
    # ── GROUP F ──────────────────────────────────────────────────────────────
    ("Belgium", "New Zealand"):                   "Lumen Field, Seattle",
    ("Egypt", "Iran"):                            "BC Place, Vancouver",
    ("Belgium", "Egypt"):                         "Arrowhead Stadium, Kansas City",
    ("Iran", "New Zealand"):                      "BMO Field, Toronto",
    ("Iran", "Belgium"):                          "SoFi Stadium, Los Angeles",
    ("New Zealand", "Egypt"):                     "Rose Bowl, Los Angeles",
    # ── GROUP G ──────────────────────────────────────────────────────────────
    ("Netherlands", "Curaçao"):                   "Hard Rock Stadium, Miami",
    ("Senegal", "Sweden"):                        "Mercedes-Benz Stadium, Atlanta",
    ("Netherlands", "Senegal"):                   "NRG Stadium, Houston",
    ("Sweden", "Curaçao"):                        "Estadio BBVA, Monterrey",
    ("Sweden", "Netherlands"):                    "MetLife Stadium, New York/NJ",
    ("Curaçao", "Senegal"):                       "Estadio Akron, Guadalajara",
    # ── GROUP H ──────────────────────────────────────────────────────────────
    ("Germany", "Serbia"):                        "Gillette Stadium, Boston",
    ("Colombia", "Uzbekistan"):                   "SoFi Stadium, Los Angeles",
    ("Germany", "Colombia"):                      "Lincoln Financial Field, Philadelphia",
    ("Uzbekistan", "Serbia"):                     "BMO Field, Toronto",
    ("Uzbekistan", "Germany"):                    "Arrowhead Stadium, Kansas City",
    ("Serbia", "Colombia"):                       "Hard Rock Stadium, Miami",
    # ── GROUP I ──────────────────────────────────────────────────────────────
    ("France", "Senegal"):                        "AT&T Stadium, Dallas",
    ("Iraq", "Norway"):                           "BC Place, Vancouver",
    ("France", "Iraq"):                           "Mercedes-Benz Stadium, Atlanta",
    ("Norway", "Senegal"):                        "Rose Bowl, Los Angeles",
    ("Norway", "France"):                         "MetLife Stadium, New York/NJ",
    ("Senegal", "Iraq"):                          "Levi's Stadium, San Francisco",
    # ── GROUP J ──────────────────────────────────────────────────────────────
    ("Argentina", "Algeria"):                     "MetLife Stadium, New York/NJ",
    ("Austria", "Jordan"):                        "Estadio Azteca, Mexico City",
    ("Argentina", "Austria"):                     "Rose Bowl, Los Angeles",
    ("Jordan", "Algeria"):                        "Estadio Akron, Guadalajara",
    ("Jordan", "Argentina"):                      "Hard Rock Stadium, Miami",
    ("Algeria", "Austria"):                       "NRG Stadium, Houston",
    # ── GROUP K ──────────────────────────────────────────────────────────────
    ("Portugal", "DR Congo"):                     "Lumen Field, Seattle",
    ("Portugal", "Uzbekistan"):                   "Lincoln Financial Field, Philadelphia",
    ("DR Congo", "Colombia"):                     "Estadio BBVA, Monterrey",
    ("DR Congo", "Portugal"):                     "Mercedes-Benz Stadium, Atlanta",
    ("Colombia", "Uzbekistan"):                   "BMO Field, Toronto",
    # ── GROUP L ──────────────────────────────────────────────────────────────
    ("England", "Croatia"):                       "SoFi Stadium, Los Angeles",
    ("Ghana", "Panama"):                          "Estadio Azteca, Mexico City",
    ("England", "Ghana"):                         "Arrowhead Stadium, Kansas City",
    ("Panama", "Croatia"):                        "Estadio BBVA, Monterrey",
    ("Panama", "England"):                        "MetLife Stadium, New York/NJ",
    ("Croatia", "Ghana"):                         "NRG Stadium, Houston",
    # ── KNOCKOUT STAGES ──────────────────────────────────────────────────────
    # Quarter-finals
    # QF: MetLife, AT&T Dallas, Rose Bowl, Mercedes-Benz Atlanta (Jul 4-5)
    # Semi-finals
    # SF: MetLife (Jul 11), Rose Bowl (Jul 12)
    # Third place: Hard Rock Stadium, Miami (Jul 15)
    # FINAL: MetLife Stadium, New York/NJ (Jul 19)
}

# ─── FLAG MAPPING ─────────────────────────────────────────────────────────────
ABBR_MAP = {
    "Mexico": "MEX", "South Africa": "RSA", "South Korea": "KOR", "Czechia": "CZE",
    "Czech Republic": "CZE", "Canada": "CAN", "Bosnia-Herzegovina": "BIH",
    "Qatar": "QAT", "Switzerland": "SUI", "Brazil": "BRA", "Morocco": "MAR",
    "Haiti": "HAI", "Scotland": "SCO", "United States": "USA", "USA": "USA",
    "Australia": "AUS", "Turkey": "TUR", "Türkiye": "TUR", "Paraguay": "PAR",
    "Argentina": "ARG", "France": "FRA", "England": "ENG", "Spain": "ESP",
    "Germany": "GER", "Portugal": "POR", "Netherlands": "NED", "Belgium": "BEL",
    "Japan": "JPN", "Iran": "IRN", "Senegal": "SEN", "Nigeria": "NGA",
    "Egypt": "EGY", "Colombia": "COL", "Uruguay": "URU", "Ecuador": "ECU",
    "Croatia": "CRO", "Ghana": "GHA", "Panama": "PAN", "Curaçao": "CUW",
    "Saudi Arabia": "KSA", "Cape Verde": "CPV", "Iraq": "IRQ", "Norway": "NOR",
    "Algeria": "ALG", "Austria": "AUT", "Jordan": "JOR", "DR Congo": "COD",
    "Uzbekistan": "UZB", "New Zealand": "NZL", "Sweden": "SWE", "Poland": "POL",
    "Serbia": "SRB", "Ukraine": "UKR", "Wales": "WAL", "Denmark": "DEN", "Ivory Coast": "CIV", 
    "Côte d'Ivoire": "CIV", "Tunisia": "TUN", "DR Congo": "COD",
    "Congo DR": "COD", "Democratic Republic of Congo": "COD",
}

def flag(name):
    clean = name.strip()
    for country, abbr in ABBR_MAP.items():
        if country.lower() in clean.lower() or clean.lower() in country.lower():
            return abbr
    return "?"

# ─── API FETCHING ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_matches():
    try:
        r = requests.get(f"{BASE_URL}/competitions/WC/matches", headers=HEADERS, timeout=10)
        r.raise_for_status()
        raw = r.json().get("matches", [])
        matches = []
        today_str = datetime.now().strftime("%b %d")
        for m in raw:
            home_name = m["homeTeam"]["name"] or "TBD"
            away_name = m["awayTeam"]["name"] or "TBD"
            status = m["status"]
            score_h = m["score"]["fullTime"]["home"]
            score_a = m["score"]["fullTime"]["away"]
            if status == "FINISHED":
                score_str = f"{score_h} - {score_a}"
                badge = "FT"
            elif status in ["IN_PLAY", "PAUSED"]:
                h = m["score"]["halfTime"]["home"] or 0
                a = m["score"]["halfTime"]["away"] or 0
                score_str = f"{h} - {a}"
                badge = "LIVE"
            else:
                score_str = "vs"
                badge = "UPCOMING"
            utc_dt = datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
            local_dt = utc_dt.astimezone()
            date_str = local_dt.strftime("%b %d")
            grp_raw = m.get("group") or ""
            group = grp_raw.replace("GROUP_", "") if grp_raw else "KO"
            stage = m.get("stage", "")
            matches.append({
                "group": group,
                "stage": stage,
                "home": f"{flag(home_name)} {home_name}",
                "away": f"{flag(away_name)} {away_name}",
                "home_name": home_name,
                "away_name": away_name,
                "score": score_str,
                "date": date_str,
                "venue": m.get("venue") or VENUE_MAP.get((home_name, away_name)) or VENUE_MAP.get((away_name, home_name)) or "TBD",
                "status": badge,
                "utc": utc_dt,
                "is_today": date_str == today_str,
            })
        return matches
    except Exception as e:
        st.error(f"⚠️ Could not fetch matches: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_standings():
    try:
        r = requests.get(f"{BASE_URL}/competitions/WC/standings", headers=HEADERS, timeout=10)
        r.raise_for_status()
        raw = r.json().get("standings", [])
        groups = {}
        for standing in raw:
            grp_name = (standing.get("group") or "").replace("GROUP_", "")
            if not grp_name:
                continue
            table = []
            for i, row in enumerate(standing["table"]):
                name = row["team"]["name"]
                gd = row["goalDifference"]
                # calculate form from W/D/L columns
                form_dots = ""
                w, d, l = row["won"], row["draw"], row["lost"]
                form_results = ["W"] * w + ["D"] * d + ["L"] * l
                for ch in form_results[-5:]:
                    if ch == "W":
                        form_dots += "<span style='display:inline-block;width:10px;height:10px;border-radius:50%;background:#00ff88;margin:0 				1px;'></span>"
                    elif ch == "D":
                        form_dots += "<span style='display:inline-block;width:10px;height:10px;border-radius:50%;background:#FFD700;margin:0 				1px;'></span>"
                    elif ch == "L":
                        form_dots += "<span style='display:inline-block;width:10px;height:10px;border-radius:50%;background:#ef4444;margin:0 				1px;'></span>"
                table.append({
                    "pos": i + 1,
                    "team": f"{flag(name)} {name}",
                    "p": row["playedGames"],
                    "w": row["won"],
                    "d": row["draw"],
                    "l": row["lost"],
                    "gf": row["goalsFor"],
                    "ga": row["goalsAgainst"],
                    "gd": f"+{gd}" if gd > 0 else str(gd),
                    "pts": row["points"],
		    "form": form_dots,
                })
            groups[grp_name] = table
        return groups
    except Exception as e:
        st.error(f"⚠️ Could not fetch standings: {e}")
        return {}

@st.cache_data(ttl=120)
def fetch_scorers():
    try:
        r = requests.get(f"{BASE_URL}/competitions/WC/scorers?limit=10", headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json().get("scorers", [])
    except:
        return []

# ─── LOAD LIVE DATA ───────────────────────────────────────────────────────────
with st.spinner("⚽ Loading live World Cup data..."):
	MATCHES = fetch_matches()
	GROUPS  = fetch_standings()
	SCORERS = fetch_scorers()

# ─── STATIC DATA ─────────────────────────────────────────────────────────────
CONFEDERATIONS = {
    "UEFA (Europe)":       {"teams": 16, "color": "#3b82f6"},
    "CONMEBOL (S. America)": {"teams": 6, "color": "#10b981"},
    "CONCACAF (N/C America)": {"teams": 6, "color": "#f59e0b"},
    "CAF (Africa)":        {"teams": 9, "color": "#ef4444"},
    "AFC (Asia)":          {"teams": 8, "color": "#a855f7"},
    "OFC (Oceania)":       {"teams": 1, "color": "#14b8a6"},
}

FUN_FACTS = [
    ("🏟️ BIGGEST EVER", "48 teams — 50% more than any previous World Cup. For the first time, three continents host simultaneously."),
    ("📅 39 DAYS", "The longest World Cup ever. 104 matches from June 11 to July 19 — up from 64 in Qatar 2022."),
    ("⚽ FIRST ROUND OF 32", "32 of 48 teams advance — the most inclusive knockout format in World Cup history."),
    ("🏆 ARGENTINA DEFEND", "La Albiceleste defend their Qatar 2022 crown. Messi plays his likely final World Cup."),
    ("🇧🇷 BRAZIL'S 23RD", "Brazil appear for a record 23rd consecutive World Cup, hunting a 6th title."),
    ("🎙️ FINAL AT METLIFE", "The final on July 19 at MetLife Stadium, New Jersey — capacity 82,500."),
]

TITLE_CONTENDERS = [
    {"team": "🇦🇷 Argentina",  "odds": "5/1",  "strength": 92},
    {"team": "🇫🇷 France",     "odds": "9/2",  "strength": 90},
    {"team": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England",   "odds": "6/1",  "strength": 88},
    {"team": "🇧🇷 Brazil",     "odds": "6/1",  "strength": 87},
    {"team": "🇪🇸 Spain",      "odds": "7/1",  "strength": 86},
    {"team": "🇩🇪 Germany",    "odds": "8/1",  "strength": 84},
    {"team": "🇵🇹 Portugal",   "odds": "10/1", "strength": 83},
    {"team": "🇳🇱 Netherlands","odds": "12/1", "strength": 82},
]

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0;">
      <div style="font-family:'Bebas Neue',sans-serif; font-size:28px; color:#FFD700; letter-spacing:3px;">🏆 FIFA World Cup 2026</div>
      <div style="font-size:10px; color:#4b5563; text-transform:uppercase; letter-spacing:2px;">🇺🇸 🇨🇦 🇲🇽 · Live Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    section = st.radio(
        "Navigate",
        ["🏠 Overview", "📅 Matches", "📊 Group Standings", "🏆 Contenders", "🌍 Tournament Map", "🧠 AI Predictor"],
        label_visibility="collapsed"
    )
    st.markdown("---")

    if section in ["📅 Matches", "📊 Group Standings"]:
        available_groups = ["All Groups"] + sorted(
            set(m["group"] for m in MATCHES if len(m["group"]) == 1)
        )
        selected_group = st.selectbox("🔍 Filter Group", available_groups)
        st.caption("Filters matches & standings by group")
    else:
        selected_group = "All Groups"

    live_count = sum(1 for m in MATCHES if m["status"] == "LIVE")
    today_count = sum(1 for m in MATCHES if m["is_today"])
    played_count = sum(1 for m in MATCHES if m["status"] == "FT")

    st.markdown(f"""
    <div style="margin-top: 16px; padding: 12px; background: #111827; border-radius: 10px; border: 1px solid rgba(255,215,0,0.1);">
      <div style="font-size:10px; color:#6b7890; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">📍 Live Stats</div>
      <div style="font-size:12px; color:#d1d5db; line-height:2;">
        🟢 Live now: <strong style="color:#00ff88;">{live_count}</strong><br>
        📅 Today: <strong style="color:#FFD700;">{today_count}</strong><br>
        ✅ Played: <strong>{played_count}</strong> / 104<br>
        🏆 Final: MetLife NJ · Jul 19
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top: 16px; text-align:center; font-size:11px; color:#374151;">
      🔄 Data refreshes every 60s<br>
      Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# ─── LIVE TICKER ─────────────────────────────────────────────────────────────
live_matches = [m for m in MATCHES if m["status"] == "LIVE"]
if live_matches:
    ticker_items = " &nbsp;·&nbsp; ".join(
        f"⚽ {m['home']} <strong>{m['score']}</strong> {m['away']}"
        for m in live_matches
    )
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #001a0a, #002d15, #001a0a);
        border: 1px solid rgba(0,255,136,0.3);
        border-radius: 10px; padding: 10px 20px;
        display: flex; align-items: center; gap: 16px;
        margin-bottom: 16px; overflow: hidden;
        animation: pulse 2s infinite;
    ">
        <span style="
            background: #00ff88; color: #000;
            font-size: 11px; font-weight: 800;
            padding: 3px 10px; border-radius: 20px;
            letter-spacing: 1px; white-space: nowrap;
            animation: pulse 2s infinite;
        ">🔴 LIVE</span>
        <div style="font-size: 13px; color: #e8eaf0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {ticker_items}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HERO BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">FIFA WORLD CUP 2026</div>
  <div class="hero-sub">🇺🇸 United States &nbsp;·&nbsp; 🇨🇦 Canada &nbsp;·&nbsp; 🇲🇽 Mexico &nbsp;·&nbsp; June 11 – July 19, 2026</div>
  <div class="hero-stats">
    <div class="hero-stats">
    <div class="hero-stat"><div class="num">48</div><div class="lbl">Teams</div></div>
    <div class="hero-stat"><div class="num">104</div><div class="lbl">Matches</div></div>
    <div class="hero-stat"><div class="num">16</div><div class="lbl">Venues</div></div>
    <div class="hero-stat"><div class="num">39</div><div class="lbl">Days</div></div>
    <div class="hero-stat"><div class="num">3</div><div class="lbl">Host Nations</div></div>
    <div class="hero-stat"><div class="num">12</div><div class="lbl">Groups</div></div>
  </div>
  <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(255,215,0,0.1); display:flex; align-items:center; justify-content:space-between;">
    <div style="font-size:12px; color:#4b5563;">
      Built by <strong style="color:#FFD700;">Shubham Acharya</strong> &nbsp;·&nbsp; Data Analyst
    </div>
    <div style="display:flex; gap:12px;">
      <a href="https://www.linkedin.com/in/YOUR_LINKEDIN/" target="_blank" style="font-size:11px; color:#60a5fa; text-decoration:none;">🔗 LinkedIn</a>
      <a href="https://shubhamac20.github.io/portfolio" target="_blank" style="font-size:11px; color:#60a5fa; text-decoration:none;">🌐 Portfolio</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HELPER: RENDER MATCH CARD ────────────────────────────────────────────────
def render_match(m, show_date=True):
    if m["status"] == "LIVE":
        badge = "<span class='live-badge'>🔴 LIVE</span>"
        card_cls = "match-card live"
    elif m["status"] == "UPCOMING":
        badge = "<span class='upcoming-badge'>⏰ UPCOMING</span>"
        card_cls = "match-card"
    else:
        badge = "<span class='ft-badge'>FT</span>"
        card_cls = "match-card"
    date_bit = f"&nbsp; {m['date']}" if show_date else ""
    st.markdown(f"""
    <div class="{card_cls}">
      <div class="match-group">GROUP {m['group']} &nbsp; {badge}{date_bit}</div>
      <div class="match-teams">
        <div class="match-team">{m['home']}</div>
        <div class="match-score">{m['score']}</div>
        <div class="match-team right">{m['away']}</div>
      </div>
      <div class="match-meta">🏟️ {m['venue']}</div>
    </div>""", unsafe_allow_html=True)

# ─── SECTION: OVERVIEW ────────────────────────────────────────────────────────
if section == "🏠 Overview":

    live_count  = sum(1 for m in MATCHES if m["status"] == "LIVE")
    today_count = sum(1 for m in MATCHES if m["is_today"])
    played_count= sum(1 for m in MATCHES if m["status"] == "FT")

    cols = st.columns(4)
    metrics = [
        ("✅", str(played_count), "Matches Played"),
        ("🟢", str(live_count),   "Live Now"),
        ("📅", str(today_count),  "Today's Matches"),
        ("🏆", "ARG",             "Defending Champs"),
    ]
    for col, (icon, val, lbl) in zip(cols, metrics):
        col.markdown(f"""
        <div class="metric-card">
          <div class="icon">{icon}</div>
          <div class="value">{val}</div>
          <div class="label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    # Countdown to next match
    upcoming = sorted([m for m in MATCHES if m["status"] == "UPCOMING"], key=lambda x: x["utc"])
    if upcoming:
        next_match = upcoming[0]
        now = datetime.now(timezone.utc)
        diff = next_match["utc"] - now
        total_secs = int(diff.total_seconds())
        if total_secs > 0:
            hours   = total_secs // 3600
            minutes = (total_secs % 3600) // 60
            seconds = total_secs % 60
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #0f1f3d, #1a0a2e);
                border: 1px solid rgba(255,215,0,0.3);
                border-radius: 14px; padding: 20px 28px;
                margin-top: 24px; margin-bottom: 20px;
                display: flex; align-items: center; justify-content: space-between;
            ">
                <div>
                    <div style="font-size:10px; color:#FF6B35; font-weight:700; text-transform:uppercase; letter-spacing:2px; margin-bottom:6px;">⏱️ Next Match</div>
                    <div style="font-size:16px; font-weight:700; color:#e8eaf0;">{next_match['home']} vs {next_match['away']}</div>
                    <div style="font-size:11px; color:#4b5563; margin-top:4px;">📅 {next_match['date']} &nbsp;·&nbsp; 🏟️ {next_match['venue']}</div>
                </div>
                <div style="display:flex; gap:12px; text-align:center;">
                    <div style="background:#111827; border:1px solid rgba(255,215,0,0.15); border-radius:10px; padding:12px 16px;">
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:36px; color:#FFD700; line-height:1;">{hours:02d}</div>
                        <div style="font-size:10px; color:#6b7890; text-transform:uppercase; letter-spacing:1px;">Hrs</div>
                    </div>
                    <div style="background:#111827; border:1px solid rgba(255,215,0,0.15); border-radius:10px; padding:12px 16px;">
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:36px; color:#FFD700; line-height:1;">{minutes:02d}</div>
                        <div style="font-size:10px; color:#6b7890; text-transform:uppercase; letter-spacing:1px;">Min</div>
                    </div>
                    <div style="background:#111827; border:1px solid rgba(255,215,0,0.15); border-radius:10px; padding:12px 16px;">
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:36px; color:#FFD700; line-height:1;">{seconds:02d}</div>
                        <div style="font-size:10px; color:#6b7890; text-transform:uppercase; letter-spacing:1px;">Sec</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Live matches
    live_matches = [m for m in MATCHES if m["status"] == "LIVE"]
    if live_matches:
        st.markdown("<div class='section-header'>🔴 LIVE NOW</div>", unsafe_allow_html=True)
        for m in live_matches:
            render_match(m, show_date=False)

    # Today's matches
    today_matches = [m for m in MATCHES if m["is_today"] and m["status"] != "LIVE"]
    if today_matches:
        today_label = datetime.now().strftime("%B %d").upper()
        st.markdown(f"<div class='section-header'>TODAY'S ACTION — {today_label}</div>", unsafe_allow_html=True)
        cols = st.columns(min(len(today_matches), 3))
        for col, m in zip(cols, today_matches):
            badge = "<span class='upcoming-badge'>⏰ UPCOMING</span>" if m["status"] == "UPCOMING" else "<span class='ft-badge'>FT</span>"
            col.markdown(f"""
            <div class="match-card">
              <div class="match-group">GROUP {m['group']} &nbsp; {badge}</div>
              <div class="match-teams">
                <div class="match-team">{m['home']}</div>
                <div class="match-score">{m['score']}</div>
                <div class="match-team right">{m['away']}</div>
              </div>
              <div class="match-meta">🏟️ {m['venue']}</div>
            </div>""", unsafe_allow_html=True)

    # Recent results
    recent = [m for m in MATCHES if m["status"] == "FT"][-5:][::-1]
    if recent:
        st.markdown("<div class='section-header'>RECENT RESULTS</div>", unsafe_allow_html=True)
        for m in recent:
            render_match(m)

    # Fun Facts
    st.markdown("<div class='section-header'>TOURNAMENT FACTS</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (label, text) in enumerate(FUN_FACTS):
        cols[i % 3].markdown(f"""
        <div class="fun-fact">
          <div class="ff-label">{label}</div>
          <div class="ff-text">{text}</div>
        </div>""", unsafe_allow_html=True)

    # Confederation pie
    st.markdown("<div class='section-header'>TEAMS BY CONFEDERATION</div>", unsafe_allow_html=True)
    fig = go.Figure(data=[go.Pie(
        labels=list(CONFEDERATIONS.keys()),
        values=[v["teams"] for v in CONFEDERATIONS.values()],
        hole=0.6,
        marker=dict(colors=[v["color"] for v in CONFEDERATIONS.values()], line=dict(color='#0a0e1a', width=3)),
        textinfo='label+value',
        hovertemplate="<b>%{label}</b><br>Teams: %{value}<extra></extra>",
        textfont=dict(color='white', size=12),
    )])
    fig.add_annotation(text="48<br><span style='font-size:12px'>Teams</span>",
                       x=0.5, y=0.5, font=dict(size=22, color='#FFD700', family='Bebas Neue'), showarrow=False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8eaf0'), showlegend=True,
        legend=dict(orientation='v', font=dict(color='#8892a4', size=12), bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=10, b=10, l=10, r=10), height=360
    )
    st.plotly_chart(fig, use_container_width=True)

# Goals per group bar chart
    st.markdown("<div class='section-header'>GOALS PER GROUP</div>", unsafe_allow_html=True)
    if GROUPS:	
        grp_names, grp_goals, grp_matches = [], [], []
        for grp, teams in sorted(GROUPS.items()):
            total_goals = sum(t["gf"] for t in teams)
            total_matches = sum(t["p"] for t in teams) // 2
            grp_names.append(f"Group {grp}")
            grp_goals.append(total_goals)
            grp_matches.append(max(total_matches, 1))

        avg_per_match = [round(g / m, 2) for g, m in zip(grp_goals, grp_matches)]
        colors = ["#FFD700" if g == max(grp_goals) else "#FF6B35" if g >= sorted(grp_goals)[-3] else "#3b82f6" for g in grp_goals]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=grp_names, y=grp_goals,
            marker=dict(color=colors, line=dict(color='rgba(0,0,0,0)', width=0)),
            text=[f"{g} goals<br>{a}/match" for g, a in zip(grp_goals, avg_per_match)],
            textposition='outside',
            textfont=dict(color='#e8eaf0', size=11),
            hovertemplate="<b>%{x}</b><br>Total Goals: %{y}<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#6b7890'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#6b7890'),
            font=dict(color='#e8eaf0'), height=320,
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("🥇 Gold = most goals · 🟠 Orange = top 3 · 🔵 Blue = rest")


# ─── SECTION: MATCHES ─────────────────────────────────────────────────────────
elif section == "📅 Matches":
    tab1, tab2, tab3, tab4 = st.tabs(["📅 All Matches", "🔥 Today", "🗓️ Timeline", "⚽ Top Scorers"])

    with tab1:
        pool = MATCHES if selected_group == "All Groups" else [m for m in MATCHES if m["group"] == selected_group]
        if not pool:
            st.info("No matches found for this group yet.")
        for m in pool:
            render_match(m)

    with tab2:
        today_pool = [m for m in MATCHES if m["is_today"]]
        if not today_pool:
            st.info("No matches scheduled for today.")
        for m in today_pool:
            render_match(m, show_date=False)

    with tab3:
        # Group matches by date
        from collections import defaultdict
        by_date = defaultdict(list)
        for m in MATCHES:
            by_date[m["date"]].append(m)

        for date in sorted(by_date.keys(), key=lambda d: datetime.strptime(d, "%b %d")):
            day_matches = by_date[date]
            ft   = sum(1 for m in day_matches if m["status"] == "FT")
            live = sum(1 for m in day_matches if m["status"] == "LIVE")
            upcoming = sum(1 for m in day_matches if m["status"] == "UPCOMING")

            if live > 0:
                dot = f"<span style='color:#00ff88; font-size:10px;'>● LIVE</span>"
            elif ft == len(day_matches):
                dot = f"<span style='color:#4b5563; font-size:10px;'>✓ Done</span>"
            else:
                dot = f"<span style='color:#2563eb; font-size:10px;'>○ Upcoming</span>"

            st.markdown(f"""
            <div style="margin-bottom: 6px;">
              <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                <div style="font-family:'Bebas Neue',sans-serif; font-size:18px; color:#FFD700; letter-spacing:2px;">{date}</div>
                {dot}
                <div style="font-size:11px; color:#4b5563;">{len(day_matches)} match{'es' if len(day_matches)>1 else ''}</div>
              </div>
              <div style="display:flex; gap:8px; overflow-x:auto; padding-bottom:8px; scrollbar-width:thin;">
            """, unsafe_allow_html=True)

            for m in day_matches:
                if m["status"] == "LIVE":
                    border = "rgba(0,255,136,0.5)"
                    score_color = "#00ff88"
                elif m["status"] == "FT":
                    border = "rgba(255,255,255,0.07)"
                    score_color = "#FFD700"
                else:
                    border = "rgba(37,99,235,0.4)"
                    score_color = "#6b7890"

                st.markdown(f"""
                <div style="
                    min-width: 160px; background:#111827;
                    border: 1px solid {border};
                    border-radius: 10px; padding: 12px 14px;
                    flex-shrink: 0;
                ">
                    <div style="font-size:9px; color:#FF6B35; font-weight:700; letter-spacing:1px; margin-bottom:6px;">GRP {m['group']}</div>
                    <div style="font-size:12px; font-weight:600; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{m['home']}</div>
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:20px; color:{score_color}; letter-spacing:2px; text-align:center; margin:4px 0;">{m['score']}</div>
                    <div style="font-size:12px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{m['away']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div></div><hr style='border-color:rgba(255,255,255,0.05); margin:12px 0;'>", unsafe_allow_html=True)

    with tab4:
        if not SCORERS:
            st.info("No scorer data available yet — check back once matches have been played.")
        else:
            st.markdown("<div class='section-header'>TOP SCORERS</div>", unsafe_allow_html=True)
            for i, s in enumerate(SCORERS):
                name  = s["player"]["name"]
                team  = s["team"]["name"]
                goals = s.get("goals", 0) or 0
                assists = s.get("assists", 0) or 0
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
                st.markdown(f"""
                <div class="match-card">
                  <div class="match-teams">
                    <div class="match-team">{medal} {flag(team)} {name}</div>
                    <div class="match-score">{goals}</div>
                    <div class="match-team right" style="color:#6b7890; font-size:13px;">{team} · {assists} ast</div>
                  </div>
                </div>""", unsafe_allow_html=True)

# ─── SECTION: GROUP STANDINGS ─────────────────────────────────────────────────
elif section == "📊 Group Standings":
    if not GROUPS:
        st.info("Standings not available yet. The tournament may just be starting!")
    else:
        groups_to_show = sorted(GROUPS.keys()) if selected_group == "All Groups" else [selected_group]
        max_pts = max((t["pts"] for g in GROUPS.values() for t in g), default=9)
        max_gf  = max((t["gf"]  for g in GROUPS.values() for t in g), default=1)

        for grp in groups_to_show:
            if grp not in GROUPS:
                continue
            st.markdown(f"<div class='section-header'>GROUP {grp.replace('Group ', '')}</div>", unsafe_allow_html=True)
            rows = ""
            for team in GROUPS[grp]:
                p = team["pos"]
                qualifier_cls = "qualify" if p <= 2 else ""
                glow_cls = "glow-gold" if p == 1 else "glow-silver" if p == 2 else "glow-bronze" if p == 3 else ""

                # points progress bar
                bar_w = int((team["pts"] / max(max_pts, 1)) * 80)
                pts_html = f"""
                  <div class="pts-bar-wrap">
                    <div class="pts-bar" style="width:{bar_w}px;"></div>
                    <strong style="color:#FFD700;">{team['pts']}</strong>
                  </div>"""

                # goals sparkline
                gf = team["gf"]
                spark_h = int((gf / max(max_gf, 1)) * 18) if gf > 0 else 3
                spark_html = f"""
                  <div class="spark-wrap">
                    <div class="spark-bar" style="height:{spark_h}px;"></div>
                    <span style="font-size:12px; color:#60a5fa;">{gf}</span>
                  </div>"""

                rows += f"""
                <tr class="{qualifier_cls} {glow_cls}">
                  <td><span class="pos-badge pos-{p}">{p}</span>{team['team']} <span style="margin-left:6px;">{team['form']}</span></td>
                  <td>{team['p']}</td><td>{team['w']}</td><td>{team['d']}</td><td>{team['l']}</td>
                  <td>{spark_html}</td>
                  <td>{team['ga']}</td><td>{team['gd']}</td>
                  <td>{pts_html}</td>
                </tr>"""

            st.markdown(f"""
            <table class="standings-table">
              <thead><tr>
                <th>Team</th>
                <th>P</th><th>W</th><th>D</th><th>L</th>
                <th>GF</th><th>GA</th><th>GD</th><th>PTS</th>
              </tr></thead>
              <tbody>{rows}</tbody>
            </table>
            <div style="font-size:11px; color:#4b5563; margin: 8px 0 24px 0;">
              🟡 Top 2 advance · + best 8 third-place teams reach Round of 32
            </div>""", unsafe_allow_html=True)

# ─── SECTION: CONTENDERS ──────────────────────────────────────────────────────
elif section == "🏆 Contenders":
    st.markdown("<div class='section-header'>TITLE CONTENDERS — HOVER TO FLIP</div>", unsafe_allow_html=True)

    CONTENDER_STATS = [
        {"team": "Argentina",   "odds": "5/1",  "strength": 92, "titles": 3, "fifa_rank": 1,  "best": "Winners 2022",   "crest": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg"},
        {"team": "France",      "odds": "9/2",  "strength": 90, "titles": 2, "fifa_rank": 3,  "best": "Winners 2018",   "crest": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_France.svg"},
        {"team": "England",     "odds": "6/1",  "strength": 88, "titles": 1, "fifa_rank": 5,  "best": "Winners 1966",   "crest": "https://upload.wikimedia.org/wikipedia/commons/b/be/Flag_of_England.svg"},
        {"team": "Brazil",      "odds": "6/1",  "strength": 87, "titles": 5, "fifa_rank": 5,  "best": "Winners 2002",   "crest": "https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Brazil.svg"},
        {"team": "Spain",       "odds": "7/1",  "strength": 86, "titles": 1, "fifa_rank": 6,  "best": "Winners 2010",   "crest": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Spain.svg"},
        {"team": "Germany",     "odds": "8/1",  "strength": 84, "titles": 4, "fifa_rank": 4,  "best": "Winners 2014",   "crest": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Flag_of_Germany.svg"},
        {"team": "Portugal",    "odds": "10/1", "strength": 83, "titles": 0, "fifa_rank": 7,  "best": "3rd Place 1966", "crest": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Portugal.svg"},
        {"team": "Netherlands", "odds": "12/1", "strength": 82, "titles": 0, "fifa_rank": 8,  "best": "Runner-up 2010", "crest": "https://upload.wikimedia.org/wikipedia/commons/2/20/Flag_of_the_Netherlands.svg"},
    ]

    cols = st.columns(4)
    for i, t in enumerate(CONTENDER_STATS):
        bar = "█" * int(t["strength"] / 10) + "░" * (10 - int(t["strength"] / 10))
        cols[i % 4].markdown(f"""
        <div class="flip-card">
          <div class="flip-inner">
            <div class="flip-front">
              <img src="{t['crest']}" style="width:64px; height:64px; object-fit:contain; margin-bottom:8px;" />
              <div style="font-weight:700; font-size:15px;">{t['team']}</div>
              <div style="margin-top:10px; font-size:11px; color:#FFD700; background:rgba(255,215,0,0.08); padding:4px 10px; border-radius:20px; display:inline-block;">Odds: {t['odds']}</div>
              <div style="margin-top:8px; font-size:10px; color:#4b5563;">Hover for stats ↗</div>
            </div>
            <div class="flip-back">
              <img src="{t['crest']}" style="width:32px; height:32px; object-fit:contain; margin-bottom:6px;" />
              <div style="font-size:12px; color:#FFD700; font-weight:700; margin-bottom:8px;">{t['team']}</div>
              <div style="font-size:12px; color:#d1d5db; line-height:2;">
                🏆 Titles: <strong>{t['titles']}</strong><br>
                📊 FIFA Rank: <strong>#{t['fifa_rank']}</strong><br>
                ⭐ Best: <strong>{t['best']}</strong><br>
                💪 Strength: <strong>{t['strength']}/100</strong>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─── SECTION: TOURNAMENT MAP ──────────────────────────────────────────────────
elif section == "🌍 Tournament Map":
    st.markdown("<div class='section-header'>HOST VENUES</div>", unsafe_allow_html=True)

    venues = [
        {"city": "New York/New Jersey", "stadium": "MetLife Stadium",      "cap": "82,500", "matches": 8,  "note": "🏆 FINAL",   "lat": 40.8135, "lon": -74.0744},
        {"city": "Los Angeles",         "stadium": "SoFi Stadium",          "cap": "70,240", "matches": 8,  "note": "Semi-final", "lat": 33.9534, "lon": -118.3392},
        {"city": "Dallas",              "stadium": "AT&T Stadium",          "cap": "80,000", "matches": 8,  "note": "QF venue",   "lat": 32.7480, "lon": -97.0929},
        {"city": "San Francisco",       "stadium": "Levi's Stadium",        "cap": "68,500", "matches": 6,  "note": "Group stage","lat": 37.4032, "lon": -121.9696},
        {"city": "Miami",               "stadium": "Hard Rock Stadium",     "cap": "64,767", "matches": 7,  "note": "R32 venue",  "lat": 25.9580, "lon": -80.2389},
        {"city": "Seattle",             "stadium": "Lumen Field",           "cap": "68,740", "matches": 6,  "note": "Group stage","lat": 47.5952, "lon": -122.3316},
        {"city": "Boston",              "stadium": "Gillette Stadium",      "cap": "65,878", "matches": 6,  "note": "Group stage","lat": 42.0909, "lon": -71.2643},
        {"city": "Kansas City",         "stadium": "Arrowhead Stadium",     "cap": "76,416", "matches": 6,  "note": "Group stage","lat": 39.0490, "lon": -94.4839},
        {"city": "Houston",             "stadium": "NRG Stadium",           "cap": "72,220", "matches": 6,  "note": "Group stage","lat": 29.6847, "lon": -95.4107},
        {"city": "Philadelphia",        "stadium": "Lincoln Financial",     "cap": "69,576", "matches": 6,  "note": "Group stage","lat": 39.9008, "lon": -75.1674},
        {"city": "Atlanta",             "stadium": "Mercedes-Benz Stadium", "cap": "71,000", "matches": 6,  "note": "Group stage","lat": 33.7553, "lon": -84.4006},
        {"city": "Mexico City",         "stadium": "Estadio Azteca",        "cap": "87,500", "matches": 5,  "note": "🎉 Opening", "lat": 19.3029, "lon": -99.1505},
        {"city": "Guadalajara",         "stadium": "Estadio Akron",         "cap": "49,850", "matches": 4,  "note": "MX venue",   "lat": 20.6887, "lon": -103.4671},
        {"city": "Monterrey",           "stadium": "Estadio BBVA",          "cap": "53,500", "matches": 4,  "note": "MX venue",   "lat": 25.6690, "lon": -100.2478},
        {"city": "Toronto",             "stadium": "BMO Field",             "cap": "30,000", "matches": 4,  "note": "CA venue",   "lat": 43.6333, "lon": -79.4190},
        {"city": "Vancouver",           "stadium": "BC Place",              "cap": "54,500", "matches": 4,  "note": "CA venue",   "lat": 49.2768, "lon": -123.1118},
    ]

    df_venues = pd.DataFrame(venues)
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=df_venues["lat"], lon=df_venues["lon"],
        mode='markers+text',
        marker=dict(
            size=df_venues["matches"] * 2 + 10,
            color=df_venues["matches"],
            colorscale=[[0, '#1a3a5c'], [0.5, '#FF6B35'], [1.0, '#FFD700']],
            line=dict(color='white', width=1), showscale=True,
            colorbar=dict(title=dict(text="Matches", font=dict(color='#8892a4', size=11)), tickfont=dict(color='#8892a4'))
        ),
        text=df_venues["city"],
        textfont=dict(color='white', size=9),
        textposition='top center',
        customdata=df_venues[["stadium", "cap", "matches", "note"]],
        hovertemplate="<b>%{text}</b><br>🏟️ %{customdata[0]}<br>Capacity: %{customdata[1]}<br>Matches: %{customdata[2]}<br>%{customdata[3]}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            scope='north america', bgcolor='rgba(0,0,0,0)',
            landcolor='#1a2035', oceancolor='#0a0e1a',
            countrycolor='#2d3748', coastlinecolor='#374151',
            showland=True, showocean=True, showcoastlines=True, showcountries=True,
            projection_type='natural earth',
        ),
        margin=dict(t=0, b=0, l=0, r=0), height=480,
        font=dict(color='#e8eaf0'),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-header'>VENUE DETAILS</div>", unsafe_allow_html=True)
    df_table = df_venues[["city", "stadium", "cap", "matches", "note"]].copy()
    df_table.columns = ["City", "Stadium", "Capacity", "Matches", "Note"]
    df_table = df_table.sort_values("Matches", ascending=False).reset_index(drop=True)
    st.dataframe(
        df_table, use_container_width=True, hide_index=True,
        column_config={
            "Matches": st.column_config.ProgressColumn("Matches", min_value=0, max_value=10, format="%d"),
            "Note": st.column_config.TextColumn("Highlight"),
        }
    )

# ─── SECTION: AI PREDICTOR ────────────────────────────────────────────────────
elif section == "🧠 AI Predictor":
    st.markdown("<div class='section-header'>🤖 AI SCORE PREDICTOR</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="fun-fact">
      <div class="ff-label">⚡ Powered by Claude AI</div>
      <div class="ff-text">Select any two upcoming teams and get an AI-powered match prediction with reasoning, score forecast, and key player insight.</div>
    </div>
    """, unsafe_allow_html=True)

    # Get all unique teams from upcoming matches
    upcoming_matches = [m for m in MATCHES if m["status"] == "UPCOMING"]
    all_teams = sorted(set(
        [m["home_name"] for m in upcoming_matches] +
        [m["away_name"] for m in upcoming_matches]
    ))

    if not all_teams:
        st.info("No upcoming matches available right now!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            team_a = st.selectbox("🏠 Home Team", all_teams, key="team_a")
        with col2:
            remaining = [t for t in all_teams if t != team_a]
            team_b = st.selectbox("✈️ Away Team", remaining, key="team_b")

        # Find relevant standings for context
        def get_team_stats(team_name):
            for grp, teams in GROUPS.items():
                for t in teams:
                    if team_name.lower() in t["team"].lower():
                        return grp, t
            return None, None

        grp_a, stats_a = get_team_stats(team_a)
        grp_b, stats_b = get_team_stats(team_b)

        context_a = f"Group {grp_a}: {stats_a['p']}P {stats_a['w']}W {stats_a['d']}D {stats_a['l']}L, {stats_a['gf']} goals scored, {stats_a['pts']} pts" if stats_a else "No stats yet"
        context_b = f"Group {grp_b}: {stats_b['p']}P {stats_b['w']}W {stats_b['d']}D {stats_b['l']}L, {stats_b['gf']} goals scored, {stats_b['pts']} pts" if stats_b else "No stats yet"

        if st.button("⚡ Generate Prediction", use_container_width=True):
            with st.spinner("🤖 Claude is analysing the match..."):
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_KEY"])
                    prompt = f"""You are an expert football analyst for the FIFA World Cup 2026.

Predict the match between {team_a} (Home) vs {team_b} (Away).

Current tournament stats:
- {team_a}: {context_a}
- {team_b}: {context_b}

Provide your response in exactly this format:
PREDICTED SCORE: [Home score] - [Away score]
CONFIDENCE: [Low/Medium/High]
WINNER: [Team name or Draw]
KEY FACTOR: [One sentence on the deciding factor]
ANALYSIS: [3-4 sentences of match analysis covering form, strengths, weaknesses]
ONE TO WATCH: [One key player from either side and why]"""

                    message = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    response = message.content[0].text

                    # Parse response
                    lines = response.strip().split("\n")
                    parsed = {}
                    for line in lines:
                        for key in ["PREDICTED SCORE", "CONFIDENCE", "WINNER", "KEY FACTOR", "ANALYSIS", "ONE TO WATCH"]:
                            if line.startswith(key + ":"):
                                parsed[key] = line.replace(key + ":", "").strip()

                    score     = parsed.get("PREDICTED SCORE", "? - ?")
                    conf      = parsed.get("CONFIDENCE", "Medium")
                    winner    = parsed.get("WINNER", "TBD")
                    key_fact  = parsed.get("KEY FACTOR", "")
                    analysis  = parsed.get("ANALYSIS", response)
                    one_watch = parsed.get("ONE TO WATCH", "")

                    conf_color = "#00ff88" if conf == "High" else "#FFD700" if conf == "Medium" else "#ef4444"

                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0f1f3d, #1a0a2e); border: 1px solid rgba(255,215,0,0.3); border-radius: 16px; padding: 28px; margin-top: 16px;">

                      <div style="text-align:center; margin-bottom:20px;">
                        <div style="font-size:13px; color:#6b7890; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;">Predicted Score</div>
                        <div style="font-family:'Bebas Neue',sans-serif; font-size:64px; color:#FFD700; letter-spacing:6px; line-height:1;">{score}</div>
                        <div style="font-size:14px; color:#e8eaf0; margin-top:4px;">{team_a} vs {team_b}</div>
                      </div>

                      <div style="display:flex; gap:12px; margin-bottom:20px; justify-content:center;">
                        <div style="background:#111827; border-radius:10px; padding:10px 20px; text-align:center;">
                          <div style="font-size:10px; color:#6b7890; text-transform:uppercase; letter-spacing:1px;">Winner</div>
                          <div style="font-size:15px; font-weight:700; color:#e8eaf0; margin-top:2px;">{winner}</div>
                        </div>
                        <div style="background:#111827; border-radius:10px; padding:10px 20px; text-align:center;">
                          <div style="font-size:10px; color:#6b7890; text-transform:uppercase; letter-spacing:1px;">Confidence</div>
                          <div style="font-size:15px; font-weight:700; color:{conf_color}; margin-top:2px;">{conf}</div>
                        </div>
                      </div>

                      <div style="background:#111827; border-radius:10px; padding:16px; margin-bottom:12px;">
                        <div style="font-size:10px; color:#FF6B35; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">⚡ Key Factor</div>
                        <div style="font-size:13px; color:#d1d5db; line-height:1.6;">{key_fact}</div>
                      </div>

                      <div style="background:#111827; border-radius:10px; padding:16px; margin-bottom:12px;">
                        <div style="font-size:10px; color:#FF6B35; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">📊 Analysis</div>
                        <div style="font-size:13px; color:#d1d5db; line-height:1.6;">{analysis}</div>
                      </div>

                      <div style="background:#111827; border-radius:10px; padding:16px;">
                        <div style="font-size:10px; color:#FF6B35; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">⭐ One to Watch</div>
                        <div style="font-size:13px; color:#d1d5db; line-height:1.6;">{one_watch}</div>
                      </div>

                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"⚠️ Prediction failed: {e}")
