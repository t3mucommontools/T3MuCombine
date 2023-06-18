import ROOT
from collections import OrderedDict, deque

import argparse
parser = argparse.ArgumentParser('create a .sh file to export the ranges from the run2 workspace')
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-i', '--input',  required=True)
parser.add_argument('-S', '--scale' , default=5, type=float, help='Number of sigmas for the polynomial ranges')
args = parser.parse_args()

DEFAULT_RANGE = lambda par: (-30, 30)
class Category:
  EXCLUDE = ['m3m', 'M3m', 'r']
  ranges = {
    'slope'       : DEFAULT_RANGE,
    'c_PowerLaw'  : DEFAULT_RANGE,
    'p0A'         : lambda par: (0, 1),
    'p0B'         : lambda par: (0, 1),
    'p0C'         : lambda par: (0, 1),
    'p1A'         : lambda par: (0, 1),
    'p1B'         : lambda par: (0, 1),
    'p1C'         : lambda par: (0, 1),
    'p4A'         : lambda par: (0, 1),
    'p4B'         : lambda par: (0, 1),
    'p4C'         : lambda par: (0, 1),
    'HLT_TkMu'    : lambda par: (-5, 5),
    'HLT_Mu'      : lambda par: (-5, 5),
    'muonID'      : lambda par: (-5, 5),
    'mc_stat'     : lambda par: (-5, 5),
    'br_Wmunu'    : lambda par: (-5, 5),
    'br_Wtaunu'   : lambda par: (-5, 5),
    'xs_W'        : lambda par: (-5, 5),
    'Lumi'        : lambda par: (-5, 5),
    'WNLO'        : lambda par: (-5, 5),
    'alpha_cb'    : lambda par: (-10, 10),
    'n_cb'        : lambda par: (0, 200),
    'f_cb'        : lambda par: (0,1),
    'bkgNorm'     : lambda par: (0, 1e+5),
    'DsNorm'      : lambda par: (-5,5),
    'ySig'        : lambda par: (-5,5),
    'WNorm'       : lambda par: (-5,5),
    'hlt_'        : lambda par: (-5,5),
    'Unc'         : lambda par: (-5,5),
    '_norm'       : lambda par: (0.99, 1.01),
    'c_Bernstein' : lambda par: (0,1),
    'sigma'       : lambda par: (0.001, 0.1),
    'c_Polynomial': lambda par: (par.getVal()-args.scale*par.getError(), par.getVal()+args.scale*par.getError()),
  }
  @staticmethod
  def get_range(par):
    for key, ran in Category.ranges.items():
      if key in par.GetName(): return ran(par)
    return DEFAULT_RANGE(par)
  def __init__(self, name, file, ID='', wspace='w_all'):
    self.id     = ID
    self.wspace = wspace
    self.name   = name
    self.file   = file
    self.values = []
  def parse(self):
    wspace = self.file.Get(self.wspace)
    params = ROOT.RooArgList(wspace.allVars())
    params = [params.at(i) for i in range(params.getSize()) if not params.at(i).GetName() in Category.EXCLUDE]
    params = [p for p in params if 'Bernstein' in p.GetName() or any(n in p.GetName() for n in [
      'p0A',
      'p0B',
      'p0C',
      'p1A',
      'p1B',
      'p1C',
      'p4A',
      'p4B',
      'p4C',
    ])]
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


run2_merged = ROOT.TFile.Open(args.input, "READ")
RUN2_GROUPS={'RUN2_PARS': ["Run2"]}
RUN2_CATEGORY = Category(name="Run2", file=run2_merged, ID="RUN2", wspace="w")
RUN2_CATEGORY.parse()
RUN2_COLLECTION=Collection(categories=[RUN2_CATEGORY], groups=RUN2_GROUPS)
RUN2_COLLECTION.write(args.output)
