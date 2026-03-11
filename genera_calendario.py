
import pandas as pd

def round_robin_schedule(players):
    """
    Genera un calendario round-robin per i match (senza turni/giornate).
    """
    if len(players) % 2 != 0:
        players.append("BYE")

    n = len(players)
    half = n // 2
    schedule = []
    match_id = 1

    rotation = players[1:]
    for _ in range(n - 1):
        left = players[0]
        right = rotation[-1]
        pairs = [(left, right)]

        for i in range(half - 1):
            pairs.append((rotation[i], rotation[-i - 2]))

        for p1, p2 in pairs:
            if p1 != "BYE" and p2 != "BYE":
                schedule.append({
                    "MatchID": match_id,
                    "Player 1": p1,
                    "Player 2": p2
                })
                match_id += 1

        rotation = [rotation[-1]] + rotation[:-1]

    return pd.DataFrame(schedule)

# Carica giocatori
df_players = pd.read_csv("players.csv")
players = df_players["Nome"].tolist()

df_matches = round_robin_schedule(players)

df_matches.to_csv("calendario.csv", index=False)
print("Calendario round-robin salvato in output/calendario.csv")