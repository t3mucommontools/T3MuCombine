from __future__ import print_function
import ROOT
from ROOT import RooFit
import os
import gc; gc.disable()
import argparse
parser = argparse.ArgumentParser('''
This script is a python adaptation of the HNL discrete profiling c++ code
https://github.com/BParkHNLs/flashggFinalFit/blob/mg-branch/Background/test/fTest.cpp
NOTE: input files must contain a branch called 'mass' and possibly be already skimmed.
NOTE: the code will probably crash on exit. This is somehow related to the RooChi2Var object.
'''
)
parser.add_argument('-c', '--category'  , type=str  , default='3glb_17_A'       , help='category to fit'                    )
parser.add_argument('-m', '--mass'      , type=str  , default='tripletMass'        , help='name of the 3mu mass variable'      )
parser.add_argument('-t', '--tree'      , type=str  , default='OutputTree'        , help='name of the input tree'             )
parser.add_argument('-M', '--max-order' , type=int  , default=6             , help='max pdf order to consider'          )
parser.add_argument('-U', '--unblind'   , action='store_true'                          , help='don\'t use blinded ranges'          )
args = parser.parse_args()


filename = '/eos/user/f/fsimone/Tau23Mu_anatools/optim_Combine/T3MCombine/workdir/CMSSW_10_2_13/src/CombineHarvester/T3M_HF/inputdata/t3mminitree_xgb_2017_2may22_ptmu3.root'
#filename = '/eos/user/f/fsimone/Tau23Mu_anatools/optim_Combine/T3MCombine/workdir/CMSSW_10_2_13/src/CombineHarvester/T3M_HF/inputdata/t3mminitree_xgb_2018_2may22_ptmu3.root'

bdt_name = "bdt_cv"
categ_name = "category"
MClabel_name = "isMC"
weight_name = "weight"

mass = ROOT.RooRealVar(args.mass, args.mass, 38, 1.62, 2.0, 'GeV')
roobdt = ROOT.RooRealVar(bdt_name, bdt_name, -2, 2);
roocategory = ROOT.RooRealVar(categ_name, categ_name, 0, 2); #mass resolution category 0=A, 1=B, 2=C
roomc = ROOT.RooRealVar(MClabel_name, MClabel_name, 0, 4); #0=data, 1=Ds, 2=B0, 3=Bp, 4=W
rooweight = ROOT.RooRealVar(weight_name, weight_name, 0, 1); #normalisation of MC including corrections i.e. PU reweighting

mass.setRange('unblinded', 1.62, 2.0)

category = args.category

mass_range_left = {
        '3glb_17_A': [1.62, 1.75],
        '3glb_18_A': [1.62, 1.75],
        '3glb_17_B': [1.62, 1.74],
        '3glb_18_B': [1.62, 1.74],
        '3glb_17_C': [1.62, 1.73],
        '3glb_18_C': [1.62, 1.73]
        }

mass_range_right = {
        '3glb_17_A': [1.80, 2.0],
        '3glb_18_A': [1.80, 2.0],
        '3glb_17_B': [1.82, 2.0],
        '3glb_18_B': [1.82, 2.0],
        '3glb_17_C': [1.83, 2.0],
        '3glb_18_C': [1.83, 2.0]
        }

data_cut = MClabel_name+'==0 '

bdt_cuts = {
        '3glb_17_A': bdt_name+'>0.5825',
        '3glb_18_A': bdt_name+'>0.2225',
        '3glb_17_B': bdt_name+'>0.6175',
        '3glb_18_B': bdt_name+'>0.2325',
        '3glb_17_C': bdt_name+'>0.4725',
        '3glb_18_C': bdt_name+'>0.4525'
        }

category_cuts = {
        '3glb_17_A': categ_name+'==0',
        '3glb_18_A': categ_name+'==0',
        '3glb_17_B': categ_name+'==1',
        '3glb_18_B': categ_name+'==1',
        '3glb_17_C': categ_name+'==2',
        '3glb_18_C': categ_name+'==2'
        }

mass.setRange('left', mass_range_left[category][0], mass_range_left[category][1])
mass.setRange('right', mass_range_right[category][0], mass_range_right[category][1])
pdfs = ROOT.RooWorkspace('pdfs')

rootfile = ROOT.TFile(filename, 'READ')
tree = rootfile.Get(args.tree)
args.max_order = min(args.max_order, tree.GetEntries()-2)

getattr(pdfs, 'import')(mass)
c_powerlaw = ROOT.RooRealVar("c_PowerLaw", "", 1, 0, 10)
powerlaw = ROOT.RooGenericPdf("PowerLaw", "TMath::Power(@0, @1)", ROOT.RooArgList(mass, c_powerlaw))
getattr(pdfs, 'import')(powerlaw)

#pdfs.factory("Exponential::Exponential(mass, slope[0, -10, 10])")
exp_slope = ROOT.RooRealVar('exp_slope', 'exp_slope', 0, -10, 10)
expo = ROOT.RooExponential('Exponential', 'Exponential', mass, exp_slope)
getattr(pdfs, 'import')(expo)

BernsteinMap = {}
ChebychevMap = {}

## Bernstein polynomials
for i in range(1, args.max_order+1):
  c_bernstein = [ ROOT.RooRealVar('c_Bernstein{}'.format(j), 'c_Bernstein{}'.format(j), 0.01, -10, 10) for j in range(1,i+1)]
  c_chebychev = [ ROOT.RooRealVar('c_Chebychev{}'.format(j), 'c_Chebychev{}'.format(j), 0.01, -10, 10) for j in range(1,i+1)]
  BernsteinMap['Bertnstein{}'.format(i)] = ROOT.RooBernstein('Bernstein{}'.format(i), 'Bernstein{}'.format(i), mass, ROOT.RooArgList(*c_bernstein))
  ChebychevMap['Chebychev{}'.format(i)] = ROOT.RooChebychev('Chebychev{}'.format(i), 'Chebychev{}'.format(i), mass, ROOT.RooArgList(*c_chebychev))
  #pdfs.factory('Bernstein::Bernstein{}(mass, {})'.format(i, c_bernstein))
  #pdfs.factory('Chebychev::Chebychev{}(mass, {})'.format(i, c_chebychev))
  getattr(pdfs, 'import')(BernsteinMap['Bertnstein{}'.format(i)])
  getattr(pdfs, 'import')(ChebychevMap['Chebychev{}'.format(i)])

wspace = ROOT.RooWorkspace('wspace')
getattr(wspace, 'import')(mass)
wspace.var(args.mass).setBins(38)

variables = ROOT.RooArgSet(mass);
variables.add(roobdt)
variables.add(roocategory)
variables.add(roomc)
variables.add(rooweight)

data = ROOT.RooDataSet('data', '', tree, variables, data_cut+"&&"+category_cuts[category]+"&&"+bdt_cuts[category],"weight")#.binnedClone('data')
hist = data.binnedClone('histo')
getattr(wspace, 'import')(data)
print(data_cut+"&&"+category_cuts[category]+"&&"+bdt_cuts[category])

frame = wspace.var(args.mass).frame()
wspace.data('data').plotOn(frame)

envelope = ROOT.RooArgList("envelope")

can = ROOT.TCanvas()
leg = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)

gofmax  = 0
bestfit = None
#families = ['PowerLaw', 'Bernstein', 'Chebychev', 'Exponential']
families = ['PowerLaw', 'Bernstein', 'Exponential']
allpdfs_list = ROOT.RooArgList(pdfs.allPdfs())
allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]
chi2Map = {}
for j, fam in enumerate(families):
  pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
  mnlls    = []
  for i, pdf in enumerate(pdf_list):
    norm = ROOT.RooRealVar("nbkg", "", 0, 1e+3)
    ext_pdf = ROOT.RooAddPdf(pdf.GetName()+"_ext", "", ROOT.RooArgList(pdf), ROOT.RooArgList(norm)) if not 'Bernstein' in pdf.GetName() else pdf
    results = ext_pdf.fitTo(data,  ROOT.RooFit.Save(True), ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'), ROOT.RooFit.Extended(not 'Bernstein' in pdf.GetName()))
    chi2 = ROOT.RooChi2Var("chi2"+pdf.GetName(), "", ext_pdf, hist, ROOT.RooFit.DataError(ROOT.RooAbsData.Expected))
    mnll = results.minNll()+(i*0.5)

    gof_prob = 0
    #gof_prob = ROOT.TMath.Prob(chi2Map[fam].getVal(), hist.numEntries()-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
    gof_prob = ROOT.TMath.Prob(chi2.getVal(), hist.numEntries()-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
    fis_prob = ROOT.TMath.Prob(-2.*(mnlls[-1]-mnll), 1) if len(mnlls) else 0

    mnlls.append(mnll)

    print(">>>", pdf.GetName(), gof_prob, fis_prob)

    if gof_prob > 0.01 and fis_prob < 0.1 and results.covQual()==3::
      if gof_prob > gofmax:
        gofmax = gof_prob
        bestfit = pdf.GetName()
      envelope.add(pdf)
      print(">>>"+pdf.GetName()+" added to envelope")
      pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()), ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'))
    del chi2 # RooChi2Var makes the code crash at the end of the execution. This line makes it crash faster.
for pdf in [envelope.at(i) for i in range(envelope.getSize())]:
  leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (bestfit)" if bestfit==pdf.GetName() else pdf.GetName(), "l")

frame.Draw()
leg.Draw("SAME")
can.Update()
can.Modified()
can.SaveAs("test.png")

cat = ROOT.RooCategory("roomultipdf_cat", "")

print(envelope.getSize())

multipdf = ROOT.RooMultiPdf("multipdf", "", cat, envelope)
cat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(bestfit))
outerspace = ROOT.RooWorkspace('ospace')
getattr(outerspace, 'import')(envelope)
getattr(outerspace, 'import')(multipdf)

if not os.path.exists('MultiPdfWorkspaces'):
  os.makedirs("MultiPdfWorkspaces")
outerspace.writeToFile("MultiPdfWorkspaces/"+args.category+".root")

print("\nExecution is complete. I may crash in peace\n")
#import pdb; pdb.set_trace()
