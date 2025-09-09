import pandas as pd

class ComonNordin:
    def __init__(self):
        # Initialisation si nécessaire
        pass

    def coble(self):
        """
        Crée un DataFrame vide avec la structure demandée.
        Colonnes :
        - id_projet
        - type_nordin
        - num_tranche
        - d_nordin_op
        - d_nordin_redevances_ht
        - d_nordin_ttc
        """
        columns = [
            "id_projet",
            "type_nordin",
            "num_tranche",
            "d_nordin_op",
            "d_nordin_redevances_ht",
            "d_nordin_ttc"
        ]
        df = pd.DataFrame(columns=columns)
        return df

# Exemple d'utilisation
if __name__ == "__main__":
    cn = ComonNordin()
    df_nordin = cn.coble()
    print(df_nordin)
