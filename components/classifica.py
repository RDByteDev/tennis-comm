import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import GRAD_COLORS


def render(standings: pd.DataFrame, played_count: int) -> None:
    st.markdown("# 🏆 Classifica")
    st.caption("Posizionamento attuale basato su punti, set e game")

    if played_count == 0:
        st.info("🤔 Nessun risultato ancora — aggiorna il CSV per iniziare!")
        return

    st.divider()

    # ── Tabella classifica ────────────────────────────────────────────────────
    max_pts = max(standings["Pts"].max(), 1)

    for i, row in standings.iterrows():
        medal = ["🥇", "🥈", "🥉"] + ["🏅"] * (len(standings) - 3)
        pos_icon = medal[i] if i < len(medal) else f"{i+1}."

        with st.container(border=True):
            col_pos, col_name, col_stats, col_chart = st.columns([0.8, 2.5, 2.5, 2])

            with col_pos:
                st.markdown(f"## {pos_icon}")
                st.caption(f"#{i+1}")

            with col_name:
                st.markdown(f"### {row['Giocatore']}")
                progress = row["Pts"] / max_pts
                st.progress(progress)
                st.caption(f"**{row['Pts']}** punti")

            with col_stats:
                # Record
                wins_color = "🟢" if row["V"] >= row["S"] else "🔴"
                st.write(f"{wins_color} **{row['V']}–{row['S']}** record")

                # Set ratio
                total_set = row['Set+'] + row['Set-']
                st.caption(f"📊 Set: {row['Set+']}–{row['Set-']}")

                # Game ratio
                total_game = row['Game+'] + row['Game-']
                st.caption(f"🎾 Game: {row['Game+']}–{row['Game-']}")

            with col_chart:
                # Mini card metriche
                st.metric("Vittorie", f"{row['V']}")
                st.metric("Sconfitte", f"{row['S']}")

    # ── Grafico principale ────────────────────────────────────────────────────
    st.divider()
    st.markdown("## 📈 Distribuzione Punti")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=standings["Giocatore"],
        y=standings["Pts"],
        marker=dict(
            color=GRAD_COLORS[:len(standings)],
            line=dict(color="rgba(15, 23, 42, 0.2)", width=1),
            cornerradius=8,
        ),
        text=standings["Pts"],
        textposition="outside",
        textfont=dict(size=12, color="#0F172A"),
        hovertemplate="<b>%{x}</b><br>Punti: %{y}<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=350,
        margin=dict(t=30, b=30, l=30, r=30),
        xaxis=dict(
            showgrid=False,
            color="#64748B",
            showline=True,
            linewidth=1,
            linecolor="rgba(15, 23, 42, 0.1)",
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(15, 23, 42, 0.05)",
            color="#64748B",
            showline=True,
            linewidth=1,
            linecolor="rgba(15, 23, 42, 0.1)",
        ),
        font=dict(size=12, color="#0F172A", family="Outfit"),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Stats supplementari ───────────────────────────────────────────────────
    st.divider()
    st.markdown("## 📊 Statistiche Globali")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Giocatori", len(standings))
    with col2:
        st.metric("Leader", standings.iloc[0]["Giocatore"] if len(standings) > 0 else "—")
    with col3:
        avg_pts = standings["Pts"].mean()
        st.metric("Media Punti", f"{avg_pts:.1f}")
    with col4:
        max_diff = standings.iloc[0]["Pts"] - standings.iloc[-1]["Pts"]
        st.metric("Differenza", f"+{max_diff}")

