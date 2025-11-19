from typing import List
from pydantic import BaseModel
import pandas as pd



class ServicePayload(BaseModel):
    """
    Classe pour extraire et normaliser les données tarifaires IBT4 depuis un SimulationPayload.
    
    Mappage des attributs basés sur les références Excel:
    - description_tarif_ibt4_c2 : Description Tarif IBT4'!$C$2
    - couts_service_ep_epa_c11 : Couts du Service EP EPA'!$C$11
    - description_tarif_ibt4_d2 : Description Tarif IBT4'!D2
    - couts_service_ep_epa_d11 : Couts du Service EP EPA'!D11
    - description_tarif_ibt4_f2 : Description Tarif IBT4'!$F$2
    - couts_service_ep_epa_f11 : Couts du Service EP EPA'!$F$11
    """
    
    # Colonne C - Tarification Eau Potable (EP)
    description_tarif_ibt4_c2: float  # Abonnement EP
    couts_service_ep_epa_c11: float  # Coût fixe EP
    
    # Colonne D - Tarification Assainissement
    description_tarif_ibt4_d2: float  # Abonnement Assainissement
    couts_service_ep_epa_d11: float  # Coût fixe Assainissement
    
    # Colonne F - Tarification EPA (Eau Potable + Assainissement)
    description_tarif_ibt4_f2: float  # Abonnement EPA
    couts_service_ep_epa_f11: float  # Coût fixe EPA
    
    # Informations complémentaires sur les paliers
    paliers_ep: List[dict]  # Paliers de consommation EP
    paliers_assainissement: List[dict]  # Paliers de consommation Assainissement
    paliers_epa: List[dict]  # Paliers de consommation EPA
    
    @classmethod
    def from_simulation_payload(cls, payload: 'SimulationPayload') -> 'ServicePayload':
        """
        Crée une instance de ServicePayload à partir d'un SimulationPayload.
        
        Args:
            payload: Instance de SimulationPayload contenant les données de simulation
            
        Returns:
            Instance de TarifIBT4 avec les attributs normalisés
        """
        # Extraction des paliers EP
        paliers_ep = [
            {
                "seuil": tier.threshold,
                "prix_ht": tier.price,
                "prix_ttc": payload.potable_water_prix_tiers_ttc[i]
            }
            for i, tier in enumerate(payload.tariff.drinking_water.usage_tiers)
        ]
        
        # Extraction des paliers Assainissement
        paliers_assainissement = [
            {
                "seuil": tier.threshold,
                "prix_ht": tier.price,
                "prix_ttc": payload.sanitation_prix_tiers_ttc[i]
            }
            for i, tier in enumerate(payload.tariff.sanitation.usage_tiers)
        ]
        
        # Extraction des paliers EPA
        paliers_epa = [
            {
                "seuil": tier.threshold,
                "prix_ht": tier.price,
                "prix_ttc": payload.epa_prix_tiers_ttc[i]
            }
            for i, tier in enumerate(payload.tariff.epa().usage_tiers)
        ]
        
        return cls(
            # Colonne C - EP
            description_tarif_ibt4_c2=payload.tariff.drinking_water.subscription,
            couts_service_ep_epa_c11=payload.primitives.drinking_water.fixed_costs,
            
            # Colonne D - Assainissement
            description_tarif_ibt4_d2=payload.tariff.sanitation.subscription,
            couts_service_ep_epa_d11=payload.primitives.sanitation.fixed_costs,
            
            # Colonne F - EPA
            description_tarif_ibt4_f2=payload.tariff.epa().subscription,
            couts_service_ep_epa_f11=payload.primitives.epa().fixed_costs,
            
            # Paliers
            paliers_ep=paliers_ep,
            paliers_assainissement=paliers_assainissement,
            paliers_epa=paliers_epa
        )
    
    def get_prix_base_ttc_ep(self, payload: 'SimulationPayload') -> float:
        """Retourne le prix de base TTC pour l'eau potable."""
        return payload.potable_water_prix_base_ttc
    
    def get_prix_base_ttc_assainissement(self, payload: 'SimulationPayload') -> float:
        """Retourne le prix de base TTC pour l'assainissement."""
        return payload.sanitation_prix_base_ttc
    
    def get_prix_base_ttc_epa(self, payload: 'SimulationPayload') -> float:
        """Retourne le prix de base TTC pour EPA."""
        return payload.epa_prix_base_ttc
    
    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire avec des clés lisibles.
        
        Returns:
            Dictionnaire contenant toutes les données tarifaires
        """
        return {
            "eau_potable": {
                "abonnement": self.description_tarif_ibt4_c2,
                "couts_fixes": self.couts_service_ep_epa_c11,
                "paliers": self.paliers_ep
            },
            "assainissement": {
                "abonnement": self.description_tarif_ibt4_d2,
                "couts_fixes": self.couts_service_ep_epa_d11,
                "paliers": self.paliers_assainissement
            },
            "epa": {
                "abonnement": self.description_tarif_ibt4_f2,
                "couts_fixes": self.couts_service_ep_epa_f11,
                "paliers": self.paliers_epa
            }
        }
    
    def __repr__(self) -> str:
        """Représentation textuelle de l'objet."""
        return (
            f"ServicePayload(\n"
            f"  EP: abonnement={self.description_tarif_ibt4_c2}€, "
            f"coûts_fixes={self.couts_service_ep_epa_c11}€\n"
            f"  Assainissement: abonnement={self.description_tarif_ibt4_d2}€, "
            f"coûts_fixes={self.couts_service_ep_epa_d11}€\n"
            f"  EPA: abonnement={self.description_tarif_ibt4_f2}€, "
            f"coûts_fixes={self.couts_service_ep_epa_f11}€\n"
            f")"
        )


# Exemple d'utilisation
if __name__ == "__main__":
    pass
    
    # Créer ou charger un payload de simulation
    # payload = SimulationPayload(...)
    
    # Créer une instance de ServicePayload
    # service_payload = ServicePayload.from_simulation_payload(payload)
    
    # Afficher les données
    # print(service_payload)
    # print("\nDictionnaire:", service_payload.to_dict())
    
    # Accéder aux attributs normalisés
    # print(f"\nAbonnement EP: {service_payload.description_tarif_ibt4_c2}€")
    # print(f"Coûts fixes EP: {service_payload.couts_service_ep_epa_c11}€")