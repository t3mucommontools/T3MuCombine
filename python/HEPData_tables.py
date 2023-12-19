import hepdata_lib
from hepdata_lib import Variable, Uncertainty, Table, Submission

submission = Submission()

# Create the HEPData table
table90 = Table("Upper limits at 90% CL")
table95 = Table("Upper limits at 95% CL")

# Add column headers
table90.description = "Expected and observed upper limits on the $\\tau\\to3\mu$ branching fraction at 90% of confidence level for different categories of the analyis."
table90.location = "Data from Sec. 6."
table90.keywords["observables"] = ["CLS"]
table90.keywords["cmenergies"] = [13000.0]
table90.keywords["phrases"] = ["Decay", "Muon production", "Tau production", "Branching Fraction", "Beauty", "Charm", "Strange", "W Production"]
table90.keywords["reactions"] = [
  "P P --> D+ X",
  "P P --> D/S+ X",
  "P P --> B0 X",
  "P P --> B+ X",
  "P P --> B/S X",
  "P P --> W X", 
  "D+ --> TAU+ NUTAU",
  "D/S+ --> TAU+ NUTAU",
  "B0 --> TAU+ NUTAU X",
  "B/S --> TAU+ NUTAU X",
  "B+ --> TAU+ NUTAU X",
  "W+ --> TAU+ NUTAU",
  "TAU+ --> MU+ MU+ MU-"
]

table95.description = "Expected and observed upper limits on the $\\tau\\to3\mu$ branching fraction at 95% of confidence level for the Run2 combination."
table95.location = "Data from Sec. 6."
table95.keywords["observables"] = ["CLS"]
table95.keywords["phrases"] = ["Decay", "Muon production", "Tau production", "Branching Fraction", "Beauty", "Charm", "Strange", "W Production"]
table95.keywords["cmenergies"] = [13000.0]
table95.keywords["reactions"] = [
  "P P --> D+ X",
  "P P --> D/S+ X",
  "P P --> B0 X",
  "P P --> B+ X",
  "P P --> B/S X",
  "P P --> W X", 
  "D+ --> TAU+ NUTAU",
  "D/S+ --> TAU+ NUTAU",
  "B0 --> TAU+ NUTAU X",
  "B/S --> TAU+ NUTAU X",
  "B+ --> TAU+ NUTAU X",
  "W+ --> TAU+ NUTAU",
  "TAU+ --> MU+ MU+ MU-"
]

# Define the variables
var_cat90 = Variable("category", is_independent=True , is_binned=False)
var_exp90 = Variable("expected upper limit on $\\tau\\to3\mu$ at 90% CL", is_independent=False, is_binned=False)
var_obs90 = Variable("observed upper limit on $\\tau\\to3\mu$ at 90% CL", is_independent=False, is_binned=False)

var_cat95 = Variable("category", is_independent=True , is_binned=False)
var_exp95 = Variable("expected upper limit on $\\tau\\to3\mu$ at 95% CL", is_independent=False, is_binned=False)
var_obs95 = Variable("observed upper limit on $\\tau\\to3\mu$ at 95% CL", is_independent=False, is_binned=False)

# Add the variables to the table
table90.add_variable(var_cat90)
table90.add_variable(var_exp90)
table90.add_variable(var_obs90)

table95.add_variable(var_cat95)
table95.add_variable(var_exp95)
table95.add_variable(var_obs95)


values90 = {# category: (expected, observed)
  'Heavy Flavour 2017-2018'      : (3.6e-8, 3.4e-8),
  'W 2017-2018'                  : (5.6e-8, 8.0e-8),
  'Heavy Flavour and W 2017-2018': (2.7e-8, 3.1e-8),
  'Result on the Run2 dataset'   : (2.4e-8, 2.9e-8),
}

values95 = {# category: (expected, observed)
  'Result on the Run2 dataset'   : (3.0e-8, 3.6e-8),
}

var_cat90.values = [k     for k in values90.keys()  ]
var_exp90.values = [v[0]  for v in values90.values()]
var_obs90.values = [v[1]  for v in values90.values()]

var_cat95.values = [k     for k in values95.keys()  ]
var_exp95.values = [v[0]  for v in values95.values()]
var_obs95.values = [v[1]  for v in values95.values()]

submission.add_table(table90)
submission.add_table(table95)
submission.create_files("HEPDATA_T3M", remove_old=True)