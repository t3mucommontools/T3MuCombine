import ROOT
from collections import OrderedDict, deque

import argparse
parser = argparse.ArgumentParser('create a .sh file to export the ranges of the HF parameters')
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-S', '--scale' , default=5, type=float, help='Number of sigmas for the polynomial ranges')
args = parser.parse_args()

class Category:
  DEFAULT_RANGE = lambda par: (-100, 100)
  EXCLUDE       = ['m3m', 'm0_A', 'm0_B', 'm0_C', 'alpha_cb_A', 'alpha_cb_B', 'alpha_cb_C', 'n_cb_A', 'n_cb_B', 'n_cb_C']
  ranges = {
    'slope'       : DEFAULT_RANGE,
    'c_PowerLaw'  : DEFAULT_RANGE,
    'f_cb'        : DEFAULT_RANGE,
    'Bernstein'   : lambda par: (0,1),
    'sigma'       : lambda par: (0.001, 0.1),
    'c_Polynomial': lambda par: (par.getVal()-args.scale*par.getError(), par.getVal()+args.scale*par.getError()),
  }
  @staticmethod
  def get_range(par):
    for key, ran in Category.ranges.items():
      if key in par.GetName(): return ran(par)
    return Category.DEFAULT_RANGE(par)
  def __init__(self, name, file, ID=''):
    self.id     = ID
    self.name   = name
    self.file   = file
    self.values = []
  def parse(self):
    wspace = self.file.Get("w_all")
    params = ROOT.RooArgList(wspace.allVars())
    params = [params.at(i) for i in range(params.getSize()) if not params.at(i).GetName() in Category.EXCLUDE and self.id in params.at(i).GetName()]
    self.values = ':\\\n'.join(['{}={},{}'.format(p.GetName(),*Category.get_range(p)) for p in params])

class Collection:
  def __init__(self, categories, groups={}):
    self.c = OrderedDict([(c.name, c) for c in categories])
    self.g = groups
  def write(self, filepath):
    towrite = '\n'.join([
      'export {N}="\\\n{V}"'.format(N=nam, V=cat.values) for nam, cat in self.c.items()]+[
      'export {N}={V}'.format(N=nam, V=':'.join(['${}'.format(c) for c in lst])) for nam, lst in self.g.items()
      ])
    with open(filepath, 'w') as output_file:
      output_file.write(towrite)


# input files
whereami="/gwpool/users/lguzzi/Tau3Mu/2017_2018/combine_test/"
fbkg_3gl_17 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/ThreeGlobal/2017/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root"        , "READ")
fbkg_3gl_18 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/ThreeGlobal/2018/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root"        , "READ")
fsig_3gl_17 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/ThreeGlobal/2017/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root"     , "READ")
fsig_3gl_18 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/ThreeGlobal/2018/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root"     , "READ")
fbkg_2gl_17 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/TwoGlobalTracker/2017/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root"   , "READ")
fbkg_2gl_18 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/TwoGlobalTracker/2018/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root"   , "READ")
fsig_2gl_17 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/TwoGlobalTracker/2017/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root", "READ")
fsig_2gl_18 = ROOT.TFile.Open(whereami+"/T3MuCombine/T3MCombineAll/preapproval/TwoGlobalTracker/2018/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root", "READ")

HF_GROUPS = OrderedDict([
  # three global
  ('BKG_3GL_17'    , ['BKG_3GL_A1_17', 'BKG_3GL_A2_17', 'BKG_3GL_A3_17', 'BKG_3GL_B1_17', 'BKG_3GL_B2_17', 'BKG_3GL_B3_17', 'BKG_3GL_C1_17', 'BKG_3GL_C2_17', 'BKG_3GL_C3_17']),
  ('BKG_3GL_18'    , ['BKG_3GL_A1_18', 'BKG_3GL_A2_18', 'BKG_3GL_A3_18', 'BKG_3GL_B1_18', 'BKG_3GL_B2_18', 'BKG_3GL_B3_18', 'BKG_3GL_C1_18', 'BKG_3GL_C2_18', 'BKG_3GL_C3_18']),
  ('SIG_3GL_17_TMP', ['SIG_3GL_A1_17', 'SIG_3GL_A2_17', 'SIG_3GL_A3_17', 'SIG_3GL_B1_17', 'SIG_3GL_B2_17', 'SIG_3GL_B3_17', 'SIG_3GL_C1_17', 'SIG_3GL_C2_17', 'SIG_3GL_C3_17']),
  ('SIG_3GL_18_TMP', ['SIG_3GL_A1_18', 'SIG_3GL_A2_18', 'SIG_3GL_A3_18', 'SIG_3GL_B1_18', 'SIG_3GL_B2_18', 'SIG_3GL_B3_18', 'SIG_3GL_C1_18', 'SIG_3GL_C2_18', 'SIG_3GL_C3_18']),
  ('SIG_3GL_17'    , ['SIG_3GL_17_TMP', 'SIG_DUPLICATED']),
  ('SIG_3GL_18'    , ['SIG_3GL_18_TMP', 'SIG_DUPLICATED']),
  ('SIG_3GL'       , ['SIG_3GL_17_TMP', 'SIG_3GL_18_TMP', 'SIG_DUPLICATED']),
  ('BKG_3GL'       , ['BKG_3GL_17', 'BKG_3GL_18']),
  ('ALL_3GL'       , ['BKG_3GL', 'SIG_3GL']),
  # two global one tracker
  ('BKG_2GL_17'    , ['BKG_2GL_A1_17', 'BKG_2GL_A2_17', 'BKG_2GL_B1_17', 'BKG_2GL_B2_17', 'BKG_2GL_C1_17', 'BKG_2GL_C2_17']),
  ('BKG_2GL_18'    , ['BKG_2GL_A1_18', 'BKG_2GL_A2_18', 'BKG_2GL_B1_18', 'BKG_2GL_B2_18', 'BKG_2GL_C1_18', 'BKG_2GL_C2_18']),
  ('SIG_2GL_17_TMP', ['SIG_2GL_A1_17', 'SIG_2GL_A2_17', 'SIG_2GL_B1_17', 'SIG_2GL_B2_17', 'SIG_2GL_C1_17', 'SIG_2GL_C2_17']),
  ('SIG_2GL_18_TMP', ['SIG_2GL_A1_18', 'SIG_2GL_A2_18', 'SIG_2GL_B1_18', 'SIG_2GL_B2_18', 'SIG_2GL_C1_18', 'SIG_2GL_C2_18']),
  ('SIG_2GL_17'    , ['SIG_2GL_17_TMP', 'SIG_DUPLICATED']),
  ('SIG_2GL_18'    , ['SIG_2GL_18_TMP', 'SIG_DUPLICATED']),
  ('SIG_2GL'       , ['SIG_2GL_17_TMP', 'SIG_2GL_18_TMP', 'SIG_DUPLICATED']),
  ('BKG_2GL'       , ['BKG_2GL_17', 'BKG_2GL_18']),
  ('ALL_2GL'       , ['BKG_2GL', 'SIG_2GL']),
  # HF
  ('BKG_HF'        , ['BKG_2GL', 'BKG_3GL']),
  ('SIG_HF'        , ['SIG_3GL_17_TMP', 'SIG_3GL_18_TMP', 'SIG_2GL_17_TMP', 'SIG_2GL_18_TMP', 'SIG_DUPLICATED']),
  ('ALL_HF'        , ['SIG_HF', 'BKG_HF']),
])

HF_CATEGORIES = deque([
  # three global 2017 background
  Category(name='BKG_3GL_A1_17', file=fbkg_3gl_17, ID='_A1'),
  Category(name='BKG_3GL_A2_17', file=fbkg_3gl_17, ID='_A2'),
  Category(name='BKG_3GL_A3_17', file=fbkg_3gl_17, ID='_A3'),
  Category(name='BKG_3GL_B1_17', file=fbkg_3gl_17, ID='_B1'),
  Category(name='BKG_3GL_B2_17', file=fbkg_3gl_17, ID='_B2'),
  Category(name='BKG_3GL_B3_17', file=fbkg_3gl_17, ID='_B3'),
  Category(name='BKG_3GL_C1_17', file=fbkg_3gl_17, ID='_C1'),
  Category(name='BKG_3GL_C2_17', file=fbkg_3gl_17, ID='_C2'),
  Category(name='BKG_3GL_C3_17', file=fbkg_3gl_17, ID='_C3'),
  # three global 2018 background
  Category(name='BKG_3GL_A1_18', file=fbkg_3gl_18, ID='_A1'),
  Category(name='BKG_3GL_A2_18', file=fbkg_3gl_18, ID='_A2'),
  Category(name='BKG_3GL_A3_18', file=fbkg_3gl_18, ID='_A3'),
  Category(name='BKG_3GL_B1_18', file=fbkg_3gl_18, ID='_B1'),
  Category(name='BKG_3GL_B2_18', file=fbkg_3gl_18, ID='_B2'),
  Category(name='BKG_3GL_B3_18', file=fbkg_3gl_18, ID='_B3'),
  Category(name='BKG_3GL_C1_18', file=fbkg_3gl_18, ID='_C1'),
  Category(name='BKG_3GL_C2_18', file=fbkg_3gl_18, ID='_C2'),
  Category(name='BKG_3GL_C3_18', file=fbkg_3gl_18, ID='_C3'),
  # three global 2017 signal
  Category(name='SIG_3GL_A1_17', file=fsig_3gl_17, ID='_A1'),
  Category(name='SIG_3GL_A2_17', file=fsig_3gl_17, ID='_A2'),
  Category(name='SIG_3GL_A3_17', file=fsig_3gl_17, ID='_A3'),
  Category(name='SIG_3GL_B1_17', file=fsig_3gl_17, ID='_B1'),
  Category(name='SIG_3GL_B2_17', file=fsig_3gl_17, ID='_B2'),
  Category(name='SIG_3GL_B3_17', file=fsig_3gl_17, ID='_B3'),
  Category(name='SIG_3GL_C1_17', file=fsig_3gl_17, ID='_C1'),
  Category(name='SIG_3GL_C2_17', file=fsig_3gl_17, ID='_C2'),
  Category(name='SIG_3GL_C3_17', file=fsig_3gl_17, ID='_C3'),
  # three global 2018 signal
  Category(name='SIG_3GL_A1_18', file=fsig_3gl_17, ID='_A1'),
  Category(name='SIG_3GL_A2_18', file=fsig_3gl_17, ID='_A2'),
  Category(name='SIG_3GL_A3_18', file=fsig_3gl_17, ID='_A3'),
  Category(name='SIG_3GL_B1_18', file=fsig_3gl_17, ID='_B1'),
  Category(name='SIG_3GL_B2_18', file=fsig_3gl_17, ID='_B2'),
  Category(name='SIG_3GL_B3_18', file=fsig_3gl_17, ID='_B3'),
  Category(name='SIG_3GL_C1_18', file=fsig_3gl_17, ID='_C1'),
  Category(name='SIG_3GL_C2_18', file=fsig_3gl_17, ID='_C2'),
  Category(name='SIG_3GL_C3_18', file=fsig_3gl_17, ID='_C3'),
  # two global tracker 2017 background
  Category(name='BKG_2GL_A1_17', file=fbkg_2gl_17, ID='_A1'),
  Category(name='BKG_2GL_A2_17', file=fbkg_2gl_17, ID='_A2'),
  Category(name='BKG_2GL_B1_17', file=fbkg_2gl_17, ID='_B1'),
  Category(name='BKG_2GL_B2_17', file=fbkg_2gl_17, ID='_B2'),
  Category(name='BKG_2GL_C1_17', file=fbkg_2gl_17, ID='_C1'),
  Category(name='BKG_2GL_C2_17', file=fbkg_2gl_17, ID='_C2'),
  # two global tracker 2018 background
  Category(name='BKG_2GL_A1_18', file=fbkg_2gl_18, ID='_A1'),
  Category(name='BKG_2GL_A2_18', file=fbkg_2gl_18, ID='_A2'),
  Category(name='BKG_2GL_B1_18', file=fbkg_2gl_18, ID='_B1'),
  Category(name='BKG_2GL_B2_18', file=fbkg_2gl_18, ID='_B2'),
  Category(name='BKG_2GL_C1_18', file=fbkg_2gl_18, ID='_C1'),
  Category(name='BKG_2GL_C2_18', file=fbkg_2gl_18, ID='_C2'),
  # two global tracker 2017 background
  Category(name='SIG_2GL_A1_17', file=fsig_2gl_17, ID='_A1'),
  Category(name='SIG_2GL_A2_17', file=fsig_2gl_17, ID='_A2'),
  Category(name='SIG_2GL_B1_17', file=fsig_2gl_17, ID='_B1'),
  Category(name='SIG_2GL_B2_17', file=fsig_2gl_17, ID='_B2'),
  Category(name='SIG_2GL_C1_17', file=fsig_2gl_17, ID='_C1'),
  Category(name='SIG_2GL_C2_17', file=fsig_2gl_17, ID='_C2'),
  # two global tracker 2018 background
  Category(name='SIG_2GL_A1_18', file=fsig_2gl_18, ID='_A1'),
  Category(name='SIG_2GL_A2_18', file=fsig_2gl_18, ID='_A2'),
  Category(name='SIG_2GL_B1_18', file=fsig_2gl_18, ID='_B1'),
  Category(name='SIG_2GL_B2_18', file=fsig_2gl_18, ID='_B2'),
  Category(name='SIG_2GL_C1_18', file=fsig_2gl_18, ID='_C1'),
  Category(name='SIG_2GL_C2_18', file=fsig_2gl_18, ID='_C2'),
])

for c in HF_CATEGORIES: c.parse()

# duplicated signal parameters
SIG_DUPLICATED = Category(name='SIG_DUPLICATED', file=None)
SIG_DUPLICATED.values = "\
alpha_cb_A=-100,100:\\\n\
alpha_cb_B=-100,100:\\\n\
alpha_cb_C=-100,100:\\\n\
m0_A=-100,100:\\\n\
m0_B=-100,100:\\\n\
m0_C=-100,100:\\\n\
n_cb_A=-100,100:\\\n\
n_cb_B=-100,100:\\\n\
n_cb_C=-100,100"   # bypass missing year / category in the signal parameters
HF_CATEGORIES.appendleft(SIG_DUPLICATED)
HF_COLLECTIONS = Collection(categories=HF_CATEGORIES, groups=HF_GROUPS)
HF_COLLECTIONS.write(args.output)
