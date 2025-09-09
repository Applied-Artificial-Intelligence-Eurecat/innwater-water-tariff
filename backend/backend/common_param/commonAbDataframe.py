import pandas as pd
from CommoAbsrvinsert import CommoAbsrvinsert
class CommonAbDataframe:
    def __init__(self):
        self.columns = [
            "id_projet",
            "type_abonnement",
            "prix_ht_op",
            "redevances",
            "prix_ht_tva",
            "montant_tva_par_unite_service",
            "prix_ttc"
        ]

    def create_dataframe(self):
        data = [
            [1, "EPA", 34.235, 0, 34.235, 1.94699, 36.18199],
            [2, "A",   15.545, 0, 15.545, 1.55450, 17.09950],
            [3, "EP",  18.690, 0, 18.690, 0.39249, 19.08249]
        ]
        return pd.DataFrame(data, columns=self.columns)


if __name__ == "__main__":
    # Générer le DataFrame
    projet_df = CommonAbDataframe()
    df = projet_df.create_dataframe()
    print("✅ DataFrame généré :")
    print(df)

    # Insérer dans la base
    inserter = CommoAbsrvinsert("database.db")
    inserter.insert_dataframe(df)
    inserter.close()
    print("✅ Insertion terminée dans la table 'commonAb'")
