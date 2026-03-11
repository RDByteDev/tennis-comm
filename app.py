"""
app.py — Tennis Challenge moderne e accattivante
Avvia con:  streamlit run app.py
"""

import streamlit as st
from data import load_csv, clean, compute_standings
from theme import apply_theme, COLORS
import components.classifica  as pg_classifica
import components.risultati   as pg_risultati
import components.calendario  as pg_calendario
import components.statistiche as pg_statistiche
import components.finali      as pg_finali

# ── Theme ─────────────────────────────────────────────────────────────────────
apply_theme()

# ── Dati ──────────────────────────────────────────────────────────────────────
df           = load_csv()
played_df    = df[df["vincitore"].apply(clean) != ""]
pending_df   = df[df["vincitore"].apply(clean) == ""]
standings    = compute_standings(df)
players_list = sorted(set(df["player1"].tolist() + df["player2"].tolist()))
pct          = int(len(played_df) / len(df) * 100) if len(df) else 0
leader       = standings.iloc[0] if len(standings) and not played_df.empty else None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Hero
    st.markdown("# 🎾 Tennis Challenge")
    st.markdown("**Prima Edizione — 2026**")
    st.divider()

    # Statistiche principali
    st.markdown("### 📊 Torneo")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Giocate", len(played_df), delta=f"+{len(played_df)}")
    with col2:
        st.metric("Rimanenti", len(pending_df))

    st.progress(pct / 100)
    st.caption(f"**{pct}%** del torneo completato")

    # Leader
    if leader is not None:
        st.divider()
        st.markdown("### 👑 Leader")
        st.markdown(f"**{leader['Giocatore']}**")

        col_pts, col_w = st.columns(2)
        with col_pts:
            st.metric("Punti", leader['Pts'])
        with col_w:
            st.metric("Record", f"{leader['V']}–{leader['S']}")

    st.divider()

    # Navigazione
    st.markdown("### 🗂️ Sezioni")
    nav = st.radio(
        "Seleziona",
        ["Classifica", "Risultati", "Calendario", "Statistiche", "Finali"],
        label_visibility="collapsed",
    )

    st.divider()
    col_ref, col_upd = st.columns(2)
    with col_ref:
        if st.button("🔄 Refresh", use_container_width=True):
            load_csv.clear()
            st.rerun()
    with col_upd:
        st.button("⚙️ Info", use_container_width=True)

# ── Routing ───────────────────────────────────────────────────────────────────
if nav == "Classifica":
    pg_classifica.render(standings, len(played_df))

elif nav == "Risultati":
    pg_risultati.render(played_df)

elif nav == "Calendario":
    pg_calendario.render(pending_df)

elif nav == "Statistiche":
    pg_statistiche.render(df, played_df, standings, players_list)

elif nav == "Finali":
    pg_finali.render(df, standings, players_list)