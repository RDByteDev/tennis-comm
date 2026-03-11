import streamlit as st
import pandas as pd
from config import CSV_PATH, CSV_TTL, CSV_RENAME, PTS_WIN_2_0, PTS_WIN_2_1, PTS_LOSS_1_2


@st.cache_data(ttl=CSV_TTL)
def load_csv() -> pd.DataFrame:
    if not CSV_PATH.exists():
        st.error(f"File non trovato: `{CSV_PATH.resolve()}`  \nMetti `partite.csv` nella cartella dell'app.")
        st.stop()
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
    df = df.rename(columns=CSV_RENAME)
    df["match_id"] = pd.to_numeric(df["match_id"], errors="coerce")
    return df


def clean(v) -> str:
    return "" if str(v).strip() in {"nan", "None", ""} else str(v).strip()


def parse_set(s: str):
    try:
        a, b = str(s).strip().split("-")
        return int(a), int(b)
    except Exception:
        return None


def fmt_sets(row: pd.Series) -> str:
    parts = [clean(row[c]) for c in ("set1", "set2", "set3") if clean(row.get(c, ""))]
    return "  ·  ".join(parts)


def compute_standings(df: pd.DataFrame) -> pd.DataFrame:
    players = sorted(set(df["player1"].tolist() + df["player2"].tolist()))
    acc = {p: dict(PG=0, V=0, S=0, SV=0, SS=0, GV=0, GS=0) for p in players}
    played = df[df["vincitore"].apply(clean) != ""]

    for _, r in played.iterrows():
        w, p1, p2 = clean(r["vincitore"]), r["player1"], r["player2"]
        loser = p2 if w == p1 else p1
        acc[w]["V"]  += 1; acc[w]["PG"] += 1
        acc[loser]["S"] += 1; acc[loser]["PG"] += 1
        for col in ("set1", "set2", "set3"):
            ps = parse_set(clean(r.get(col, "")))
            if not ps:
                continue
            a, b = ps
            if a > b:   acc[p1]["SV"] += 1; acc[p2]["SS"] += 1
            elif b > a: acc[p2]["SV"] += 1; acc[p1]["SS"] += 1
            acc[p1]["GV"] += a; acc[p1]["GS"] += b
            acc[p2]["GV"] += b; acc[p2]["GS"] += a

    rows = []
    for p, v in acc.items():
        pm = df[((df["player1"]==p)|(df["player2"]==p)) & (df["vincitore"].apply(clean)!="")]
        pts = 0
        for _, r in pm.iterrows():
            p1, p2 = r["player1"], r["player2"]
            sp = [parse_set(clean(r.get(c,""))) for c in ("set1","set2","set3")]
            sw = sum(1 for x in sp if x and ((x[0]>x[1] and p==p1) or (x[1]>x[0] and p==p2)))
            sl = sum(1 for x in sp if x and ((x[0]<x[1] and p==p1) or (x[1]<x[0] and p==p2)))
            if p == clean(r["vincitore"]):
                pts += PTS_WIN_2_0 if sl == 0 else PTS_WIN_2_1
            elif sw == 1:
                pts += PTS_LOSS_1_2
        rows.append({"Giocatore": p, "PG": v["PG"], "V": v["V"], "S": v["S"],
                     "Pts": pts, "Set+": v["SV"], "Set-": v["SS"],
                     "Game+": v["GV"], "Game-": v["GS"]})

    return (pd.DataFrame(rows)
            .sort_values(["Pts","V","Set+","Game+"], ascending=False)
            .reset_index(drop=True))
