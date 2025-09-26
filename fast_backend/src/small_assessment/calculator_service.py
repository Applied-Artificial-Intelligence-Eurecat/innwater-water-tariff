from abc import ABC
from pathlib import Path

import numpy as np
import pandas as pd

from src.initial.schemas import SimulationPayload


class AbstractSimulation(ABC):

    def __init__(self, simulation_payload: SimulationPayload):
        self.simulation = simulation_payload
        self.df = None

    @property
    def is_sanitation(self):
        return 'Assainissement Collectif (1 = oui)'


class SimulationFinished(AbstractSimulation):

    def __init__(self, simulation_id, simulation_payload: SimulationPayload):
        super().__init__(simulation_payload)
        self.df = pd.read_csv(f'data/simulation_data/{simulation_id}/middle_metrics.csv')

    def total_tariff_sanitation_subscription_fee(self):
        return self.df['Facture_IBT_C_BCP AO'].sum()

    def only_subscription_tariff_sanitation_subscription_fee(self):
        val = self.df['C_EP_BCP HY'].sum()

        return val


    def ibt_c_bcp_co(self, df):
        df[
            'Facture_IBT_C_BCP AK'] = self.simulation.tariff.drinking_water.subscription + self.simulation.potable_water_base_tva_per_unit_of_service + \
                                      df['Facture_IBT_C_BCP F'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  0].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[0]) + df[
                                          'Facture_IBT_C_BCP H'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  1].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[1]) + df[
                                          'Facture_IBT_C_BCP J'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  2].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[2]
                                      ) + df['Facture_IBT_C_BCP K'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  3].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[3]
                                      )
        df['Facture_IBT_C_BCP BM'] = (
                df[self.is_sanitation] * (
                self.simulation.tariff.sanitation.subscription + self.simulation.sanitation_base_tva_per_unit_of_service +
                df['Facture_IBT_C_BCP F'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            0].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[0]) + df[
                    'Facture_IBT_C_BCP H'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            1].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[1]) + df[
                    'Facture_IBT_C_BCP J'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            2].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[2]
                ) + df['Facture_IBT_C_BCP K'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            3].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[3]
                )
        )
        )
        bill_bcp_co_result = df['Facture_IBT_C_BCP BM'] + df['Facture_IBT_C_BCP AK']
        return bill_bcp_co_result



    def bill_bl_tbse(self):
        TBSE_AI = self.simulation.primitives.drinking_water.tbse_base_prix + self.df[
            'C_et_F_TBSE P'] * self.simulation.tbse_ep_variable_prix
        print("TBSE AI", TBSE_AI)
        self.df['C_et_F_TBSE AI'] = TBSE_AI
        self.df['C_et_F_TBSE AW'] = self.df[self.is_sanitation] * (
                    self.simulation.primitives.sanitation.tbse_base_prix + self.df[
                'C_et_F_TBSE P'] * self.simulation.tbse_a_variable_prix)
        print("Saving TBSEBL")
        bl_tbse = self.df['C_et_F_TBSE AI'] + self.df['C_et_F_TBSE AW']
        return bl_tbse

    def only_subscription_tariff_potable_water_subscription_fee(self):
        print("drinking water subscription fee", self.simulation.tariff.drinking_water.subscription)
        result = len(self.df) * self.simulation.tariff.drinking_water.subscription
        print("result", result)
        return result

    def total_tariff_potable_water_subscription_fee(self):
        return self.df['Facture_IBT_C_BCP R'].sum()  # Facture_IBT_C_BCP!R469

    def only_tariff_drinking_water_subscription_fee(self):
        val = self.df['C_EP_BCP HM'].sum()
        return val


class SimulationCalculator(AbstractSimulation):

    def __init__(self, simulation: SimulationPayload, g1_df: pd.DataFrame, g2_df: pd.DataFrame):
        super().__init__(simulation)
        self.simulation = simulation
        self.g1_df = g1_df
        self.g2_df = g2_df
        self.df = pd.concat([self.g1_df, self.g2_df])
        self.df = self.affordability_initialization()

    def save_simulation_data(self, simulation_id):
        path = Path(f'data/simulation_data/{simulation_id}')
        path.mkdir(parents=True, exist_ok=True)
        path_file = path / 'middle_metrics.csv'
        self.df.to_csv(path_file, index=False)

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
        df['Partie Captive C et Fact Q'] = df['Partie Captive C et Fact C Total'].apply(np.exp)
        df['Partie Captive C et Fact R'] = df['Partie Captive C et Fact Q'] * 90

        df['C_EP_BCP Terme ln Part Captive'] = ((df['Partie Captive C et Fact C Total'].apply(
            np.exp))).apply(np.log)  # C_EP_BCP J 23
        df['C_EP_BCP J'] = df['C_EP_BCP Terme ln Part Captive']

        df['C_PP H'] = df['Revenu_Imputé_2'] / 30
        df['C_PP J'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_prix_base_ttc + (
                df[self.is_sanitation] * self.simulation.epa_prix_base_ttc) / 90
        print(self.simulation.potable_water_nordin_tiers)
        print(self.simulation.epa_nordin_tiers)

        df['C_PP L'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_nordin_tiers[0] + (
                df[self.is_sanitation] * self.simulation.epa_nordin_tiers[0])
        df['C_PP M'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_nordin_tiers[1] + (
                df[self.is_sanitation] * self.simulation.epa_nordin_tiers[1])
        df['C_PP N'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_nordin_tiers[2] + (
                df[self.is_sanitation] * self.simulation.epa_nordin_tiers[2])
        df['C_PP O'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_nordin_tiers[3] + (
                df[self.is_sanitation] * self.simulation.epa_nordin_tiers[3])

        df['C_PP W'] = (df['C_PP H'] + df['C_PP J'] + df['C_PP N'] / 90)
        df['C_PP X'] = (df['C_PP H'] + df['C_PP J'] + df['C_PP O'] / 90)
        df['C_PP Z'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_prix_tiers_ttc[-4] + (
                df[self.is_sanitation] * self.simulation.epa_prix_tiers_ttc[-4])
        df['C_PP AA'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_prix_tiers_ttc[-3] + (
                df[self.is_sanitation] * self.simulation.epa_prix_tiers_ttc[-3])
        df['C_PP AB'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_prix_tiers_ttc[-2] + (
                df[self.is_sanitation] * self.simulation.epa_prix_tiers_ttc[-2])
        df['C_PP AC'] = (1 - df[self.is_sanitation]) * self.simulation.potable_water_prix_tiers_ttc[-1] + (
                df[self.is_sanitation] * self.simulation.epa_prix_tiers_ttc[-1])

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

        return df

    def facture_ibt_c_pp(self, df: pd.DataFrame) -> pd.DataFrame:
        # --- pull frequently used parameters into locals (faster, cleaner) ---
        tw = self.simulation.tariff.drinking_water
        tiers = tw.usage_tiers
        th1 = tiers[1].threshold
        thm3 = tiers[-3].threshold
        thm2 = tiers[-2].threshold
        thm1 = tiers[-1].threshold

        prix_base = self.simulation.potable_water_prix_base_ttc
        prix_tiers = np.asarray(self.simulation.potable_water_prix_tiers_ttc, dtype=float)  # [0..3]
        fees_dw = float(self.simulation.primitives.taxation.drinking_water.fees)
        base_tva = float(self.simulation.potable_water_base_tva_per_unit_of_service)
        fees_tva = np.asarray(self.simulation.potable_water_fees_tva_per_unit_of_service, dtype=float)  # [-4..-1]

        # Sanitation params
        san = self.simulation.tariff.sanitation
        san_sub = float(san.subscription)
        san_prices = np.asarray([t.price for t in san.usage_tiers], dtype=float)  # [0..3]
        fees_san = float(self.simulation.primitives.taxation.sanitation.fees)
        san_base_tva = float(self.simulation.sanitation_base_tva_per_unit_of_service)
        san_fees_tva = np.asarray(self.simulation.sanitation_fees_tva_per_unit_of_service, dtype=float)  # [0..3]

        # --- inputs as arrays ---
        x = df['C_PP BM'].to_numpy(dtype=float)
        is_san = df[self.is_sanitation].to_numpy(dtype=float)  # assume bool/0-1; cast to float for multiplications

        # --- drinking water tiered quantities (vectorized, no .apply) ---
        F = np.minimum(x, th1)
        G = np.maximum(x - th1, 0.0)
        H = np.minimum(G, (thm2 - thm3))
        I = np.maximum(x - thm2, 0.0)
        J = np.minimum(I, (thm1 - thm2))
        K = np.maximum(x - thm1, 0.0)

        # Prices per tier
        M = prix_base
        N = F * prix_tiers[0]
        O = H * prix_tiers[1]
        P = J * prix_tiers[2]
        Q = K * prix_tiers[3]
        # R not needed downstream for final outputs (kept as example)
        # R = M + N + O + P + Q

        # Drinking water fees
        T = F * fees_dw
        U = H * fees_dw
        V = J * fees_dw
        W = K * fees_dw
        # X = (F + H + J + K) * fees_dw  # not needed for final outputs

        # TVA per unit of service
        Y = base_tva
        Z = F * fees_tva[-4]
        AA = H * fees_tva[-3]
        AB = J * fees_tva[-2]
        AC = K * fees_tva[-1]

        AD = Y + Z + AA + AB + AC
        AE = M + Y
        AF = N + T + Z
        AG = O + U + AA
        AH = P + V + AB
        AI = Q + W + AC
        AK = AI + AH + AG + AF + AE

        # --- sanitation (masked by is_san) ---
        AO = is_san * san_sub
        AP = is_san * F * san_prices[0]
        AQ = is_san * H * san_prices[1]
        AR = is_san * J * san_prices[2]
        AS = is_san * K * san_prices[3]
        # AT = AO + AP + AQ + AR + AS  # not needed for final outputs

        AV = is_san * F * fees_san
        AW = is_san * H * fees_san
        AX = is_san * J * fees_san
        AY = is_san * K * fees_san
        # AZ = AV + AW + AX + AY  # not needed for final outputs

        BA = is_san * san_base_tva
        BB = is_san * san_fees_tva[0] * F
        BC = is_san * san_fees_tva[1] * H
        BD = is_san * san_fees_tva[2] * J
        BE = is_san * san_fees_tva[3] * K
        # BF = BA + BB + BC + BD + BE  # not needed for final outputs

        BG = AO + BA
        BH = AP + AV + BB
        BI = AQ + AW + BC
        BJ = AR + AX + BD
        BK = AS + AY + BE
        BM = BK + BJ + BI + BH + BG

        CO = AK + BM

        df.loc[:, 'Facture IBT C PP AE'] = AE
        df.loc[:, 'Facture IBT C PP AK'] = AK
        df.loc[:, 'Facture IBT C PP BG'] = BG
        df.loc[:, 'Facture IBT C PP BM'] = BM
        df.loc[:, 'Facture IBT C PP CO'] = CO
        df['Taylor Abonnement EP / EPA'] = df['Facture IBT C PP AE'] + df[
            'Facture IBT C PP BG']  # Facture_IBT_C_PP '!CI11
        df['Taylor Terme ln Revenu'] = self.calculate_taylor_rf_jour(df).apply(
            np.log) * self.simulation.demand.coefficients.a6
        df['Taylor Montant de la Facture EP/EPA'] = df['Facture IBT C PP CO']

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

    def affordability_initialization(self) -> pd.DataFrame:
        df = self.consumption_per_trimestre()
        self.facture_ibt_c_pp(df)
        self.c_taylor(df)
        self.c_ep_bcp(df)
        self.facture_ibt_bcp(df)
        self.c_et_f_tbse()
        self.partie_base_c_et_fact()
        self.var_par_menages()
        self.donnes(df)
        self.calculate_poor(df)
        self.environmental_cost_reduit()
        return df

    def calculate_poor(self, df):
        df['UC OECD'] = 1 + (df['nbpers'] - df['nenf'] - 1) * 0.5 + df['nenf'] * 0.3
        df['Level OECD'] = df['Revenu_Imputé_2'] / df['UC OECD']
        df['poor'] = df['Level OECD'] <= self.simulation.primitives.social_data.poverty

    def donnes(self, df):
        df['Donnees J'] = df['C_EP_BCP HM'] - df['C_PP BM']
        df['Donnees K'] = (df['Donnees J'] > 0).astype(float)
        df['Donnees U'] = df['C_EP_BCP HM'] - df['C_et_F_TBSE P']
        df['Donnees V'] = df['C_PP BM'] - df['C_et_F_TBSE P']
        df['Donnees X'] = (df['Donnees U'] > 0).astype(float)

    def c_et_f_tbse(self):
        self.df['C_et_F_TBSE H'] = (1 - self.df[self.is_sanitation]) * (self.simulation.tbse_potable_water_base_prix) + (
                self.df[self.is_sanitation] * self.simulation.tbse_epa_base_prix)
        self.df['C_et_F_TBSE I'] = self.df['C_et_F_TBSE H'] / 90
        self.df['C_et_F_TBSE K'] = self.df['C_PP H'] - self.df['C_et_F_TBSE I']
        self.df['C_et_F_TBSE M'] = self.simulation.demand.coefficients.a6 * self.df['C_et_F_TBSE K'].apply(np.log)
        # =$O$3*LN((1-$E12)*$G$3+$E12*$G$7)
        self.df['C_et_F_TBSE L'] = self.simulation.demand.coefficients.a5 * np.log(
            (1 - self.df[self.is_sanitation]) * self.simulation.tbse_potable_water_variable_prix + self.df[
                self.is_sanitation] * self.simulation.tbse_epa_variable_prix)
        self.df['C_et_F_TBSE N'] = self.df['C_et_F_TBSE L'] + self.df['C_et_F_TBSE M'] + self.df['Partie Captive C et Fact C Total']
        self.df['C_et_F_TBSE O'] = self.df['C_et_F_TBSE N'].apply(np.exp)
        self.df['C_et_F_TBSE P'] = 90 * self.df['C_et_F_TBSE O']

        bl_tbse = self.bill_bl_tbse()
        self.df.loc[:, 'C_et_F_TBSE BL'] = bl_tbse

    def bill_bl_tbse(self):
        TBSE_AI = self.simulation.primitives.drinking_water.tbse_base_prix + self.df[
            'C_et_F_TBSE P'] * self.simulation.tbse_ep_variable_prix
        print("TBSE AI", TBSE_AI)
        self.df['C_et_F_TBSE AI'] = TBSE_AI
        self.df['C_et_F_TBSE AW'] = self.df[self.is_sanitation] * (
                    self.simulation.primitives.sanitation.tbse_base_prix + self.df[
                'C_et_F_TBSE P'] * self.simulation.tbse_a_variable_prix)
        print("Saving TBSEBL")
        bl_tbse = self.df['C_et_F_TBSE AI'] + self.df['C_et_F_TBSE AW']
        return bl_tbse

    def facture_ibt_bcp(self, df):
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
        # =$F11*O$3
        df['Facture_IBT_C_BCP N'] = df['Facture_IBT_C_BCP F'] * self.simulation.tariff.drinking_water.usage_tiers[
            0].price
        # =$H11*O$4
        df['Facture_IBT_C_BCP O'] = df['Facture_IBT_C_BCP H'] * self.simulation.tariff.drinking_water.usage_tiers[
            1].price
        # =$H11*O$4
        df['Facture_IBT_C_BCP P'] = df['Facture_IBT_C_BCP J'] * self.simulation.tariff.drinking_water.usage_tiers[
            2].price
        # =$J11*O$5
        df['Facture_IBT_C_BCP Q'] = df['Facture_IBT_C_BCP K'] * self.simulation.tariff.drinking_water.usage_tiers[
            3].price
        # =$N11+O$3+P$4+Q$5
        df['Facture_IBT_C_BCP R'] = self.simulation.tariff.drinking_water.subscription + df['Facture_IBT_C_BCP N'] + df[
            'Facture_IBT_C_BCP O'] + df['Facture_IBT_C_BCP P'] + \
                                    df['Facture_IBT_C_BCP Q']

        df[
            'Facture_IBT_C_BCP AK'] = self.simulation.tariff.drinking_water.subscription + self.simulation.potable_water_base_tva_per_unit_of_service + \
                                      df['Facture_IBT_C_BCP F'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  0].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[0]) + df[
                                          'Facture_IBT_C_BCP H'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  1].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[1]) + df[
                                          'Facture_IBT_C_BCP J'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  2].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[2]
                                      ) + df['Facture_IBT_C_BCP K'] * (
                                              self.simulation.tariff.drinking_water.usage_tiers[
                                                  3].price + self.simulation.primitives.taxation.drinking_water.fees +
                                              self.simulation.potable_water_fees_tva_per_unit_of_service[3]
                                      )

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

        df['Facture_IBT_C_BCP CO'] = self.ibt_c_bcp_co(df)

    def ibt_c_bcp_co(self, df):
        df['Facture_IBT_C_BCP BM'] = (
                df[self.is_sanitation] * (
                self.simulation.tariff.sanitation.subscription + self.simulation.sanitation_base_tva_per_unit_of_service +
                df['Facture_IBT_C_BCP F'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            0].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[0]) + df[
                    'Facture_IBT_C_BCP H'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            1].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[1]) + df[
                    'Facture_IBT_C_BCP J'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            2].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[2]
                ) + df['Facture_IBT_C_BCP K'] * (
                        self.simulation.tariff.sanitation.usage_tiers[
                            3].price + self.simulation.primitives.taxation.sanitation.fees +
                        self.simulation.sanitation_fees_tva_per_unit_of_service[3]
                )
        )
        )
        bill_bcp_co_result = df['Facture_IBT_C_BCP BM'] + df['Facture_IBT_C_BCP AK']
        return bill_bcp_co_result

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

    def total_tariff_potable_water_subscription_fee(self):
        return self.df['Facture_IBT_C_BCP R'].sum()

    def only_subscription_tariff_potable_water_subscription_fee(self):
        return len(self.df) * self.simulation.tariff.drinking_water.subscription

    def environmental_cost_reduit(self):
        df = self.df
        pass
