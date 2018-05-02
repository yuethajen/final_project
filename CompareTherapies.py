import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov


# simulating PCT
# create a cohort
cohort_PCT = MarkovCls.Cohort(
    id=0,
    pop_size=2000,
    therapy=P.Therapies.PCT)
# simulate the cohort
simOutputs_PCT = cohort_PCT.simulate()

# simulating antibiotics
# create a cohort
cohort_antibiotics = MarkovCls.Cohort(
    id=1,
    pop_size=2000,
    therapy=P.Therapies.ANTIBIOTICS)
# simulate the cohort
simOutputs_antibiotics = cohort_antibiotics.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_antibiotics, simOutputs_PCT)

# print the estimates for the mean survival time and mean time to AIDS
SupportMarkov.print_outcomes(simOutputs_antibiotics, "Standard treatment:")
SupportMarkov.print_outcomes(simOutputs_PCT, "PCT:")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_antibiotics, simOutputs_PCT)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_antibiotics, simOutputs_PCT)
