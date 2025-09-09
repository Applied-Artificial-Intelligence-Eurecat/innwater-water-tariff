import numpy as np
import pandas as pd
from RootDataService import RootDataService
import logging
from typing import Optional, Dict, List, Union

class DataGenerator:
    """
    Générateur de données avec support pour données réelles et calculs dérivés
    """
    
    def __init__(self, n_rows: int = 1000, db_path: str = "database.db", 
                 default_id_projet: int = 1, id_projet: Optional[int] = None):
        """
        Initialise le générateur de données
        
        Parameters:
        n_rows (int): Nombre de lignes maximum à utiliser (pour échantillonnage)
        db_path (str): Chemin vers la base de données
        default_id_projet (int): ID de projet par défaut
        id_projet (int, optional): ID de projet spécifique à utiliser
        """
        self.n_rows = n_rows
        self.db_path = db_path
        self.default_id_projet = default_id_projet
        self.current_id_projet = id_projet if id_projet is not None else default_id_projet
        self.data_service = RootDataService(db_path, default_id_projet)
        self.logger = logging.getLogger(__name__)
        self.real_data = None  # Cache pour les données réelles
        self.available_projects = None  # Cache pour les projets disponibles
        
        # Configuration des mappings de colonnes
        self.column_mapping = {
            'jardin (1 = oui)': 'jardin',
            'Piscine (1= oui)': 'Piscine', 
            'Assainissement Collectif (1=oui)': 'Assainissement_Collectif',
            'maison (1 = oui)': 'maison',
            'naa (Nombre d\'adultes actifs)': 'naa',
            'nana (Nombre d\'adultes non actifs)': 'nana',
            'Revenu_Imputé_2': 'revenu',
            'Revenu imputé': 'revenu',
        }
        
        # Colonnes requises pour les calculs
        self.required_columns = {
            'SNWA': ['naa', 'nana'],
            'Garden_Weather': ['jardin', 'Freq_Nombre_de_Jours_sans_pluie'],
            'UC_Oxford': ['nbpers', 'nenf'],
            'UC_OCDE': ['nbpers', 'nenf'],
            'Niveau_vie_Oxford': ['revenu', 'UC_Oxford'],
            'Niveau_vie_OCDE': ['revenu', 'UC_OCDE']
        }
    
    def _reset_index_if_duplicated(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Réinitialise l'index si des doublons sont détectés
        
        Parameters:
        df (pd.DataFrame): DataFrame à vérifier et corriger
        
        Returns:
        pd.DataFrame: DataFrame avec index unique
        """
        if df.index.has_duplicates:
            print("⚠️  Index dupliqués détectés, réinitialisation...")
            df = df.reset_index(drop=True)
            print(f"✅ Index réinitialisé: {len(df)} lignes avec index unique")
        return df
    
    def load_real_data(self, force_reload: bool = False, 
                      id_projet: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Charge les données réelles depuis la base de données avec gestion d'erreurs améliorée
        
        Parameters:
        force_reload (bool): Force le rechargement même si les données sont déjà en cache
        id_projet (int, optional): ID de projet spécifique. Si None, utilise self.current_id_projet
        
        Returns:
        pd.DataFrame: Données réelles de la base ou None si erreur
        """
        project_id = id_projet if id_projet is not None else self.current_id_projet
        
        # Vérifier si on doit recharger (nouveau projet ou force_reload)
        if (self.real_data is None or force_reload or 
            (self.real_data is not None and 
             'id_projet' in self.real_data.columns and 
             self.real_data['id_projet'].iloc[0] != project_id)):
            
            try:
                print(f"🔄 Chargement des données réelles depuis la base (projet {project_id})...")
                self.real_data = self.data_service.get_all_data(id_projet=project_id)
                
                if self.real_data is None or len(self.real_data) == 0:
                    print(f"❌ Aucune donnée trouvée pour le projet {project_id}")
                    return None
                
                # Correction CRITIQUE: Reset index après chargement
                self.real_data = self._reset_index_if_duplicated(self.real_data)
                
                # Vérifier que id_projet est présent dans les données
                if 'id_projet' not in self.real_data.columns:
                    print("⚠️  Colonne id_projet manquante, ajout avec valeur par défaut")
                    self.real_data['id_projet'] = project_id
                
                print(f"✅ {len(self.real_data)} lignes chargées pour le projet {project_id}")
                
                # Validation basique des données
                self._validate_data(self.real_data)
                
            except Exception as e:
                error_msg = f"Erreur lors du chargement: {e}"
                print(f"❌ {error_msg}")
                self.logger.error(f"Erreur dans load_real_data: {e}", exc_info=True)
                return None
        
        return self.real_data.copy() if self.real_data is not None else None
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """
        Valide les données chargées
        
        Parameters:
        df (pd.DataFrame): DataFrame à valider
        """
        if df.empty:
            raise ValueError("DataFrame vide")
            
        # Vérifier les doublons d'index
        if df.index.has_duplicates:
            raise ValueError("Index contient des doublons après validation")
            
        # Vérifier les colonnes critiques
        critical_columns = ['nbpers', 'nenf']  # Colonnes essentielles pour les calculs
        missing_critical = [col for col in critical_columns if col not in df.columns]
        
        if missing_critical:
            self.logger.warning(f"Colonnes critiques manquantes: {missing_critical}")
        
        # Statistiques de validation
        null_stats = df.isnull().sum()
        high_null_cols = null_stats[null_stats > len(df) * 0.5].index.tolist()
        
        if high_null_cols:
            self.logger.warning(f"Colonnes avec >50% de valeurs nulles: {high_null_cols}")
    
    def get_base_data(self, sample_size: Optional[int] = None, 
                     id_projet: Optional[int] = None) -> pd.DataFrame:
        """
        Récupère les données de base avec échantillonnage optionnel
        
        Parameters:
        sample_size (int, optional): Taille de l'échantillon. Si None, utilise self.n_rows
        id_projet (int, optional): ID de projet spécifique
        
        Returns:
        pd.DataFrame: Données réelles (éventuellement échantillonnées)
        """
        # Charger les données réelles
        df = self.load_real_data(id_projet=id_projet)
        
        if df is None or len(df) == 0:
            raise ValueError("Impossible de charger les données réelles")
        
        # Déterminer la taille de l'échantillon
        if sample_size is None:
            sample_size = self.n_rows
        
        # Échantillonner si nécessaire
        if len(df) > sample_size:
            print(f"📊 Échantillonnage: {sample_size} lignes sur {len(df)} disponibles")
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
            print(f"✅ Index réinitialisé après échantillonnage")
        else:
            print(f"📊 Utilisation de toutes les données disponibles: {len(df)} lignes")
        
        # Vérification finale de l'index
        df = self._reset_index_if_duplicated(df)
        
        # Standardiser les noms de colonnes (en préservant id_projet)
        df = self._standardize_column_names(df)
        
        return df
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardise les noms de colonnes avec nettoyage amélioré
        
        Parameters:
        df (pd.DataFrame): DataFrame avec les noms originaux
        
        Returns:
        pd.DataFrame: DataFrame avec noms standardisés
        """
        # Copier le DataFrame pour éviter les modifications inattendues
        df_renamed = df.copy()
        
        # S'assurer que l'index est propre
        df_renamed = self._reset_index_if_duplicated(df_renamed)
        
        # Préserver la colonne id_projet si elle existe
        id_projet_column = None
        if 'id_projet' in df_renamed.columns:
            id_projet_column = df_renamed['id_projet'].copy()
        
        # Appliquer le mapping défini
        df_renamed = df_renamed.rename(columns=self.column_mapping)
        
        # Nettoyage général des noms de colonnes (sauf id_projet)
        new_columns = []
        for col in df_renamed.columns:
            if col == 'id_projet':
                new_columns.append(col)  # Préserver id_projet tel quel
            else:
                cleaned_col = (col.strip()  # Supprimer espaces
                              .replace(' ', '_')  # Remplacer espaces par underscores
                              .replace('(', '').replace(')', '')  # Supprimer parenthèses
                              .replace('=', ''))  # Supprimer signes égal
                new_columns.append(cleaned_col)
        
        df_renamed.columns = new_columns
        
        # Restaurer la colonne id_projet si elle était présente
        if id_projet_column is not None and 'id_projet' not in df_renamed.columns:
            df_renamed['id_projet'] = id_projet_column
        
        # Afficher les colonnes disponibles
        print(f"\n📋 Colonnes disponibles après standardisation ({len(df_renamed.columns)}):")
        for i, col in enumerate(df_renamed.columns, 1):
            if col == 'id_projet':
                unique_projects = df_renamed[col].nunique() if col in df_renamed.columns else 0
                print(f"   {i:2d}. {col} (📌 {unique_projects} projet(s) unique(s))")
            else:
                print(f"   {i:2d}. {col}")
        
        return df_renamed
    
    def _safe_division(self, numerator: pd.Series, denominator: pd.Series, 
                      operation_name: str = "division") -> pd.Series:
        """
        Effectue une division sécurisée entre deux Series en évitant les problèmes d'index
        
        Parameters:
        numerator (pd.Series): Série numérateur
        denominator (pd.Series): Série dénominateur
        operation_name (str): Nom de l'opération pour les logs
        
        Returns:
        pd.Series: Résultat de la division avec index propre
        """
        try:
            # Convertir en arrays numpy pour éviter les problèmes d'alignement d'index
            num_values = numerator.values
            den_values = denominator.values
            
            # Division avec gestion des zéros et infinis
            result_values = np.where(
                (den_values != 0) & (~np.isnan(den_values)) & (~np.isnan(num_values)),
                num_values / den_values,
                np.nan
            )
            
            # Créer une nouvelle Series avec un index propre
            result = pd.Series(result_values, index=range(len(result_values)))
            
            print(f"   ✅ {operation_name} effectuée avec méthode sécurisée")
            return result
            
        except Exception as e:
            print(f"   ❌ Erreur dans {operation_name}: {e}")
            # Retourner une série de NaN en cas d'erreur
            return pd.Series([np.nan] * len(numerator), index=range(len(numerator)))

    def calculate_derived_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les variables dérivées avec méthode de division sécurisée
        
        Parameters:
        df (DataFrame): DataFrame contenant les données réelles
        
        Returns:
        DataFrame: DataFrame avec les variables dérivées ajoutées
        """
        print("\n🧮 Calcul des variables dérivées...")
        
        # CORRECTION CRITIQUE: S'assurer que l'index est unique ET créer un DataFrame complètement nouveau
        df_result = df.copy().reset_index(drop=True)
        print(f"   🔧 DataFrame réinitialisé: {df_result.shape}, Index unique: {not df_result.index.has_duplicates}")
        
        # Dictionnaire pour suivre les calculs réussis
        calculation_status = {}
        
        try:
            # 1. SNWA = nana / (naa + nana) - Méthode vectorielle simple
            if self._can_calculate('SNWA', df_result):
                naa_vals = df_result['naa'].values
                nana_vals = df_result['nana'].values
                denominator_vals = naa_vals + nana_vals
                
                snwa_vals = np.where(denominator_vals > 0, nana_vals / denominator_vals, 0)
                df_result['SNWA'] = snwa_vals
                
                calculation_status['SNWA'] = True
                print("   ✅ SNWA calculé (méthode vectorielle)")
            else:
                calculation_status['SNWA'] = False
                print("   ❌ Impossible de calculer SNWA (colonnes naa/nana manquantes)")
            
            # 2. Garden * Weather - Méthode vectorielle
            weather_col = self._find_weather_column(df_result)
            if 'jardin' in df_result.columns and weather_col:
                jardin_vals = df_result['jardin'].values
                weather_vals = df_result[weather_col].values
                df_result['Garden_Weather'] = jardin_vals * weather_vals
                
                calculation_status['Garden_Weather'] = True
                print(f"   ✅ Garden_Weather calculé (méthode vectorielle avec {weather_col})")
            elif 'jardin' in df_result.columns:
                # Valeur par défaut si pas de données météo
                default_weather = 50
                df_result['Garden_Weather'] = df_result['jardin'].values * default_weather
                calculation_status['Garden_Weather'] = True
                print(f"   ⚠️  Garden_Weather calculé avec valeur météo par défaut ({default_weather})")
            else:
                calculation_status['Garden_Weather'] = False
                print("   ❌ Impossible de calculer Garden_Weather (colonne jardin manquante)")
            
            # 3. UC Oxford - Méthode vectorielle
            if self._can_calculate('UC_Oxford', df_result):
                nbpers_vals = df_result['nbpers'].values
                nenf_vals = df_result['nenf'].values
                
                uc_oxford_vals = np.maximum(
                    1 + (nbpers_vals - nenf_vals - 1) * 0.7 + nenf_vals * 0.5,
                    0.1  # Valeur minimale
                )
                df_result['UC_Oxford'] = uc_oxford_vals
                
                calculation_status['UC_Oxford'] = True
                print("   ✅ UC Oxford calculé (méthode vectorielle)")
            else:
                calculation_status['UC_Oxford'] = False
                print("   ❌ Impossible de calculer UC Oxford (colonnes nbpers/nenf manquantes)")
            
            # 4. UC OCDE - Méthode vectorielle
            if self._can_calculate('UC_OCDE', df_result):
                nbpers_vals = df_result['nbpers'].values
                nenf_vals = df_result['nenf'].values
                
                uc_ocde_vals = np.maximum(
                    1 + (nbpers_vals - nenf_vals - 1) * 0.5 + nenf_vals * 0.3,
                    0.1  # Valeur minimale
                )
                df_result['UC_OCDE'] = uc_ocde_vals
                
                calculation_status['UC_OCDE'] = True
                print("   ✅ UC OCDE calculé (méthode vectorielle)")
            else:
                calculation_status['UC_OCDE'] = False
                print("   ❌ Impossible de calculer UC OCDE (colonnes nbpers/nenf manquantes)")
            
            # 5. Niveau de vie Oxford - MÉTHODE SÉCURISÉE
            revenue_col = self._find_revenue_column(df_result)
            if revenue_col and 'UC_Oxford' in df_result.columns:
                print(f"   🔧 Calcul Niveau_vie_Oxford avec méthode sécurisée...")
                
                # Utiliser la méthode de division sécurisée
                niveau_vie_oxford = self._safe_division(
                    df_result[revenue_col], 
                    df_result['UC_Oxford'],
                    "Niveau_vie_Oxford"
                )
                df_result['Niveau_vie_Oxford'] = niveau_vie_oxford
                
                calculation_status['Niveau_vie_Oxford'] = True
                print(f"   ✅ Niveau de vie Oxford calculé (avec {revenue_col})")
            else:
                calculation_status['Niveau_vie_Oxford'] = False
                print("   ❌ Impossible de calculer Niveau de vie Oxford")
            
            # 6. Niveau de vie OCDE - MÉTHODE SÉCURISÉE
            if revenue_col and 'UC_OCDE' in df_result.columns:
                print(f"   🔧 Calcul Niveau_vie_OCDE avec méthode sécurisée...")
                
                # Utiliser la méthode de division sécurisée
                niveau_vie_ocde = self._safe_division(
                    df_result[revenue_col], 
                    df_result['UC_OCDE'],
                    "Niveau_vie_OCDE"
                )
                df_result['Niveau_vie_OCDE'] = niveau_vie_ocde
                
                calculation_status['Niveau_vie_OCDE'] = True
                print(f"   ✅ Niveau de vie OCDE calculé (avec {revenue_col})")
            else:
                calculation_status['Niveau_vie_OCDE'] = False
                print("   ❌ Impossible de calculer Niveau de vie OCDE")
            
        except Exception as e:
            error_msg = f"Erreur lors du calcul des variables dérivées: {e}"
            print(f"   ❌ {error_msg}")
            self.logger.error(f"Erreur dans calculate_derived_variables: {e}", exc_info=True)
            
            # En cas d'erreur, diagnostics supplémentaires
            print(f"   🔍 Diagnostic approfondi:")
            print(f"      - Forme du DataFrame: {df_result.shape}")
            print(f"      - Index dupliqués: {df_result.index.has_duplicates}")
            print(f"      - Type d'index: {type(df_result.index)}")
            print(f"      - Colonnes dupliquées: {df_result.columns.has_duplicates}")
            if hasattr(df_result.index, 'nunique'):
                print(f"      - Index uniques: {df_result.index.nunique()}/{len(df_result)}")
            
            # Vérifier les colonnes spécifiques impliquées dans l'erreur
            if revenue_col:
                revenue_series = df_result[revenue_col]
                print(f"      - Colonne revenue '{revenue_col}': {len(revenue_series)} valeurs")
                print(f"      - Revenue index dupliqués: {revenue_series.index.has_duplicates}")
            
            if 'UC_Oxford' in df_result.columns:
                uc_series = df_result['UC_Oxford']
                print(f"      - Colonne UC_Oxford: {len(uc_series)} valeurs")
                print(f"      - UC_Oxford index dupliqués: {uc_series.index.has_duplicates}")
        
        # Résumé des calculs
        successful_calcs = sum(calculation_status.values())
        total_calcs = len(calculation_status)
        print(f"\n📊 Résumé calculs: {successful_calcs}/{total_calcs} variables calculées avec succès")
        
        # Vérification finale de l'intégrité
        df_result = self._reset_index_if_duplicated(df_result)
        
        return df_result
    
    def _can_calculate(self, variable_name: str, df: pd.DataFrame) -> bool:
        """
        Vérifie si une variable peut être calculée
        
        Parameters:
        variable_name (str): Nom de la variable à calculer
        df (pd.DataFrame): DataFrame à vérifier
        
        Returns:
        bool: True si le calcul est possible
        """
        if variable_name not in self.required_columns:
            return False
        
        required_cols = self.required_columns[variable_name]
        return all(col in df.columns for col in required_cols)
    
    def _find_weather_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Trouve une colonne météo dans le DataFrame
        
        Parameters:
        df (pd.DataFrame): DataFrame à analyser
        
        Returns:
        str: Nom de la colonne météo trouvée ou None
        """
        weather_patterns = [
            'Freq_Nombre_de_Jours_sans_pluie',
            'jours_sans_pluie',
            'weather',
            'meteo'
        ]
        
        for pattern in weather_patterns:
            matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
            if matching_cols:
                return matching_cols[0]
        
        return None
    
    def _find_revenue_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Trouve une colonne de revenu dans le DataFrame
        
        Parameters:
        df (pd.DataFrame): DataFrame à analyser
        
        Returns:
        str: Nom de la colonne de revenu trouvée ou None
        """
        revenue_patterns = [
            'revenu',
            'Revenu_Imputé_2', 
            'Revenu_imputé',
            'income',
            'salaire'
        ]
        
        for pattern in revenue_patterns:
            if pattern in df.columns:
                return pattern
            # Recherche insensible à la casse
            matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
            if matching_cols:
                return matching_cols[0]
        
        return None
    
    def generate_complete_dataset(self, sample_size: Optional[int] = None,
                                 id_projet: Optional[int] = None) -> pd.DataFrame:
        """
        Génère le dataset complet avec toutes les variables (réelles + dérivées)
        
        Parameters:
        sample_size (int, optional): Taille de l'échantillon
        id_projet (int, optional): ID de projet spécifique
        
        Returns:
        DataFrame: Dataset complet avec variables calculées
        """
        project_id = id_projet if id_projet is not None else self.current_id_projet
        
        print("=" * 60)
        print("GÉNÉRATION DU DATASET COMPLET AVEC DONNÉES RÉELLES")
        print(f"📌 Projet ID: {project_id}")
        print("=" * 60)
        
        # Récupérer les données réelles de base
        df = self.get_base_data(sample_size, id_projet=project_id)
        
        # Calculer les variables dérivées
        df = self.calculate_derived_variables(df)
        
        # Nettoyage final
        df = self._clean_final_dataset(df)
        
        # Vérifier et assurer la présence de id_projet
        if 'id_projet' not in df.columns:
            df['id_projet'] = project_id
            print(f"⚠️  Colonne id_projet ajoutée avec la valeur {project_id}")
        
        print(f"\n✅ Dataset complet généré: {df.shape}")
        print(f"   • Variables totales: {len(df.columns)}")
        print(f"   • Lignes: {len(df)}")
        print(f"   • Projet(s): {df['id_projet'].nunique()} unique(s)")
        print(f"   • Index unique: {not df.index.has_duplicates}")
        
        return df
    
    def _clean_final_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoyage final du dataset
        
        Parameters:
        df (pd.DataFrame): DataFrame à nettoyer
        
        Returns:
        pd.DataFrame: DataFrame nettoyé
        """
        df_clean = df.copy()
        
        # S'assurer que l'index est propre
        df_clean = self._reset_index_if_duplicated(df_clean)
        
        # Remplacer les infinis par NaN
        df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
        
        # Optionnel: supprimer les lignes avec trop de valeurs manquantes
        # threshold = len(df_clean.columns) * 0.5  # 50% des colonnes doivent être non-nulles
        # df_clean = df_clean.dropna(thresh=threshold)
        
        return df_clean
    
    def get_data_quality_report(self, id_projet: Optional[int] = None) -> Dict:
        """
        Génère un rapport de qualité des données
        
        Parameters:
        id_projet (int, optional): ID de projet spécifique
        
        Returns:
        Dict: Rapport de qualité des données
        """
        df = self.load_real_data(id_projet=id_projet)
        if df is None:
            return {"error": "Impossible de charger les données"}
        
        report = {
            "shape": df.shape,
            "columns_count": len(df.columns),
            "rows_count": len(df),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "null_counts": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "index_duplicates": df.index.has_duplicates,
            "index_unique_count": df.index.nunique() if hasattr(df.index, 'nunique') else len(df.index.unique())
        }
        
        # Informations sur les projets
        if 'id_projet' in df.columns:
            report["projects_info"] = {
                "unique_projects": df['id_projet'].nunique(),
                "project_counts": df['id_projet'].value_counts().to_dict(),
                "current_project": id_projet if id_projet else self.current_id_projet
            }
        
        # Statistiques pour colonnes numériques
        if report["numeric_columns"]:
            numeric_stats = df[report["numeric_columns"]].describe()
            report["numeric_statistics"] = numeric_stats.to_dict()
        
        return report
    
    def display_real_data(self, limit: Optional[int] = None, 
                         id_projet: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Récupère et affiche les données réelles avec rapport de qualité
        
        Parameters:
        limit (int, optional): Nombre de lignes à afficher
        id_projet (int, optional): ID de projet spécifique
        """
        try:
            project_id = id_projet if id_projet is not None else self.current_id_projet
            print("=" * 60)
            print("AFFICHAGE DES DONNÉES RÉELLES")
            print(f"📌 Projet ID: {project_id}")
            print("=" * 60)
            
            df = self.load_real_data(id_projet=project_id)
            if df is None:
                return None
            
            # Générer le rapport de qualité
            quality_report = self.get_data_quality_report(id_projet=project_id)
            
            # Limiter l'affichage si demandé
            if limit and len(df) > limit:
                df_display = df.head(limit)
                print(f"Affichage des {limit} premières lignes sur {len(df)} disponibles")
            else:
                df_display = df
                print(f"Affichage de toutes les {len(df)} lignes")
            
            # Affichage des informations générales
            print(f"\n📊 INFORMATIONS GÉNÉRALES:")
            print(f"   • Forme du DataFrame: {quality_report['shape']}")
            print(f"   • Utilisation mémoire: {quality_report['memory_usage_mb']:.2f} MB")
            print(f"   • Colonnes numériques: {len(quality_report['numeric_columns'])}")
            print(f"   • Colonnes catégorielles: {len(quality_report['categorical_columns'])}")
            print(f"   • Index dupliqués: {'❌ OUI' if quality_report['index_duplicates'] else '✅ NON'}")
            print(f"   • Index uniques: {quality_report['index_unique_count']}/{len(df)}")
            
            # Informations sur les projets
            if "projects_info" in quality_report:
                proj_info = quality_report["projects_info"]
                print(f"   • Projets uniques dans les données: {proj_info['unique_projects']}")
                print(f"   • Projet courant: {proj_info['current_project']}")
                if proj_info['unique_projects'] > 1:
                    print(f"   • Distribution par projet: {proj_info['project_counts']}")
            
            # Affichage des colonnes avec informations de qualité
            print(f"\n📋 COLONNES DISPONIBLES:")
            for i, col in enumerate(df.columns, 1):
                null_count = quality_report['null_counts'].get(col, 0)
                null_pct = (null_count / len(df)) * 100
                dtype = quality_report['data_types'].get(col, 'unknown')
                
                # Marquer spécialement la colonne id_projet
                marker = "📌" if col == 'id_projet' else "  "
                print(f"   {i:2d}. {marker} {col:<30} | {dtype:<10} | Nulls: {null_count:4d} ({null_pct:5.1f}%)")
            
            # Affichage des premières lignes
            print(f"\n👀 PREMIÈRES LIGNES:")
            print(df_display.head())
            
            # Statistiques descriptives pour les colonnes numériques
            if quality_report["numeric_columns"]:
                print(f"\n📈 STATISTIQUES DESCRIPTIVES (colonnes numériques):")
                print(df[quality_report["numeric_columns"]].describe())
            
            print("\n" + "=" * 60)
            return df
            
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.logger.error(f"Erreur dans display_real_data: {e}", exc_info=True)
            return None
    
    def save_dataset(self, filename: str = "real_dataset_with_calculations.csv", 
                    sample_size: Optional[int] = None,
                    id_projet: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Sauvegarde le dataset complet avec gestion d'erreurs améliorée
        
        Parameters:
        filename (str): Nom du fichier
        sample_size (int, optional): Taille de l'échantillon
        id_projet (int, optional): ID de projet spécifique
        
        Returns:
        pd.DataFrame: Dataset sauvegardé ou None si erreur
        """
        try:
            dataset = self.generate_complete_dataset(sample_size, id_projet=id_projet)
            
            # Validation avant sauvegarde
            if dataset is None or dataset.empty:
                raise ValueError("Dataset vide, impossible de sauvegarder")
            
            # Vérification finale de l'index avant sauvegarde
            dataset = self._reset_index_if_duplicated(dataset)
            
            dataset.to_csv(filename, index=False)
            
            project_info = ""
            if 'id_projet' in dataset.columns:
                unique_projects = dataset['id_projet'].nunique()
                if unique_projects == 1:
                    project_info = f" (Projet {dataset['id_projet'].iloc[0]})"
                else:
                    project_info = f" ({unique_projects} projets)"
            
            print(f"💾 Dataset sauvegardé dans {filename}")
            print(f"   • {len(dataset)} lignes")
            print(f"   • {len(dataset.columns)} colonnes{project_info}")
            print(f"   • Taille fichier: {self._get_file_size(filename)}")
            print(f"   • Index unique: {not dataset.index.has_duplicates}")
            
            return dataset
            
        except Exception as e:
            error_msg = f"Erreur lors de la sauvegarde: {e}"
            print(f"❌ {error_msg}")
            self.logger.error(f"Erreur dans save_dataset: {e}", exc_info=True)
            return None
    
    def _get_file_size(self, filename: str) -> str:
        """
        Obtient la taille d'un fichier de manière lisible
        
        Parameters:
        filename (str): Chemin vers le fichier
        
        Returns:
        str: Taille formatée
        """
        try:
            import os
            size_bytes = os.path.getsize(filename)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} TB"
        except:
            return "Taille inconnue"
    
    def compare_original_vs_calculated(self, sample_size: int = 10) -> Optional[pd.DataFrame]:
        """
        Compare les données originales avec les variables calculées
        
        Parameters:
        sample_size (int): Nombre de lignes à afficher pour la comparaison
        
        Returns:
        pd.DataFrame: Dataset complet ou None si erreur
        """
        try:
            print("=" * 60)
            print("COMPARAISON DONNÉES ORIGINALES VS CALCULÉES")
            print("=" * 60)
            
            # Données originales
            original_df = self.load_real_data()
            if original_df is None:
                return None
            
            # S'assurer que l'index est propre dès le départ
            original_df = self._reset_index_if_duplicated(original_df)
            
            # Dataset complet avec calculs
            complete_df = self.generate_complete_dataset()
            
            # Identifier les nouvelles colonnes (calculées)
            original_cols = set(original_df.columns)
            complete_cols = set(complete_df.columns)
            calculated_cols = list(complete_cols - original_cols)
            
            print(f"\n📊 RÉSUMÉ:")
            print(f"   • Colonnes originales: {len(original_cols)}")
            print(f"   • Colonnes calculées: {len(calculated_cols)}")
            print(f"   • Total: {len(complete_cols)}")
            print(f"   • Index original dupliqués: {'❌ OUI' if original_df.index.has_duplicates else '✅ NON'}")
            print(f"   • Index final dupliqués: {'❌ OUI' if complete_df.index.has_duplicates else '✅ NON'}")
            
            if calculated_cols:
                print(f"\n🧮 NOUVELLES COLONNES CALCULÉES:")
                for col in sorted(calculated_cols):
                    non_null_count = complete_df[col].notna().sum()
                    print(f"   • {col:<25} | Valeurs non-nulles: {non_null_count}")
                
                print(f"\n👀 ÉCHANTILLON AVEC NOUVELLES VARIABLES ({sample_size} lignes):")
                # Sélectionner les colonnes les plus pertinentes pour l'affichage
                base_cols = ['revenu', 'nbpers', 'nenf', 'naa', 'nana', 'jardin']
                available_base_cols = [col for col in base_cols if col in complete_df.columns]
                cols_to_show = available_base_cols + calculated_cols[:5]  # Limiter l'affichage
                
                print(complete_df[cols_to_show].head(sample_size))
            else:
                print("\n⚠️  Aucune nouvelle variable n'a pu être calculée")
            
            print("\n" + "=" * 60)
            return complete_df
            
        except Exception as e:
            error_msg = f"Erreur dans la comparaison: {e}"
            print(f"❌ {error_msg}")
            self.logger.error(f"Erreur dans compare_original_vs_calculated: {e}", exc_info=True)
            return None
    
    def diagnose_index_issues(self, id_projet: Optional[int] = None) -> Dict:
        """
        Diagnostic spécialisé pour les problèmes d'index
        
        Parameters:
        id_projet (int, optional): ID de projet spécifique
        
        Returns:
        Dict: Rapport de diagnostic des index
        """
        print("🔍 DIAGNOSTIC DES PROBLÈMES D'INDEX")
        print("=" * 50)
        
        try:
            df = self.load_real_data(id_projet=id_projet)
            if df is None:
                return {"error": "Impossible de charger les données"}
            
            diagnostic = {
                "total_rows": len(df),
                "index_type": str(type(df.index)),
                "has_duplicates": df.index.has_duplicates,
                "unique_index_count": df.index.nunique() if hasattr(df.index, 'nunique') else len(df.index.unique()),
                "index_dtype": str(df.index.dtype),
                "index_name": df.index.name,
                "sample_index_values": df.index[:10].tolist()
            }
            
            if diagnostic["has_duplicates"]:
                # Analyser les doublons
                duplicated_index = df.index[df.index.duplicated(keep=False)]
                diagnostic["duplicate_count"] = len(duplicated_index)
                diagnostic["duplicate_values"] = duplicated_index.value_counts().head(10).to_dict()
                
                print(f"❌ Index dupliqués détectés!")
                print(f"   • Total de lignes: {diagnostic['total_rows']}")
                print(f"   • Index uniques: {diagnostic['unique_index_count']}")
                print(f"   • Doublons: {diagnostic['duplicate_count']}")
                print(f"   • Valeurs les plus dupliquées: {diagnostic['duplicate_values']}")
            else:
                print(f"✅ Index propre!")
                print(f"   • Total de lignes: {diagnostic['total_rows']}")
                print(f"   • Tous les index sont uniques")
            
            print(f"\n📋 DÉTAILS DE L'INDEX:")
            print(f"   • Type: {diagnostic['index_type']}")
            print(f"   • Dtype: {diagnostic['index_dtype']}")
            print(f"   • Nom: {diagnostic['index_name']}")
            print(f"   • Échantillon: {diagnostic['sample_index_values']}")
            
            return diagnostic
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {e}")
            return {"error": str(e)}


# Exemple d'utilisation avec données réelles et gestion d'erreurs renforcée
if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data_generator.log'),
            logging.StreamHandler()
        ]
    )
    
    print("🚀 DATA GENERATOR AVEC DONNÉES RÉELLES (VERSION CORRIGÉE)")
    print("=" * 80)
    
    try:
        # Créer une instance du générateur
        generator = DataGenerator(n_rows=500, db_path="database.db")
        
        # Test de connectivité avec diagnostic d'index
        print("0️⃣  TEST DE CONNECTIVITÉ ET DIAGNOSTIC D'INDEX")
        test_data = generator.load_real_data()
        if test_data is None:
            print("❌ Impossible de se connecter à la base de données")
            print("Vérifiez que le fichier database.db existe et contient des données")
            exit(1)
        
        # Diagnostic spécialisé des index
        #diagnostic = generator.diagnose_index_issues()
        
        # 1. Afficher les données réelles brutes
        print("\n1️⃣  AFFICHAGE DES DONNÉES RÉELLES BRUTES")
        df_real = generator.display_real_data(limit=10)
        
       
        
    except Exception as e:
        print(f"\n❌ ERREUR PRINCIPALE: {e}")
        logging.error(f"Erreur principale: {e}", exc_info=True)
        print("\nVérifiez que:")
        print("1. Le fichier database.db existe dans le répertoire courant")
        print("2. La table contient des données valides")
        print("3. Les permissions de lecture sont accordées")
        print("4. Les colonnes nécessaires existent (revenu, nbpers, nenf, etc.)")
        print("5. Consultez le fichier data_generator.log pour plus de détails")
        print("6. NOUVEAU: L'index des données ne contient pas de doublons")