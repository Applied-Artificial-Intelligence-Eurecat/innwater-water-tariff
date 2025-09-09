import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

# Importer le modèle depuis l'autre fichier
from common_param.CommonTarifTBSE import CommonTarifTBSEModel # adapte le nom si nécessaire

@dataclass
class CommonTarifTBSEModelDTO:
    """DTO (Data Transfer Object) pour la table CommonTarifTBSEModel"""
    id: Optional[int] = None
    id_projet: Optional[int] = None
    nature_tarif: Optional[str] = None
    type_tarif: Optional[str] = None
    prix_ht_op: Optional[float] = None
    redevances: Optional[float] = None
    prix_ht_tva: Optional[float] = None
    montant_tva_unite_service: Optional[float] = None
    prix_ttc: Optional[float] = None
    
    def validate(self) -> List[str]:
        errors = []
        if self.id_projet is None or self.id_projet <= 0:
            errors.append("id_projet doit être un entier positif")
        if not self.nature_tarif or not self.nature_tarif.strip():
            errors.append("nature_tarif est obligatoire")
        if not self.type_tarif or not self.type_tarif.strip():
            errors.append("type_tarif est obligatoire")
        if self.prix_ht_op is not None and self.prix_ht_op < 0:
            errors.append("prix_ht_op ne peut pas être négatif")
        if self.redevances is not None and self.redevances < 0:
            errors.append("redevances ne peut pas être négatif")
        if self.prix_ht_tva is not None and self.prix_ht_tva < 0:
            errors.append("prix_ht_tva ne peut pas être négatif")
        if self.montant_tva_unite_service is not None and self.montant_tva_unite_service < 0:
            errors.append("montant_tva_unite_service ne peut pas être négatif")
        if self.prix_ttc is not None and self.prix_ttc < 0:
            errors.append("prix_ttc ne peut pas être négatif")
        return errors
    
    def is_valid(self) -> bool:
        return len(self.validate()) == 0

class CommonTarifTBSESrv:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    # --- Méthodes existantes pour CRUD ---
    def add_tarif(self, tarif_dto: CommonTarifTBSEModelDTO) -> int:
        errors = tarif_dto.validate()
        if errors:
            raise ValueError(f"Données invalides: {', '.join(errors)}")
        query = """
        INSERT INTO CommonTarifTBSEModel 
        (id_projet, nature_tarif, type_tarif, prix_ht_op, redevances, 
         prix_ht_tva, montant_tva_unite_service, prix_ttc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            tarif_dto.id_projet,
            tarif_dto.nature_tarif,
            tarif_dto.type_tarif,
            tarif_dto.prix_ht_op or 0,
            tarif_dto.redevances or 0,
            tarif_dto.prix_ht_tva or 0,
            tarif_dto.montant_tva_unite_service or 0,
            tarif_dto.prix_ttc or 0
        )
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    
    # --- Nouvelle méthode pour persister le DataFrame par défaut ---
    def persist_default_dataframe(self, id_projet_default=1) -> List[int]:
        df = CommonTarifTBSEModel.create_default_dataframe(id_projet_default)
        inserted_ids = []
        for _, row in df.iterrows():
            dto = CommonTarifTBSEModelDTO(
                id_projet=row["id_projet"],
                nature_tarif=row["nature_tarif"],
                type_tarif=row["type_tarif"],
                prix_ht_op=row["prix_ht_op"],
                redevances=row["redevances"],
                prix_ht_tva=row["prix_ht_tva"],
                montant_tva_unite_service=row["montant_tva_unite_service"],
                prix_ttc=row["prix_ttc"]
            )
            inserted_id = self.add_tarif(dto)
            inserted_ids.append(inserted_id)
        return inserted_ids

# --- Main ---
if __name__ == "__main__":
    service = CommonTarifTBSESrv("database.db")
    try:
        # Persister le DataFrame par défaut avec id_projet = 1
        inserted_ids = service.persist_default_dataframe(id_projet_default=1)
        print(f"Tarifs insérés avec les IDs : {inserted_ids}")
    except sqlite3.OperationalError as e:
        print(f"Erreur de base de données : {e}")
        print("Vérifiez que la table CommonTarifTBSEModel existe dans database.db")
    except Exception as e:
        print(f"Erreur générale : {e}")
