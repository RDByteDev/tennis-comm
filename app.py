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
    padding: 52px 20px 28px; position: relative; overflow: hidden;
}
.hero-wrap::before {
    content: ''; position: absolute; top: -80px; right: -80px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(99,179,237,0.15) 0%, transparent 65%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,179,237,0.15); border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px; padding: 4px 12px;
    font-size: 11px; font-weight: 600; color: #63B3ED;
    letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px;
}
.hero-title {
    font-size: clamp(32px, 5vw, 42px); font-weight: 800;
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
.scard-num { font-size: 26px; font-weight: 800; letter-spacing: -0.5px; line-height: 1; }
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
    font-size: 11px;
    font-weight: 700;
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
.mnames .w { color: #63B3ED; font-weight: 700; }
.mnames .l { color: rgba(255,255,255,0.3); }
.mnames .vs { font-size: 10px; color: rgba(255,255,255,0.2); }
.msub { font-size: 11px; color: rgba(255,255,255,0.3); margin-top: 2px; font-variant-numeric: tabular-nums; }

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
</style>
""", unsafe_allow_html=True)

# ─── LOAD CSV ────────────────────────────────────────────────────────────────────
CSV_PATH = Path("partite.csv")

@st.cache_data(ttl=30)
def load_csv() -> pd.DataFrame:
    if not CSV_PATH.exists():
        st.error(f"File non trovato: `{CSV_PATH.resolve()}`\n\nMetti `calendario.csv` nella stessa cartella di `torneo_app_local.py`.")
        st.stop()
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
    # Normalize column names to internal keys
    df = df.rename(columns={
        "MatchID":    "match_id",
        "Data":       "data",
        "Orario":     "orario",
        "Luogo":      "luogo",
        "Player 1":   "player1",
        "Player 2":   "player2",
        "Set 1":      "set1",
        "Set 2":      "set2",
        "Set 3":      "set3",
        "Vincitore":  "vincitore",
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
    parts = [clean(r[c]) for c in ["set1","set2","set3"] if clean(r.get(c,"")) != ""]
    return "  ·  ".join(parts) if parts else ""

def compute_standings(df) -> pd.DataFrame:
    players = sorted(set(df["player1"].tolist() + df["player2"].tolist()))
    s = {p: {"PG":0,"V":0,"S":0,"SV":0,"SS":0,"GV":0,"GS":0} for p in players}
    played = df[df["vincitore"].apply(clean) != ""]
    for _, r in played.iterrows():
        w, p1, p2 = clean(r["vincitore"]), r["player1"], r["player2"]
        l = p2 if w == p1 else p1
        s[w]["V"] += 1; s[w]["PG"] += 1
        s[l]["S"] += 1; s[l]["PG"] += 1
        for col in ["set1","set2","set3"]:
            parsed = parse_set(clean(r.get(col,"")))
            if parsed:
                a, b = parsed
                if a > b:   s[p1]["SV"] += 1; s[p2]["SS"] += 1
                elif b > a: s[p2]["SV"] += 1; s[p1]["SS"] += 1
                s[p1]["GV"] += a; s[p1]["GS"] += b
                s[p2]["GV"] += b; s[p2]["GS"] += a
    rows = [{"Giocatore":p, "PG":v["PG"], "V":v["V"], "S":v["S"],
             "Pts":v["V"]*3, "Set+":v["SV"], "Set-":v["SS"],
             "Game+":v["GV"], "Game-":v["GS"]} for p,v in s.items()]
    return pd.DataFrame(rows).sort_values(["Pts","V","Set+","Game+"], ascending=False).reset_index(drop=True)

RANK_ICON  = {0:"🥇", 1:"🥈", 2:" 🥉 ", 3:" 🏅"}
GRAD_COLORS = ["#63B3ED","#9F7AEA","#F6AD55","#FC8181","#68D391","#76E4F7"]

# ─── DATA ────────────────────────────────────────────────────────────────────────
df           = load_csv()
played_df    = df[df["vincitore"].apply(clean) != ""]
pending_df   = df[df["vincitore"].apply(clean) == ""]
standings    = compute_standings(df)
players_list = sorted(set(df["player1"].tolist() + df["player2"].tolist()))
pct          = int(len(played_df) / len(df) * 100) if len(df) else 0
leader       = standings.iloc[0] if len(standings) and len(played_df) else None

# ─── HERO ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-badge">🎾 Cemento · 2026</div>
    <div class="hero-title">Prima edizione <span>Amici del Tennis</span></div>
    <div class="hero-sub">{len(players_list)} giocatori</div>
</div>
""", unsafe_allow_html=True)

# ─── STAT STRIP ──────────────────────────────────────────────────────────────────
leader_card = ""
if leader is not None:
    leader_card = (
        '<div class="scard">'
        '<div class="scard-num" style="background:linear-gradient(135deg,#63B3ED,#9F7AEA);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">'
        f'{leader["Pts"]}</div>'
        f'<div class="scard-lbl">🏆 {leader["Giocatore"]}</div>'
        '</div>'
    )

st.markdown(
    '<div class="stat-strip">'
    '<div class="scard">'
    f'<div class="scard-num" style="color:#34C759">{len(played_df)}</div>'
    '<div class="scard-lbl">Giocate</div>'
    '</div>'
    '<div class="scard">'
    f'<div class="scard-num" style="color:#FF9F0A">{len(pending_df)}</div>'
    '<div class="scard-lbl">Da giocare</div>'
    '</div>'
    '<div class="scard">'
    f'<div class="scard-num">{pct}%</div>'
    '<div class="scard-lbl">Completato</div>'
    f'<div class="prog-bar"><div class="prog-fill" style="width:{pct}%"></div></div>'
    '</div>'
    + leader_card +
    '</div>',
    unsafe_allow_html=True
)

# ─── REFRESH BUTTON ──────────────────────────────────────────────────────────────
_, col_ref = st.columns([6, 1])
with col_ref:
    if st.button("↻ Aggiorna"):
        load_csv.clear()
        st.rerun()

# ─── TABS ─────────────────────────────────────────────────────────────────────────
# Added "Finali" to the tab list
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Classifica", "Risultati", "Calendario", "Statistiche", "Finali"])

# ══════════════════════════════════════════════════════
# TAB 1 — CLASSIFICA
# ══════════════════════════════════════════════════════
with tab1:
    if len(played_df) == 0:
        st.markdown('<div style="padding:32px 20px;text-align:center"><p>Nessun risultato nel CSV ancora</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sec-lbl">Classifica Generale</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-group">', unsafe_allow_html=True)
        max_pts = max(standings["Pts"].max(), 1)
        for i, row in standings.iterrows():
            icon  = RANK_ICON.get(i, str(i+1))
            bar   = int((row["Pts"] / max_pts) * 100)
            grad  = GRAD_COLORS[i % len(GRAD_COLORS)]
            grad2 = GRAD_COLORS[(i+1) % len(GRAD_COLORS)]
            wl    = "#34C759" if row["V"] >= row["S"] else "#FF6B60"
            st.markdown(
                f'<div class="grow">'
                f'<div class="rank-icon">{icon}</div>'
                '<div style="flex:1;min-width:0">'
                f'<div class="rname">{row["Giocatore"]}</div>'
                '<div style="display:flex;gap:10px;align-items:center;margin-top:3px;flex-wrap:wrap">'
                f'<span style="font-size:11px;color:{wl};font-weight:700">{row["V"]}V · {row["S"]}S</span>'
                '<span style="font-size:10px;color:rgba(255,255,255,0.2)">·</span>'
                f'<span style="font-size:11px;color:rgba(255,255,255,0.3)">Set {row["Set+"]}/{row["Set-"]}</span>'
                '<span style="font-size:10px;color:rgba(255,255,255,0.2)">·</span>'
                f'<span style="font-size:11px;color:rgba(255,255,255,0.3)">Game {row["Game+"]}/{row["Game-"]}</span>'
                '</div>'
                f'<div class="prog-bar" style="margin-top:6px">'
                f'<div class="prog-fill" style="width:{bar}%;background:{grad}"></div></div>'
                '</div>'
                '<div style="text-align:right;flex-shrink:0;margin-left:12px">'
                f'<div class="rpts" style="background:linear-gradient(135deg,{grad},{grad2});'
                f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">'
                f'{row["Pts"]}</div>'
                '<div class="rpts-lbl">punti</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-lbl">Distribuzione Punti</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for i, (_, row) in enumerate(standings.iterrows()):
            fig.add_trace(go.Bar(
                x=[row["Giocatore"]], y=[row["Pts"]],
                marker=dict(color=GRAD_COLORS[i % len(GRAD_COLORS)], cornerradius=8, opacity=0.85),
                text=[row["Pts"]], textposition="outside",
                textfont=dict(color="rgba(255,255,255,0.5)", size=12),
                showlegend=False,
            ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="-apple-system, sans-serif", color="rgba(255,255,255,0.4)", size=12),
            height=250, showlegend=False, barmode="group",
            xaxis=dict(showgrid=False, zeroline=False, showline=False, tickfont=dict(color="rgba(255,255,255,0.5)", size=12)),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False, showline=False),
            margin=dict(t=16, b=8, l=8, r=8),
        )
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════
# TAB 2 — RISULTATI
# ══════════════════════════════════════════════════════
with tab2:
    if len(played_df) == 0:
        st.markdown('<div style="padding:32px 20px;text-align:center"><p>Nessuna partita giocata ancora</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sec-lbl">Partite Giocate</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-group">', unsafe_allow_html=True)
        for _, r in played_df.sort_values("match_id", ascending=False).iterrows():
            p1, p2, w = r["player1"], r["player2"], clean(r["vincitore"])
            c1 = "w" if w == p1 else "l"
            c2 = "w" if w == p2 else "l"
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
                '</div>'
                f'<span class="pill pg">✓ {w}</span>'
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
        st.markdown('<div class="sec-lbl">Da Giocare</div>', unsafe_allow_html=True)
        if len(pending_df) == 0:
            st.markdown('<div class="glass-group"><div class="grow" style="justify-content:center"><span class="pill pg">🎉 Tutto completato!</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-group">', unsafe_allow_html=True)
            for _, r in pending_df.sort_values("match_id").iterrows():
                st.markdown(
                    f'<div class="grow">'
                    f'<div class="mbadge">M{int(r["match_id"]):02d}</div>'
                    '<div class="mcenter">'
                    '<div class="mnames">'
                    f'<span>{r["player1"]}</span><span class="vs">vs</span><span>{r["player2"]}</span>'
                    '</div>'
                    f'<div class="msub">{clean(r.get("data",""))} · {clean(r.get("orario",""))}</div>'
                    '</div>'
                    '<span class="pill pn">⏳</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

    with col_full:
        st.markdown('<div class="sec-lbl">Calendario Completo</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-group">', unsafe_allow_html=True)
        for _, r in df.sort_values("match_id").iterrows():
            done = clean(r.get("vincitore","")) != ""
            p1c  = "w" if done and clean(r["vincitore"]) == r["player1"] else ("l" if done else "")
            p2c  = "w" if done and clean(r["vincitore"]) == r["player2"] else ("l" if done else "")
            right = f'<span class="pill pg">✓ {clean(r["vincitore"])}</span>' if done else '<span class="pill pn">⏳</span>'
            score = fmt_sets(r) if done else f'{clean(r.get("data",""))} · {clean(r.get("orario",""))}'
            st.markdown(
                f'<div class="grow" style="opacity:{"1" if done else "0.5"}">'
                f'<div class="mbadge">M{int(r["match_id"]):02d}</div>'
                '<div class="mcenter">'
                '<div class="mnames">'
                f'<span class="{p1c}">{r["player1"]}</span>'
                '<span class="vs">vs</span>'
                f'<span class="{p2c}">{r["player2"]}</span>'
                '</div>'
                f'<div class="msub">{score}</div>'
                '</div>'
                + right +
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 4 — STATISTICHE
# ══════════════════════════════════════════════════════
with tab4:
    if len(played_df) == 0:
        st.markdown('<div style="padding:32px 20px;text-align:center"><p>Inserisci i risultati nel CSV per vedere le statistiche</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sec-lbl">Seleziona Giocatore</div>', unsafe_allow_html=True)
        sel = st.selectbox("", players_list, label_visibility="collapsed")

        p_all    = df[(df["player1"] == sel) | (df["player2"] == sel)]
        p_played = p_all[p_all["vincitore"].apply(clean) != ""]
        p_wins   = p_played[p_played["vincitore"].apply(clean) == sel]
        p_losses = p_played[p_played["vincitore"].apply(clean) != sel]
        wr       = f"{int(len(p_wins)/len(p_played)*100)}%" if len(p_played) else "—"
        prow     = standings[standings["Giocatore"] == sel].iloc[0] if sel in standings["Giocatore"].values else None

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Partite",    len(p_played))
        c2.metric("Win Rate",   wr)
        c3.metric("Game Vinti", int(prow["Game+"]) if prow is not None else 0)
        c4.metric("Game Persi", int(prow["Game-"]) if prow is not None else 0)

        if len(p_played):
            col_pie, col_list = st.columns([1, 2])

            with col_pie:
                st.markdown('<div class="sec-lbl">Record</div>', unsafe_allow_html=True)
                fig_p = go.Figure(go.Pie(
                    labels=["Vittorie","Sconfitte"],
                    values=[len(p_wins), max(len(p_losses),0)],
                    marker=dict(colors=["#63B3ED","rgba(255,255,255,0.08)"],
                                line=dict(color="rgba(0,0,0,0)", width=0)),
                    textfont=dict(color="#F5F5F7"), hole=0.65, textinfo="percent",
                ))
                fig_p.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30,b=8,l=0,r=0), height=180,
                    font=dict(family="-apple-system"), showlegend=False,
                    annotations=[dict(text=wr, x=0.5, y=0.5, font=dict(size=20,color="#63B3ED"), showarrow=False)]
                )
                st.plotly_chart(fig_p, use_container_width=True)

                if prow is not None:
                    sv_tot = int(prow["Set+"]) + int(prow["Set-"])
                    gv_tot = int(prow["Game+"]) + int(prow["Game-"])
                    st.markdown(
                        '<div class="glass-group" style="margin:0 0 12px">'
                        '<div class="grow" style="justify-content:space-between">'
                        '<span style="font-size:12px;color:rgba(255,255,255,0.4);font-weight:600">SET VINTI</span>'
                        f'<span style="font-size:15px;font-weight:700;color:#9F7AEA">{int(prow["Set+"])} / {sv_tot}</span>'
                        '</div>'
                        '<div class="grow" style="justify-content:space-between">'
                        '<span style="font-size:12px;color:rgba(255,255,255,0.4);font-weight:600">GAME VINTI</span>'
                        f'<span style="font-size:15px;font-weight:700;color:#F6AD55">{int(prow["Game+"])} / {gv_tot}</span>'
                        '</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

            with col_list:
                st.markdown('<div class="sec-lbl">Storico Partite</div>', unsafe_allow_html=True)
                st.markdown('<div class="glass-group">', unsafe_allow_html=True)
                for _, r in p_played.sort_values("match_id").iterrows():
                    won  = clean(r["vincitore"]) == sel
                    opp  = r["player2"] if r["player1"] == sel else r["player1"]
                    pill = '<span class="pill pg">✓ Vinta</span>' if won else '<span class="pill pr">✗ Persa</span>'
                    sc   = "w" if won else "l"
                    osc  = "l" if won else "w"
                    st.markdown(
                        f'<div class="grow">'
                        f'<div class="mbadge">M{int(r["match_id"]):02d}</div>'
                        '<div class="mcenter">'
                        '<div class="mnames">'
                        f'<span class="{sc}">{sel}</span>'
                        '<span class="vs">vs</span>'
                        f'<span class="{osc}">{opp}</span>'
                        '</div>'
                        f'<div class="msub">{fmt_sets(r)}</div>'
                        '</div>'
                        + pill +
                        '</div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
        #-AA-

        st.markdown('<div class="sec-lbl">Tutti i Giocatori</div>', unsafe_allow_html=True)
        st.dataframe(
            standings.assign(Pos=range(1, len(standings)+1)).set_index("Pos"),
            use_container_width=True
        )


# ══════════════════════════════════════════════════════
# TAB 5 — FINALI & HEAD TO HEAD
# ══════════════════════════════════════════════════════
with tab5:
    # --- SEZIONE 1: TABELLONE FINALE ---
    st.markdown('<div class="sec-lbl">Incroci Fase Finale (Provvisorio)</div>', unsafe_allow_html=True)

    if len(standings) < 4:
        st.info("La classifica deve contenere almeno 4 giocatori per generare le semifinali.")
    else:
        # Recuperiamo i primi 4
        top_4 = standings.head(4).copy()
        p1 = top_4.iloc[0]["Giocatore"]
        p2 = top_4.iloc[1]["Giocatore"]
        p3 = top_4.iloc[2]["Giocatore"]
        p4 = top_4.iloc[3]["Giocatore"]

        col_sf1, col_sf2 = st.columns(2)

        with col_sf1:
            st.markdown(f"""
            <div class="glass-group">
                <div style="padding:10px; text-align:center; font-size:10px; color:#FFD60A; font-weight:700; letter-spacing:1px">SEMI-FINALE A</div>
                <div class="grow">
                    <div class="mcenter">
                        <div class="mnames"><span>🥇 {p1}</span> <span class="vs">vs</span> <span>🥉 {p3}</span></div>
                        <div class="msub">1° Classificato vs 3° Classificato</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_sf2:
            st.markdown(f"""
            <div class="glass-group">
                <div style="padding:10px; text-align:center; font-size:10px; color:#FFD60A; font-weight:700; letter-spacing:1px">SEMI-FINALE B</div>
                <div class="grow">
                    <div class="mcenter">
                        <div class="mnames"><span>🥈 {p2}</span> <span class="vs">vs</span> <span>🏅 {p4}</span></div>
                        <div class="msub">2° Classificato vs 4° Classificato</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SEZIONE 2: HEAD TO HEAD ---
    st.markdown('<div class="sec-lbl">Confronto Storico (Head to Head)</div>', unsafe_allow_html=True)

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        h2h_p1 = st.selectbox("Seleziona Giocatore 1", players_list, key="h2h1", label_visibility="collapsed")
    with col_sel2:
        opts2 = [p for p in players_list if p != h2h_p1]
        h2h_p2 = st.selectbox("Seleziona Giocatore 2", opts2, key="h2h2", label_visibility="collapsed")

    # Filtriamo le partite tra i due
    h2h_all = df[((df["player1"] == h2h_p1) & (df["player2"] == h2h_p2)) |
                 ((df["player1"] == h2h_p2) & (df["player2"] == h2h_p1))]

    h2h_played = h2h_all[h2h_all["vincitore"].apply(clean) != ""]
    wins1 = len(h2h_played[h2h_played["vincitore"] == h2h_p1])
    wins2 = len(h2h_played[h2h_played["vincitore"] == h2h_p2])

    # Scoreboard H2H (Stile personalizzato)
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius:16px; padding:24px; text-align:center; margin:16px 16px 24px">
        <div style="display:flex; justify-content:center; align-items:center; gap:40px">
            <div>
                <div style="font-size:3rem; font-weight:900; color:{'#63B3ED' if wins1 >= wins2 else 'rgba(255,255,255,0.2)'}">{wins1}</div>
                <div style="font-size:1rem; font-weight:700; color:#F5F5F7; text-transform:uppercase">{h2h_p1}</div>
            </div>
            <div style="font-size:1.2rem; color:rgba(255,255,255,0.1); font-weight:800">VS</div>
            <div>
                <div style="font-size:3rem; font-weight:900; color:{'#63B3ED' if wins2 > wins1 else 'rgba(255,255,255,0.2)'}">{wins2}</div>
                <div style="font-size:1rem; font-weight:700; color:#F5F5F7; text-transform:uppercase">{h2h_p2}</div>
            </div>
        </div>
        <div style="font-size:10px; color:rgba(255,255,255,0.3); margin-top:16px; letter-spacing:2px; font-weight:600">
            {len(h2h_played)} DISPUTATE / {len(h2h_all)} TOTALI
        </div>
    </div>
    """, unsafe_allow_html=True)

    if len(h2h_played) > 0:
        st.markdown('<div class="glass-group">', unsafe_allow_html=True)
        for _, row in h2h_played.sort_values("match_id", ascending=False).iterrows():
            st.markdown(f"""
            <div class="grow">
                <div class="mbadge">M{int(row['match_id']):02d}</div>
                <div class="mcenter">
                    <div class="mnames">
                        <span>{row['player1']}</span> <span class="vs">vs</span> <span>{row['player2']}</span>
                    </div>
                    <div class="msub">{fmt_sets(row)}</div>
                </div>
                <span class="pill pg">🏆 {row['vincitore']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif len(h2h_all) > 0:
        st.info("Partita in programma nel Round Robin ma non ancora giocata.")
    else:
        st.warning("Nessuna partita prevista tra questi due giocatori.")