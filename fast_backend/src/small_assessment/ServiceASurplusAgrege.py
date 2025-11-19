import pandas as pd
import numpy as np


class ServiceASurplusAgrege:
    """
    Classe pour calculer des statistiques descriptives et des indicateurs d'inégalité
    sur des données de consommation.
    """
    
    def __init__(self):
        pass
    
    # ================ VALIDATION ================
    
    def _check_column(self, df: pd.DataFrame, col: str):
        """Vérifie qu'une colonne existe dans le DataFrame."""
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' est absente du DataFrame")
    
    # ================ STATISTIQUES DE BASE ================

    def somme_dummy(self, df: pd.DataFrame)-> int:
        """
        Calcule la somme totale des colonnes spécifiques : d1_a_moins, d1_b_plus, d1_c_eq.
        
        Args:
            df (pd.DataFrame): Le DataFrame contenant les données.
            
        Returns:
            float: La somme totale de toutes les valeurs des trois colonnes.
        """
        colonnes = ['d1_a_moins', 'd1_b_plus', 'd1_c_eq']
        total = df[colonnes].sum().sum()
        return total

    
    def compter_menages_distincts(self, df: pd.DataFrame, col_menage: str) -> int:
        """Compte le nombre de ménages distincts."""
        self._check_column(df, col_menage)
        return df[col_menage].nunique()
    
    def moyenne_conso(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule la moyenne de consommation."""
        self._check_column(df, col_conso)
        return df[col_conso].mean()
    
    def mediane_conso(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule la médiane de consommation."""
        self._check_column(df, col_conso)
        return df[col_conso].median()
    
    def min_conso(self, df: pd.DataFrame, col_conso: str) -> float:
        """Retourne la consommation minimale."""
        self._check_column(df, col_conso)
        return df[col_conso].min()
    
    def max_conso(self, df: pd.DataFrame, col_conso: str) -> float:
        """Retourne la consommation maximale."""
        self._check_column(df, col_conso)
        return df[col_conso].max()
    
    def Q1(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule le 1er quartile (25e percentile)."""
        self._check_column(df, col_conso)
        return df[col_conso].quantile(0.25)
    
    def Q3(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule le 3e quartile (75e percentile)."""
        self._check_column(df, col_conso)
        return df[col_conso].quantile(0.75)
    
    def calculer_D1(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule le 1er décile (10e percentile)."""
        self._check_column(df, col_conso)
        return df[col_conso].quantile(0.1)
    
    def calculer_D9(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule le 9e décile (90e percentile)."""
        self._check_column(df, col_conso)
        return df[col_conso].quantile(0.9)
    
    # ================ DISPERSION ================
    
    def variance_conso(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule la variance de consommation."""
        self._check_column(df, col_conso)
        return df[col_conso].var()
    
    def ecart_type_conso(self, df: pd.DataFrame, col_conso: str) -> float:
        """Calcule l'écart-type de consommation."""
        self._check_column(df, col_conso)
        return df[col_conso].std()
    
    def coeff_variation(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Calcule le coefficient de variation (CV = écart-type / moyenne).
        Retourne NaN si la moyenne est nulle.
        """
        mean = self.moyenne_conso(df, col_conso)
        if mean == 0:
            return np.nan
        return self.ecart_type_conso(df, col_conso) / mean
    
    # ================ MAD ET SCHUTZ ================
    
    def MAD(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Mean Absolute Deviation (écart absolu moyen par rapport à la moyenne).
        MAD = moyenne(|x - moyenne(x)|)
        """
        self._check_column(df, col_conso)
        serie = df[col_conso].dropna()
        mean_val = serie.mean()
        return (np.abs(serie - mean_val)).mean()
    
    def MAPE(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Mean Absolute Percentage Error (écart absolu moyen relatif à la moyenne).
        MAPE = 100 * moyenne(|x - moyenne(x)| / moyenne(x))
        """
        self._check_column(df, col_conso)
        serie = df[col_conso].dropna()
        mean_val = serie.mean()
        if mean_val == 0:
            return np.nan
        return (np.abs(serie - mean_val) / mean_val).mean() * 100
    
    def Schutz(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Indice de Schutz = 1 - (MAD / Moyenne).
        Mesure de concentration alternative au Gini.
        """
        self._check_column(df, col_conso)
        serie = df[col_conso].dropna()
        mean_val = serie.mean()
        if mean_val == 0:
            return np.nan
        mad = (np.abs(serie - mean_val)).mean()
        return 1 - (mad / mean_val)
    
    # ================ TRI ET PRÉPARATION ================
    
    def orderConsoQ(self, df: pd.DataFrame, col_conso: str) -> pd.DataFrame:
        """
        Trie le DataFrame selon plusieurs critères hiérarchiques:
        1. assaini (croissant) si présent
        2. menage_pauvre (décroissant) si présent
        3. col_conso (croissant)
        
        Retourne un DataFrame avec les colonnes pertinentes.
        """
        self._check_column(df, col_conso)
        
        # Colonnes à conserver
        cols_keep = []
        if "menage" in df.columns:
            cols_keep.append("menage")
        if "assaini" in df.columns:
            cols_keep.append("assaini")
        if "menage_pauvre" in df.columns:
            cols_keep.append("menage_pauvre")
        cols_keep.append(col_conso)
        
        # Critères de tri
        cols_sort = []
        asc_flags = []
        
        if "assaini" in df.columns:
            cols_sort.append("assaini")
            asc_flags.append(True)
        
        if "menage_pauvre" in df.columns:
            cols_sort.append("menage_pauvre")
            asc_flags.append(False)  # Décroissant
        
        cols_sort.append(col_conso)
        asc_flags.append(True)
        
        df_sorted = df.sort_values(by=cols_sort, ascending=asc_flags).reset_index(drop=True)
        return df_sorted[cols_keep]
    
    def rangValeurConso(self, df: pd.DataFrame, col_conso: str) -> pd.DataFrame:
        """
        Ajoute le rang et le produit rang × valeur de consommation.
        Utile pour les calculs de concentration.
        """
        self._check_column(df, col_conso)
        df = df.copy().reset_index(drop=True)
        df['rang'] = df.index + 1
        df['rang_valeur'] = df['rang'] * df[col_conso]
        
        cols_to_return = ['rang', 'rang_valeur']
        if "menage" in df.columns:
            cols_to_return.insert(0, "menage")
        
        return df[cols_to_return]
    
    # ================ INDICES DE GINI ================
    
    def _gini_interne(self, x, w=None):
        if w is None:
            w = np.ones_like(x)
        
        # Remove missing values
        valid = ~(np.isnan(x) | np.isnan(w))
        x, w = x[valid], w[valid]
        
        if len(x) == 0 or np.all(w == 0):
            return np.nan  # Pas de données valides
        
        if np.any(w < 0):
            raise ValueError("Au moins un poids est négatif")
        
        # Normalize weights
        w = w / np.sum(w)
        
        # Sort values and weights
        order = np.argsort(x)
        x, w = x[order], w[order]
        
        # Cumulative sums
        p = np.cumsum(w)
        nu = np.cumsum(w * x)
        
        if nu[-1] != 0:
            nu /= nu[-1]
        else:
            return np.nan
        
        # Gini calculation
        gini = np.sum(nu[1:] * p[:-1]) - np.sum(nu[:-1] * p[1:])
        return gini
    
    def calculer_gini(self, df: pd.DataFrame, col_conso: str, col_poids: str = None) -> float:
        """
        Calcule le coefficient de Gini avec poids optionnels.
        Utilise la méthode des sommes cumulatives (comme votre fonction initiale).
        
        Args:
            df: DataFrame contenant les données
            col_conso: Colonne de consommation
            col_poids: Colonne de pondération (optionnel)
            
        Returns:
            Coefficient de Gini
        """
        self._check_column(df, col_conso)
        
        if col_poids:
            self._check_column(df, col_poids)
            mask = df[col_conso].notna() & df[col_poids].notna()
            x = df.loc[mask, col_conso].values
            w = df.loc[mask, col_poids].values
        else:
            x = df[col_conso].dropna().values
            w = None
        
        try:
            return self._gini_interne(x, w)
        except (ValueError, ZeroDivisionError):
            return np.nan
    
    def calculer_gini_simple(self, df: pd.DataFrame, col_conso: str, col_poids: str = None) -> float:
        """
        Alias de calculer_gini pour compatibilité avec l'ancien code.
        """
        return self.calculer_gini(df, col_conso, col_poids)
    
    def calculer_gini_avec_poids(self, df: pd.DataFrame, col_conso: str, 
                                  col_poids: str = None) -> float:
        """
        Alias de calculer_gini pour compatibilité avec l'ancien code.
        """
        return self.calculer_gini(df, col_conso, col_poids)
    
    def decomposer_gini(self, df: pd.DataFrame, col_conso: str, col_groupe: str, 
                        col_poids: str = None) -> dict:
        """
        Décompose le Gini par groupes (within, between, overlap).
        Utilise la fonction _gini_decomp_interne basée sur votre code initial.
        
        Args:
            df: DataFrame
            col_conso: Colonne de consommation
            col_groupe: Colonne définissant les groupes
            col_poids: Colonne de pondération (optionnel)
            
        Returns:
            Dictionnaire avec la décomposition complète du Gini
        """
        self._check_column(df, col_conso)
        self._check_column(df, col_groupe)
        
        if col_poids:
            self._check_column(df, col_poids)
        
        x = df[col_conso].values
        z = df[col_groupe].values
        w = df[col_poids].values if col_poids else None
        
        return self._gini_decomp_interne(x, z, w)
    
    def _gini_decomp_interne(self, x, z, w=None):
        """
        Fonction interne de décomposition du Gini basée sur votre code initial.
        
        Args:
            x: Array des valeurs de consommation
            z: Array des groupes
            w: Array des poids (optionnel)
            
        Returns:
            Dictionnaire avec décomposition complète
        """
        if w is None:
            w = np.ones_like(x)
        
        z_factorized = pd.factorize(z)[0]
        df = pd.DataFrame({
            'x': np.array(x, dtype=float), 
            'z': z_factorized, 
            'w': np.array(w, dtype=float)
        })
        df = df.dropna()
        
        # Group splitting
        df_split = {key: df[df['z'] == key] for key in df['z'].unique()}
        n_group = df.groupby('z')['w'].sum()
        
        # Means
        x_mean = np.average(df['x'], weights=df['w'])
        x_mean_group = {
            key: np.average(df_split[key]['x'], weights=df_split[key]['w']) 
            for key in df_split
        }
        share_group = {
            key: df_split[key]['w'].sum() / df['w'].sum() 
            for key in df_split
        }
        share_group_income = {
            key: share_group[key] * x_mean_group[key] / x_mean 
            for key in df_split
        }
        
        # Gini calculations
        gini_total = self._gini_interne(df['x'].values, df['w'].values)
        gini_group = {
            key: self._gini_interne(df_split[key]['x'].values, df_split[key]['w'].values) 
            for key in df_split
        }
        gini_group_contribution = {
            key: gini_group[key] * share_group[key] * share_group_income[key] 
            for key in df_split
        }
        gini_within = sum(gini_group_contribution.values())
        gini_between = self._gini_interne(
            np.array(list(x_mean_group.values())), 
            n_group.values
        )
        gini_overlap = gini_total - gini_within - gini_between
        
        return {
            'gini_decomp': {
                'gini_total': gini_total,
                'gini_within': gini_within,
                'gini_between': gini_between,
                'gini_overlap': gini_overlap
            },
            'gini_group': {
                'gini_group': gini_group,
                'gini_group_contribution': gini_group_contribution
            },
            'mean': {
                'mean_total': x_mean,
                'mean_group': x_mean_group
            },
            'share_groups': share_group,
            'share_income_groups': share_group_income,
            'number_cases': {
                'n_weighted': df['w'].sum(),
                'n_group_weighted': n_group
            }
        }
    
    # ================ RATIOS D'INÉGALITÉ ================
    
    def ratio_interdeciles(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Calcule le ratio D9/D1.
        Mesure l'écart entre les plus riches et les plus pauvres.
        """
        d1 = self.calculer_D1(df, col_conso)
        d9 = self.calculer_D9(df, col_conso)
        if d1 == 0:
            return np.nan
        return d9 / d1
    
    def ratio_20_80(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Calcule le ratio S80/S20 (moyenne des 20% les plus riches / moyenne des 20% les plus pauvres).
        """
        self._check_column(df, col_conso)
        df_sorted = df.sort_values(by=col_conso).reset_index(drop=True)
        N = len(df_sorted)
        k = max(1, int(N * 0.2))
        
        lowest_20_mean = df_sorted[col_conso].iloc[:k].mean()
        highest_20_mean = df_sorted[col_conso].iloc[-k:].mean()
        
        if lowest_20_mean == 0:
            return np.nan
        
        return highest_20_mean / lowest_20_mean
    
    def coefficient_yule(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Calcule le coefficient de Yule = (Q3 - Q1) / (Q3 + Q1).
        Mesure d'asymétrie de la distribution.
        """
        q1 = self.Q1(df, col_conso)
        q3 = self.Q3(df, col_conso)
        denominateur = q3 + q1
        if denominateur == 0:
            return np.nan
        return (q3 - q1) / denominateur
    
    # ================ POSITION DE LA MOYENNE ================
    
    def F_moyenne(self, df: pd.DataFrame, col_conso: str) -> float:
        """
        Position en % de la moyenne dans la distribution.
        Équivalent à RANG.POURCENTAGE.INCLURE dans Excel.
        """
        self._check_column(df, col_conso)
        mean_val = df[col_conso].mean()
        values = np.sort(df[col_conso].dropna().values)
        
        if len(values) == 0:
            return np.nan
        
        rank = np.searchsorted(values, mean_val, side="right")
        return 100 * rank / len(values)
    
    # ================ COURBE DE LORENZ ================
    
    def courbe_lorenz(self, df: pd.DataFrame, col_conso: str) -> tuple:
        """
        Calcule les coordonnées de la courbe de Lorenz.
        
        Returns:
            (cumul_population, cumul_conso): Tuples numpy pour tracer la courbe
        """
        self._check_column(df, col_conso)
        df_sorted = df.sort_values(by=col_conso).reset_index(drop=True)
        
        n = len(df_sorted)
        cumul_pop = np.linspace(0, 1, n + 1)
        
        conso_cumul = np.insert(
            np.cumsum(df_sorted[col_conso]) / df_sorted[col_conso].sum(), 
            0, 
            0
        )
        
        return cumul_pop, conso_cumul
    
    # ================ RÉSUMÉS STATISTIQUES ================
    
    def resume_statistiques(self, df: pd.DataFrame, col_conso: str, col_groupe: str = None) -> pd.DataFrame:
        """
        Calcule un résumé complet des statistiques descriptives et d'inégalité.
        Si col_groupe est fourni, inclut la décomposition du Gini (total, within, between, overlap).
        
        Returns:
            DataFrame avec deux colonnes: Indicateur et Valeur
        """
        self._check_column(df, col_conso)
        
        # Pré-calcul des valeurs réutilisées
        q1 = self.Q1(df, col_conso)
        q3 = self.Q3(df, col_conso)
        d1 = self.calculer_D1(df, col_conso)
        d9 = self.calculer_D9(df, col_conso)
        
        stats = [
            # Tendances centrales
            ("Moyenne", self.moyenne_conso(df, col_conso)),
            ("Médiane", self.mediane_conso(df, col_conso)),
            ("Min", self.min_conso(df, col_conso)),
            ("Max", self.max_conso(df, col_conso)),
            ("Q1", q1),
            ("Q3", q3),
            ("D1", d1),
            ("D9", d9),
            ("F (Moyenne)", self.F_moyenne(df, col_conso)),
            
            # Dispersion
            ("Variance", self.variance_conso(df, col_conso)),
            ("Écart-type", self.ecart_type_conso(df, col_conso)),
            ("MAD", self.MAD(df, col_conso)),
            ("MAPE", self.MAPE(df, col_conso)),
            ("Coeff Variation", self.coeff_variation(df, col_conso)),
            
            # Étendues
            ("Étendue Interquartiles", q3 - q1),
            ("Étendue Interdéciles", d9 - d1),
            ("Coefficient de Yule", self.coefficient_yule(df, col_conso)),
            
            # Concentration
            ("Gini (global)", self.calculer_gini(df, col_conso)),
            ("Schutz", self.Schutz(df, col_conso)),
            ("Ratio interdéciles (D9/D1)", self.ratio_interdeciles(df, col_conso)),
            ("Ratio S80/S20", self.ratio_20_80(df, col_conso)),
        ]
        
        # Ajout de la décomposition du Gini si col_groupe est fourni
        if col_groupe:
            self._check_column(df, col_groupe)
            gini_decomp = self.decomposer_gini(df, col_conso, col_groupe)
            gini_stats = gini_decomp["gini_decomp"]
            
            stats.extend([
                ("Gini total", gini_stats["gini_total"]),
                ("Inégalité intra-groupes (within)", gini_stats["gini_within"]),
                ("Inégalité inter-groupes (between)", gini_stats["gini_between"]),
                ("Chevauchement (overlap)", gini_stats["gini_overlap"]),
            ])
        
        return pd.DataFrame(stats, columns=["Indicateur", "Valeur"])

    
    def resume_short(self, df: pd.DataFrame, col_conso: str) -> pd.DataFrame:
        """
        Résumé rapide avec les indicateurs essentiels.
        
        Returns:
            DataFrame avec Moyenne, Médiane, Variance et Gini
        """
        self._check_column(df, col_conso)
        
        stats = [
            ("Moyenne", self.moyenne_conso(df, col_conso)),
            ("Médiane", self.mediane_conso(df, col_conso)),
            ("Variance", self.variance_conso(df, col_conso)),
            ("Gini", self.calculer_gini(df, col_conso)),
        ]
        
        return pd.DataFrame(stats, columns=["Indicateur", "Valeur"])
    
    def resume_par_groupe(self, df: pd.DataFrame, col_conso: str, col_groupe: str) -> pd.DataFrame:
        """
        Calcule les statistiques principales par groupe.
        
        Returns:
            DataFrame avec une ligne par groupe et colonnes: Groupe, N, Moyenne, Médiane, Gini
        """
        self._check_column(df, col_conso)
        self._check_column(df, col_groupe)
        
        resultats = []
        for groupe, data in df.groupby(col_groupe):
            resultats.append({
                'Groupe': groupe,
                'N': len(data),
                'Moyenne': data[col_conso].mean(),
                'Médiane': data[col_conso].median(),
                'Écart-type': data[col_conso].std(),
                'Gini': self.calculer_gini(data, col_conso)
            })
        
        return pd.DataFrame(resultats)