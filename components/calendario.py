import streamlit as st
import pandas as pd
from data import clean


def render(pending_df: pd.DataFrame) -> None:
    st.markdown("# 📅 Partite da Giocare")
    st.caption("Prossimi incontri in programma")

    if pending_df.empty:
        st.success("🎉 **Incredibile!** Tutte le partite sono state giocate!")
        st.balloons()
        return

    st.divider()

    # ── Statistiche ───────────────────────────────────────────────────────────
    col_tot, col_prog = st.columns([2, 1])
    with col_tot:
        st.markdown(f"## **{len(pending_df)} partite** in programma")
    with col_prog:
        st.caption("Da giocare")

    st.divider()

    # ── Timeline ──────────────────────────────────────────────────────────────
    for idx, (_, r) in enumerate(pending_df.sort_values("match_id").iterrows()):
        d = clean(r.get("data", ""))
        o = clean(r.get("orario", ""))

        # Determina lo stato
        if d in {"01/01/1900", ""} and o in {"00:00", ""}:
            date_str = "⏳ Da definire"
            status_color = "🟡"
        else:
            date_str = f"📍 {d} • {o}"
            status_color = "🟢"

        with st.container(border=True):
            col_id, col_players, col_date, col_status = st.columns([0.7, 2.5, 1.8, 0.8])

            with col_id:
                st.markdown(f"**M{int(r['match_id']):02d}**")
                st.caption("Match")

            with col_players:
                st.markdown(f"### {r['player1']}")
                st.markdown(f"*vs*")
                st.markdown(f"### {r['player2']}")

            with col_date:
                st.markdown(f"### {date_str}")

            with col_status:
                st.markdown(f"## {status_color}")
                if d not in {"01/01/1900", ""} or o not in {"00:00", ""}:
                    st.caption("📋 Programmata")
                else:
                    st.caption("📝 In sospeso")

        if idx < len(pending_df) - 1:
            st.divider()
