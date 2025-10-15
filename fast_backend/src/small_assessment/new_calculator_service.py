import numpy as np
import pandas as pd

from calculator_service import AbstractSimulation
from src.initial.schemas import SimulationPayload


class NewSimulation(AbstractSimulation):

    def __init__(self, simulation: SimulationPayload, g1_df: pd.DataFrame, g2_df: pd.DataFrame):
        super().__init__(simulation)
        self.simulation = simulation
        self.g1_df = g1_df
        self.g2_df = g2_df
        self.df = pd.concat([self.g1_df, self.g2_df])
        self.captive_consumption = None
        self.base_consumption = None

    def is_sanitation(self):
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

