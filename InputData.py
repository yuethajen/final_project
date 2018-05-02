
SIM_LENGTH = 40   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DELTA_T = 1         # years (length of time step, how frequently you look at the patient)
DISCOUNT = 0.03

# transition matrix
TRANS_MATRIX_PCT = [
    [0,     0.229,   0,      0.771],   # sick
    [0,     0.857,   0.029,  0.114],   # antibiotics
    [0,     0,       0.833,  0.167],   # side-effect
    [0,     0,       0,      1.0],     # well
    ]

# transition matrix
TRANS_MATRIX_ANTI = [
    [0,     0.631,   0,      0.369],   # sick
    [0,     0.849,   0.037,  0.114],   # antibiotics
    [0,     0,       0.833,  0.167],   # side-effect
    [0,     0,       0,      1.0],     # well
    ]

# annual cost of each health state (PCT)
ANNUAL_STATE_COST_PCT = [
    40,     # sick
    33,      # antibiotics
    33,      # side effect
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


