import pickle
import time
from collections import defaultdict
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from src.core.models import Simulation
from src.initial.population_service import save_population_data_given_simulation_info
from src.initial.schemas import SimulationPayload
from src.small_assessment.effeco.gini_decomp import gini_decomp
from src.small_assessment.mock_simulation import PAYLOAD

SANITATION_COLUMN = 'Assainissement Collectif (1 = oui)'


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


class NewSimulation:

    def __init__(self, simulation: SimulationPayload, g1_df: pd.DataFrame, g2_df: pd.DataFrame):
        self.simulation: SimulationPayload = simulation
        self.g1_df = g1_df
        self.g2_df = g2_df
        self.df = pd.concat([self.g1_df, self.g2_df])
        self.calculate_poor()
        self.calculate_captive_consumption()
        self.calculate_base_consumption()
        self.calculate_tbse_consumption()
        self.calculate_ibt_pp_consumption()
        self.calculate_ibt_pp_receipt()
        self.calculate_taylor_consumption()
        self.calculate_bcp_consumption()
        self.calculate_overconsumption()
        self.calculate_receipts()
        self.calculate_par()
        self.calculate_first_tier_consumption()
        self.calculate_aproximate_demand_consumptions()
        self.calculate_delta_economic_efficiency()
        self.calculate_overconsumption_approximate()
        self.calculate_environmental_costs()
        self.calculate_rex()

    def calculate_poor(self):
        uc_oecd = 1 + (self.df['nbpers'] - self.df['nenf'] - 1) * 0.5 + self.df['nenf'] * 0.3
        self.level_oecd = self.df['Revenu_Imputé_2'] / uc_oecd
        self.is_poor = self.level_oecd <= self.simulation.primitives.social_data.poverty

    def is_sanitation(self):
        return (self.df[SANITATION_COLUMN] == 1)

    def calculate_captive_consumption(self):
        self.captive_consumption = (self.simulation.demand.coefficients.a0 +
                                    self.simulation.demand.coefficients.a1 * self.df['nbpers'].apply(np.log) +
                                    self.simulation.demand.coefficients.a2 * self.df['SNWA'] +
                                    self.simulation.demand.coefficients.a3 * self.df['Piscine (1 = oui)'] +
                                    self.simulation.demand.coefficients.a4 * self.df['Garden * Wheather'])
        print("LEN, DF", len(self.df))
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
        bill_tbse = ((
                             self.simulation.tbse_potable_water_base_prix + self.is_sanitation() * self.simulation.tbse_sanitation_base_prix) / 3)
        daily_diff_tbse = (self.df['Revenu_Imputé_2'] - bill_tbse) / 30
        ttc = (self.simulation.tbse_potable_water_variable_prix + self.is_sanitation()
               * self.simulation.tbse_sanitation_variable_prix).apply(
            np.log) * self.simulation.demand.coefficients.a5

        daily_diff_tbse = daily_diff_tbse.apply(np.log) * self.simulation.demand.coefficients.a6
        sum_pv = ttc + daily_diff_tbse
        self.tbse_consumption = self.captive_consumption + sum_pv
        self.tbse_consumption_per_day = self.tbse_consumption.apply(np.exp)
        self.tbse_consumption_per_trim = self.tbse_consumption_per_day * 90

    def calculate_nordin_ibt_pp_consumption(self, captive_consumption: float, ep_prix_ttc, epa_prix_ttc,
                                            ep_nordin_tier_ttc: float, epa_nordin_tier_ttc: float):
        def apply(row):
            daily_income = row['Revenu_Imputé_2'] / 30
            daily_subscription = (self.simulation.epa_prix_base_ttc if row[
                SANITATION_COLUMN] else self.simulation.potable_water_prix_base_ttc) / 90
            daily_subscription_tier = (
                                          epa_nordin_tier_ttc if row[SANITATION_COLUMN] else ep_nordin_tier_ttc
                                      ) / 90
            daily_virtual_income = np.log(
                daily_income - daily_subscription + daily_subscription_tier) * self.simulation.demand.coefficients.a6
            prix_ttc = np.log(
                epa_prix_ttc if row[SANITATION_COLUMN] else ep_prix_ttc) * self.simulation.demand.coefficients.a5
            consumption_ = 90 * np.exp(prix_ttc + daily_virtual_income + captive_consumption)
            return daily_subscription_tier, consumption_

        return apply

    def calculate_ibt_pp_consumption(self):
        thresholds = list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers))
        consumptions = []

        daily_subscription_ibt_pp_results = defaultdict(list)

        for i, row in self.df.iterrows():
            results = []
            for i_tier, (ep_prix_ttc,
                         epa_prix_ttc,
                         ep_nordin_tier,
                         epa_nordin_tier) in enumerate(zip(self.simulation.potable_water_prix_tiers_ttc,
                                                           self.simulation.epa_prix_tiers_ttc,
                                                           self.simulation.potable_water_nordin_tiers,
                                                           self.simulation.epa_nordin_tiers)):
                daily_subscription_tier, ibt_pp_consumption = self.calculate_nordin_ibt_pp_consumption(
                    self.captive_consumption[i],
                    ep_prix_ttc,
                    epa_prix_ttc,
                    ep_nordin_tier,
                    epa_nordin_tier
                )(row)
                results.append(ibt_pp_consumption)
                daily_subscription_ibt_pp_results[i_tier].append(daily_subscription_tier)

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
        sanitation_tiers = sanitation_tiers * self.is_sanitation()
        sanitation_results = sanitation_results * self.is_sanitation()

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
        daily_subscription_ttc = (self.df[SANITATION_COLUMN].apply(
            lambda x: self.simulation.epa_prix_base_ttc if x else self.simulation.potable_water_prix_base_ttc)) / 90

        for i in range(num_periods):
            log_revenue = (self.df['Revenu_Imputé_2'] / 30 - daily_subscription_ttc).apply(
                np.log) * self.simulation.demand.coefficients.a6
            log_avg_price = cvm.apply(np.log) * self.simulation.demand.coefficients.a5

            last_cv_taylor = (log_revenue + log_avg_price + self.captive_consumption).apply(np.exp) * 90
            self.taylor_consumptions.append(last_cv_taylor)
            current_df = pd.DataFrame({"consumption": last_cv_taylor, "sanitation": self.is_sanitation()})
            cv = current_df.apply(decompose_value_carry_and_prix(
                thresholds=list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers)),
                potable_water_prix_ttc=self.simulation.potable_water_prix_tiers_ttc,
                sanitation_prix_ttc=self.simulation.sanitation_prix_tiers_ttc
            ), axis=1)
            cvm = cv / last_cv_taylor
        return self.taylor_consumptions[num_periods]

    def calculate_bcp_consumption(self):
        if self.simulation.launch.periods == 0:
            return self.ibt_pp_consumption
        taylor_consumption = self.taylor_consumptions[1] / 90
        ibt_pp_consumption = self.ibt_pp_consumption / 90

        taylor_ln = taylor_consumption.apply(np.log)
        ibt_pp_ln = ibt_pp_consumption.apply(np.log)

        daily_subscription = (self.simulation.potable_water_prix_base_ttc + self.simulation.sanitation_prix_base_ttc *
                              self.is_sanitation()) / 90
        log_revenue_taylor = ((self.df['Revenu_Imputé_2'] / 30 - daily_subscription).apply(
            np.log) * self.simulation.demand.coefficients.a6)

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
            ), axis=1)
            cvm = cv / last_bcp
            ln_taylor_price = cvm.apply(np.log) * self.simulation.demand.coefficients.a5
            taylor_ln = log_revenue_taylor + ln_taylor_price + self.captive_consumption
        return self.bcp_consumptions

    def calculate_overconsumption(self):
        self.overconsumption = self.bcp_consumptions[self.simulation.launch.periods] - self.ibt_pp_consumption
        return self.overconsumption

    def calculate_first_tier_consumption(self):
        self.first_tier_a_i = ((self.df[
                                    'Revenu_Imputé_2'] / 30) ** self.simulation.demand.coefficients.a6) * self.captive_consumption_per_day
        self.first_tier_consumption_per_day = (
                ((self.simulation.primitives.drinking_water.variable_costs +
                  self.simulation.primitives.environment.average_variable_cost)
                 ** self.simulation.demand.coefficients.a5) * self.first_tier_a_i)
        self.first_tier_consumption_per_trim = self.first_tier_consumption_per_day * 90

    def calculate_aproximate_demand_consumptions(self):
        self.tbse_a_consumption_per_trim = self._aproximate_demand_consumption_calculation(
            self.simulation.tbse_potable_water_variable_prix, self.simulation.tbse_sanitation_variable_prix)

        # IBT PP A
        possible_ibt_consumptions = []
        for potable_water_ttc, sanitation_ttc in zip(self.simulation.potable_water_prix_tiers_ttc,
                                                     self.simulation.sanitation_prix_tiers_ttc):
            possible_ibt_consumptions.append(self._aproximate_demand_consumption_calculation(potable_water_ttc,
                                                                                             sanitation_ttc))
        ibt_pp_a_consumption_per_trim = []
        for i in range(len(possible_ibt_consumptions[0])):
            found = False
            for ithreshold, (usage_tiers, next_usage_tier) in enumerate(
                    zip(self.simulation.tariff.drinking_water.usage_tiers,
                        self.simulation.tariff.drinking_water.usage_tiers[1:])):
                if usage_tiers.threshold <= possible_ibt_consumptions[ithreshold][i] < next_usage_tier.threshold:
                    ibt_pp_a_consumption_per_trim.append(possible_ibt_consumptions[ithreshold][i])
                    found = True
                    break
                elif ithreshold + 1 < len(self.simulation.tariff.drinking_water.usage_tiers) and (
                        usage_tiers.threshold <= possible_ibt_consumptions[ithreshold + 1][
                    i] < next_usage_tier.threshold):
                    ibt_pp_a_consumption_per_trim.append(possible_ibt_consumptions[ithreshold + 1][i])
                    found = True
                    break
            if not found:
                ibt_pp_a_consumption_per_trim.append(possible_ibt_consumptions[-1][i])
        self.ibt_pp_a_consumption_per_trim = pd.Series(ibt_pp_a_consumption_per_trim)
        self.ibt_a_consumption_per_trim = self.ibt_pp_a_consumption_per_trim + self.overconsumption

    def calculate_delta_economic_efficiency(self):
        self.delta_tbse_a = self.tbse_a_consumption_per_trim - self.first_tier_consumption_per_trim
        self.delta_ibt_pp_a = self.ibt_pp_a_consumption_per_trim - self.first_tier_consumption_per_trim
        self.delta_ibt_a = self.ibt_a_consumption_per_trim - self.first_tier_consumption_per_trim

    def _aproximate_demand_consumption_calculation(self, potable_water_ttc_price, sanitation_ttc_price):
        is_sanitation = self.is_sanitation().astype(float)
        tbse_ttc_price = potable_water_ttc_price + is_sanitation * sanitation_ttc_price
        daily_consumption_ttc = self.first_tier_a_i * (tbse_ttc_price ** self.simulation.demand.coefficients.a5)
        return daily_consumption_ttc * 90

    def calculate_overconsumption_approximate(self):
        self.tbse_a_surplus_contr_var = self._calculation_variation_contribution_overconsumption(
            self.tbse_a_consumption_per_trim)
        self.ibt_pp_a_surplus_contr_var = self._calculation_variation_contribution_overconsumption(
            self.ibt_pp_a_consumption_per_trim
        )
        self.ibt_a_surplus_contr_var = self._calculation_variation_contribution_overconsumption(
            self.ibt_a_consumption_per_trim
        )

        self.tbse_a_receipt = self.__calculate_generic_tbse_receipt(self.tbse_a_consumption_per_trim)
        self.ibt_pp_a_receipt = self.__calculate_generic_ibt_receipt(self.ibt_pp_a_consumption_per_trim)
        self.ibt_a_receipt = self.__calculate_generic_ibt_receipt(self.ibt_a_consumption_per_trim)

        self.ibt_pp_surplus_consumption = self._calculate_surplus_consumption_receipt(
            self.ibt_pp_a_consumption_per_trim, self.ibt_pp_a_receipt)
        self.ibt_surplus_consumption = self._calculate_surplus_consumption_receipt(self.ibt_a_consumption_per_trim,
                                                                                   self.ibt_a_receipt)
        self.delta_ibt_surplus_consumption = self._calculate_surplus_consumption_receipt(
            self.ibt_a_consumption_per_trim,
            self.ibt_a_receipt,
            self.ibt_pp_a_consumption_per_trim,
            self.ibt_pp_a_receipt
        )

    def _calculate_surplus_consumption_receipt(self, consumption, receipt, other_consumption=None, other_receipt=None):
        consumption_per_day = consumption / 90
        if other_consumption is None:
            other_consumption = self.tbse_a_consumption_per_trim
        if other_receipt is None:
            other_receipt = self.tbse_a_receipt
        tbse_consumption_per_day = other_consumption / 90
        elastic_price = abs(self.simulation.demand.coefficients.a5)
        coef = (1 - elastic_price) / elastic_price
        coef_beta = elastic_price / (1 - elastic_price)
        variation_surplus = coef_beta * self.first_tier_b_i * (
                tbse_consumption_per_day ** (-coef) - consumption_per_day ** (-coef)) * 90
        delta_fact_ttc = receipt - other_receipt
        variation_surplus_consumption = variation_surplus - delta_fact_ttc
        return variation_surplus_consumption

    def _calculation_variation_contribution_overconsumption(self, consumption_trim):
        elastic_price = abs(self.simulation.demand.coefficients.a5)
        coef = (1 - elastic_price) / elastic_price
        coef_beta = elastic_price / (1 - elastic_price)
        self.first_tier_b_i = self.first_tier_a_i ** (1 / elastic_price)
        variation_i1 = coef_beta * self.first_tier_b_i * (
                self.first_tier_consumption_per_day ** (-coef) - (consumption_trim / 90) ** (-coef)
        )
        variation_i2 = (consumption_trim / 90 - self.first_tier_consumption_per_day) * (
                self.simulation.primitives.environment.average_variable_cost + self.simulation.primitives.drinking_water.variable_costs
        )
        agg_surplus_contribution_variation_eur_per_quarter = (variation_i1 - variation_i2) * 90
        return agg_surplus_contribution_variation_eur_per_quarter

    def calculate_environmental_costs(self):
        is_g1 = ~self.is_sanitation()
        cost_env_no_recuperable = (is_g1 *
                                   max(self.simulation.primitives.environment.average_variable_cost
                                       - self.simulation.primitives.taxation.drinking_water.fees, 0)) + (
                                          self.is_sanitation() * max(
                                      self.simulation.primitives.environment.average_variable_cost
                                      - self.simulation.primitives.taxation.drinking_water.fees
                                      - self.simulation.primitives.taxation.sanitation.fees
                                      - self.simulation.primitives.sanitation.variable_costs,
                                      0)
                                  )
        self.first_tier_env_cost = cost_env_no_recuperable * self.first_tier_consumption_per_trim
        self.tbse_env_cost = cost_env_no_recuperable * self.tbse_consumption_per_trim
        self.ibt_env_cost = cost_env_no_recuperable * self.bcp_consumptions[self.simulation.launch.periods]
        self.ibt_pp_env_cost = cost_env_no_recuperable * self.ibt_pp_consumption
        self.overconsumption_env_cost = cost_env_no_recuperable * self.overconsumption

    def calculate_rex(self):
        drinking_water_agence = self._calculate_agence_rex(self.bcp_consumptions[self.simulation.launch.periods],
                                                           self.simulation.primitives.taxation.drinking_water.fees,
                                                           self.simulation.primitives.drinking_water.number_of_subscribers)
        sanitation_agence = self._calculate_agence_rex(
            self.bcp_consumptions[self.simulation.launch.periods][self.is_sanitation()],
            self.simulation.primitives.taxation.sanitation.fees,
            self.simulation.primitives.sanitation.number_of_subscribers)

        self.water_agency_exercise_duty = drinking_water_agence + sanitation_agence

        drinking_water_mean_state_fee = self.__calculate_state_variable_rex(
            self.bcp_consumptions[self.simulation.launch.periods],
            self.simulation.primitives.drinking_water.number_of_subscribers,
            self.simulation.potable_water_base_tva_per_unit_of_service,
            self.simulation.potable_water_fees_tva_per_unit_of_service,
            self.simulation.tariff.drinking_water.usage_tiers)

        sanitation_mean_state_fee = self.__calculate_state_variable_rex(
            self.bcp_consumptions[self.simulation.launch.periods][self.is_sanitation()],
            self.simulation.primitives.sanitation.number_of_subscribers,
            self.simulation.sanitation_base_tva_per_unit_of_service,
            self.simulation.sanitation_fees_tva_per_unit_of_service,
            self.simulation.tariff.sanitation.usage_tiers
        )

        self.state_avt_total = drinking_water_mean_state_fee + sanitation_mean_state_fee

    def _calculate_agence_rex(self, consumption, fees, number_of_subscribers):
        level_service = number_of_subscribers * (4 * np.mean(consumption))
        total = fees * level_service
        return total

    def __calculate_state_variable_rex(self, consumption, num_subscribers, tva_base, tva_tiers, usage_tiers):
        drinking_water_constant_state = tva_base * 4
        drinking_water_variable_state = np.mean(self.__calculate_state_variable_ibt_receipt(consumption,
                                                                                            usage_tiers,
                                                                                            tva_tiers))
        mean_state_fee = (drinking_water_variable_state + drinking_water_constant_state) * num_subscribers
        return mean_state_fee

    def __calculate_generic_tbse_receipt(self, consumption):
        potable_receipt = self.simulation.tbse_potable_water_base_prix + consumption * self.simulation.tbse_potable_water_variable_prix
        sanitation_receipt = self.is_sanitation().astype(float) * (
                self.simulation.tbse_sanitation_base_prix + consumption *
                self.simulation.tbse_sanitation_variable_prix)
        return potable_receipt + sanitation_receipt

    def __calculate_state_variable_ibt_receipt(self, consumption, tariff_tiers, tva_fees):
        thresholds = list(map(lambda x: x.threshold, tariff_tiers))

        res = []

        for j, consumption_value in enumerate(consumption):
            val = 0
            for usage_tier, tva_fee, consumption_tier in zip(tariff_tiers, tva_fees,
                                                             decompose_value(consumption_value, thresholds)):
                val += (consumption_tier * tva_fee)
            res.append(val)
        return pd.Series(res)

    def __calculate_generic_ibt_receipt(self, consumption, add_splitted_receipt=False):
        thresholds = list(map(lambda x: x.threshold, self.simulation.tariff.drinking_water.usage_tiers))

        res = []
        potable_water_res = []
        potable_water_only_consumption_receipt = []

        sanitation_res = []
        sanitation_only_consumption_receipt = []

        for j, consumption_value in enumerate(consumption):
            potable_water_receipt = self.simulation.tariff.drinking_water.subscription + self.simulation.potable_water_base_tva_per_unit_of_service
            if add_splitted_receipt:
                potable_water_only_consumption_receipt.append(self.simulation.tariff.drinking_water.subscription)

            for usage_tiers, ttc_tier, consumption_tier in zip(self.simulation.tariff.drinking_water.usage_tiers,
                                                               self.simulation.potable_water_prix_tiers_ttc,
                                                               decompose_value(consumption_value, thresholds)):
                if add_splitted_receipt:
                    potable_water_only_consumption_receipt[j] += consumption_tier * usage_tiers.price
                potable_water_receipt += consumption_tier * ttc_tier

            sanitation_receipt = self.simulation.tariff.sanitation.subscription + self.simulation.sanitation_base_tva_per_unit_of_service
            if add_splitted_receipt:
                sanitation_only_consumption_receipt.append(self.simulation.tariff.sanitation.subscription)
            for usage_tier, ttc_tier, consumption_tier in zip(self.simulation.tariff.sanitation.usage_tiers,
                                                              self.simulation.sanitation_prix_tiers_ttc,
                                                              decompose_value(consumption_value, thresholds)):
                if add_splitted_receipt:
                    sanitation_only_consumption_receipt[j] += consumption_tier * usage_tier.price
                sanitation_receipt += consumption_tier * ttc_tier
            sanitation_receipt *= self.is_sanitation()[j]

            total_receipt = potable_water_receipt + sanitation_receipt
            res.append(total_receipt)
            if add_splitted_receipt:
                potable_water_res.append(potable_water_receipt)
                sanitation_res.append(sanitation_receipt)

        if add_splitted_receipt:
            return np.array(res), np.array(potable_water_res), np.array(sanitation_res), np.array(
                potable_water_only_consumption_receipt), np.array(
                sanitation_only_consumption_receipt) * self.is_sanitation()
        return np.array(res)

    def calculate_receipts(self):
        self.tbse_base_receipt = self.__calculate_generic_tbse_receipt(self.base_consumption_per_trim)
        self.tbse_tbse_consumption_receipt = self.__calculate_generic_tbse_receipt(self.tbse_consumption_per_trim)
        self.ibt_base_receipt = self.__calculate_generic_ibt_receipt(self.base_consumption_per_trim)
        (self.ibt_bcp_receipt,
         self.potable_water_ibt_bcp_receipt,
         self.sanitation_ibt_bcp_receipt,
         self.potable_water_ibt_bcp_consumption_receipt,
         self.sanitation_ibt_bcp_consumption_receipt) = self.__calculate_generic_ibt_receipt(
            self.bcp_consumptions[self.simulation.launch.periods], add_splitted_receipt=True)

    def calculate_par(self):
        self.par_ibt = (self.ibt_base_receipt / 3) / self.df['Revenu_Imputé_2'] * 100
        self.par_tbse = (self.tbse_base_receipt / 3) / self.df['Revenu_Imputé_2'] * 100

        self.ibt_par_headcount = (self.par_ibt > self.simulation.primitives.social_data.threshold_par).astype(float)
        self.tbse_par_headcount = (self.par_tbse > self.simulation.primitives.social_data.threshold_par).astype(float)

        par_threshold = self.simulation.primitives.social_data.threshold_par / 100 * 3 * self.df['Revenu_Imputé_2']

        self.ibt_par_excess = (self.ibt_base_receipt - par_threshold).clip(lower=0)
        self.tbse_par_excess = (self.tbse_base_receipt - par_threshold).clip(lower=0)

        self.ibt_par_excess_rank = get_rank(self.ibt_par_excess)
        self.tbse_par_excess_rank = get_rank(self.tbse_par_excess)

        self.ibt_ginis = get_gini(self.ibt_par_excess, 1 / len(self.df) * 100)
        self.tbse_ginis = get_gini(self.tbse_par_excess, 1 / len(self.df) * 100)
        self.ibt_unafford_ginis = get_gini(self.ibt_par_excess, 1 / (self.ibt_par_excess > 0).sum() * 100)
        self.tbse_unafford_ginis = get_gini(self.tbse_par_excess, 1 / (self.tbse_par_excess > 0).sum() * 100)

    def get_df(self):
        self.df['par_ibt'] = self.par_ibt
        self.df['par_tbse'] = self.par_tbse
        self.df['base_consumption_per_trim'] = self.base_consumption_per_trim
        self.df['tbse_consumption_per_trim'] = self.tbse_consumption_per_trim
        self.df['ibt_pp_consumption'] = self.ibt_pp_consumption
        self.df['ibt_bcp_consumption'] = self.bcp_consumptions[self.simulation.launch.periods]
        self.df['tbse_base_receipt'] = self.tbse_base_receipt
        self.df['ibt_bcp_receipt'] = self.ibt_bcp_receipt
        self.df['ibt_base_receipt'] = self.ibt_base_receipt
        return self.df


def get_gini(excess, constant):
    df_ = pd.DataFrame(
        {"ibt_par_excess": excess, }
    )
    df_.sort_values(by="ibt_par_excess", inplace=True)
    df_['rank'] = df_['ibt_par_excess'] / excess.sum() * 100
    df_['addition'] = df_['rank'].cumsum()
    res = constant * (df_['addition'] + df_['addition'].shift(1).fillna(0))
    return res


def get_rank(excess):
    df_ = pd.DataFrame({
        "ibt_par_excess": excess,
    })
    df_.sort_values(by="ibt_par_excess", inplace=True)
    df_['rank'] = list(range(len(df_)))
    df_['rank'] = df_["rank"] / len(excess)
    df_.sort_index(inplace=True)
    return df_["rank"].values


def save_simulation(simulation_id, new_simulation: NewSimulation):
    simulation_path = Path(f'data/simulation_data/{simulation_id}/simulation.pkl')
    if not simulation_path.parent.exists():
        simulation_path.parent.mkdir(parents=True, exist_ok=True)
    with open(simulation_path, 'wb') as f:
        pickle.dump(new_simulation, f)


async def get_or_create_simulation_from_payload(simulation_id, simulation: Simulation,
                                                payload: SimulationPayload) -> NewSimulation:
    from pathlib import Path

    simulation_path = Path(f'data/simulation_data/{simulation_id}/simulation.pkl')
    if simulation_path.exists():
        with open(simulation_path, 'rb') as f:
            return pickle.load(f)
    df = await save_population_data_given_simulation_info(
        total_subscribers=simulation.primitives.cost_potable_water.subscribers_number,
        sanitation_subscribers=simulation.primitives.cost_sanitation.subscribers_number,
        bd=simulation.population.database_path,
        eps=simulation.population.eps,
        std=simulation.population.std,
        use_original_datasource=simulation.population.original_datasource,
        simulation_id=simulation.id,
    )
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    new_simulation = NewSimulation(payload, g1_df, g2_df)
    save_simulation(simulation_id, new_simulation)
    return new_simulation


def main():
    df = pd.read_csv(
        '/Users/oriol.alas/PROJECTS/INNWATER/innwater-water-tariff/fast_backend/data/data.csv',
        index_col=0
    )
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    start = time.time()
    simulation = NewSimulation(PAYLOAD, g1_df, g2_df)

    gini_result = gini_decomp(simulation.ibt_par_excess, simulation.is_sanitation())

    print(time.time() - start)
    # save_simulation(2, simulation)
    # import pickle
    # with open("simulation.pickle", "rb") as f:
    #    obj = pickle.load(f)


if __name__ == '__main__':
    main()
