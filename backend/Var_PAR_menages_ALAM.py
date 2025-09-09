import sqlite3

class Var_PAR_menages_ALAM:
    def __init__(self, database: str, table_name: str, id_projet: int):
        self.database = database
        self.table_name = table_name
        self.id_projet = id_projet

    def mettre_a_jour(self):
        """Met à jour par_ibt et par_tbse pour le projet donné."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        # Mise à jour par_ibt
        cursor.execute(f"""
            UPDATE {self.table_name}
            SET par_ibt = CASE
                WHEN revenunetmois IS NOT NULL AND revenunetmois != 0
                THEN (100.0 * (a_tmin_ibt / 3.0)) / revenunetmois
                ELSE 0
            END
            WHERE id_projet = ?
        """, (self.id_projet,))

        # Mise à jour par_tbse
        cursor.execute(f"""
            UPDATE {self.table_name}
            SET par_tbse = CASE
                WHEN revenunetmois IS NOT NULL AND revenunetmois != 0
                THEN (100.0 * (a_tmin_tbse / 3.0)) / revenunetmois
                ELSE 0
            END
            WHERE id_projet = ?
        """, (self.id_projet,))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Projet {self.id_projet} mis à jour : par_ibt et par_tbse")

# Exemple de main
def main():
    projet = Var_PAR_menages_ALAM(
        database="database.db",
        table_name="VarParMenageResult",
        id_projet=1
    )
    projet.mettre_a_jour()

if __name__ == "__main__":
    main()
