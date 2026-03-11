import streamlit as st
import pandas as pd
from data import clean, fmt_sets


def render(played_df: pd.DataFrame) -> None:
    st.markdown("# 🎾 Risultati")
    st.caption("Elenco di tutte le partite giocate")

    if played_df.empty:
        st.info("📭 Nessuna partita giocata ancora. Torna presto!")
        return

    st.divider()

    # ── Header con statistiche ────────────────────────────────────────────────
    col_tot, col_stats = st.columns([2, 1])
    with col_tot:
        st.markdown(f"## Totale: **{len(played_df)} partite** disputate")
    with col_stats:
        st.caption(f"Ultimi risultati in basso")

    st.divider()

    # ── Risultati ─────────────────────────────────────────────────────────────
    for idx, (_, r) in enumerate(played_df.sort_values("match_id", ascending=False).iterrows()):
        p1, p2, w = r["player1"], r["player2"], clean(r["vincitore"])
        score = fmt_sets(r)

        # Determina il vincitore
        is_p1_winner = w == p1

        with st.container(border=True):
            col_id, col_match, col_vs, col_score = st.columns([0.7, 1.8, 0.5, 1.5])

            with col_id:
                st.markdown(f"**M{int(r['match_id']):02d}**")
                st.caption("Match")

            with col_match:
                # Primo giocatore
                if is_p1_winner:
                    st.markdown(f"### 🟢 {p1}")
                else:
                    st.markdown(f"### {p1}")

                # Secondo giocatore
                if not is_p1_winner:
                    st.markdown(f"### 🟢 {p2}")
                else:
                    st.markdown(f"### {p2}")

            with col_vs:
                st.markdown("")
                st.markdown("**vs**")

            with col_score:
                st.markdown(f"## {score if score else '—'}")
                if is_p1_winner:
                    st.caption(f"✅ {p1} vince")
                else:
                    st.caption(f"✅ {p2} vince")

        # Separatore tra partite
        if idx < len(played_df) - 1:
            st.divider()
