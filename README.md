# 🎾 Amici del Tennis Challenge

## Avvio

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

Metti `partite.csv` nella stessa cartella di `app.py`.

## Struttura

```
torneo/
├── .streamlit/
│   └── config.toml      # tema dark + colori
├── app.py               # entry point: sidebar + routing
├── config.py            # costanti (colori, punteggi, path)
├── data.py              # caricamento CSV, helpers, calcolo classifica
└── pages/
    ├── classifica.py
    ├── risultati.py
    ├── calendario.py
    ├── statistiche.py
    └── finali.py
```

## Formato `partite.csv`

| MatchID | Player 1 | Player 2 | Set 1 | Set 2 | Set 3 | Vincitore |
|---------|----------|----------|-------|-------|-------|-----------|
| 1       | Mario    | Luigi    | 6-3   | 6-4   |       | Mario     |

Lascia **Vincitore** vuoto per le partite non ancora giocate.

## Punteggio

| Risultato | Vincitore | Perdente |
|-----------|-----------|---------|
| 2-0       | 3 pt      | 0 pt    |
| 2-1       | 2 pt      | 1 pt    |
