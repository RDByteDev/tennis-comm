import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data import clean, fmt_sets


def render(df: pd.DataFrame, played_df: pd.DataFrame,
           standings: pd.DataFrame, players_list: list[str]) -> None:
    st.markdown("# 📊 Statistiche Giocatore")
    st.caption("Analisi dettagliata delle prestazioni")

    if played_df.empty:
        st.info("📭 Inserisci i risultati nel CSV per vedere le statistiche.")
        return

    st.divider()

    # ── Selezione giocatore ───────────────────────────────────────────────────
    sel = st.selectbox(
        "Seleziona giocatore da analizzare",
        players_list,
        label_visibility="collapsed"
    )

    prow     = standings[standings["Giocatore"] == sel].iloc[0] if sel in standings["Giocatore"].values else None
    p_played = df[((df["player1"]==sel)|(df["player2"]==sel)) & (df["vincitore"].apply(clean)!="")]
    p_wins   = p_played[p_played["vincitore"].apply(clean) == sel]
    win_rate = round(len(p_wins) / len(p_played) * 100) if len(p_played) else 0

    st.divider()

    # ── Metriche principali ───────────────────────────────────────────────────
    st.markdown(f"## {sel}")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Partite", len(p_played), delta="giocate")
    with col2:
        st.metric("Vittorie", len(p_wins), delta=f"{win_rate}%")
    with col3:
        st.metric("Sconfitte", len(p_played) - len(p_wins))
    with col4:
        st.metric("Win %", f"{win_rate}%")
    with col5:
        st.metric("Set +", int(prow["Set+"]) if prow is not None else 0)

    if p_played.empty:
        st.info("Nessuna partita giocata da questo giocatore.")
        return

    st.divider()

    # ── Grafici ───────────────────────────────────────────────────────────────
    col_chart1, col_chart2 = st.columns(2)

    # Donut chart
    with col_chart1:
        st.markdown("### Record")
        losses = len(p_played) - len(p_wins)
        fig_pie = go.Figure(go.Pie(
            labels=["Vittorie", "Sconfitte"],
            values=[len(p_wins), losses],
            hole=0.5,
            marker=dict(
                colors=["#10B981", "#E5E7EB"],
                line=dict(color="#FFFFFF", width=2)
            ),
            textinfo="label+percent",
            textfont=dict(size=12, color="#0F172A"),
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            height=320,
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(size=12, color="#0F172A", family="Outfit"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart set
    with col_chart2:
        st.markdown("### Set e Game")
        if prow is not None:
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name="Set",
                x=["Set", "Game"],
                y=[prow["Set+"], prow["Game+"]],
                marker_color="#3B82F6",
                text=[int(prow["Set+"]), int(prow["Game+"])],
                textposition="outside",
            ))
            fig_bar.add_trace(go.Bar(
                name="Game",
                x=["Set", "Game"],
                y=[prow["Set-"], prow["Game-"]],
                marker_color="#E5E7EB",
                text=[int(prow["Set-"]), int(prow["Game-"])],
                textposition="outside",
            ))
            fig_bar.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                height=320,
                margin=dict(t=20, b=20, l=20, r=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(15, 23, 42, 0.05)"),
                font=dict(size=12, color="#0F172A", family="Outfit"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # ── Storico partite ──────────────────────────────────────────────────────
    st.markdown("### Storico Partite")

    for idx, (_, r) in enumerate(p_played.sort_values("match_id", ascending=False).iterrows()):
        won = clean(r["vincitore"]) == sel
        opp = r["player2"] if r["player1"] == sel else r["player1"]
        score = fmt_sets(r)
        result_icon = "✅ WON" if won else "❌ LOST"

        with st.container(border=True):
            col_match_id, col_opponent, col_score, col_result = st.columns([0.7, 2, 1.5, 1.2])

            with col_match_id:
                st.markdown(f"**M{int(r['match_id']):02d}**")
                st.caption("Match")

            with col_opponent:
                st.markdown(f"### vs {opp}")
                st.caption(f"{sel}")

            with col_score:
                st.markdown(f"## {score or '—'}")

            with col_result:
                result_color = "green" if won else "red"
                st.markdown(f":{result_color}[### {result_icon}]")

        if idx < len(p_played) - 1:
            st.divider()

    st.divider()

    # ── Classifica generale ───────────────────────────────────────────────────
    st.markdown("### Classifica Generale")
    display = standings.copy()
    display.index = range(1, len(display) + 1)
    display.index.name = "Pos"
    st.dataframe(
        display,
        use_container_width=True,
        column_config={
            "Giocatore": st.column_config.TextColumn("Giocatore", width="medium"),
            "Pts": st.column_config.NumberColumn("Punti", format="%d"),
            "V": st.column_config.NumberColumn("Vittorie", format="%d"),
            "S": st.column_config.NumberColumn("Sconfitte", format="%d"),
        }
    )
