import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.ROOT.EnableImplicitMT(10)
from hepdata_lib.root_utils import get_hist_1d_points
from hepdata_lib            import Variable, Uncertainty, Table, Submission
import numpy as np

submission = Submission()

phiveto   = "(( ((abs(cand_refit_mass12-1.020)<0.02)*(cand_charge12==0)) + \
                ((abs(cand_refit_mass13-1.020)<0.02)*(cand_charge13==0)) + \
                ((abs(cand_refit_mass23-1.020)<0.02)*(cand_charge23==0)) ) == 0)"
omegaveto = "(( ((abs(cand_refit_mass12-0.782)<0.02)*(cand_charge12==0)) + \
                ((abs(cand_refit_mass13-0.782)<0.02)*(cand_charge13==0)) + \
                ((abs(cand_refit_mass23-0.782)<0.02)*(cand_charge23==0)) ) == 0)"
baseline = " & ".join([
  "abs(cand_charge) == 1",
  "abs(cand_refit_tau_mass - 1.8) < 0.2",
  "(HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Charge1_matched==1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_matched==1)",
  "((mu1_refit_pt > 3.5 & abs(mu1_refit_eta) < 1.2) || (mu1_refit_pt > 2.0 & abs(mu1_refit_eta) >= 1.2 & abs(mu1_refit_eta) < 2.4))",
  "((mu2_refit_pt > 3.5 & abs(mu2_refit_eta) < 1.2) || (mu2_refit_pt > 2.0 & abs(mu2_refit_eta) >= 1.2 & abs(mu2_refit_eta) < 2.4))",
  "((mu3_refit_pt > 3.5 & abs(mu3_refit_eta) < 1.2) || (mu3_refit_pt > 2.0 & abs(mu3_refit_eta) >= 1.2 & abs(mu3_refit_eta) < 2.4))",
  "mu1_refit_muonid_medium==1",
  "mu2_refit_muonid_medium==1",
  "mu3_refit_muonid_medium==1",
  "mu1_refit_pt > 7",
  "(cand_refit_dR12 < 0.5 || cand_refit_dR13 < 0.5 || cand_refit_dR23 < 0.5)",
  "(cand_refit_mass12 < 1.9 || cand_refit_mass13 < 1.9 || cand_refit_mass23 < 1.9)",
  "cand_refit_tau_pt > 15",
  "abs(cand_refit_tau_eta) < 2.5",
  "tau_sv_ls>2",
  phiveto, omegaveto
])
catA17 = "(year==17 & bdt>0.991 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass>0.000 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass<0.007)"
catB17 = "(year==17 & bdt>0.994 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass>0.007 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass<0.012)"
catC17 = "(year==17 & bdt>0.992 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass>0.012 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass<9999.)"
catA18 = "(year==18 & bdt>0.995 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass>0.000 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass<0.007)"
catB18 = "(year==18 & bdt>0.998 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass>0.007 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass<0.012)"
catC18 = "(year==18 & bdt>0.994 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass>0.012 & sqrt(cand_refit_tau_massE)/cand_refit_tau_mass<9999.)"

mc = ROOT.RDataFrame('tree', '/gwpool/users/lguzzi/Tau3Mu/2017_2018/BDT/singleclass/ntuples/signal_threeMedium_weighted_16Mar2022.root').Filter(baseline)
da = ROOT.RDataFrame('tree', '/gwpool/users/lguzzi/Tau3Mu/2017_2018/BDT/singleclass/ntuples/background_threeMedium-UNBLINDED.root')     .Filter(baseline)

class MyVariable:
  def __init__(self,
  name                , # variable name as saved in the root file
  binning             , # (nbins, min, max)
  entries             , # dictionary of samples for the current variable (data, mc)
  heplabelx           , # x label
  heptablename        , # table name
  binned      = False , 
  units       = ''    ,
  description = ''    , # table description
  location    = ''    , # table location
  keywords    = {'observables': []},
  ):
    self.entries  = entries
    self.variable = Variable(name, is_independent=True, is_binned=binned, units=units, values=list(np.linspace(binning[1],binning[2],binning[0])))
    
    self.histograms = [
      entry.Histo1D(("{} ({})".format(name, k), '', *binning), name) for k, entry in entries.items()
    ]

    self.table = Table(heptablename)
    self.table.description  = description
    self.table.location     = location
    self.table.keywords     = keywords
    self.table.add_variable(self.variable)

  def fetch(self):
    for ptr in self.histograms:
      hst = ptr.GetValue()
      var = Variable    (hst.GetName(), is_independent=False, is_binned=self.variable.is_binned, units=self.variable.units, values=[hst.GetBinContent(i) for i in range(1,hst.GetSize()-1)])
      err = Uncertainty ('uncertainty', is_symmetric=False) 
      err.values = MyVariable.gamma_error(var)
      var.add_uncertainty(err)
      self.table.add_variable(var)
  @staticmethod
  def gamma_error(var):
    return [(
      ROOT.Math.gamma_quantile  ((1 - 0.6827)/2,y   ,1.) if y else 0, 
      ROOT.Math.gamma_quantile_c((1 - 0.6827)/2,y+1 ,1.) )
      for y in var.values
    ]

TABLES = [
  MyVariable('cand_refit_tau_pt', (50, 0, 80)       ,
    entries       = {'data': da, 'W\to3\mu\nu MC': mc}          ,
    units         = 'GeV'                           ,
    heplabelx     = 'Trimuon transverse momentum'   ,
    heptablename  = 'Figure 5a'                     , 
    location      = 'Data from figure 5 on page 10' ,
    description   = 'Signal and background distributions of the signal candidate transverse momentum, used for the W boson analysis BDT training.',
    keywords      = {'observables': ['transverse', 'momentum', 'signal', 'candidate']},
  ),
  MyVariable('tau_sv_prob', (50, 0, 1)                        ,
    entries       = {'data': da, 'W\to3\mu\nu MC': mc}                    ,
    units         = 'GeV'                                     ,
    heplabelx     = 'Trimuon vertex fit #chi^{2} probability' ,
    heptablename  = 'Figure 5b'                               ,
    location      = 'Data from figure 5 on page 10'           ,
    description   = 'Signal and background distributions of the signal candidate secondary vertex fit p-value, used for the W boson analysis BDT training.',
    keywords      = {'observables': ['secondary', 'vertex', 'fit', 'probability', 'chi', 'chi2']},
  ),
  MyVariable('tau_sv_cos', (100, 0.9985, 1)                           ,
    entries       = {'data': da, 'W\to3\mu\nu MC': mc}                            ,
    units         = 'GeV'                                             ,
    heplabelx     = 'Cosine of the 2D pointing angle cos(#alpha_{2D})',
    heptablename  = 'Figure 5c'                                       ,
    location      = 'Data from figure 5 on page 10'                   ,
    description   = 'Signal and background distributions of the signal candidate secondary vertex pointing angle cosine, used for the W boson analysis BDT training.',
    keywords      = {'observables': ['signal', 'candidate', 'relative', 'iosolation']},
  ),
  MyVariable('cand_refit_tau_dBetaIsoCone0p8strength0p2_rel', (50, 0, 1),
    entries       = {'data': da, 'W\to3\mu\nu MC': mc}                  ,
    units         = 'GeV'                                   ,
    heplabelx     = 'Trimuon relative isolation'            ,
    heptablename  = 'Figure 5d'                             ,
    location      = 'Data from figure 5 on page 10'         ,
    description   = 'Signal and background distributions of the signal candidate isolation, used for the W boson analysis BDT training.',
    keywords      = {'observables': ['signal', 'candidate', 'relative', 'iosolation']},
  ),
  MyVariable('cand_refit_tau_mass', (40, 1.6, 2.0),
    entries       = {'data': da.Filter(catA18), 'W\to3\mu\nu MC': mc.Filter(catA18)},
    units         = 'GeV'                                   ,
    heplabelx     = 'm(3#mu)'                               ,
    heptablename  = 'Figure 6a'                             ,
    location      = 'Data from figure 6 on page 11'         ,
    description   = 'Invariant mass distribution of the signal candidates in the leading category of 2018.',
    keywords      = {'observables': ['signal', 'candidate', 'invariant', 'mass', 'leading', '2018']},
  ),
  MyVariable('cand_refit_tau_mass', (40, 1.6, 2.0),
    entries       = {'data': da.Filter(catB18), 'W\to3\mu\nu MC': mc.Filter(catB18)},
    units         = 'GeV'                                   ,
    heplabelx     = 'm(3#mu)'                               ,
    heptablename  = 'Figure 6b'                             ,
    location      = 'Data from figure 6 on page 11'         ,
    description   = 'Invariant mass distribution of the signal candidates in the sub-leading category of 2018.',
    keywords      = {'observables': ['signal', 'candidate', 'invariant', 'mass', 'subleading', '2018']},
  ),
  MyVariable('cand_refit_tau_mass', (40, 1.6, 2.0),
    entries       = {'data': da.Filter(catC18), 'W\to3\mu\nu MC': mc.Filter(catC18)},
    units         = 'GeV'                                   ,
    heplabelx     = 'm(3#mu)'                               ,
    heptablename  = 'Figure 6c'                             ,
    location      = 'Data from figure 6 on page 11'         ,
    description   = 'Invariant mass distribution of the signal candidates in the trailing category of 2018.',
    keywords      = {'observables': ['signal', 'candidate', 'invariant', 'mass', 'trailing', '2018']},
  ),
  MyVariable('cand_refit_tau_mass', (40, 1.6, 2.0),
    entries       = {'data': da.Filter(catA17), 'W\to3\mu\nu MC': mc.Filter(catA17)},
    units         = 'GeV'                                   ,
    heplabelx     = 'm(3#mu)'                               ,
    heptablename  = 'Supplementary figure a'                             ,
    location      = '',
    description   = 'Invariant mass distribution of the signal candidates in the leading category of 2017.',
    keywords      = {'observables': ['signal', 'candidate', 'invariant', 'mass', 'leading', '2017']},
  ),
  MyVariable('cand_refit_tau_mass', (40, 1.6, 2.0),
    entries       = {'data': da.Filter(catB17), 'W\to3\mu\nu MC': mc.Filter(catB17)},
    units         = 'GeV'                                   ,
    heplabelx     = 'm(3#mu)'                               ,
    heptablename  = 'Supplementary figure b'                             ,
    location      = '',
    description   = 'Invariant mass distribution of the signal candidates in the sub-leading category of 2017.',
    keywords      = {'observables': ['signal', 'candidate', 'invariant', 'mass', 'subleading', '2017']},
  ),
  MyVariable('cand_refit_tau_mass', (40, 1.6, 2.0),
    entries       = {'data': da.Filter(catC17), 'W\to3\mu\nu MC': mc.Filter(catC17)},
    units         = 'GeV'                                   ,
    heplabelx     = 'm(3#mu)'                               ,
    heptablename  = 'Supplementary figure c'                             ,
    location      = '',
    description   = 'Invariant mass distribution of the signal candidates in the trailing category of 2017.',
    keywords      = {'observables': ['signal', 'candidate', 'invariant', 'mass', 'trailing', '2017']},
  ),
]
for tab in TABLES:
  tab.fetch()
  submission.add_table(tab.table)
submission.create_files("WChannel", remove_old=True)