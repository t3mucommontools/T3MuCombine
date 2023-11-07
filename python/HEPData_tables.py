import hepdata_lib
from hepdata_lib import Variable, Uncertainty, Table, Submission

submission = Submission()

# Create the HEPData table
table90 = Table("90")
table95 = Table("95")

# Add column headers
table90.description = "Expected and observed upper limits on the #tau->3#mu branching fraction at 90\% of confidence level, expressed in units of 10^{-8}, for different categories of the analyis."
table90.location = "Data from Sec. 6 (page 12)."
table90.keywords["observables"] = ["expected", "observed", "upper", "limit", "90"]

table95.description = "Expected and observed upper limits on the #tau->3#mu branching fraction at 95\% of confidence level, expressed in units of 10^{-8}, for the Run2 combination."
table95.location = "Data from Sec. 6 (page 12)."
table95.keywords["observables"] = ["expected", "observed", "upper", "limit", "95"]

# Define the variables
var_cat90 = Variable("category", is_independent=True , is_binned=False)
var_exp90 = Variable("expected", is_independent=False, is_binned=False)
var_obs90 = Variable("observed", is_independent=False, is_binned=False)

var_cat95 = Variable("category", is_independent=True , is_binned=False)
var_exp95 = Variable("expected", is_independent=False, is_binned=False)
var_obs95 = Variable("observed", is_independent=False, is_binned=False)

# Add the variables to the table
table90.add_variable(var_cat90)
table90.add_variable(var_exp90)
table90.add_variable(var_obs90)

table95.add_variable(var_cat90)
table95.add_variable(var_exp90)
table95.add_variable(var_obs90)


values90 = {# category: (expected, observed)
  'Heavy Flavour 2017-2018'      : (3.6, 3.4),
  'W 2017-2018'                  : (5.6, 8.0),
  'Heavy Flavour and W 2017-2018': (2.7, 3.1),
  'Result on the Run2 dataset'   : (2.4, 2.9),
}

values95 = {# category: (expected, observed)
  'Result on the Run2 dataset'   : (3.0, 3.6),
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