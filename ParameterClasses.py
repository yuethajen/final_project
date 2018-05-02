from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData2 as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random


class HealthStats(Enum):
    """ health states of patients with HIV """
    SICK = 0
    ANTIBIOTICS = 1
    SIDE_EFFECT = 2
    WELL = 3


class Therapies(Enum):
    """ mono vs. combination therapy """
    PCT = 0
    ANTIBIOTICS = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.SICK

        # calculate the adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT*Data.DELTA_T

        # transition probability matrix of the selected therapy
        self._prob_matrix = []

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.PCT:
            self._prob_matrix = Data.TRANS_MATRIX_PCT
        else:
            self._prob_matrix = Data.TRANS_MATRIX_ANTI

        # annual state costs and utilities
        self._annualStateCosts = []
        if self._therapy == Therapies.PCT:
            self._annualStateCosts = Data.ANNUAL_STATE_COST_PCT
        else:
            self._annualStateCosts = Data.ANNUAL_STATE_COST_ANTI

        # annual state utilities
        self._annualStateUtilities = []
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_annual_state_cost(self, state):
        return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        return self._annualStateUtilities[state.value]

