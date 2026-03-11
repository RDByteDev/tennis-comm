import pandas as pd
import os

# Leggi il CSV delle partite generate
df_matches = pd.read_csv("calendario.csv")

# Valori di default che puoi modificare
default_data = "01/01/1900"
default_orario = "00:00"
default_luogo = "Nusco Stadium"
default_set1 = ""
default_set2 = ""
default_set3 = ""
default_vincitore = ""
default_superficie = "Cemento"

def crea_csv_partite(df, output_folder="."):
    # Assicurati che la cartella output esista
    os.makedirs(output_folder, exist_ok=True)

    # Aggiungi colonne con valori di default
    df_out = df.copy()
    df_out["Data"] = default_data
    df_out["Orario"] = default_orario
    df_out["Luogo"] = default_luogo
    df_out["Set 1"] = default_set1
    df_out["Set 2"] = default_set2
    df_out["Set 3"] = default_set3
    df_out["Vincitore"] = default_vincitore
    df_out["Superficie"] = default_superficie

    # Seleziona colonne nell'ordine richiesto
    df_out = df_out[["MatchID", "Data", "Orario", "Luogo", "Player 1", "Player 2",
                     "Set 1", "Set 2", "Set 3", "Vincitore", "Superficie"]]

    # Salva CSV nel path corretto
    output_path = os.path.join(output_folder, "partite.csv")
    df_out.to_csv(output_path, index=False)
    print(f"CSV generato: {output_path}")

# Esegui la funzione
crea_csv_partite(df_matches)
