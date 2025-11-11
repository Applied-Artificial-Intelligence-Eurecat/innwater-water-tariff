from typing import List, Iterable

import numpy as np
import pandas as pd

from calculator_service import AbstractSimulation
from src.initial.schemas import SimulationPayload


def decompose_value_carry(thresholds):
    def apply(value):
        """
        Decomposes `value` into segments defined by `thresholds`.

        Example:
            value = 32
            thresholds = [0, 15, 30, 60]
            → [15, 15, 2, 0]
        """
        if not thresholds or len(thresholds) < 2:
            raise ValueError("Thresholds must contain at least two values (start and end).")

        decomposed = []
        remaining = value

        for i in range(len(thresholds) - 1):
            lower, upper = thresholds[i], thresholds[i + 1]
            segment = max(0, min(remaining, upper - lower))
            decomposed.append(segment)
            remaining -= segment

        decomposed.append(max(0, remaining))
        return decomposed

    return apply


def decompose_value_carry_and_prix(thresholds, potable_water_prix_ttc: List[float], sanitation_prix_ttc: List[float]):
    def apply(row):
        """
        Decomposes `value` into segments defined by `thresholds`.

        Example:
            value = 32
            thresholds = [0, 15, 30, 60]
            → [15, 15, 2, 0]
        """
        decomposed = decompose_value_carry(thresholds)(row['consumption'])
        result = 0
        for decomposed_consumption, ep_ttc, a_ttc in zip(decomposed, potable_water_prix_ttc, sanitation_prix_ttc):
            result += decomposed_consumption * ep_ttc
            if row['sanitation']:
                result += decomposed_consumption * a_ttc
        return result

    return apply


def decompose_value(value: float, thresholds: List[float]) -> List[float]:
    return decompose_value_carry(thresholds)(value)


class NewSimulation(AbstractSimulation):

    def __init__(self, simulation: SimulationPayload, g1_df: pd.DataFrame, g2_df: pd.DataFrame):
        super().__init__(simulation)
        self.simulation: SimulationPayload = simulation
        self.g1_df = g1_df
        self.g2_df = g2_df
        self.df = pd.concat([self.g1_df, self.g2_df])
        self.calculate_captive_consumption()
        self.calculate_base_consumption()
        self.calculate_tbse_consumption()
        self.calculate_ibt_pp_consumption()
        self.calculate_ibt_pp_receipt()
        self.calculate_taylor_consumption()
        self.calculate_bcp_consumption()
        self.calculate_overconsumption()

    def is_sanitation(self) -> Iterable[bool]:
        return self.df['Assainissement Collectif (1 = oui)'] == 1

    def calculate_captive_consumption(self):
        self.captive_consumption = (self.simulation.demand.coefficients.a0 +
                                    self.simulation.demand.coefficients.a1 * self.df['nbpers'].apply(np.log) +
                                    self.simulation.demand.coefficients.a2 * self.df['SNWA'] +
                                    self.simulation.demand.coefficients.a3 * self.df['Piscine (1 = oui)'] +
                                    self.simulation.demand.coefficients.a4 * self.df['Garden * Wheather'])
        self.captive_consumption_per_day = self.captive_consumption.apply(np.exp)
        self.captive_consumption_per_trim = self.captive_consumption_per_day * 90

    def calculate_base_consumption(self):
        self.base_consumption = (self.simulation.demand.coefficients.a0 +
                                 self.simulation.demand.coefficients.a1 * self.df['nbpers'].apply(np.log) +
                                 self.simulation.demand.coefficients.a2 * self.df['SNWA'] +
                                 self.simulation.demand.coefficients.a3 * self.df['Piscine (1 = oui)'] *
                                 self.simulation.demand.has_pool +
                                 self.simulation.demand.coefficients.a4 * self.df['Garden * Wheather'] *
                                 self.simulation.demand.has_garden)
        self.base_consumption_per_day = self.base_consumption.apply(np.exp)
        self.base_consumption_per_trim = self.base_consumption_per_day * 90

    def calculate_tbse_consumption(self):
        daily_income = self.reself.df['Revenu_Imputé_2'] / 30
        bill_tbse = ((self.simulation.tbse_potable_water_base_prix + self.df[
            self.is_sanitation()] * self.simulation.tbse_sanitation_base_prix) / 90)
        diff_tbse = daily_income - bill_tbse
        ttc = (self.simulation.tbse_potable_water_variable_prix + self.df[
            self.is_sanitation()] * self.simulation.tbse_sanitation_variable_prix).apply(
            np.log) * self.simulation.demand.coefficients.a5
        diff_tbse = diff_tbse.apply(np.log) * self.simulation.demand.coefficients.a6
        sum_pv = ttc + diff_tbse
        self.tbse_consumption = self.captive_consumption + sum_pv
        self.tbse_consumption_per_day = self.tbse_consumption.apply(np.exp)
        self.tbse_consumption_per_trim = self.tbse_consumption_per_day * 90

    def calculate_nordin_ibt_pp_consumption(self, captive_consumption: float, ep_prix_ttc, epa_prix_ttc,
                                            ep_nordin_tier_ttc: float, epa_nordin_tier_ttc: float):
        def apply(row):
            daily_income = row['Revenu_Imputé_2'] / 30
            daily_subscription = (self.simulation.epa_prix_base_ttc if row[
                self.is_sanitation()] else self.simulation.potable_water_prix_base_ttc) / 90
            daily_subscription_tier = (
                                          epa_nordin_tier_ttc if row[self.is_sanitation()] else ep_nordin_tier_ttc
                                      ) / 90
            daily_virtual_income = (daily_income - daily_subscription + daily_subscription_tier).apply(
                np.log) * self.simulation.demand.coefficients.a6
            prix_ttc = (epa_prix_ttc if row[self.is_sanitation()] else ep_prix_ttc).apply(
                np.log) * self.simulation.demand.coefficients.a5
            return daily_subscription_tier, 90 * (prix_ttc + daily_virtual_income + captive_consumption).apply(np.exp)

        return apply

    def calculate_ibt_pp_consumption(self):
        thresholds = list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers))
        consumptions = []

        daily_subscription_ibt_pp_results = []

        for i, row in self.df.iterrows():
            results = []
            for (ep_prix_ttc,
                 epa_prix_ttc,
                 ep_nordin_tier,
                 epa_nordin_tier) in zip(self.simulation.potable_water_prix_tiers_ttc,
                                         self.simulation.epa_prix_tiers_ttc,
                                         self.simulation.potable_water_nordin_tiers,
                                         self.simulation.epa_nordin_tiers):
                daily_subscription_tier, ibt_pp_consumption = self.calculate_nordin_ibt_pp_consumption(
                    self.captive_consumption[i],
                    ep_prix_ttc,
                    epa_prix_ttc,
                    ep_nordin_tier,
                    epa_nordin_tier
                )(row)
                results.append(ibt_pp_consumption)
                daily_subscription_ibt_pp_results.append(daily_subscription_tier)

            found = False

            for threshold, next_threshold, ibt_pp, next_ibt_pp in zip(thresholds, thresholds[1:], results, results[1:]):
                if threshold <= ibt_pp < next_threshold:
                    consumptions.append(ibt_pp)
                    found = True
                    break
                elif ibt_pp >= next_threshold > next_ibt_pp:
                    consumptions.append(next_threshold)
                    found = True
                    break
            if not found:
                consumptions.append(results[-1])
        self.ibt_pp_daily_subscription_all_taxes = pd.Series(daily_subscription_ibt_pp_results)
        self.ibt_pp_consumption = pd.Series(consumptions)

    def calculate_ibt_pp_receipt(self):
        thresholds = list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers))
        prices = list(map(lambda x: x.price, self.simulation.tariff.drinking_water.usage_tiers))
        fee = self.simulation.primitives.taxation.drinking_water.fees
        tva_tiers = self.simulation.potable_water_fees_tva_per_unit_of_service
        tva_base = self.simulation.potable_water_base_tva_per_unit_of_service

        water_potable_tiers, water_potable_results = self.__calculate_bill_ibt(fee, prices, thresholds, tva_base,
                                                                               tva_tiers)
        sanitation_tiers, sanitation_results = self.__calculate_bill_ibt(fee, prices, thresholds,
                                                                         tva_base, tva_tiers)
        sanitation_tiers = sanitation_tiers * self.df[self.is_sanitation()]
        sanitation_results = sanitation_results * self.df[self.is_sanitation()]

        self.ibt_pp_tiers_receipt = water_potable_tiers + sanitation_tiers
        self.ibt_pp_receipt = water_potable_results + sanitation_results

    def __calculate_bill_ibt(self, fee, prices, thresholds, tva_base, tva_tiers):
        results = []
        tier_parts_result = []
        for consumption in self.ibt_pp_consumption:
            decomposed_consumptions = decompose_value(consumption, thresholds)
            tier_parts = 0
            for consumption_tier, price_tier, tva_tier in zip(decomposed_consumptions, prices, tva_tiers):
                tier_parts += (consumption_tier * price_tier +
                               consumption_tier * fee +
                               consumption_tier * tva_tier)
            price = self.simulation.tariff.drinking_water.subscription + tva_base + tier_parts
            tier_parts_result.append(tier_parts)
            results.append(price)
        return pd.Series(tier_parts_result), pd.Series(results)

    def calculate_taylor_consumption(self):
        num_periods = self.simulation.launch.periods
        if num_periods == 0:
            return self.ibt_pp_consumption

        return self.__calculate_taylor_consumption_with_period(num_periods)

    def __calculate_taylor_consumption_with_period(self, num_periods):
        cv = self.ibt_pp_tiers_receipt
        last_cv_taylor = self.ibt_pp_consumption
        cvm = cv / last_cv_taylor
        self.taylor_consumptions = [last_cv_taylor]
        for i in range(num_periods):
            log_revenue = (self.df['Revenu_Imputé_2'] - self.ibt_pp_daily_subscription_all_taxes).apply(
                np.log) * self.simulation.demand.coefficients.a6
            log_avg_price = cvm.apply(np.log) * self.simulation.demand.coefficients.a5

            last_cv_taylor = (log_revenue + log_avg_price + self.captive_consumption).apply(np.exp) * 90
            self.taylor_consumptions.append(last_cv_taylor)
            current_df = pd.DataFrame({"consumption": last_cv_taylor, "sanitation": self.is_sanitation()})
            cv = current_df.apply(decompose_value_carry_and_prix(
                thresholds=list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers)),
                potable_water_prix_ttc=self.simulation.potable_water_prix_tiers_ttc,
                sanitation_prix_ttc=self.simulation.sanitation_prix_tiers_ttc
            ))
            cvm = cv / last_cv_taylor
        return self.taylor_consumptions[num_periods]

    def calculate_bcp_consumption(self):
        if self.simulation.launch.periods == 0:
            return self.ibt_pp_consumption
        taylor_consumption = self.taylor_consumptions[1] / 90
        ibt_pp_consumption = self.ibt_pp_consumption / 90
        ibt_pp_ln = ibt_pp_consumption.apply(np.log)
        daily_subscription = (self.simulation.potable_water_prix_base_ttc + self.simulation.sanitation_prix_base_ttc *
                              self.df[self.is_sanitation()]) / 90
        log_revenue_taylor = ((self.df['Revenu_Imputé_2'] / 30 - daily_subscription).apply(
            np.log) * self.simulation.demand.coefficients.a6)

        taylor_ln = taylor_consumption.apply(np.log)

        self.bcp_consumptions = [self.ibt_pp_consumption]

        for i in range(self.simulation.launch.periods):
            bcp_ln = ((1 - self.simulation.demand.k) * taylor_ln + self.simulation.demand.k * ibt_pp_ln).apply(np.exp)
            last_bcp = bcp_ln * 90
            self.bcp_consumptions.append(last_bcp)
            current_df = pd.DataFrame({"consumption": last_bcp, "sanitation": self.is_sanitation()})
            cv = current_df.apply(decompose_value_carry_and_prix(
                thresholds=list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers)),
                potable_water_prix_ttc=self.simulation.potable_water_prix_tiers_ttc,
                sanitation_prix_ttc=self.simulation.sanitation_prix_tiers_ttc
            ))
            cvm = cv / last_bcp
            ln_taylor_price = cvm.apply(np.log) * self.simulation.demand.coefficients.a5
            taylor_ln = log_revenue_taylor + ln_taylor_price + self.captive_consumption
        return self.bcp_consumptions

    def calculate_overconsumption(self):
        self.overconsumption = self.ibt_pp_consumption - self.bcp_consumptions[self.simulation.launch.periods]
        return self.overconsumption

    def __calculate_generic_tbse_receipt(self, consumption):
        potable_receipt = self.simulation.tbse_potable_water_base_prix + consumption * self.simulation.tbse_potable_water_variable_prix
        sanitation_receipt = self.df[self.is_sanitation()] * (self.simulation.tbse_sanitation_base_prix + consumption *
                                                              self.simulation.tbse_sanitation_variable_prix)
        return potable_receipt + sanitation_receipt

    def __calculate_generic_ibt_receipt(self, consumption):
        thresholds = list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers))

        potable_water_receipt = self.simulation.tariff.drinking_water.subscription + self.simulation.potable_water_base_tva_per_unit_of_service
        for ttc_tier, consumption_tier in zip(self.simulation.potable_water_prix_tiers_ttc,
                                              decompose_value(consumption, thresholds)):
            potable_water_receipt += consumption_tier * ttc_tier

        sanitation_receipt = self.simulation.tariff.sanitation.subscription + self.simulation.sanitation_base_tva_per_unit_of_service
        for ttc_tier, consumption_tier in zip(self.simulation.sanitation_prix_tiers_ttc,
                                              decompose_value(consumption, thresholds)):
            sanitation_receipt += consumption_tier * ttc_tier
        sanitation_receipt *= self.df[self.is_sanitation()]

        return potable_water_receipt + sanitation_receipt

    def calculate_receipts(self):
        self.tbse_captive_receipt = self.__calculate_generic_tbse_receipt(self.captive_consumption)
        self.tbse_base_receipt = self.__calculate_generic_tbse_receipt(self.base_consumption)

        
