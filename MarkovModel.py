import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import scr.RandomVariantGenerators as rndClasses
import scr.EconEvalClasses as EconCls
import ParameterClasses as P
import InputData2 as Data

# patient class simulates patient, patient monitor follows patient, cohort simulates a cohort,
#  cohort outcome extracts info from simulation and returns it back


class Patient:  # when you store in self then all the things in that class have access to it
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: parameter object
        """

        self._id = id
        # random number generator
        self._rng = None
        # parameters
        self._param = parameters
        # state monitor
        self._stateMonitor = PatientStateMonitor(parameters)
        # simulate time step
        self._delta_t = parameters.get_delta_t() # length of time step!

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """
        # random number generator for this patient
        self._rng = rndClasses.RNG(self._id)  # from now on use random number generator from support library

        k = 0  # current time step

        # while the patient is alive and simulation length is not yet reached
        while self._stateMonitor.get_if_alive() and k*self._delta_t < sim_length:
            # find transition probabilities of future state
            trans_prob = self._param.get_transition_prob(self._stateMonitor.get_current_state())
            # create an empirical distribution
            empirical_dist = rndClasses.Empirical(trans_prob)
            # sample from the empirical distribution to get a new state
            # (return an integer from {0, 1, 2, ...}
            new_state_index = empirical_dist.sample(self._rng) # pass RNG

            # update health state
            self._stateMonitor.update(k, P.HealthStats(new_state_index))

            # increment time step
            k += 1

    def get_survival_time(self):
        """ returns the patient's survival time"""
        return self._stateMonitor.get_survival_time()

    def get_total_discounted_cost(self):
        """ :returns total discounted cost """
        return self._stateMonitor.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        """ :returns total discounted utility"""
        return self._stateMonitor.get_total_discounted_utility()


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):
        """
        :param parameters: patient parameters
        """
        # current health state
        self._currentState = parameters.get_initial_health_state()
        self._delta_t = parameters.get_delta_t()
        self._survivalTime = 0

        # monitoring cost and utility outcomes
        self._costUtilityOutcomes = PatientCostUtilityMonitor(parameters)

    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state
        """
        # updates state of patient
        # if the patient has died, do nothing
        if not self.get_if_alive():
            return

        # update survival time (time to get well)
        if next_state is P.HealthStats.WELL and k == 0:
            self._survivalTime = 0
        else:
            self._survivalTime = (k-1) * self._delta_t  # k is number of steps its been, delta t is length of time

        # collect cost and utility outcomes
        self._costUtilityOutcomes.update(k, self._currentState, next_state)

        # update current health state
        self._currentState = next_state

    def get_if_alive(self):
        result = True
        if self._currentState == P.HealthStats.WELL:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def get_survival_time(self):
        """ returns the patient survival time """
        # return survival time only if the patient has died
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None

    def get_total_discounted_cost(self):
        """ :returns total discounted cost """
        return self._costUtilityOutcomes.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        """ :returns total discounted utility"""
        return self._costUtilityOutcomes.get_total_discounted_utility()


class Cohort:
    def __init__(self, id, pop_size, therapy):
        """ create a cohort of patients
        :param id: an integer to specify the seed of the random number generator
        """
        self._initial_pop_size = pop_size
        self._patients = []      # list of patients

        # populate the cohort
        for i in range(self._initial_pop_size):
            # create a new patient (use id * pop_size + i as patient id)
            patient = Patient(id * self._initial_pop_size + i, P.ParametersFixed(therapy))
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self):
        """ simulate the cohort of patients over the specified number of time-steps
        :returns outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            patient.simulate(Data.SIM_LENGTH)

        # return the cohort outputs
        return CohortOutputs(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class CohortOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from a simulated cohort
        :param simulated_cohort: a cohort after being simulated
        """

        self._survivalTimes = []        # patients' survival times
        self._costs = []                # patients' discounted total costs
        self._utilities = []            # patients' discounted total utilities

        # survival curve
        self._survivalCurve = \
            PathCls.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # get the patient survival time
            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)           # store the survival time of this patient
                self._survivalCurve.record(survival_time, -1)       # update the survival curve

            # cost and utility
            self._costs.append(patient.get_total_discounted_cost())
            self._utilities.append(patient.get_total_discounted_utility())

        # summary statistics
        self._sumStat_survivalTime = StatCls.SummaryStat('Patient time to bacterial infection free', self._survivalTimes)
        self._sumStat_cost = StatCls.SummaryStat('Patient discounted cost', self._costs)
        self._sumStat_utility = StatCls.SummaryStat('Patient discounted utility', self._utilities)

    def get_survival_times(self):
        return self._survivalTimes

    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime

    def get_survival_curve(self):
        return self._survivalCurve

    def get_costs(self):
        return self._costs

    def get_utilities(self):
        return self._utilities

    def get_sumStat_discounted_cost(self):
        return self._sumStat_cost

    def get_sumStat_discounted_utility(self):
        return self._sumStat_utility


class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        # model parameters for this patient
        self._param = parameters

        # total cost and utility
        self._totalDiscountedCost = 0
        self._totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param k: simulation time step
        :param current_state: current health state
        :param next_state: next health state
        """

        # update cost
        cost = self._param.get_annual_state_cost(current_state) * self._param.get_delta_t()
        # update utility
        utility = self._param.get_annual_state_utility(current_state) * self._param.get_delta_t()



        if next_state in [P.HealthStats.WELL]:
            utility += 1*(Data.SIM_LENGTH - k)

        # update total discounted cost and utility (corrected for the half-cycle effect)
        self._totalDiscountedCost += \
            EconCls.pv(cost, self._param.get_adj_discount_rate() / 2, 2*k + 1)
        self._totalDiscountedUtility += \
            EconCls.pv(utility, self._param.get_adj_discount_rate() / 2, 2*k + 1)

    def get_total_discounted_cost(self):
        """ :returns total discounted cost """
        return self._totalDiscountedCost

    def get_total_discounted_utility(self):
        """ :returns total discounted utility"""
        return self._totalDiscountedUtility

