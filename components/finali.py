import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data import clean, fmt_sets


def render(df: pd.DataFrame, standings: pd.DataFrame, players_list: list[str]) -> None:
    st.markdown("# ⚔️ Finali & Head to Head")
    st.caption("Tabellone della fase finale e confronti diretti")

    # ── Tabellone ─────────────────────────────────────────────────────────────
    st.markdown("## 🏆 Fase Finale")

    if len(standings) < 4:
        st.warning("⚠️ Servono almeno 4 giocatori in classifica per la fase finale.")
    else:
        p1, p2, p3, p4 = [standings.iloc[i]["Giocatore"] for i in range(4)]

        st.divider()
        col_a, col_vs1, col_b = st.columns([1.5, 0.5, 1.5])

        with col_a:
            with st.container(border=True):
                st.markdown("### 🥇 Semi-finale A")
                st.markdown(f"**{p1}** *(1°)*")
                st.markdown("*vs*")
                st.markdown(f"**{p3}** *(3°)*")
                st.caption("Il vincitore va in Finale")

        with col_vs1:
            st.markdown("")
            st.markdown("**→**")

        with col_b:
            with st.container(border=True):
                st.markdown("### 🥈 Semi-finale B")
                st.markdown(f"**{p2}** *(2°)*")
                st.markdown("*vs*")
                st.markdown(f"**{p4}** *(4°)*")
                st.caption("Il vincitore va in Finale")

    st.divider()

    # ── Head to Head ──────────────────────────────────────────────────────────
    st.markdown("## 🎾 Confronto Diretto")
    st.caption("Seleziona due giocatori per vedere il loro head-to-head")

    col1, col2 = st.columns(2)
    with col1:
        h1 = st.selectbox(
            "Giocatore 1",
            players_list,
            key="h2h_p1",
            label_visibility="collapsed"
        )
    with col2:
        h2 = st.selectbox(
            "Giocatore 2",
            [p for p in players_list if p != h1],
            key="h2h_p2",
            label_visibility="collapsed"
        )

    h2h_all    = df[((df["player1"]==h1)&(df["player2"]==h2)) | ((df["player1"]==h2)&(df["player2"]==h1))]
    h2h_played = h2h_all[h2h_all["vincitore"].apply(clean) != ""]
    w1 = len(h2h_played[h2h_played["vincitore"] == h1])
    w2 = len(h2h_played[h2h_played["vincitore"] == h2])

    st.divider()

    # ── Scoreboard ────────────────────────────────────────────────────────────
    st.markdown("### Risultato H2H")
    c_p1, c_vs, c_p2 = st.columns([1.5, 0.5, 1.5])

    with c_p1:
        with st.container(border=True):
            st.markdown(f"## {h1}")
            st.markdown(f"# {w1}")
            st.caption("vittorie")

    with c_vs:
        st.markdown("")
        st.markdown("# vs")

    with c_p2:
        with st.container(border=True):
            st.markdown(f"## {h2}")
            st.markdown(f"# {w2}")
            st.caption("vittorie")

    st.divider()
    st.caption(f"**{len(h2h_played)} partite disputate** • {len(h2h_all)} totali in programma")

    if h2h_played.empty:
        msg = "📭 Partita in programma ma non ancora giocata." if len(h2h_all) > 0 else "❌ Nessuna partita prevista tra questi due giocatori."
        st.info(msg)
        return

    # ── Grafico H2H ──────────────────────────────────────────────────────────
    st.markdown("### Statistiche H2H")

    fig_h2h = go.Figure()

    fig_h2h.add_trace(go.Bar(
        x=[h1, h2],
        y=[w1, w2],
        marker=dict(
            color=["#3B82F6", "#8B5CF6"],
            line=dict(color="rgba(15, 23, 42, 0.2)", width=1),
            cornerradius=8,
        ),
        text=[w1, w2],
        textposition="outside",
        textfont=dict(size=14, color="#0F172A"),
        hovertemplate="<b>%{x}</b><br>Vittorie: %{y}<extra></extra>",
    ))

    fig_h2h.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=300,
        margin=dict(t=30, b=30, l=30, r=30),
        xaxis=dict(showgrid=False, showline=True, linewidth=1, linecolor="rgba(15, 23, 42, 0.1)"),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(15, 23, 42, 0.05)"),
        font=dict(size=12, color="#0F172A", family="Outfit"),
    )

    st.plotly_chart(fig_h2h, use_container_width=True)

    st.divider()

    # ── Storico partite ──────────────────────────────────────────────────────
    st.markdown("### Storico Partite")

    for idx, (_, r) in enumerate(h2h_played.sort_values("match_id", ascending=False).iterrows()):
        winner = r['vincitore']
        is_h1_winner = winner == h1

        with st.container(border=True):
            col_id, col_match, col_score, col_win = st.columns([0.7, 2, 1.2, 1.2])

            with col_id:
                st.markdown(f"**M{int(r['match_id']):02d}**")
                st.caption("Match")

            with col_match:
                st.markdown(f"{r['player1']} vs {r['player2']}")

            with col_score:
                score = fmt_sets(r)
                st.markdown(f"## {score or '—'}")

            with col_win:
                if is_h1_winner:
                    st.markdown(f"**{h1}** 🟢")
                else:
                    st.markdown(f"**{h2}** 🟢")

        if idx < len(h2h_played) - 1:
            st.divider()
