"""
🎾 Torneo Round Robin — CSV Edition
Legge i dati direttamente da calendario.csv
Aggiorna il CSV per aggiornare i risultati.

    pip install streamlit pandas plotly
    streamlit run torneo_app_local.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Torneo Tennis", page_icon="🎾", layout="wide", initial_sidebar_state="collapsed")

# ─── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp {
    font-family: -apple-system, 'SF Pro Display', 'Inter', BlinkMacSystemFont, sans-serif;
    background: #0A0A0F;
    color: #F5F5F7;
    -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ── */
.hero-wrap {
    background: linear-gradient(160deg, #1A1A2E 0%, #16213E 40%, #0F3460 70%, #1A1A2E 100%);
    padding: 2px 10px 18px; position: relative; overflow: hidden;
}
.hero-wrap::before {
    content: ''; position: absolute; top: -80px; right: -80px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,179,237,0.15) 0%, transparent 65%);
    border-radius: 90%;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,179,237,0.15); border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px; padding: 4px 12px;
    font-size: 11px; font-weight: 300; color: #63B3ED;
    letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2px;margin-top: 10px;
}
.hero-title {
    font-size: clamp(32px, 5vw, 42px); font-weight: 200;
    letter-spacing: -1px; color: #F5F5F7; line-height: 1.05;
}
.hero-title span {
    background: linear-gradient(135deg, #63B3ED, #9F7AEA);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-size: 14px; color: rgba(255,255,255,0.4); margin-top: 6px; }

/* ── STAT STRIP ── */
.stat-strip { display: flex; gap: 10px; padding: 16px 16px 8px; overflow-x: auto; scrollbar-width: none; }
.stat-strip::-webkit-scrollbar { display: none; }
.scard {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 14px 16px; min-width: 100px; flex: 1;
    position: relative; overflow: hidden;
}
.scard::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
}
.scard-num { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; line-height: 1; }
.scard-lbl { font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.35); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
.prog-bar { height: 3px; background: rgba(255,255,255,0.08); border-radius: 2px; margin-top: 8px; overflow: hidden; }
.prog-fill { height: 3px; border-radius: 2px; background: linear-gradient(90deg, #63B3ED, #9F7AEA); }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.03) !important; padding: 0 16px !important;
    gap: 0 !important; border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    overflow-x: auto; scrollbar-width: none;
}
[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar { display: none; }
[data-testid="stTabs"] button {
    font-family: -apple-system, sans-serif !important; font-size: 13px !important;
    font-weight: 500 !important; color: rgba(255,255,255,0.35) !important;
    border-bottom: 2px solid transparent !important; border-radius: 0 !important;
    padding: 14px 14px !important; letter-spacing: 0 !important;
    text-transform: none !important; white-space: nowrap !important;
    background: transparent !important; transition: color 0.2s !important;
}
[data-testid="stTabs"] button:hover { color: rgba(255,255,255,0.65) !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #63B3ED !important; border-bottom: 2px solid #63B3ED !important; font-weight: 700 !important;
}
[data-testid="stTabs"] [role="tabpanel"] { padding: 0 !important; background: transparent !important; }

/* ── SECTION LABEL ── */
.sec-lbl {
    font-size: 15px;
    font-weight: 500;
    color: #FFD60A;   /* yellow */
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 20px 20px 8px;
}

/* ── GLASS GROUP ── */
.glass-group {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; margin: 0 16px 12px; overflow: hidden;
    position: relative;
}
.glass-group::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    pointer-events: none;
}
.grow {
    display: flex; align-items: center; padding: 13px 16px; gap: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.05); min-height: 54px;
    transition: background 0.1s;
}
.grow:last-child { border-bottom: none; }
.grow:hover { background: rgba(255,255,255,0.03); }

/* ── MATCH ROW ── */
.mbadge {
    background: rgba(255,255,255,0.07); border-radius: 7px;
    padding: 3px 8px; font-size: 10px; font-weight: 700;
    color: rgba(255,255,255,0.3); min-width: 36px; text-align: center;
    flex-shrink: 0; letter-spacing: 0.04em;
}
.mcenter { flex: 1; min-width: 0; }
.mnames { display: flex; align-items: center; gap: 7px; font-size: 15px; font-weight: 500; color: #F5F5F7; }
.mnames .w { color: #63B3ED; font-weight: 600; }
.mnames .l { color: rgba(255,255,255,0.3); }
.mnames .l2 { color: rgba(255,255,255,0.7); }
.mnames .vs { font-size: 10px; color: rgba(255,255,255,0.2); }
.msub { font-size: 15px; color: rgba(255,255,255,0.5); margin-top: 2px; font-variant-numeric: tabular-nums; }

/* ── PILLS ── */
.pill { display: inline-flex; align-items: center; gap: 3px; border-radius: 20px; padding: 4px 10px; font-size: 11px; font-weight: 700; flex-shrink: 0; white-space: nowrap; }
.pg { background: rgba(52,199,89,0.15); color: #34C759; border: 1px solid rgba(52,199,89,0.25); }
.pr { background: rgba(255,59,48,0.12); color: #FF6B60; border: 1px solid rgba(255,59,48,0.2); }
.pb { background: rgba(99,179,237,0.12); color: #63B3ED; border: 1px solid rgba(99,179,237,0.2); }
.pn { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.1); }

/* ── STANDINGS ── */
.rank-icon { font-size: 20px; width: 30px; text-align: center; flex-shrink: 0; }
.rname { font-size: 15px; font-weight: 700; color: #F5F5F7; }
.rsub { font-size: 11px; color: rgba(255,255,255,0.3); margin-top: 2px; }
.rpts { font-size: 24px; font-weight: 800; letter-spacing: -0.5px; flex-shrink: 0; margin-left: auto; }
.rpts-lbl { font-size: 9px; color: rgba(255,255,255,0.3); text-align: right; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important; padding: 16px 18px !important; position: relative; overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.35) !important; font-size: 10px !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; font-weight: 700 !important; }
[data-testid="stMetricValue"] { color: #F5F5F7 !important; font-size: 26px !important; font-weight: 800 !important; letter-spacing: -0.5px !important; }
[data-testid="stMetricValue"] * { color: #F5F5F7 !important; }

/* ── SELECT / LABELS ── */
.stSelectbox > div > div { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #F5F5F7 !important; }
label { font-size: 12px !important; font-weight: 600 !important; color: rgba(255,255,255,0.35) !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }

/* ── MISC ── */
div[data-testid="stAlert"] { border-radius: 12px !important; }
p { color: rgba(255,255,255,0.5); font-size: 14px; }
::-webkit-scrollbar { width: 0; height: 0; }
.stPlotlyChart { margin: 0 16px 12px !important; border-radius: 16px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.06) !important; }
[data-testid="stDataFrame"] { background: rgba(255,255,255,0.04) !important; border-radius: 12px !important; margin: 0 16px !important; }
/* ── BUTTON ── */
.stButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #F5F5F7 !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    border-color: rgba(255,255,255,0.25) !important;
}

.stButton > button:active {
    transform: scale(0.97);
}
.hero-wrap{
padding:26px 28px;
border-radius:12px;
background:rgba(255,255,255,0.02);
border:1px solid rgba(255,255,255,0.06);
margin-bottom:20px;
}

.hero-top{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:6px;
}

.hero-tournament{
font-size:11px;
letter-spacing:1.4px;
text-transform:uppercase;
color:rgba(255,255,255,0.35);
font-weight:600;
}

.hero-year{
font-size:12px;
font-weight:700;
color:#FFD60A;
}

.hero-title{
font-size:30px;
font-weight:800;
letter-spacing:-0.3px;
color:white;
}

.hero-title span{
color:#FFD60A;
}

.hero-meta{
display:flex;
gap:8px;
margin-top:12px;
flex-wrap:wrap;
}

.hero-pill{
font-size:11px;
padding:5px 10px;
border-radius:14px;
background:rgba(255,255,255,0.05);
color:rgba(255,255,255,0.6);
font-weight:500;
}
</style>
""", unsafe_allow_html=True)

# ─── LOAD CSV ────────────────────────────────────────────────────────────────────
CSV_PATH = Path("partite.csv")


@st.cache_data(ttl=30)
def load_csv() -> pd.DataFrame:
    if not CSV_PATH.exists():
        st.error(
            f"File non trovato: `{CSV_PATH.resolve()}`\n\nMetti `calendario.csv` nella stessa cartella di `torneo_app_local.py`.")
        st.stop()
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
    # Normalize column names to internal keys
    df = df.rename(columns={
        "MatchID": "match_id",
        "Data": "data",
        "Orario": "orario",
        "Luogo": "luogo",
        "Player 1": "player1",
        "Player 2": "player2",
        "Set 1": "set1",
        "Set 2": "set2",
        "Set 3": "set3",
        "Vincitore": "vincitore",
        "Superficie": "superficie",
    })
    df["match_id"] = pd.to_numeric(df["match_id"], errors="coerce")
    return df


# ─── HELPERS ────────────────────────────────────────────────────────────────────
def parse_set(s: str):
    try:
        a, b = str(s).strip().split("-")
        return int(a), int(b)
    except Exception:
        return None


def clean(v) -> str:
    return "" if str(v).strip() in ["nan", "None", ""] else str(v).strip()


def fmt_sets(r) -> str:
    parts = [clean(r[c]) for c in ["set1", "set2", "set3"] if clean(r.get(c, "")) != ""]
    return "  ·  ".join(parts) if parts else ""


def compute_standings(df) -> pd.DataFrame:
    players = sorted(set(df["player1"].tolist() + df["player2"].tolist()))
    s = {p: {"PG": 0, "V": 0, "S": 0, "SV": 0, "SS": 0, "GV": 0, "GS": 0} for p in players}
    played = df[df["vincitore"].apply(clean) != ""]
    for _, r in played.iterrows():
        w, p1, p2 = clean(r["vincitore"]), r["player1"], r["player2"]
        l = p2 if w == p1 else p1
        s[w]["V"] += 1;
        s[w]["PG"] += 1
        s[l]["S"] += 1;
        s[l]["PG"] += 1
        for col in ["set1", "set2", "set3"]:
            parsed = parse_set(clean(r.get(col, "")))
            if parsed:
                a, b = parsed
                if a > b:
                    s[p1]["SV"] += 1;
                    s[p2]["SS"] += 1
                elif b > a:
                    s[p2]["SV"] += 1;
                    s[p1]["SS"] += 1
                s[p1]["GV"] += a;
                s[p1]["GS"] += b
                s[p2]["GV"] += b;
                s[p2]["GS"] += a
    rows = []
    for p, v in s.items():
        pts = 0
        # Calcolo dei punti partita
        played_matches = df[((df["player1"] == p) | (df["player2"] == p)) & (df["vincitore"].apply(clean) != "")]
        for _, r in played_matches.iterrows():
            w, p1, p2 = clean(r["vincitore"]), r["player1"], r["player2"]
            l = p2 if w == p1 else p1
            sets_played = [parse_set(clean(r.get(c, ""))) for c in ["set1", "set2", "set3"]]
            sets_won = sum(1 for s in sets_played if s and ((s[0] > s[1] and p == p1) or (s[1] > s[0] and p == p2)))
            sets_lost = sum(1 for s in sets_played if s and ((s[0] < s[1] and p == p1) or (s[1] < s[0] and p == p2)))

            if p == w:  # vincitore
                if sets_won == 2 and sets_lost == 0:
                    pts += 3
                elif sets_won == 2 and sets_lost == 1:
                    pts += 2
            else:  # sconfitto
                if sets_won == 1 and sets_lost == 2:
                    pts += 1
                # 0 punti se perde 0-2
        rows.append({
            "Giocatore": p,
            "PG": v["PG"],
            "V": v["V"],
            "S": v["S"],
            "Pts": pts,
            "Set+": v["SV"],
            "Set-": v["SS"],
            "Game+": v["GV"],
            "Game-": v["GS"]
        })
    return pd.DataFrame(rows).sort_values(["Pts", "V", "Set+", "Game+"], ascending=False).reset_index(drop=True)


RANK_ICON = {0: "🥇", 1: "🥈", 2: " 🥉 ", 3: " 🏅"}
GRAD_COLORS = ["#63B3ED", "#9F7AEA", "#F6AD55", "#FC8181", "#68D391", "#76E4F7"]

# ─── DATA ────────────────────────────────────────────────────────────────────────
df = load_csv()
played_df = df[df["vincitore"].apply(clean) != ""]
pending_df = df[df["vincitore"].apply(clean) == ""]
standings = compute_standings(df)
players_list = sorted(set(df["player1"].tolist() + df["player2"].tolist()))
pct = int(len(played_df) / len(df) * 100) if len(df) else 0
leader = standings.iloc[0] if len(standings) and len(played_df) else None

# ─── HERO ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
<div class="hero-top">
<div class="hero-tournament">TORNEO AMATORIALE</div>
<div class="hero-year">2026</div>
</div>
<div class="hero-title">
Amici del Tennis
<span>Challenge</span>
</div>
<div class="hero-meta">
<span class="hero-pill">🎾 Superficie: Cemento</span>
<span class="hero-pill">🏆 Prima Edizione</span>
<span class="hero-pill">📍 Nusco</span>
</div>
</div>
""", unsafe_allow_html=True)
# ─── REFRESH BUTTON ──────────────────────────────────────────────────────────────
_, col_ref = st.columns([6, 1])
with col_ref:
    if st.button("↻ Aggiorna"):
        load_csv.clear()
        # st.rerun()
# ─── STAT STRIP ──────────────────────────────────────────────────────────────────
leader_card = ""
if leader is not None:
    leader_card = (
        '<div class="scard">'
        '<div class="scard-num">'
        f'{leader["Giocatore"]}</div>'
        f'<div class="scard-lbl">🏆 Leader con {leader["Pts"]} pt</div>'
        '</div>'
    )

# ─── TABS ─────────────────────────────────────────────────────────────────────────
# Added "Finali" to the tab list
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Classifica", "Risultati", "Partite rimanenti", "Statistiche", "Finali (Provvisorio)"])

# ══════════════════════════════════════════════════════
# TAB 1 — CLASSIFICA
# ══════════════════════════════════════════════════════
with tab1:
    if len(played_df) == 0:
        st.markdown(
            '<div style="padding:32px 20px;text-align:center">'
            '<p>Nessun risultato nel CSV ancora</p>'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown('<div class="glass-group">', unsafe_allow_html=True)

        # HEADER CLASSIFICA
        st.markdown(
            '<div style="display:flex;padding:10px 12px;'
            'font-size:11px;font-weight:600;'
            'color:rgba(255,255,255,0.35);'
            'border-bottom:1px solid rgba(255,255,255,0.05)">'

            '<div style="width:40px">#</div>'
            '<div style="flex:1">Giocatore</div>'
            '<div style="width:70px;text-align:center">Pts</div>'
            '<div style="width:90px;text-align:center">W-L</div>'
            '<div style="width:110px;text-align:center">Set</div>'
            '<div style="width:120px;text-align:center">Game</div>'
            '</div>',
            unsafe_allow_html=True
        )

        for i, row in standings.iterrows():
            wl = "#34C759" if row["V"] >= row["S"] else "#FF6B60"

            st.markdown(
                f'<div style="display:flex;align-items:center;'
                'padding:10px 12px;border-bottom:1px solid rgba(255,255,255,0.03)">'

                # Rank
                f'<div style="width:40px;font-weight:600">'
                f'{i + 1}'
                '</div>'

                # Player
                f'<div style="flex:1;font-weight:500;color:rgba(255,255,255,0.7)">'
                f'{row["Giocatore"]}'
                '</div>'

                # Points
                f'<div style="width:70px;text-align:center;'
                'font-weight:700;color:#FFD60A">'
                f'{row["Pts"]}'
                '</div>'

                # Wins Losses
                f'<div style="width:90px;text-align:center;'
                f'color:{wl};font-weight:600">'
                f'{row["V"]}-{row["S"]}'
                '</div>'

                # Sets
                f'<div style="width:110px;text-align:center;'
                'color:rgba(255,255,255,0.6)">'
                f'{row["Set+"]}-{row["Set-"]}'
                '</div>'

                # Games
                f'<div style="width:120px;text-align:center;'
                'color:rgba(255,255,255,0.6)">'
                f'{row["Game+"]}-{row["Game-"]}'
                '</div>'

                '</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 2 — RISULTATI
# ══════════════════════════════════════════════════════
with tab2:
    if len(played_df) == 0:
        st.markdown('<div style="padding:32px 20px;text-align:center"><p>Nessuna partita giocata ancora</p></div>',
                    unsafe_allow_html=True)
    else:
        # st.markdown('<div class="sec-lbl">Partite Giocate</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-group">', unsafe_allow_html=True)
        for _, r in played_df.sort_values("match_id", ascending=False).iterrows():
            p1, p2, w = r["player1"], r["player2"], clean(r["vincitore"])
            c1 = "pill pg" if w == p1 else "l2"
            c2 = "pill pg" if w == p2 else "l2"
            score = fmt_sets(r)
            st.markdown(
                f'<div class="grow">'
                f'<div class="mbadge">M{int(r["match_id"]):02d}</div>'
                '<div class="mcenter">'
                '<div class="mnames">'
                f'<span class="{c1}">{p1}</span>'
                '<span class="vs">vs</span>'
                f'<span class="{c2}">{p2}</span>'
                '</div>'
                f'<div class="msub">{score}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 3 — CALENDARIO
# ══════════════════════════════════════════════════════
with tab3:
    col_pend, col_full = st.columns(2)

    with col_pend:
        # st.markdown('<div class="sec-lbl">Da Giocare</div>', unsafe_allow_html=True)
        if len(pending_df) == 0:
            st.markdown(
                '<div class="glass-group"><div class="grow" style="justify-content:center"><span class="pill pg">🎉 Tutto completato!</span></div></div>',
                unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-group">', unsafe_allow_html=True)
            for _, r in pending_df.sort_values("match_id").iterrows():
                # --- LOGICA DATA/ORA ---
                d_raw = clean(r.get("data", ""))
                o_raw = clean(r.get("orario", ""))

                if (d_raw in ["01/01/1900", ""]) and (o_raw in ["00:00", ""]):
                    info_tempo = "Da definire"
                else:
                    info_tempo = f"{d_raw} · {o_raw}"

                st.markdown(
                    f'<div class="grow">'
                    f'<div class="mbadge">M{int(r["match_id"]):02d}</div>'
                    '<div class="mcenter">'
                    '<div class="mnames">'
                    f'<span class="l2">{r["player1"]}</span><span class="vs">vs</span><span class="l2">{r["player2"]}</span>'
                    '</div>'
                    f'<div class="msub">{info_tempo}</div>'
                    '</div>'
                    '<span class="pill pn" style="background: rgba(255,214,10,0.15); color: #FFD60A; border: 1px solid rgba(255,214,10,0.3);">⏳</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 4 — STATISTICHE
# ══════════════════════════════════════════════════════
with tab4:

    if len(played_df) == 0:
        st.markdown(
            '<div style="padding:40px;text-align:center;color:rgba(255,255,255,0.5)">'
            'Inserisci i risultati nel CSV per visualizzare le statistiche'
            '</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            '<div class="sec-lbl" style="color:#FFD60A">Statistiche Torneo</div>',
            unsafe_allow_html=True
        )
        # ---------- HERO STATS ----------
        st.markdown(
            f"""
<div style="display:flex;gap:12px;margin-bottom:18px">
<div class="scard">
<div class="scard-num" style="color:#34C759">{len(played_df)}</div>
<div class="scard-lbl">Match Giocati</div>
</div>
<div class="scard">
<div class="scard-num" style="color:#FF9F0A">{len(pending_df)}</div>
<div class="scard-lbl">Match Restanti</div>
</div>
<div class="scard">
<div class="scard-num">{pct}%</div>
<div class="scard-lbl">Torneo Completato</div>
<div class="prog-bar">
<div class="prog-fill" style="width:{pct}%"></div>
</div>
</div>
{leader_card}
</div>
""",
            unsafe_allow_html=True
        )

        # ---------- PLAYER SELECT ----------
        st.markdown(
            '<div class="sec-lbl" style="color:#FFD60A">Statistiche Giocatore</div>',
            unsafe_allow_html=True
        )

        sel = st.selectbox(
            "Seleziona Giocatore",
            players_list,
            label_visibility="collapsed"
        )

        # ---------- DATA ----------
        p_all = df[(df["player1"] == sel) | (df["player2"] == sel)]
        p_played = p_all[p_all["vincitore"].apply(clean) != ""]

        p_wins = p_played[p_played["vincitore"].apply(clean) == sel]
        p_losses = p_played[p_played["vincitore"].apply(clean) != sel]

        wr = f"{int(len(p_wins) / len(p_played) * 100)}%" if len(p_played) else "—"

        prow = standings[standings["Giocatore"] == sel].iloc[0] if sel in standings["Giocatore"].values else None

        # ---------- KPI PLAYER ----------
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Partite", len(p_played))

        with c2:
            st.metric("Win Rate", wr)

        with c3:
            st.metric("Game Vinti", int(prow["Game+"]) if prow is not None else 0)

        with c4:
            st.metric("Game Persi", int(prow["Game-"]) if prow is not None else 0)

        # ---------- MATCH HISTORY ----------
        if len(p_played):

            st.markdown(
                '<div class="sec-lbl" style="margin-top:20px">Storico Partite</div>',
                unsafe_allow_html=True
            )

            st.markdown('<div class="glass-group">', unsafe_allow_html=True)

            for _, r in p_played.sort_values("match_id").iterrows():

                won = clean(r["vincitore"]) == sel
                opp = r["player2"] if r["player1"] == sel else r["player1"]

                pill = (
                    '<span class="pill pg">Vinta</span>'
                    if won
                    else '<span class="pill pr">Persa</span>'
                )

                sc = "w" if won else "l"
                osc = "l" if won else "w"

                st.markdown(
                    f'''
<div class="grow">
<div class="mbadge">M{int(r["match_id"]):02d}</div>
<div class="mcenter">
<div class="mnames">
<span class="{sc}">{sel}</span>
<span class="vs">vs</span>
<span class="{osc}">{opp}</span>
</div>
<div class="msub">
{fmt_sets(r)}
</div>
</div>
{pill}
</div>
''',
                    unsafe_allow_html=True
                )

            st.markdown('</div>', unsafe_allow_html=True)
# ══════════════════════════════════════════════════════
# TAB 5 — FINALI & HEAD TO HEAD
# ══════════════════════════════════════════════════════
with tab5:
    if len(standings) < 4:
        st.info("Servono almeno 4 giocatori in classifica per generare le semifinali.")

    else:

        top4 = standings.head(4)

        p1 = top4.iloc[0]["Giocatore"]
        p2 = top4.iloc[1]["Giocatore"]
        p3 = top4.iloc[2]["Giocatore"]
        p4 = top4.iloc[3]["Giocatore"]

        col1, col2 = st.columns(2)

        with col1:

            html_sf1 = f"""
            <br>
<div class="glass-group">

<div style="text-align:center;font-size:11px;letter-spacing:1px;font-weight:600;
color:rgba(255,255,255,0.5);margin-bottom:8px">
SEMIFINALE 1
</div>

<div style="display:flex;flex-direction:column;gap:8px">

<div style="padding:10px 12px;background:rgba(255,255,255,0.02);border-radius:6px">
<span style="color:#FFD60A;font-weight:700">#1</span>
<span style="margin-left:8px;margin-left:8px;color:rgba(255,255,255,0.7)">{p1}</span>
</div>

<div style="margin-left:8px;font-size:25px;color:rgba(255,255,255,0.25)">vs</div>

<div style="padding:10px 12px;background:rgba(255,255,255,0.02);border-radius:6px">
<span style="color:#FFD60A;font-weight:700">#3</span>
<span style="margin-left:8px;margin-left:8px;color:rgba(255,255,255,0.7)">{p3}</span>
</div>

</div>

</div>
"""
            st.markdown(html_sf1, unsafe_allow_html=True)

        with col2:

            html_sf2 = f"""
            <br>
<div class="glass-group">

<div style="text-align:center;font-size:11px;letter-spacing:1px;font-weight:600;
color:rgba(255,255,255,0.5);margin-bottom:8px">
SEMIFINALE 2
</div>

<div style="display:flex;flex-direction:column;gap:8px">

<div style="padding:10px 12px;background:rgba(255,255,255,0.02);border-radius:6px">
<span style="color:#FFD60A;font-weight:700">#2</span>
<span style="margin-left:8px;color:rgba(255,255,255,0.7)">{p2}</span>
</div>

<div style="margin-left:8px;font-size:25px;color:rgba(255,255,255,0.25)">vs</div>

<div style="padding:10px 12px;background:rgba(255,255,255,0.02);border-radius:6px">
<span style="color:#FFD60A;font-weight:700">#4</span>
<span style="margin-left:8px;margin-left:8px;color:rgba(255,255,255,0.7)">{p4}</span>
</div>

</div>

</div>
"""
            st.markdown(html_sf2, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
