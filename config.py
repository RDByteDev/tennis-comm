from pathlib import Path

CSV_PATH  = Path("partite.csv")
CSV_TTL   = 30  # secondi cache

GRAD_COLORS = ["#63B3ED", "#9F7AEA", "#F6AD55", "#FC8181", "#68D391", "#76E4F7"]
RANK_EMOJI  = {0: "🥇", 1: "🥈", 2: "🥉", 3: "🏅"}

CSV_RENAME = {
    "MatchID": "match_id", "Data": "data", "Orario": "orario",
    "Luogo": "luogo", "Player 1": "player1", "Player 2": "player2",
    "Set 1": "set1", "Set 2": "set2", "Set 3": "set3",
    "Vincitore": "vincitore", "Superficie": "superficie",
}

# Punteggio
PTS_WIN_2_0  = 3
PTS_WIN_2_1  = 2
PTS_LOSS_1_2 = 1
