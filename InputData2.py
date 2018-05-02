#ED

SIM_LENGTH = 40   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DELTA_T = 1         # years (length of time step, how frequently you look at the patient)
DISCOUNT = 0.03

# transition matrix
TRANS_MATRIX_PCT = [
    [0,     0.713,      0,          0.287],   # sick
    [0,     0.8699,     0.0195,     0.1106],   # antibiotics
    [0,     0,          0.8532,     0.1468],   # side-effect
    [0,     0,          0,          1.0],     # well
    ]

# transition matrix
TRANS_MATRIX_ANTI = [
    [0,     0.832,    0,      0.168],   # sick
    [0,     0.9014,   0.0205, 0.0781],   # antibiotics
    [0,     0,        0.8926, 0.1074],   # side-effect
    [0,     0,        0,      1.0],     # well
    ]

# annual cost of each health state (PCT)
ANNUAL_STATE_COST_PCT = [
    40,     # sick
    73,      # antibiotics
    73,      # side effect
    0]      # well

# annual cost of each health state (antibiotics)
ANNUAL_STATE_COST_ANTI = [
    0,      # sick
    33,      # antibiotics
    33,      # side effect
    0]      # well

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    0.7,    # sick
    0.7,    # antibiotics
    0.6,    # side effect
    1.0]    # well


