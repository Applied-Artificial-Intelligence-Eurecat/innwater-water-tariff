import numpy as np
import pandas as pd

from src.initial.population_service import process_population_sample_df
from src.initial.schemas import *


def calculate_net_cost_service(num_subscribers: int, charge_fix: float, social_sampling_rate: float,
                               total_group_subscription_fee: float,
                               bcp_at_469: float, c_ep_bcp_hy_481: float,
                               costs_service_f7: float, fixed_costs: float):
    produit_per_abonne = 4 * (bcp_at_469 - total_group_subscription_fee) / social_sampling_rate
    r_variable = num_subscribers * produit_per_abonne
    r_fixes = num_subscribers * charge_fix * 4
    total_produit = r_fixes + r_variable
    social_sampling_rate_coef = num_subscribers / social_sampling_rate
    print("social", social_sampling_rate_coef)
    level_of_service = 4 * (social_sampling_rate_coef * c_ep_bcp_hy_481)
    variable_costs = level_of_service * costs_service_f7
    total_charges = variable_costs + fixed_costs
    net_sanitation = total_produit - total_charges
    return net_sanitation


from dataclasses import dataclass

from pydantic import BaseModel


class AffordabilityRow(BaseModel):
    ibt: float
    tbse: float


class AffordabilityGeneral(BaseModel):
    headcount_ratio: AffordabilityRow
    aparent_deficit: AffordabilityRow
    efective_deficit: AffordabilityRow
    gini_index: AffordabilityRow


@dataclass
class SimulationCalculator:
    simulation: SimulationPayload
    g1_df: pd.DataFrame
    g2_df: pd.DataFrame

    def __init__(self, simulation: SimulationPayload, g1_df: pd.DataFrame, g2_df: pd.DataFrame):
        self.simulation = simulation
        self.g1_df = g1_df
        self.g2_df = g2_df
        self.df = pd.concat([self.g1_df, self.g2_df])

    @property
    @property
    def base_sanitation_subscription_fee(self):
        return (self.df[self.is_sanitation] * self.simulation.tariff.sanitation.subscription).sum()

    def partie_base_c_et_fact(self):
        df = self.df
        df['Partie_Base_C_et_Fact O'] = (
                self.simulation.demand.coefficients.a0 + (
                self.df['nbpers'].apply(np.log) * self.simulation.demand.coefficients.a1
        ) +
                (self.df["SNWA"] * self.simulation.demand.coefficients.a2) +
                (self.df[
                     'Piscine (1 = oui)'] * self.simulation.demand.coefficients.a3 * self.simulation.demand.has_pool) +
                (self.df[
                     'Garden * Wheather'] * self.simulation.demand.coefficients.a4 * self.simulation.demand.has_garden)
        )
        self.df['Partie_Base_C_et_Fact Q'] = self.df['Partie_Base_C_et_Fact O'].apply(np.exp) * 90

        self.df['Partie_Base_C_et_Fact S'] = self.df['Partie_Base_C_et_Fact Q'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[1].threshold)

        self.df['Partie_Base_C_et_Fact T'] = (
                self.df['Partie_Base_C_et_Fact Q'] -
                self.simulation.tariff.drinking_water.usage_tiers[1].threshold
        ).clip(lower=0)

        self.df['Partie_Base_C_et_Fact U'] = self.df['Partie_Base_C_et_Fact T'].clip(
            upper=(
                    self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
                    self.simulation.tariff.drinking_water.usage_tiers[1].threshold
            )
        )
        self.df['Partie_Base_C_et_Fact W'] = (
                self.df['Partie_Base_C_et_Fact Q'] -
                self.simulation.tariff.drinking_water.usage_tiers[2].threshold
        ).clip(lower=0).clip(
            upper=(
                    self.simulation.tariff.drinking_water.usage_tiers[3].threshold -
                    self.simulation.tariff.drinking_water.usage_tiers[2].threshold
            )
        )
        self.df['Partie_Base_C_et_Fact X'] = (
                self.df['Partie_Base_C_et_Fact Q'] -
                self.simulation.tariff.drinking_water.usage_tiers[3].threshold
        ).clip(lower=0)
        self.df['Partie_Base_C_et_Fact AS'] = self.df['Partie_Base_C_et_Fact S'] * \
                                              self.simulation.potable_water_prix_tiers_ttc[0]
        self.df['Partie_Base_C_et_Fact AT'] = self.df['Partie_Base_C_et_Fact U'] * \
                                              self.simulation.potable_water_prix_tiers_ttc[1]
        self.df['Partie_Base_C_et_Fact AU'] = self.df['Partie_Base_C_et_Fact W'] * \
                                              self.simulation.potable_water_prix_tiers_ttc[2]
        self.df['Partie_Base_C_et_Fact AV'] = self.df['Partie_Base_C_et_Fact X'] * \
                                              self.simulation.potable_water_prix_tiers_ttc[3]
        self.df[
            'Partie_Base_C_et_Fact AX'] = self.simulation.tariff.drinking_water.subscription + self.simulation.potable_water_base_tva_per_unit_of_service + \
                                          self.df['Partie_Base_C_et_Fact AS'] + \
                                          self.df['Partie_Base_C_et_Fact AT'] + \
                                          self.df['Partie_Base_C_et_Fact AU'] + \
                                          self.df['Partie_Base_C_et_Fact AV']

        self.df['Partie_Base_C_et_Fact BT'] = self.df[self.is_sanitation] * self.simulation.sanitation_prix_base_ttc
        self.df['Partie_Base_C_et_Fact BU'] = self.df[self.is_sanitation] * self.df['Partie_Base_C_et_Fact S'] * \
                                              self.simulation.sanitation_prix_tiers_ttc[0]
        self.df['Partie_Base_C_et_Fact BV'] = self.df[self.is_sanitation] * self.df['Partie_Base_C_et_Fact U'] * \
                                              self.simulation.sanitation_prix_tiers_ttc[1]
        self.df['Partie_Base_C_et_Fact BW'] = self.df[self.is_sanitation] * self.df['Partie_Base_C_et_Fact W'] * \
                                              self.simulation.sanitation_prix_tiers_ttc[2]
        self.df['Partie_Base_C_et_Fact BX'] = self.df[self.is_sanitation] * self.df['Partie_Base_C_et_Fact X'] * \
                                              self.simulation.sanitation_prix_tiers_ttc[3]
        self.df['Partie_Base_C_et_Fact BZ'] = self.df['Partie_Base_C_et_Fact BT'] + \
                                              self.df['Partie_Base_C_et_Fact BU'] + \
                                              self.df['Partie_Base_C_et_Fact BV'] + \
                                              self.df['Partie_Base_C_et_Fact BW'] + \
                                              self.df['Partie_Base_C_et_Fact BX']

        self.df['Partie_Base_C_et_Fact DB'] = self.df['Partie_Base_C_et_Fact BZ'] + self.df['Partie_Base_C_et_Fact AX']

        self.df['Partie_Base_C_et_Fact DV'] = self.df['Partie_Base_C_et_Fact Q'] * \
                                              self.simulation.tbse_potable_water_variable_prix + self.simulation.tbse_potable_water_base_prix
        self.df['Partie_Base_C_et_Fact EJ'] = self.df[self.is_sanitation] * (
                self.df['Partie_Base_C_et_Fact Q'] * self.simulation.tbse_sanitation_variable_prix +
                self.simulation.tbse_sanitation_base_prix
        )
        self.df['Partie_Base_C_et_Fact EX'] = self.df['Partie_Base_C_et_Fact EJ'] + self.df['Partie_Base_C_et_Fact DV']

    def consumption_per_trimestre(self):
        df = self.df
        df['Partie Captive C et Fact C Total'] = (1 * self.simulation.demand.coefficients.a0) + (
                self.simulation.demand.coefficients.a1 * df['nbpers'].apply(np.log)) + (
                                                         self.simulation.demand.coefficients.a2 * df['SNWA']) + (
                                                         self.simulation.demand.coefficients.a3 * df[
                                                     'Piscine (1 = oui)']
                                                 ) + (self.simulation.demand.coefficients.a4 * df[
            'Garden * Wheather'])  # Partie Captive C et Fact P
        df['C_EP_BCP Terme ln Part Captive'] = ((df['Partie Captive C et Fact C Total'].apply(
            np.exp))).apply(np.log)  # C_EP_BCP J 23
        df['C_EP_BCP J'] = df['C_EP_BCP Terme ln Part Captive']

        df['C_PP E'] = df[self.is_sanitation]

        df['C_PP G'] = df['Revenu_Imputé_2']
        df['C_PP H'] = df['C_PP G'] / 30
        df['C_PP J'] = (1 - df['C_PP E']) * self.simulation.potable_water_prix_base_ttc + (
                df['C_PP E'] * self.simulation.epa_prix_base_ttc) / 90

        df['C_PP L'] = (1 - df['C_PP E']) * self.simulation.potable_water_nordin_tiers[-4] + (
                df['C_PP E'] * self.simulation.epa_nordin_tiers[-4])
        df['C_PP M'] = (1 - df['C_PP E']) * self.simulation.potable_water_nordin_tiers[-3] + (
                df['C_PP E'] * self.simulation.epa_nordin_tiers[-3])
        df['C_PP N'] = (1 - df['C_PP E']) * self.simulation.potable_water_nordin_tiers[-2] + (
                df['C_PP E'] * self.simulation.epa_nordin_tiers[-2])
        df['C_PP O'] = (1 - df['C_PP E']) * self.simulation.potable_water_nordin_tiers[-1] + (
                df['C_PP E'] * self.simulation.epa_nordin_tiers[-1])

        df['C_PP W'] = (df['C_PP H'] + df['C_PP J'] + df['C_PP N'] / 90)
        df['C_PP X'] = (df['C_PP H'] + df['C_PP J'] + df['C_PP O'] / 90)
        df['C_PP Z'] = (1 - df['C_PP E']) * self.simulation.potable_water_prix_tiers_ttc[-4] + (
                df['C_PP E'] * self.simulation.epa_prix_tiers_ttc[-4])
        df['C_PP AA'] = (1 - df['C_PP E']) * self.simulation.potable_water_prix_tiers_ttc[-3] + (
                df['C_PP E'] * self.simulation.epa_prix_tiers_ttc[-3])
        df['C_PP AB'] = (1 - df['C_PP E']) * self.simulation.potable_water_prix_tiers_ttc[-2] + (
                df['C_PP E'] * self.simulation.epa_prix_tiers_ttc[-2])
        df['C_PP AC'] = (1 - df['C_PP E']) * self.simulation.potable_water_prix_tiers_ttc[-1] + (
                df['C_PP E'] * self.simulation.epa_prix_tiers_ttc[-1])

        df['C_PP AF'] = self.simulation.demand.coefficients.a6 * (
                    df['C_PP H'] + df['C_PP J'] + df['C_PP L'] / 90).apply(np.log)
        df['C_PP AG'] = self.simulation.demand.coefficients.a5 * df['C_PP Z'].apply(np.log) + df['C_PP AF']

        df['C_PP AI'] = self.simulation.demand.coefficients.a6 * (
                    df['C_PP H'] + df['C_PP J'] + df['C_PP M'] / 90).apply(np.log)
        df['C_PP AJ'] = self.simulation.demand.coefficients.a5 * df['C_PP AA'].apply(np.log) + df['C_PP AI']

        df['C_PP AL'] = self.simulation.demand.coefficients.a6 * df['C_PP W'].apply(np.log)
        df['C_PP AM'] = self.simulation.demand.coefficients.a5 * df['C_PP AB'].apply(np.log) + df['C_PP AL']

        df['C_PP AO'] = self.simulation.demand.coefficients.a6 * df['C_PP X'].apply(np.log)
        df['C_PP AP'] = self.simulation.demand.coefficients.a5 * df['C_PP AC'].apply(np.log) + df['C_PP AO']

        df['C_PP AR'] = df['Partie Captive C et Fact C Total'] + df['C_PP AG']
        df['C_PP AS'] = df['C_PP AR'].apply(np.exp)
        df['C_PP AT'] = df['C_PP AS'] * 90
        df['C_PP AW'] = (df['Partie Captive C et Fact C Total'] + df['C_PP AJ']).apply(np.exp) * 90
        df['C_PP AZ'] = (df['Partie Captive C et Fact C Total'] + df['C_PP AM']).apply(np.exp) * 90
        df['C_PP BC'] = (df['Partie Captive C et Fact C Total'] + df['C_PP AP']).apply(np.exp) * 90

        df['C_PP BE'] = (
            (df['C_PP AT'] <= self.simulation.tariff.epa().usage_tiers[1].threshold).astype(float)
        )

        df['C_PP BF'] = (
                ((df['C_PP AW'] <= self.simulation.tariff.epa().usage_tiers[1].threshold) &
                 (df['C_PP AT'] > self.simulation.tariff.epa().usage_tiers[1].threshold)).astype(float) *
                (1 - df['C_PP BE'])
        )

        df['C_PP BG'] = (
                ((df['C_PP AW'] >= self.simulation.tariff.epa().usage_tiers[1].threshold) & (
                        df['C_PP AW'] <= self.simulation.tariff.epa().usage_tiers[2].threshold)).astype(
                    float) *
                (1 - df['C_PP BE']) *
                (1 - df['C_PP BF'])
        )

        df['C_PP BH'] = (
                ((df['C_PP AW'] > self.simulation.tariff.drinking_water.usage_tiers[2].threshold) &
                 (df['C_PP AZ'] < self.simulation.tariff.drinking_water.usage_tiers[2].threshold)).astype(float) *
                # Multiplication by all terms (1-XX)
                (1 - df['C_PP BE']) *
                (1 - df['C_PP BF']) *
                (1 - df['C_PP BG'])
        )

        df['C_PP BI'] = (
                ((df['C_PP AZ'] >= self.simulation.tariff.drinking_water.usage_tiers[2].threshold) &
                 (df['C_PP AZ'] <= self.simulation.tariff.drinking_water.usage_tiers[3].threshold)).astype(float) *
                # Multiplication by all terms (1-XX)
                (1 - df['C_PP BE']) *
                (1 - df['C_PP BF']) *
                (1 - df['C_PP BG']) *
                (1 - df['C_PP BH'])
        )

        df['C_PP BJ'] = (
                ((df['C_PP AZ'] > self.simulation.tariff.drinking_water.usage_tiers[3].threshold) & (
                        df['C_PP BC'] < self.simulation.tariff.drinking_water.usage_tiers[3].threshold)).astype(
                    float) *
                (1 - df['C_PP BE']) *
                (1 - df['C_PP BF']) *
                (1 - df['C_PP BG']) *
                (1 - df['C_PP BH']) *
                (1 - df['C_PP BI']) *
                (1 - df['C_PP BH'])
        )

        df['C_PP BK'] = (df['C_PP BC'] > self.simulation.tariff.drinking_water.usage_tiers[3].threshold).astype(
            float) * (1 - df['C_PP BE']) * (1 - df['C_PP BF']) * (
                                1 - df['C_PP BG']) * (1 - df['C_PP BH']) * (1 - df['C_PP BI']) * (1 - df['C_PP BJ'])

        # =BE10*AT10+BF10*$H$4+BG10*AW10+BH10*$H$5+BI10*AZ10+BJ10*H$6+BK10*BC10
        df['C_PP BM'] = df['C_PP BE'] * df['C_PP AT'] + df['C_PP BF'] * \
                        self.simulation.tariff.drinking_water.usage_tiers[1].threshold + df['C_PP BG'] * df['C_PP AW'] + \
                        df['C_PP BH'] * self.simulation.tariff.drinking_water.usage_tiers[2].threshold + df['C_PP BI'] * \
                        df['C_PP AZ'] + df['C_PP BJ'] * self.simulation.tariff.drinking_water.usage_tiers[3].threshold + \
                        df['C_PP BK'] * df['C_PP BC']

        self.facture_ibt(df)
        self.c_taylor(df)
        self.c_ep_bcp(df)
        return df

    def facture_ibt(self, df):
        df['Facture IBT C PP F'] = df['C_PP BM'].apply(
            lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[1].threshold))
        df['Facture IBT C PP G'] = df['C_PP BM'].apply(
            lambda x: max(x - self.simulation.tariff.drinking_water.usage_tiers[1].threshold, 0))
        df['Facture IBT C PP H'] = df['Facture IBT C PP G'].apply(lambda x: min(x,
                                                                                self.simulation.tariff.drinking_water.usage_tiers[
                                                                                    -2].threshold -
                                                                                self.simulation.tariff.drinking_water.usage_tiers[
                                                                                    -3].threshold))
        df['Facture IBT C PP I'] = (
                df['C_PP BM'] - self.simulation.tariff.drinking_water.usage_tiers[-2].threshold).apply(
            lambda x: max(x, 0)
        )
        df['Facture IBT C PP J'] = df['Facture IBT C PP I'].apply(lambda x: min(x, (
                self.simulation.tariff.drinking_water.usage_tiers[-1].threshold -
                self.simulation.tariff.drinking_water.usage_tiers[-2].threshold)))
        df['Facture IBT C PP K'] = (
                df['C_PP BM'] - self.simulation.tariff.drinking_water.usage_tiers[-1].threshold).apply(
            lambda x: max(x, 0))
        df['Facture IBT C PP M'] = self.simulation.potable_water_prix_base_ttc
        df['Facture IBT C PP N'] = df['Facture IBT C PP F'] * self.simulation.potable_water_prix_tiers_ttc[0]
        df['Facture IBT C PP O'] = df['Facture IBT C PP H'] * self.simulation.potable_water_prix_tiers_ttc[1]
        df['Facture IBT C PP P'] = df['Facture IBT C PP J'] * self.simulation.potable_water_prix_tiers_ttc[2]
        df['Facture IBT C PP Q'] = df['Facture IBT C PP K'] * self.simulation.potable_water_prix_tiers_ttc[3]
        df['Facture IBT C PP R'] = df['Facture IBT C PP M'] + df['Facture IBT C PP N'] + df['Facture IBT C PP O'] + \
                                   df['Facture IBT C PP P'] + df['Facture IBT C PP Q']
        df['Facture IBT C PP T'] = df['Facture IBT C PP F'] * self.simulation.primitives.taxation.drinking_water.fees
        df['Facture IBT C PP U'] = df['Facture IBT C PP H'] * self.simulation.primitives.taxation.drinking_water.fees
        df['Facture IBT C PP V'] = df['Facture IBT C PP J'] * self.simulation.primitives.taxation.drinking_water.fees
        df['Facture IBT C PP W'] = df['Facture IBT C PP K'] * self.simulation.primitives.taxation.drinking_water.fees
        df['Facture IBT C PP X'] = (df['Facture IBT C PP F'] + df['Facture IBT C PP H'] + \
                                    df['Facture IBT C PP J'] + df[
                                        'Facture IBT C PP K']) * self.simulation.primitives.taxation.drinking_water.fees
        df['Facture IBT C PP Y'] = self.simulation.potable_water_base_tva_per_unit_of_service
        df['Facture IBT C PP Z'] = df['Facture IBT C PP F'] * \
                                   self.simulation.potable_water_fees_tva_per_unit_of_service[-4]
        Facture_IBT_C_PP_AA = df['Facture IBT C PP H'] * \
                              self.simulation.potable_water_fees_tva_per_unit_of_service[-3]
        Facture_IBT_C_PP_AB = df['Facture IBT C PP J'] * \
                              self.simulation.potable_water_fees_tva_per_unit_of_service[-2]
        df['Facture IBT C PP AC'] = df['Facture IBT C PP K'] * \
                                    self.simulation.potable_water_fees_tva_per_unit_of_service[-1]
        df['Facture IBT C PP AD'] = df['Facture IBT C PP Y'] + df['Facture IBT C PP Z'] + Facture_IBT_C_PP_AA + \
                                    Facture_IBT_C_PP_AB + df['Facture IBT C PP AC']
        df['Facture IBT C PP AE'] = df['Facture IBT C PP M'] + df['Facture IBT C PP Y']
        df['Facture IBT C PP AF'] = df['Facture IBT C PP N'] + df['Facture IBT C PP T'] + df['Facture IBT C PP Z']
        df['Facture IBT C PP AG'] = df['Facture IBT C PP O'] + df['Facture IBT C PP U'] + Facture_IBT_C_PP_AA
        df['Facture IBT C PP AH'] = df['Facture IBT C PP P'] + df['Facture IBT C PP V'] + Facture_IBT_C_PP_AB
        df['Facture IBT C PP AI'] = df['Facture IBT C PP Q'] + df['Facture IBT C PP W'] + df['Facture IBT C PP AC']
        df['Facture IBT C PP AK'] = df['Facture IBT C PP AI'] + df['Facture IBT C PP AH'] + df['Facture IBT C PP AG'] + \
                                    df['Facture IBT C PP AF'] + df['Facture IBT C PP AE']
        df['Facture IBT C PP AO'] = df[self.is_sanitation] * self.simulation.tariff.sanitation.subscription
        df['Facture IBT C PP AP'] = df[self.is_sanitation] * df['Facture IBT C PP F'] * \
                                    self.simulation.tariff.sanitation.usage_tiers[0].price
        df['Facture IBT C PP AQ'] = df[self.is_sanitation] * df['Facture IBT C PP H'] * \
                                    self.simulation.tariff.sanitation.usage_tiers[1].price
        df['Facture IBT C PP AR'] = df[self.is_sanitation] * df['Facture IBT C PP J'] * \
                                    self.simulation.tariff.sanitation.usage_tiers[2].price
        df['Facture IBT C PP AS'] = df[self.is_sanitation] * df['Facture IBT C PP K'] * \
                                    self.simulation.tariff.sanitation.usage_tiers[3].price
        df['Facture IBT C PP AT'] = df['Facture IBT C PP AO'] + df['Facture IBT C PP AP'] + df['Facture IBT C PP AQ'] + \
                                    df['Facture IBT C PP AR'] + df['Facture IBT C PP AS']
        df['Facture IBT C PP AV'] = df[self.is_sanitation] * df[
            'Facture IBT C PP F'] * self.simulation.primitives.taxation.sanitation.fees
        df['Facture IBT C PP AW'] = df[self.is_sanitation] * df[
            'Facture IBT C PP H'] * self.simulation.primitives.taxation.sanitation.fees
        df['Facture IBT C PP AX'] = df[self.is_sanitation] * df[
            'Facture IBT C PP J'] * self.simulation.primitives.taxation.sanitation.fees
        df['Facture IBT C PP AY'] = df[self.is_sanitation] * df[
            'Facture IBT C PP K'] * self.simulation.primitives.taxation.sanitation.fees
        df['Facture IBT C PP AZ'] = df['Facture IBT C PP AV'] + df['Facture IBT C PP AW'] + \
                                    df['Facture IBT C PP AX'] + df['Facture IBT C PP AY']
        df['Facture IBT C PP BA'] = df[self.is_sanitation] * self.simulation.sanitation_base_tva_per_unit_of_service
        df['Facture IBT C PP BB'] = df[self.is_sanitation] * self.simulation.sanitation_fees_tva_per_unit_of_service[
            0] * df['Facture IBT C PP F']
        df['Facture IBT C PP BC'] = df[self.is_sanitation] * self.simulation.sanitation_fees_tva_per_unit_of_service[
            1] * df['Facture IBT C PP H']
        df['Facture IBT C PP BD'] = df[self.is_sanitation] * self.simulation.sanitation_fees_tva_per_unit_of_service[
            2] * df['Facture IBT C PP J']
        df['Facture IBT C PP BE'] = df[self.is_sanitation] * self.simulation.sanitation_fees_tva_per_unit_of_service[
            3] * df['Facture IBT C PP K']
        df['Facture IBT C PP BF'] = df['Facture IBT C PP BA'] + df['Facture IBT C PP BB'] + df['Facture IBT C PP BC'] + \
                                    df['Facture IBT C PP BD'] + df['Facture IBT C PP BE']
        df['Facture IBT C PP BG'] = df['Facture IBT C PP AO'] + df['Facture IBT C PP BA']
        df['Facture IBT C PP BH'] = df['Facture IBT C PP AP'] + df['Facture IBT C PP AV'] + df['Facture IBT C PP BB']
        df['Facture IBT C PP BI'] = df['Facture IBT C PP AQ'] + df['Facture IBT C PP AW'] + df['Facture IBT C PP BC']
        df['Facture IBT C PP BJ'] = df['Facture IBT C PP AR'] + df['Facture IBT C PP AX'] + df['Facture IBT C PP BD']
        df['Facture IBT C PP BK'] = df['Facture IBT C PP AS'] + df['Facture IBT C PP AY'] + df['Facture IBT C PP BE']
        df['Facture IBT C PP BM'] = df['Facture IBT C PP BK'] + df['Facture IBT C PP BJ'] + df['Facture IBT C PP BI'] + \
                                    df['Facture IBT C PP BH'] + df['Facture IBT C PP BG']

        df['Facture IBT C PP CO'] = df['Facture IBT C PP AK'] + df['Facture IBT C PP BM']
        df['Taylor Abonnement EP / EPA'] = df['Facture IBT C PP AE'] + df[
            'Facture IBT C PP BG']  # Facture_IBT_C_PP '!CI11
        df['Taylor Terme ln Revenu'] = self.calculate_taylor_rf_jour(df).apply(
            np.log) * self.simulation.demand.coefficients.a6
        df['Taylor Montant de la Facture EP/EPA'] = df['Facture IBT C PP CO']  # Facture_IBT_C_PP '!CO11

    def c_taylor(self, df):

        df['Taylor CV Consom'] = df['Taylor Montant de la Facture EP/EPA'] - df[
            'Taylor Abonnement EP / EPA']  # C Taylor F20
        df['Taylor CVM Consom'] = df['Taylor CV Consom'] / df['C_PP BM']  # C_Taylor F21
        df['Taylor Terme ln Prix moyen'] = self.simulation.demand.coefficients.a5 * df['Taylor CVM Consom'].apply(
            np.log)
        df['Taylor Terme ln Part Captive'] = df['Partie Captive C et Fact C Total']  # Be careful with this!
        df['C Taylor Somme LN'] = df['Taylor Terme ln Revenu'] + df['Taylor Terme ln Prix moyen'] + df[
            'Taylor Terme ln Part Captive']  # C Taylor O
        df['Consom Taylor Jour'] = df['C Taylor Somme LN'].apply(np.exp)
        df['C_Taylor Q'] = df['Consom Taylor Jour'] * 90

    def c_ep_bcp(self, df):
        df['C_EP_BCP D'] = df['C_PP BM']
        df['C_EP_BCP E'] = df['C_Taylor Q']  # C_Taylor Q20
        df['C_EP_BCP H'] = df['C_EP_BCP D'] / 90  # C_EP_BCP H
        df['C_EP_BCP K'] = df['C_EP_BCP H'].apply(np.log)
        df['C_EP_BCP I'] = df['C_EP_BCP E'] / 90
        # C_EP_BCP
        df['C_EP_BCP I'] = df['C_EP_BCP E'] / 90
        df['C_EP_BCP L'] = np.log(df['C_EP_BCP I'])
        df['C_EP_BCP M'] = 100 * (df['C_EP_BCP L'] - df['C_EP_BCP K'])
        df['C_EP_BCP N'] = (self.simulation.demand.k * df['C_EP_BCP K'] +
                            (1 - self.simulation.demand.k) * df['C_EP_BCP L'])
        df['C_EP_BCP O'] = np.exp(df['C_EP_BCP N'])
        df['C_EP_BCP P'] = 90 * df['C_EP_BCP O']
        df['C_EP_BCP R'] = np.minimum(df['C_EP_BCP P'],
                                      self.simulation.tariff.drinking_water.usage_tiers[1].threshold)
        df['C_EP_BCP S'] = np.maximum(df['C_EP_BCP P'] - self.simulation.tariff.drinking_water.usage_tiers[1].threshold,
                                      0)
        df['C_EP_BCP T'] = np.minimum(df['C_EP_BCP S'],
                                      self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
                                      self.simulation.tariff.drinking_water.usage_tiers[1].threshold)
        df['C_EP_BCP U'] = np.maximum(df['C_EP_BCP P'] - self.simulation.tariff.drinking_water.usage_tiers[2].threshold,
                                      0)
        df['C_EP_BCP V'] = np.minimum(df['C_EP_BCP U'],
                                      self.simulation.tariff.drinking_water.usage_tiers[3].threshold -
                                      self.simulation.tariff.drinking_water.usage_tiers[2].threshold)
        df['C_EP_BCP W'] = np.maximum(df['C_EP_BCP P'] - self.simulation.tariff.drinking_water.usage_tiers[3].threshold,
                                      0)
        df['C_EP_BCP Y'] = (1 - df[self.is_sanitation]) * (
                self.simulation.tariff.drinking_water.subscription +
                df['C_EP_BCP R'] * self.simulation.tariff.drinking_water.usage_tiers[0].price +
                df['C_EP_BCP T'] * self.simulation.tariff.drinking_water.usage_tiers[1].price +
                df['C_EP_BCP V'] * self.simulation.tariff.drinking_water.usage_tiers[2].price +
                df['C_EP_BCP W'] * self.simulation.tariff.drinking_water.usage_tiers[3].price) + \
                           df[self.is_sanitation] * (
                                   self.simulation.tariff.epa().subscription +
                                   df['C_EP_BCP R'] * self.simulation.tariff.epa().usage_tiers[0].price +
                                   df['C_EP_BCP T'] * self.simulation.tariff.epa().usage_tiers[1].price +
                                   df['C_EP_BCP V'] * self.simulation.tariff.epa().usage_tiers[2].price +
                                   df['C_EP_BCP W'] * self.simulation.tariff.epa().usage_tiers[3].price)
        df['C_EP_BCP Z'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP P'] * self.simulation.primitives.taxation.drinking_water.fees) + \
                           df[self.is_sanitation] * (df['C_EP_BCP P'] * self.simulation.primitives.taxation.epa().fees)
        df['C_EP_BCP AA'] = (1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service + df['C_EP_BCP R'] *
                self.simulation.potable_water_fees_tva_per_unit_of_service[0] + df['C_EP_BCP T'] *
                self.simulation.potable_water_fees_tva_per_unit_of_service[1] + df['C_EP_BCP V'] *
                self.simulation.potable_water_fees_tva_per_unit_of_service[2] + df['C_EP_BCP W'] *
                self.simulation.potable_water_fees_tva_per_unit_of_service[3]) + \
                            df[self.is_sanitation] * (self.simulation.epa_base_tva_per_unit_of_service +
                                                      df['C_EP_BCP R'] *
                                                      self.simulation.epa_fees_tva_per_unit_of_service[0] +
                                                      df['C_EP_BCP T'] *
                                                      self.simulation.epa_fees_tva_per_unit_of_service[1] +
                                                      df['C_EP_BCP V'] *
                                                      self.simulation.epa_fees_tva_per_unit_of_service[2] +
                                                      df['C_EP_BCP W'] *
                                                      self.simulation.epa_fees_tva_per_unit_of_service[3])
        df['C_EP_BCP AB'] = df['C_EP_BCP Y'] + df['C_EP_BCP Z'] + df['C_EP_BCP AA']
        df['C_EP_BCP AD'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP AB'] - self.simulation.potable_water_prix_base_ttc
        ) + df[self.is_sanitation] * (df['C_EP_BCP AB'] - self.simulation.epa_prix_base_ttc)
        df['C_EP_BCP AE'] = df['C_EP_BCP AD'] / df['C_EP_BCP P']
        df['C_EP_BCP AG'] = self.calculate_taylor_rf_jour(df)
        df['C_EP_BCP AH'] = self.simulation.demand.coefficients.a6 * np.log(df['C_EP_BCP AG'])
        df['C_EP_BCP AI'] = self.simulation.demand.coefficients.a5 * np.log(df['C_EP_BCP AE'])
        df['C_EP_BCP AK'] = df['C_EP_BCP J'] + df['C_EP_BCP AI'] + df['C_EP_BCP AH']
        df['C_EP_BCP AL'] = (self.simulation.demand.k * df['C_EP_BCP K'] +
                             (1 - self.simulation.demand.k) * df['C_EP_BCP AK'])
        df['C_EP_BCP AM'] = np.exp(df['C_EP_BCP AL'])
        df['C_EP_BCP AN'] = 90 * df['C_EP_BCP AM']
        df['C_EP_BCP AP'] = df['C_EP_BCP AN'].apply(
            lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[1].threshold))
        df['C_EP_BCP AQ'] = df['C_EP_BCP AN'].apply(
            lambda x: max(x - self.simulation.tariff.drinking_water.usage_tiers[1].threshold, 0))
        df['C_EP_BCP AR'] = df['C_EP_BCP AQ'].apply(
            lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
                          self.simulation.tariff.drinking_water.usage_tiers[
                              1].threshold)
        )
        df['C_EP_BCP AS'] = df['C_EP_BCP AN'].apply(
            lambda x: max(x - self.simulation.tariff.drinking_water.usage_tiers[2].threshold, 0))
        df['C_EP_BCP AT'] = df['C_EP_BCP AS'].apply(
            lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[3].threshold -
                          self.simulation.tariff.drinking_water.usage_tiers[
                              2].threshold)
        )
        df['C_EP_BCP AU'] = df['C_EP_BCP AN'].apply(
            lambda x: max(x - self.simulation.tariff.drinking_water.usage_tiers[3].threshold, 0))
        df['C_EP_BCP AW'] = (1 - df[self.is_sanitation]) * (
                self.simulation.tariff.drinking_water.subscription +
                df['C_EP_BCP AP'] * self.simulation.tariff.drinking_water.usage_tiers[0].price +
                df['C_EP_BCP AR'] * self.simulation.tariff.drinking_water.usage_tiers[1].price +
                df['C_EP_BCP AT'] * self.simulation.tariff.drinking_water.usage_tiers[2].price +
                df['C_EP_BCP AU'] * self.simulation.tariff.drinking_water.usage_tiers[3].price
        ) + df[self.is_sanitation] * (
                                    self.simulation.tariff.epa().subscription +
                                    df['C_EP_BCP AP'] * self.simulation.tariff.epa().usage_tiers[0].price +
                                    df['C_EP_BCP AR'] * self.simulation.tariff.epa().usage_tiers[1].price +
                                    df['C_EP_BCP AT'] * self.simulation.tariff.epa().usage_tiers[2].price +
                                    df['C_EP_BCP AU'] * self.simulation.tariff.epa().usage_tiers[3].price
                            )
        df['C_EP_BCP AX'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP AN'] * self.simulation.primitives.taxation.drinking_water.fees
        ) + df[self.is_sanitation] * (
                                    df['C_EP_BCP AN'] * self.simulation.primitives.taxation.epa().fees
                            )
        df['C_EP_BCP AY'] = (1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service +
                df['C_EP_BCP AP'] * self.simulation.potable_water_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP AR'] * self.simulation.potable_water_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP AT'] * self.simulation.potable_water_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP AU'] * self.simulation.potable_water_fees_tva_per_unit_of_service[3]
        ) + df[self.is_sanitation] * (
                                    self.simulation.epa_base_tva_per_unit_of_service +
                                    df['C_EP_BCP AP'] * self.simulation.epa_fees_tva_per_unit_of_service[0] +
                                    df['C_EP_BCP AR'] * self.simulation.epa_fees_tva_per_unit_of_service[1] +
                                    df['C_EP_BCP AT'] * self.simulation.epa_fees_tva_per_unit_of_service[2] +
                                    df['C_EP_BCP AU'] * self.simulation.epa_fees_tva_per_unit_of_service[3]
                            )
        df['C_EP_BCP AZ'] = df['C_EP_BCP AW'] + df['C_EP_BCP AX'] + df['C_EP_BCP AY']
        df['C_EP_BCP BB'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP AZ'] - self.simulation.potable_water_prix_base_ttc) + df[self.is_sanitation] * (
                                    df['C_EP_BCP AZ'] - self.simulation.epa_prix_base_ttc)
        df['C_EP_BCP BC'] = df['C_EP_BCP BB'] / df['C_EP_BCP AN']
        df['C_EP_BCP BE'] = self.calculate_taylor_rf_jour(df)
        df['C_EP_BCP BF'] = self.simulation.demand.coefficients.a6 * np.log(df['C_EP_BCP BE'])
        df['C_EP_BCP BG'] = self.simulation.demand.coefficients.a5 * np.log(df['C_EP_BCP BC'])
        df['C_EP_BCP BI'] = df['C_EP_BCP J'] + df['C_EP_BCP BG'] + df['C_EP_BCP BF']
        df['C_EP_BCP BJ'] = self.simulation.demand.k * df['C_EP_BCP K'] + (
                1 - self.simulation.demand.k) * df['C_EP_BCP BI']
        df['C_EP_BCP BK'] = df['C_EP_BCP BJ'].apply(np.exp)
        df['C_EP_BCP BL'] = 90 * df['C_EP_BCP BK']
        df['C_EP_BCP BN'] = df['C_EP_BCP BL'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[-3].threshold
        )
        df['C_EP_BCP BO'] = (df['C_EP_BCP BL'] - self.simulation.tariff.drinking_water.usage_tiers[-3].threshold).clip(
            lower=0)
        df['C_EP_BCP BP'] = df['C_EP_BCP BO'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[-2].threshold -
                  self.simulation.tariff.drinking_water.usage_tiers[-3].threshold
        )
        df['C_EP_BCP BQ'] = (df['C_EP_BCP BL'] - self.simulation.tariff.drinking_water.usage_tiers[-2].threshold).clip(
            lower=0)
        df['C_EP_BCP BR'] = df['C_EP_BCP BQ'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[-1].threshold -
                  self.simulation.tariff.drinking_water.usage_tiers[-2].threshold
        )
        df['C_EP_BCP BS'] = (df['C_EP_BCP BL'] - self.simulation.tariff.drinking_water.usage_tiers[-1].threshold).clip(
            lower=0)
        df['C_EP_BCP BU'] = (1 - df[self.is_sanitation]) * (
                self.simulation.tariff.drinking_water.subscription +
                df['C_EP_BCP BN'] * self.simulation.tariff.drinking_water.usage_tiers[0].price +
                df['C_EP_BCP BP'] * self.simulation.tariff.drinking_water.usage_tiers[1].price +
                df['C_EP_BCP BR'] * self.simulation.tariff.drinking_water.usage_tiers[2].price +
                df['C_EP_BCP BS'] * self.simulation.tariff.drinking_water.usage_tiers[3].price
        ) + (df[self.is_sanitation] * (
                self.simulation.tariff.epa().subscription +
                df['C_EP_BCP BN'] * self.simulation.tariff.epa().usage_tiers[0].price +
                df['C_EP_BCP BP'] * self.simulation.tariff.epa().usage_tiers[1].price +
                df['C_EP_BCP BR'] * self.simulation.tariff.epa().usage_tiers[2].price +
                df['C_EP_BCP BS'] * self.simulation.tariff.epa().usage_tiers[3].price
        ))
        df['C_EP_BCP BV'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP BL'] * self.simulation.primitives.taxation.drinking_water.fees
        ) + (df[self.is_sanitation] * (
                df['C_EP_BCP BL'] * self.simulation.primitives.taxation.epa().fees
        ))
        df['C_EP_BCP BW'] = (1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service +
                df['C_EP_BCP BN'] * self.simulation.potable_water_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP BP'] * self.simulation.potable_water_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP BR'] * self.simulation.potable_water_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP BS'] * self.simulation.potable_water_fees_tva_per_unit_of_service[3]
        ) + (df[self.is_sanitation] * (
                self.simulation.epa_base_tva_per_unit_of_service +
                df['C_EP_BCP BN'] * self.simulation.epa_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP BP'] * self.simulation.epa_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP BR'] * self.simulation.epa_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP BS'] * self.simulation.epa_fees_tva_per_unit_of_service[3]
        ))
        df['C_EP_BCP BX'] = df['C_EP_BCP BU'] + df['C_EP_BCP BV'] + df['C_EP_BCP BW']
        # =(1-$B23)*(BX23-$G$2)+$B23*(BX23-$G$9)
        df['C_EP_BCP BZ'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP BX'] - self.simulation.potable_water_prix_base_ttc
        ) + df[self.is_sanitation] * (
                                    df['C_EP_BCP BX'] - self.simulation.epa_prix_base_ttc
                            )
        df['C_EP_BCP CA'] = df['C_EP_BCP BZ'] / df['C_EP_BCP BL']
        df['C_EP_BCP CC'] = self.calculate_taylor_rf_jour(df)
        df['C_EP_BCP CD'] = self.simulation.demand.coefficients.a6 * df['C_EP_BCP CC'].apply(np.log)
        df['C_EP_BCP CE'] = self.simulation.demand.coefficients.a5 * df['C_EP_BCP CA'].apply(np.log)
        df['C_EP_BCP CG'] = df['C_EP_BCP J'] + df['C_EP_BCP CE'] + df['C_EP_BCP CD']
        df['C_EP_BCP CH'] = (self.simulation.demand.k * df['C_EP_BCP K'] +
                             (1 - self.simulation.demand.k) * df['C_EP_BCP CG'])
        df['C_EP_BCP CI'] = np.exp(df['C_EP_BCP CH'])
        df['C_EP_BCP CJ'] = 90 * df['C_EP_BCP CI']
        df['C_EP_BCP CL'] = df['C_EP_BCP CJ'].clip(upper=self.simulation.tariff.drinking_water.usage_tiers[1].threshold)
        df['C_EP_BCP CM'] = (df['C_EP_BCP CJ'] - self.simulation.tariff.drinking_water.usage_tiers[1].threshold).clip(
            lower=0)
        df['C_EP_BCP CN'] = df['C_EP_BCP CM'].clip(
            upper=(self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
                   self.simulation.tariff.drinking_water.usage_tiers[1].threshold))
        df['C_EP_BCP CO'] = (df['C_EP_BCP CJ'] - self.simulation.tariff.drinking_water.usage_tiers[2].threshold).clip(
            lower=0)
        df['C_EP_BCP CP'] = df['C_EP_BCP CO'].clip(
            upper=(self.simulation.tariff.drinking_water.usage_tiers[3].threshold -
                   self.simulation.tariff.drinking_water.usage_tiers[2].threshold))
        df['C_EP_BCP CQ'] = (df['C_EP_BCP CJ'] - self.simulation.tariff.drinking_water.usage_tiers[3].threshold).clip(
            lower=0)
        # =(1-$B23)*($C$2+CL23*$C$3+CN23*$C$4+CP23*$C$5+CQ23*$C$6)+$B23*($C$9+CL23*$C$10+CN23*$C$11+CP23*$C$12+CQ23*$C$13)
        df['C_EP_BCP CS'] = (1 - df[self.is_sanitation]) * (
                self.simulation.tariff.drinking_water.subscription +
                self.simulation.tariff.drinking_water.usage_tiers[0].price * df['C_EP_BCP CL'] +
                self.simulation.tariff.drinking_water.usage_tiers[1].price * df['C_EP_BCP CN'] +
                self.simulation.tariff.drinking_water.usage_tiers[2].price * df['C_EP_BCP CP'] +
                self.simulation.tariff.drinking_water.usage_tiers[3].price * df['C_EP_BCP CQ']
        ) + (df[self.is_sanitation] * (
                self.simulation.tariff.epa().subscription +
                self.simulation.tariff.epa().usage_tiers[0].price * df['C_EP_BCP CL'] +
                self.simulation.tariff.epa().usage_tiers[1].price * df['C_EP_BCP CN'] +
                self.simulation.tariff.epa().usage_tiers[2].price * df['C_EP_BCP CP'] +
                self.simulation.tariff.epa().usage_tiers[3].price * df['C_EP_BCP CQ']
        ))
        # =(1-$B23)*(CJ23*$K$1)+$B23*(CJ23*$K$8)
        df['C_EP_BCP CT'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP CJ'] * self.simulation.primitives.taxation.drinking_water.fees
        ) + df[self.is_sanitation] * (df['C_EP_BCP CJ'] * self.simulation.primitives.taxation.epa().fees)
        # =(1-$B23)*($F$2+CL23*$F$3+CN23*$F$4+CP23*$F$5+CQ23*$F$6)+$B23*($F$9+CL23*$F$10+CN23*$F$11+CP23*$F$12+CQ23*$F$13)
        df['C_EP_BCP CU'] = (1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service +
                self.simulation.potable_water_fees_tva_per_unit_of_service[0] * df['C_EP_BCP CL'] +
                self.simulation.potable_water_fees_tva_per_unit_of_service[1] * df['C_EP_BCP CN'] +
                self.simulation.potable_water_fees_tva_per_unit_of_service[2] * df['C_EP_BCP CP'] +
                self.simulation.potable_water_fees_tva_per_unit_of_service[3] * df['C_EP_BCP CQ']
        ) + (df[self.is_sanitation] * (
                self.simulation.epa_base_tva_per_unit_of_service +
                self.simulation.epa_fees_tva_per_unit_of_service[0] * df['C_EP_BCP CL'] +
                self.simulation.epa_fees_tva_per_unit_of_service[1] * df['C_EP_BCP CN'] +
                self.simulation.epa_fees_tva_per_unit_of_service[2] * df['C_EP_BCP CP'] +
                self.simulation.epa_fees_tva_per_unit_of_service[3] * df['C_EP_BCP CQ']
        ))
        df['C_EP_BCP CV'] = df['C_EP_BCP CS'] + df['C_EP_BCP CT'] + df['C_EP_BCP CU']
        df['C_EP_BCP CX'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP CV'] - self.simulation.potable_water_prix_base_ttc) + df[self.is_sanitation] * (
                                    df['C_EP_BCP CV'] - self.simulation.epa_prix_base_ttc)
        df['C_EP_BCP CY'] = df['C_EP_BCP CX'] / df['C_EP_BCP CJ']
        df['C_EP_BCP DA'] = self.calculate_taylor_rf_jour(df)
        df['C_EP_BCP DB'] = self.simulation.demand.coefficients.a6 * df['C_EP_BCP DA'].apply(np.log)
        df['C_EP_BCP DC'] = self.simulation.demand.coefficients.a5 * df['C_EP_BCP CY'].apply(np.log)
        df['C_EP_BCP DE'] = df['C_EP_BCP J'] + df['C_EP_BCP DC'] + df['C_EP_BCP DB']
        df['C_EP_BCP DF'] = self.simulation.demand.k * df['C_EP_BCP K'] + (
                1 - self.simulation.demand.k) * df['C_EP_BCP DE']
        df['C_EP_BCP DG'] = df['C_EP_BCP DF'].apply(np.exp)
        df['C_EP_BCP DH'] = df['C_EP_BCP DG'] * 90
        df['C_EP_BCP DJ'] = df['C_EP_BCP DH'].apply(
            lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[1].threshold))
        df['C_EP_BCP DK'] = (df['C_EP_BCP DH'] - self.simulation.tariff.drinking_water.usage_tiers[1].threshold).apply(
            lambda x: max(x, 0))
        df['C_EP_BCP DL'] = df['C_EP_BCP DK'].apply(
            lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
                          self.simulation.tariff.drinking_water.usage_tiers[1].threshold))
        df['C_EP_BCP DM'] = (df['C_EP_BCP DH'] - self.simulation.tariff.drinking_water.usage_tiers[2].threshold).apply(
            lambda x: max(x, 0))
        df['C_EP_BCP DN'] = df['C_EP_BCP DM'].apply(lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[
            3].threshold - self.simulation.tariff.drinking_water.usage_tiers[2].threshold))
        df['C_EP_BCP DO'] = (df['C_EP_BCP DH'] - self.simulation.tariff.drinking_water.usage_tiers[3].threshold).apply(
            lambda x: max(x, 0))
        # =(1-$B23)*($C$2+DJ23*$C$3+DL23*$C$4+DN23*$C$5+DO23*$C$6)+$B23*($C$9+DJ23*$C$10+DL23*$C$11+DN23*$C$12+DO23*$C$13)
        df['C_EP_BCP DQ'] = (1 - df[self.is_sanitation]) * (self.simulation.tariff.drinking_water.subscription +
                                                            self.simulation.tariff.drinking_water.usage_tiers[0].price *
                                                            df[
                                                                'C_EP_BCP DJ'] +
                                                            self.simulation.tariff.drinking_water.usage_tiers[1].price *
                                                            df[
                                                                'C_EP_BCP DL'] +
                                                            self.simulation.tariff.drinking_water.usage_tiers[2].price *
                                                            df[
                                                                'C_EP_BCP DN'] +
                                                            self.simulation.tariff.drinking_water.usage_tiers[3].price *
                                                            df[
                                                                'C_EP_BCP DO']) + (
                                    df[self.is_sanitation] * (self.simulation.tariff.epa().subscription +
                                                              self.simulation.tariff.epa().usage_tiers[0].price * df[
                                                                  'C_EP_BCP DJ'] +
                                                              self.simulation.tariff.epa().usage_tiers[1].price * df[
                                                                  'C_EP_BCP DL'] +
                                                              self.simulation.tariff.epa().usage_tiers[2].price * df[
                                                                  'C_EP_BCP DN'] +
                                                              self.simulation.tariff.epa().usage_tiers[3].price * df[
                                                                  'C_EP_BCP DO']))
        df['C_EP_BCP DR'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP DH'] * self.simulation.primitives.taxation.drinking_water.fees) + (
                                    df[self.is_sanitation] * (
                                    df['C_EP_BCP DH'] * (self.simulation.primitives.taxation.epa().fees)))
        df['C_EP_BCP DS'] = (1 - df[self.is_sanitation]) * (self.simulation.potable_water_base_tva_per_unit_of_service +
                                                            self.simulation.potable_water_fees_tva_per_unit_of_service[
                                                                0] * df['C_EP_BCP DJ'] +
                                                            self.simulation.potable_water_fees_tva_per_unit_of_service[
                                                                1] * df['C_EP_BCP DL'] +
                                                            self.simulation.potable_water_fees_tva_per_unit_of_service[
                                                                2] * df['C_EP_BCP DN'] +
                                                            self.simulation.potable_water_fees_tva_per_unit_of_service[
                                                                3] * df['C_EP_BCP DO']) + (df[self.is_sanitation]) * (
                                    self.simulation.epa_base_tva_per_unit_of_service +
                                    self.simulation.epa_fees_tva_per_unit_of_service[0] * df['C_EP_BCP DJ'] +
                                    self.simulation.epa_fees_tva_per_unit_of_service[1] * df['C_EP_BCP DL'] +
                                    self.simulation.epa_fees_tva_per_unit_of_service[2] * df['C_EP_BCP DN'] +
                                    self.simulation.epa_fees_tva_per_unit_of_service[3] * df['C_EP_BCP DO']
                            )
        df['C_EP_BCP DT'] = df['C_EP_BCP DQ'] + df['C_EP_BCP DR'] + df['C_EP_BCP DS']
        df['C_EP_BCP DV'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP DT'] - self.simulation.potable_water_prix_base_ttc) + (
                                    df[self.is_sanitation] * (
                                    df['C_EP_BCP DT'] - self.simulation.sanitation_prix_base_ttc)
                            )
        df['C_EP_BCP DW'] = df['C_EP_BCP DV'] / df['C_EP_BCP DH']
        df['C_EP_BCP DY'] = self.calculate_taylor_rf_jour(df)
        df['C_EP_BCP DZ'] = self.simulation.demand.coefficients.a6 * df['C_EP_BCP DY'].apply(np.log)
        df['C_EP_BCP EA'] = self.simulation.demand.coefficients.a5 * df['C_EP_BCP DW'].apply(np.log)
        df['C_EP_BCP EB'] = df['C_EP_BCP J']
        df['C_EP_BCP EC'] = df['C_EP_BCP EB'] + df['C_EP_BCP EA'] + df['C_EP_BCP DZ']
        df['C_EP_BCP ED'] = self.simulation.demand.k * df['C_EP_BCP K'] + (
                1 - self.simulation.demand.k) * df['C_EP_BCP EC']
        df['C_EP_BCP EE'] = df['C_EP_BCP ED'].apply(np.exp)
        df['C_EP_BCP EF'] = df['C_EP_BCP EE'] * 90
        df['C_EP_BCP EH'] = df['C_EP_BCP EF'].apply(lambda x: min(x, self.simulation.tariff.drinking_water.usage_tiers[
            -3].threshold))
        df['C_EP_BCP EI'] = (df['C_EP_BCP EF'] - self.simulation.tariff.drinking_water.usage_tiers[
            -3].threshold).apply(lambda x: max(x, 0))
        # =MIN(EI23;$B$5-$B$4)
        df['C_EP_BCP EJ'] = (df['C_EP_BCP EI']).apply(lambda x: min(x,
                                                                    self.simulation.tariff.drinking_water.usage_tiers[
                                                                        -2].threshold -
                                                                    self.simulation.tariff.drinking_water.usage_tiers[
                                                                        -3].threshold))
        # =MAX(EF23-$B$5;0)
        df['C_EP_BCP EK'] = (df['C_EP_BCP EF'] - self.simulation.tariff.drinking_water.usage_tiers[-2].threshold).apply(
            lambda x: max(x, 0))
        df['C_EP_BCP EL'] = df['C_EP_BCP EK'].apply(lambda x: min(x,
                                                                  self.simulation.tariff.drinking_water.usage_tiers[
                                                                      -1].threshold -
                                                                  self.simulation.tariff.drinking_water.usage_tiers[
                                                                      -2].threshold))
        df['C_EP_BCP EM'] = (df['C_EP_BCP EF'] - df['C_EP_BCP EF']).apply(lambda x: max(x, 0))
        df['C_EP_BCP EO'] = (1 - df[self.is_sanitation]) * (
                self.simulation.tariff.drinking_water.subscription +
                self.simulation.tariff.drinking_water.usage_tiers[0].price * df['C_EP_BCP EH'] +
                self.simulation.tariff.drinking_water.usage_tiers[1].price * df['C_EP_BCP EJ'] +
                self.simulation.tariff.drinking_water.usage_tiers[2].price * df['C_EP_BCP EL'] +
                self.simulation.tariff.drinking_water.usage_tiers[3].price * df['C_EP_BCP EM']
        ) + (df[self.is_sanitation]) * (
                                    self.simulation.tariff.epa().subscription +
                                    self.simulation.tariff.epa().usage_tiers[0].price * df['C_EP_BCP EH'] +
                                    self.simulation.tariff.epa().usage_tiers[1].price * df['C_EP_BCP EJ'] +
                                    self.simulation.tariff.epa().usage_tiers[2].price * df['C_EP_BCP EL'] +
                                    self.simulation.tariff.epa().usage_tiers[3].price * df['C_EP_BCP EM']
                            )
        df['C_EP_BCP EP'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP EF'] * self.simulation.primitives.taxation.drinking_water.fees
        ) + (df[self.is_sanitation]) * (
                                    df['C_EP_BCP EF'] * self.simulation.primitives.taxation.epa().fees)
        df['C_EP_BCP EQ'] = (1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service +
                self.simulation.potable_water_fees_tva_per_unit_of_service[0] * df['C_EP_BCP EH'] +
                self.simulation.potable_water_fees_tva_per_unit_of_service[1] * df['C_EP_BCP EJ'] +
                self.simulation.potable_water_fees_tva_per_unit_of_service[2] * df['C_EP_BCP EL'] +
                self.simulation.potable_water_fees_tva_per_unit_of_service[3] * df['C_EP_BCP EM']
        ) + (df[self.is_sanitation]) * (
                                    self.simulation.epa_base_tva_per_unit_of_service +
                                    self.simulation.epa_fees_tva_per_unit_of_service[0] * df['C_EP_BCP EH'] +
                                    self.simulation.epa_fees_tva_per_unit_of_service[1] * df['C_EP_BCP EJ'] +
                                    self.simulation.epa_fees_tva_per_unit_of_service[2] * df['C_EP_BCP EL'] +
                                    self.simulation.epa_fees_tva_per_unit_of_service[3] * df['C_EP_BCP EM']
                            )
        df['C_EP_BCP ER'] = df['C_EP_BCP EO'] + df['C_EP_BCP EP'] + df['C_EP_BCP EQ']
        df['C_EP_BCP ET'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP ER'] - self.simulation.potable_water_prix_base_ttc) + df[self.is_sanitation] * (
                                    df['C_EP_BCP ER'] - self.simulation.sanitation_prix_base_ttc)
        df['C_EP_BCP EU'] = df['C_EP_BCP ET'] / df['C_EP_BCP EF']
        df['C_EP_BCP EW'] = self.calculate_taylor_rf_jour(df)
        df['C_EP_BCP EX'] = self.simulation.demand.coefficients.a6 * np.log(df['C_EP_BCP EW'])
        df['C_EP_BCP EY'] = self.simulation.demand.coefficients.a5 * df['C_EP_BCP EU'].apply(np.log)
        df['C_EP_BCP EZ'] = df['C_EP_BCP J']
        df['C_EP_BCP FA'] = df['C_EP_BCP EX'] + df['C_EP_BCP EY'] + df['C_EP_BCP EZ']
        df['C_EP_BCP FB'] = self.simulation.demand.k * df['C_EP_BCP K'] + (
                1 - self.simulation.demand.k) * df['C_EP_BCP FA']  # C_EP_BCP FB
        df['C_EP_BCP FC'] = df['C_EP_BCP FB'].apply(np.exp)  # C_EP_BCP FC
        df['C_EP_BCP FD'] = 90 * df['C_EP_BCP FC']
        df['C_EP_BCP FF'] = np.minimum(
            df['C_EP_BCP FD'],
            self.simulation.tariff.drinking_water.usage_tiers[1].threshold
        )
        df['C_EP_BCP FG'] = np.maximum(
            df['C_EP_BCP FD'] - self.simulation.tariff.drinking_water.usage_tiers[1].threshold,
            0
        )
        df['C_EP_BCP FH'] = np.minimum(
            df['C_EP_BCP FG'],
            self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
            self.simulation.tariff.drinking_water.usage_tiers[1].threshold
        )
        df['C_EP_BCP FI'] = np.maximum(
            df['C_EP_BCP FD'] - self.simulation.tariff.drinking_water.usage_tiers[2].threshold, 0)
        df['C_EP_BCP FJ'] = np.minimum(
            df['C_EP_BCP FI'],
            self.simulation.tariff.drinking_water.usage_tiers[3].threshold -
            self.simulation.tariff.drinking_water.usage_tiers[2].threshold
        )
        df['C_EP_BCP FK'] = np.maximum(
            df['C_EP_BCP FD'] - self.simulation.tariff.drinking_water.usage_tiers[3].threshold, 0)
        df['C_EP_BCP FM'] = (
                (1 - df[self.is_sanitation]) * (
                self.simulation.tariff.drinking_water.subscription +
                df['C_EP_BCP FF'] * self.simulation.tariff.drinking_water.usage_tiers[0].price +
                df['C_EP_BCP FH'] * self.simulation.tariff.drinking_water.usage_tiers[1].price +
                df['C_EP_BCP FJ'] * self.simulation.tariff.drinking_water.usage_tiers[2].price +
                df['C_EP_BCP FK'] * self.simulation.tariff.drinking_water.usage_tiers[3].price
        ) +
                df[self.is_sanitation] * (
                        self.simulation.tariff.epa().subscription +
                        df['C_EP_BCP FF'] * self.simulation.tariff.epa().usage_tiers[0].price +
                        df['C_EP_BCP FH'] * self.simulation.tariff.epa().usage_tiers[1].price +
                        df['C_EP_BCP FJ'] * self.simulation.tariff.epa().usage_tiers[2].price +
                        df['C_EP_BCP FK'] * self.simulation.tariff.epa().usage_tiers[3].price
                )
        )
        df['C_EP_BCP FN'] = (
                (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP FD'] * self.simulation.primitives.taxation.drinking_water.vat / 100) +
                df[self.is_sanitation] * (df['C_EP_BCP FD'] * self.simulation.primitives.taxation.epa().vat / 100)
        )
        df['C_EP_BCP FO'] = (
                (1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service +
                df['C_EP_BCP FF'] * self.simulation.potable_water_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP FH'] * self.simulation.potable_water_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP FJ'] * self.simulation.potable_water_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP FK'] * self.simulation.potable_water_fees_tva_per_unit_of_service[3]
        ) +
                df[self.is_sanitation] * (
                        self.simulation.epa_base_tva_per_unit_of_service +
                        df['C_EP_BCP FF'] * self.simulation.epa_fees_tva_per_unit_of_service[0] +
                        df['C_EP_BCP FH'] * self.simulation.epa_fees_tva_per_unit_of_service[1] +
                        df['C_EP_BCP FJ'] * self.simulation.epa_fees_tva_per_unit_of_service[2] +
                        df['C_EP_BCP FK'] * self.simulation.epa_fees_tva_per_unit_of_service[3]
                )
        )
        df['C_EP_BCP FP'] = df['C_EP_BCP FM'] + df['C_EP_BCP FN'] + df['C_EP_BCP FO']
        df['C_EP_BCP FR'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP FP'] - self.simulation.potable_water_prix_base_ttc) + \
                            df[self.is_sanitation] * (
                                    df['C_EP_BCP FP'] - self.simulation.epa_prix_base_ttc)
        df['C_EP_BCP FS'] = df['C_EP_BCP FR'] / (df['C_EP_BCP FC'] * 90)  # C_EP_BCP FS
        df['C_EP_BCP FW'] = self.simulation.demand.coefficients.a5 * df['C_EP_BCP FS'].apply(
            np.log)  # C_EP_BCP FW
        df["C_EP_BCP FU"] = self.calculate_taylor_rf_jour(df)  # C Taylor K20
        df['C_EP_BCP FV'] = self.simulation.demand.coefficients.a6 * df['C_EP_BCP FU'].apply(np.log)
        df['C_EP_BCP FY'] = df['C_EP_BCP FV'] + df['C_EP_BCP FW'] + df[
            'C_EP_BCP Terme ln Part Captive']  # C_EP_BCP FY
        df['C_EP_BCP FZ'] = self.simulation.demand.k * df['C_EP_BCP K'] + (
                1 - self.simulation.demand.k) * df['C_EP_BCP FY']  # C_EP_BCP FZ
        df['C_EP_BCP GA'] = df['C_EP_BCP FZ'].apply(np.exp)  # C_EP_BCP GA23
        df['C_EP_BCP GB'] = 90 * df['C_EP_BCP GA']  # C_EP_BCP GB23
        df['C_EP_BCP GD'] = df['C_EP_BCP GB'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[1].threshold
        )
        df['C_EP_BCP GE'] = (df['C_EP_BCP GB'] - self.simulation.tariff.drinking_water.usage_tiers[1].threshold).clip(
            lower=0)
        df['C_EP_BCP GF'] = df['C_EP_BCP GE'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[2].threshold -
                  self.simulation.tariff.drinking_water.usage_tiers[1].threshold
        )
        df['C_EP_BCP GG'] = (df['C_EP_BCP GB'] - self.simulation.tariff.drinking_water.usage_tiers[2].threshold).clip(
            lower=0)
        df['C_EP_BCP GH'] = df['C_EP_BCP GG'].clip(
            upper=self.simulation.tariff.drinking_water.usage_tiers[3].threshold -
                  self.simulation.tariff.drinking_water.usage_tiers[2].threshold
        )
        df['C_EP_BCP GI'] = (df['C_EP_BCP GB'] - self.simulation.tariff.drinking_water.usage_tiers[3].threshold).clip(
            lower=0)
        df['C_EP_BCP GK'] = ((1 - df[self.is_sanitation]) *
                             (self.simulation.tariff.drinking_water.subscription +
                              df['C_EP_BCP GD'] * self.simulation.tariff.drinking_water.usage_tiers[0].price +
                              df['C_EP_BCP GF'] * self.simulation.tariff.drinking_water.usage_tiers[1].price +
                              df['C_EP_BCP GH'] * self.simulation.tariff.drinking_water.usage_tiers[2].price +
                              df['C_EP_BCP GI'] * self.simulation.tariff.drinking_water.usage_tiers[3].price)) + (
                                    df[self.is_sanitation] *
                                    (self.simulation.tariff.epa().subscription +
                                     df['C_EP_BCP GD'] * self.simulation.tariff.epa().usage_tiers[0].price +
                                     df['C_EP_BCP GF'] * self.simulation.tariff.epa().usage_tiers[1].price +
                                     df['C_EP_BCP GH'] * self.simulation.tariff.epa().usage_tiers[2].price +
                                     df['C_EP_BCP GI'] * self.simulation.tariff.epa().usage_tiers[3].price))
        df['C_EP_BCP GL'] = ((1 - df[self.is_sanitation]) * (
                df['C_EP_BCP GB'] * self.simulation.primitives.taxation.drinking_water.fees)) + \
                            (df[self.is_sanitation] * (
                                    df['C_EP_BCP GB'] * self.simulation.primitives.taxation.epa().fees))
        df['C_EP_BCP GK'] = ((1 - df[self.is_sanitation]) * (
                self.simulation.potable_water_base_tva_per_unit_of_service +
                df['C_EP_BCP GD'] * self.simulation.potable_water_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP GF'] * self.simulation.potable_water_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP GH'] * self.simulation.potable_water_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP GI'] * self.simulation.potable_water_fees_tva_per_unit_of_service[3]
        )) + (df[self.is_sanitation] * (
                self.simulation.epa_base_tva_per_unit_of_service +
                df['C_EP_BCP GD'] * self.simulation.epa_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP GF'] * self.simulation.epa_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP GH'] * self.simulation.epa_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP GI'] * self.simulation.epa_fees_tva_per_unit_of_service[3]
        ))
        # =(1-$B23)*(GB23*$K$1)+$B23*(GB23*$K$8)
        df['C_EP_BCP GL'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP GB'] * self.simulation.primitives.taxation.drinking_water.fees
        ) + df[self.is_sanitation] * (df['C_EP_BCP GB'] * self.simulation.primitives.taxation.epa().fees)
        # ==(1-$B23)*($F$2+GD23*$F$3+GF23*$F$4+GH23*$F$5+GI23*$F$6)+$B23*($F$9+GD23*$F$10+GF23*$F$11+GH23*$F$12+GI23*$F$13)
        df['C_EP_BCP GM'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP GB'] * self.simulation.potable_water_base_tva_per_unit_of_service +
                df['C_EP_BCP GD'] * self.simulation.potable_water_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP GF'] * self.simulation.potable_water_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP GH'] * self.simulation.potable_water_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP GI'] * self.simulation.potable_water_fees_tva_per_unit_of_service[3]
        ) + (df[self.is_sanitation] * (
                df['C_EP_BCP GB'] * self.simulation.epa_base_tva_per_unit_of_service +
                df['C_EP_BCP GD'] * self.simulation.epa_fees_tva_per_unit_of_service[0] +
                df['C_EP_BCP GF'] * self.simulation.epa_fees_tva_per_unit_of_service[1] +
                df['C_EP_BCP GH'] * self.simulation.epa_fees_tva_per_unit_of_service[2] +
                df['C_EP_BCP GI'] * self.simulation.epa_fees_tva_per_unit_of_service[3]
        ))
        df['C_EP_BCP GN'] = (df['C_EP_BCP GK'] + df['C_EP_BCP GL'] + df['C_EP_BCP GM'])
        # =(1-$B23)*(GN23-$G$2)+$B23*(GN23-$G$9)
        df['C_EP_BCP GP'] = (1 - df[self.is_sanitation]) * (
                df['C_EP_BCP GN'] - self.simulation.potable_water_prix_base_ttc) + df[self.is_sanitation] * (
                                    df['C_EP_BCP GN'] - self.simulation.epa_prix_base_ttc
                            )
        df['C_EP_BCP GQ'] = df['C_EP_BCP GP'] / df['C_EP_BCP GB']
        df['C_EP_BCP GT'] = self.simulation.demand.coefficients.a6 * np.log(self.calculate_taylor_rf_jour(df))
        df['C_EP_BCP GU'] = self.simulation.demand.coefficients.a6 * np.log(df['C_EP_BCP GQ'])
        df['C_EP_BCP GW'] = (
                df['C_EP_BCP J'] +
                df['C_EP_BCP GU'] +
                df['C_EP_BCP GT']
        )
        df['C_EP_BCP GX'] = (
                self.simulation.demand.k * df['C_EP_BCP K'] +
                (1 - self.simulation.demand.k) * df['C_EP_BCP GW']
        )
        # =EXP(GX23)
        df['C_EP_BCP GY'] = df['C_EP_BCP GX'].apply(np.exp)
        # =90*GY23
        df['C_EP_BCP GZ'] = df['C_EP_BCP GY'] * 90
        df['C_EP_BCP HM'] = df['C_EP_BCP GB']
        df['C_EP_BCP HY'] = df[self.is_sanitation] * df['C_EP_BCP HM']

    def calculate_taylor_rf_jour(self, df):
        # C Talor K 20
        df['C_PP Revenu'] = df['Revenu_Imputé_2']
        df['Taylor Rev Jour'] = df['C_PP Revenu'] / 30  # C_PP!H10
        df['Taylor F jour'] = df['Taylor Abonnement EP / EPA'] / 90
        taylor_rf_jour = df['Taylor Rev Jour'] - df['Taylor F jour']
        return taylor_rf_jour

    def tariff_sanitation_subscription_fee(self):
        df = self.consumption_per_trimestre()
        df['Facture_IBT_C_BCP AO'] = df[self.is_sanitation] * self.simulation.tariff.sanitation.subscription
        # =MIN(C11;$J$2)
        df['Facture_IBT_C_BCP F'] = df['C_PP BM'].clip(upper=self.simulation.tariff.sanitation.usage_tiers[1].threshold)
        # =MAX(C11-$J$2;0)
        df['Facture_IBT_C_BCP G'] = df['C_PP BM'].apply(
            lambda x: max(x - self.simulation.tariff.sanitation.usage_tiers[1].threshold, 0))
        # =MIN(G11;$J$3-$J$2)
        df['Facture_IBT_C_BCP H'] = df['Facture_IBT_C_BCP G'].clip(
            upper=self.simulation.tariff.sanitation.usage_tiers[2].threshold -
                  self.simulation.tariff.sanitation.usage_tiers[1].threshold)
        # =MAX(C11-J$3;0)
        df['Facture_IBT_C_BCP I'] = df['C_PP BM'].apply(
            lambda x: max(x - self.simulation.tariff.sanitation.usage_tiers[2].threshold, 0))
        # =MIN(I11;J$4-J$3)
        df['Facture_IBT_C_BCP J'] = df['Facture_IBT_C_BCP I'].apply(lambda x: min(
            self.simulation.tariff.sanitation.usage_tiers[3].threshold - self.simulation.tariff.sanitation.usage_tiers[
                2].threshold, x))
        # =MAX(C11-$J$4;0)
        df['Facture_IBT_C_BCP K'] = df['C_PP BM'].apply(
            lambda x: max(x - self.simulation.tariff.sanitation.usage_tiers[3].threshold, 0))

        df['Facture_IBT_C_BCP AP'] = df[self.is_sanitation] * df['Facture_IBT_C_BCP F'] * \
                                     self.simulation.tariff.sanitation.usage_tiers[0].price
        df['Facture_IBT_C_BCP AQ'] = df[self.is_sanitation] * df['Facture_IBT_C_BCP H'] * \
                                     self.simulation.tariff.sanitation.usage_tiers[1].price
        df['Facture_IBT_C_BCP AR'] = df[self.is_sanitation] * df['Facture_IBT_C_BCP I'] * \
                                     self.simulation.tariff.sanitation.usage_tiers[2].price
        df['Facture_IBT_C_BCP AS'] = df[self.is_sanitation] * df['Facture_IBT_C_BCP J'] * \
                                     self.simulation.tariff.sanitation.usage_tiers[3].price

        df['Facture_IBT_C_BCP AT'] = df['Facture_IBT_C_BCP AO'] + df['Facture_IBT_C_BCP AP'] + \
                                     df['Facture_IBT_C_BCP AQ'] + df['Facture_IBT_C_BCP AR'] + df[
                                         'Facture_IBT_C_BCP AS']

        return df['Facture_IBT_C_BCP AT'].sum()

    def var_par_menages(self):
        #### IBT
        self.df['VAR_PAR_Menages AE'] = self.df['Partie_Base_C_et_Fact AX'] + self.df['Partie_Base_C_et_Fact BZ']
        # =100*(AE8/3)/$E8
        self.df['VAR_PAR_Menages AL'] = 100 * (self.df['VAR_PAR_Menages AE'] / 3) / self.df['Revenu_Imputé_2']
        # =SI(AL8>'Social Data'!B$5;1;0) B4 is the PAR threshold

        #### TBSE
        self.df['VAR_PAR_Menages AI'] = self.df['Partie_Base_C_et_Fact EJ'] + self.df['Partie_Base_C_et_Fact DV']
        # =100*(AI8/3)/$E8
        self.df['VAR_PAR_Menages AM'] = 100 * (self.df['VAR_PAR_Menages AI'] / 3) / self.df['Revenu_Imputé_2']

        self.df['VAR_PAR_Menages AP'] = (
                self.df['VAR_PAR_Menages AL'] > self.simulation.primitives.social_data.threshold_par).astype(float)

        self.df['VAR_PAR_Menages AQ'] = (
                self.df['VAR_PAR_Menages AM'] > self.simulation.primitives.social_data.threshold_par
        ).astype(float)

        self.df['VAR_PAR_Menages AW'] = (
                                                self.simulation.primitives.social_data.threshold_par / 100
                                        ) * 3 * self.df['Revenu_Imputé_2']

        self.df['VAR_PAR_Menages AX'] = (
                self.df['VAR_PAR_Menages AE'] -
                self.df['VAR_PAR_Menages AW']
        ).clip(lower=0)

        self.df['VAR_PAR_Menages AY'] = (
                self.df['VAR_PAR_Menages AI'] -
                self.df['VAR_PAR_Menages AW']
        ).clip(lower=0)

        small_df = self.df[['VAR_PAR_Menages AY', 'VAR_PAR_Menages AX']]
        small_df.sort_values('VAR_PAR_Menages AY')
        small_df['VAR_PAR_Menages BD'] = list(range(len(small_df)))
        small_df['VAR_PAR_Menages BD'] = small_df['VAR_PAR_Menages BD'] / len(small_df)
        small_df.sort_values('VAR_PAR_Menages AX')
        small_df['VAR_PAR_Menages BU'] = list(range(len(small_df)))
        small_df['VAR_PAR_Menages BU'] = small_df['VAR_PAR_Menages BU'] / len(small_df)
        small_df.sort_index(inplace=True)

        self.df.loc[small_df.index, 'VAR_PAR_Menages BD'] = small_df.loc[small_df.index, 'VAR_PAR_Menages BD']
        self.df.loc[small_df.index, 'VAR_PAR_Menages BU'] = small_df.loc[small_df.index, 'VAR_PAR_Menages BU']

    @property
    def is_sanitation(self):
        return 'Assainissement Collectif (1 = oui)'


def create_mock_simulation():
    return SimulationPayload(
        primitives=PrimitivesModel(
            ep=WaterServiceCostModel(
                couts_fixes=9000000,
                couts_variables=0.9,
                nombre_abonnes=47847,
            ),
            assainissement=WaterServiceCostModel(
                couts_fixes=6000000,
                couts_variables=0.40,
                nombre_abonnes=25300,
            ),
            environnement=EnvironmentalModel(
                couts_fixes_par_an=0,
                couts_variable_moyen=1.3,
            ),
            fiscalite=TaxSectionModel(
                eau_potable=TaxModel(
                    tva=2.1,
                    redevances=0.12,
                ),
                assainissement=TaxModel(
                    tva=10,
                    redevances=0.04,
                )
            ),
            donnees_sociales=SocialDataModel(
                seuil_par=3,
                seuil_car=3,
                pauvrete=800,
                grande_pauvrete=300,
            )
        ),
        population=PopulationModel(
            bd="BD",
            eps=458,
            std=0.05,
        ),
        tarification=TariffModel(
            ep=TariffSectionModel(
                abonnement=18.69,
                usage_tiers=[
                    ConsumptionThresholds(
                        seuil=0,
                        prix=0.878
                    ),
                    ConsumptionThresholds(
                        seuil=15,
                        prix=1.839
                    ),
                    ConsumptionThresholds(
                        seuil=30,
                        prix=2.768
                    ),
                    ConsumptionThresholds(
                        seuil=60,
                        prix=4.38
                    )
                ]
            ),
            assainissement=TariffSectionModel(
                abonnement=15.545,
                usage_tiers=[
                    ConsumptionThresholds(
                        seuil=0,
                        prix=1.3,
                    ),
                    ConsumptionThresholds(
                        seuil=15,
                        prix=2.12,
                    ),
                    ConsumptionThresholds(
                        seuil=30,
                        prix=2.21,
                    ),
                    ConsumptionThresholds(
                        seuil=60,
                        prix=2.5,
                    )
                ]
            )
        ),
        demande=DemandModel(
            coefficients=CoefficientModel(
                a0=-2.56,
                a1=0.48,
                a2=0.44,
                a3=0.12,
                a4=0.37,
                a5=-0.31,
                a6=0.25
            ),
            k=0.4,
            piscine=False,
            jardin=False
        ),
        launch=LaunchModel(
            periodes=4,
            nom_simulation="MockSimulation"
        )
    )


if __name__ == '__main__':
    from src.initial.schemas import *

    # PPrimitives

    simulation_payload: SimulationPayload = create_mock_simulation()

    unit_variable_cost = 0.40

    # Tariff module
    sanitation_charge_fix = 15.55

    # Generation dataset

    df = pd.read_excel(
        "/Users/oriol.alas/PROJECTS/INNWATER/innwater-water-tariff/fast_backend/data/data_La_Réunion_2.xls",
        "esfact7-ElPR1")
    g1_augmented, g2_augmented = process_population_sample_df(df,
                                                              simulation_payload.primitives.drinking_water.number_of_subscribers,
                                                              simulation_payload.primitives.sanitation.number_of_subscribers,
                                                              simulation_payload.population.eps,
                                                              simulation_payload.population.std)
    print(len(g1_augmented), len(g2_augmented))
    simulation_calculator = SimulationCalculator(simulation=simulation_payload, g1_df=g1_augmented, g2_df=g2_augmented)

    # Social Data J17 J18
    print(len(g1_augmented) + len(g2_augmented))

    all_df = pd.concat([g1_augmented, g2_augmented])
    print(all_df.columns)
    total_subscription_yearly_fee = (
            all_df['Assainissement Collectif (1 = oui)'] * simulation_payload.tariff.sanitation.subscription).sum()
    print("total_sanitation_subscription_fee", total_subscription_yearly_fee)
    print("total_sanitation_subscription_fee", simulation_calculator.base_sanitation_subscription_fee)
    social_sampling_rate = len(g2_augmented)

    facture_ibt_c_bcp = 15174.43

    c_ep_bcp_hy_481 = 6780
    fixed_costs = simulation_payload.primitives.sanitation.fixed_costs

    net_sanitation = calculate_net_cost_service(simulation_payload.primitives.sanitation.number_of_subscribers,
                                                sanitation_charge_fix, social_sampling_rate,
                                                total_subscription_yearly_fee, facture_ibt_c_bcp, c_ep_bcp_hy_481,
                                                unit_variable_cost,
                                                fixed_costs)
    print(net_sanitation)

    net_potable_water = calculate_net_cost_service(47847, 18.69, 458., 8560.02, 36577.04, 16733.67, 0.9,
                                                   9000000)
    print(net_potable_water)
