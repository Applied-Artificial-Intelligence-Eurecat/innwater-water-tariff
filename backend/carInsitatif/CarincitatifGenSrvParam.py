from typing import Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class CarincitatifGenSrvParam:
    """
    Classe de paramètres pour le service CarincitatifGenSrv
    Encapsule tous les paramètres configurables du service de statistiques
    """
    
    # Paramètres de base de données
    db_path: str = "database.db"
    table_name: str = "carInsitatifdataintermed"
    
    # Paramètres de colonnes
    column_name: str = "water_consumption_ibt"
    project_id_column: str = "id_projet"
    
    # Paramètres de projet
    default_project_id: int = 1
    
    # Paramètres de calcul des percentiles
    percentiles: Dict[str, float] = field(default_factory=lambda: {
        'percentile_10': 0.1,
        'percentile_25': 0.25,
        'percentile_75': 0.75,
        'percentile_90': 0.9
    })
    
    # Paramètres de précision (nombre de décimales)
    decimal_precision: Dict[str, int] = field(default_factory=lambda: {
        'default': 2,
        'variance': 3,
        'standard_deviation': 3,
        'mae': 3,
        'mape': 3
    })
    
    # Paramètres de connexion à la base de données
    connection_timeout: Optional[int] = None
    isolation_level: Optional[str] = None
    
    # Paramètres de validation
    validate_positive_values: bool = True
    exclude_zero_values_for_mape: bool = True
    
    # Paramètres de requêtes
    use_sample_variance: bool = True  # True pour variance d'échantillon (n-1), False pour population (n)
    
    def __post_init__(self):
        """Validation des paramètres après initialisation"""
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Valide les paramètres fournis"""
        if not isinstance(self.db_path, str) or not self.db_path.strip():
            raise ValueError("db_path doit être une chaîne non vide")
        
        if not isinstance(self.table_name, str) or not self.table_name.strip():
            raise ValueError("table_name doit être une chaîne non vide")
        
        if not isinstance(self.column_name, str) or not self.column_name.strip():
            raise ValueError("column_name doit être une chaîne non vide")
        
        if not isinstance(self.default_project_id, int) or self.default_project_id < 0:
            raise ValueError("default_project_id doit être un entier positif ou nul")
        
        # Validation des percentiles
        for name, value in self.percentiles.items():
            if not (0 <= value <= 1):
                raise ValueError(f"Le percentile {name} doit être entre 0 et 1, reçu: {value}")
        
        # Validation des précisions décimales
        for name, precision in self.decimal_precision.items():
            if not isinstance(precision, int) or precision < 0:
                raise ValueError(f"La précision pour {name} doit être un entier positif ou nul")
    
    def get_percentile_value(self, percentile_name: str) -> float:
        """
        Récupère la valeur d'un percentile spécifique
        
        Args:
            percentile_name (str): Nom du percentile
            
        Returns:
            float: Valeur du percentile
            
        Raises:
            KeyError: Si le percentile n'existe pas
        """
        if percentile_name not in self.percentiles:
            raise KeyError(f"Percentile '{percentile_name}' non trouvé. Disponibles: {list(self.percentiles.keys())}")
        return self.percentiles[percentile_name]
    
    def get_decimal_precision(self, metric_name: str) -> int:
        """
        Récupère la précision décimale pour une métrique donnée
        
        Args:
            metric_name (str): Nom de la métrique
            
        Returns:
            int: Nombre de décimales
        """
        return self.decimal_precision.get(metric_name, self.decimal_precision['default'])
    
    def add_percentile(self, name: str, value: float) -> None:
        """
        Ajoute un nouveau percentile
        
        Args:
            name (str): Nom du percentile
            value (float): Valeur du percentile (entre 0 et 1)
        """
        if not (0 <= value <= 1):
            raise ValueError(f"La valeur du percentile doit être entre 0 et 1, reçu: {value}")
        self.percentiles[name] = value
    
    def remove_percentile(self, name: str) -> None:
        """
        Supprime un percentile
        
        Args:
            name (str): Nom du percentile à supprimer
        """
        if name in self.percentiles:
            del self.percentiles[name]
    
    def set_decimal_precision(self, metric_name: str, precision: int) -> None:
        """
        Définit la précision décimale pour une métrique
        
        Args:
            metric_name (str): Nom de la métrique
            precision (int): Nombre de décimales
        """
        if not isinstance(precision, int) or precision < 0:
            raise ValueError("La précision doit être un entier positif ou nul")
        self.decimal_precision[metric_name] = precision
    
    def update_column_config(self, column_name: str, table_name: Optional[str] = None) -> None:
        """
        Met à jour la configuration des colonnes
        
        Args:
            column_name (str): Nouveau nom de colonne
            table_name (str, optional): Nouveau nom de table
        """
        if not isinstance(column_name, str) or not column_name.strip():
            raise ValueError("column_name doit être une chaîne non vide")
        
        self.column_name = column_name
        if table_name is not None:
            if not isinstance(table_name, str) or not table_name.strip():
                raise ValueError("table_name doit être une chaîne non vide")
            self.table_name = table_name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit les paramètres en dictionnaire
        
        Returns:
            Dict[str, Any]: Dictionnaire contenant tous les paramètres
        """
        return {
            'db_path': self.db_path,
            'table_name': self.table_name,
            'column_name': self.column_name,
            'project_id_column': self.project_id_column,
            'default_project_id': self.default_project_id,
            'percentiles': self.percentiles.copy(),
            'decimal_precision': self.decimal_precision.copy(),
            'connection_timeout': self.connection_timeout,
            'isolation_level': self.isolation_level,
            'validate_positive_values': self.validate_positive_values,
            'exclude_zero_values_for_mape': self.exclude_zero_values_for_mape,
            'use_sample_variance': self.use_sample_variance
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'CarincitatifGenSrvParam':
        """
        Crée une instance à partir d'un dictionnaire
        
        Args:
            config_dict (Dict[str, Any]): Dictionnaire de configuration
            
        Returns:
            CarincitatifGenSrvParam: Instance créée
        """
        return cls(**config_dict)
    
    def copy(self) -> 'CarincitatifGenSrvParam':
        """
        Crée une copie des paramètres
        
        Returns:
            CarincitatifGenSrvParam: Copie des paramètres
        """
        return CarincitatifGenSrvParam.from_dict(self.to_dict())
    
    def __repr__(self) -> str:
        """Représentation string des paramètres"""
        return (f"CarincitatifGenSrvParam("
                f"db_path='{self.db_path}', "
                f"table_name='{self.table_name}', "
                f"column_name='{self.column_name}', "
                f"default_project_id={self.default_project_id})")


# Exemples de configurations prédéfinies
class CarincitatifGenSrvParamPresets:
    """Configurations prédéfinies pour différents cas d'usage"""
    
    @staticmethod
    def water_consumption_ibt() -> CarincitatifGenSrvParam:
        """Configuration pour la consommation d'eau IBT"""
        return CarincitatifGenSrvParam(
            column_name="water_consumption_ibt",
            decimal_precision={
                'default': 2,
                'variance': 3,
                'standard_deviation': 3,
                'mae': 3,
                'mape': 3
            }
        )
    
    @staticmethod
    def water_consumption_ibt_pp() -> CarincitatifGenSrvParam:
        """Configuration pour la consommation d'eau IBT par personne"""
        return CarincitatifGenSrvParam(
            column_name="water_consumption_ibt_pp",
            decimal_precision={
                'default': 3,
                'variance': 4,
                'standard_deviation': 4,
                'mae': 4,
                'mape': 3
            }
        )
    
    @staticmethod
    def high_precision() -> CarincitatifGenSrvParam:
        """Configuration haute précision"""
        return CarincitatifGenSrvParam(
            decimal_precision={
                'default': 4,
                'variance': 6,
                'standard_deviation': 6,
                'mae': 6,
                'mape': 4
            }
        )
    
    @staticmethod
    def extended_percentiles() -> CarincitatifGenSrvParam:
        """Configuration avec percentiles étendus"""
        return CarincitatifGenSrvParam(
            percentiles={
                'percentile_5': 0.05,
                'percentile_10': 0.1,
                'percentile_25': 0.25,
                'percentile_50': 0.5,  # médiane
                'percentile_75': 0.75,
                'percentile_90': 0.9,
                'percentile_95': 0.95,
                'percentile_99': 0.99
            }
        )


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple 1: Configuration par défaut
    print("=== Configuration par défaut ===")
    params_default = CarincitatifGenSrvParam()
    print(params_default)
    print(f"Percentile 75: {params_default.get_percentile_value('percentile_75')}")
    print(f"Précision pour variance: {params_default.get_decimal_precision('variance')}")
    
    print("\n" + "="*60 + "\n")
    
    # Exemple 2: Configuration personnalisée
    print("=== Configuration personnalisée ===")
    params_custom = CarincitatifGenSrvParam(
        db_path="custom_database.db",
        column_name="custom_consumption",
        default_project_id=5,
        decimal_precision={'default': 3, 'variance': 4}
    )
    print(params_custom)
    
    print("\n" + "="*60 + "\n")
    
    # Exemple 3: Utilisation des presets
    print("=== Configurations prédéfinies ===")
    params_ibt = CarincitatifGenSrvParamPresets.water_consumption_ibt()
    print(f"Preset IBT: {params_ibt}")
    
    params_extended = CarincitatifGenSrvParamPresets.extended_percentiles()
    print(f"Percentiles disponibles: {list(params_extended.percentiles.keys())}")
    
    print("\n" + "="*60 + "\n")
    
    # Exemple 4: Modification dynamique
    print("=== Modification dynamique ===")
    params = CarincitatifGenSrvParam()
    params.add_percentile('percentile_99', 0.99)
    params.set_decimal_precision('custom_metric', 5)
    params.update_column_config('new_consumption_column')
    
    print(f"Paramètres modifiés: {params}")
    print(f"Nouveau percentile 99: {params.get_percentile_value('percentile_99')}")
    print(f"Précision custom: {params.get_decimal_precision('custom_metric')}")