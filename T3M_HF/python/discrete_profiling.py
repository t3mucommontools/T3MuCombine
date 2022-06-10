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
parser.add_argument('-s', '--settings'  , type=str  , default='config_xgboost_TwoGlobalTracker_2018.txt',    help='config file')
parser.add_argument('-c', '--category'  , type=str  , default='2glbTrk_A1'       , help='category to fit'                    )
parser.add_argument('-m', '--mass'      , type=str  , default='var_tauMassRefitted'        , help='name of the 3mu mass variable'      )
parser.add_argument('-t', '--tree'      , type=str  , default='T3MMiniTree'        , help='name of the input tree'             )
parser.add_argument('-M', '--max-order' , type=int  , default=6             , help='max pdf order to consider'          )
parser.add_argument('-U', '--unblind'   , action='store_true'                          , help='don\'t use blinded ranges'          )
args = parser.parse_args()

# Read config file
with open(args.settings, 'r') as file_:
    lines = file_.readlines()

tmpcuts = ['1', '1', '1'] + [ l.strip('\r\n') for l in lines[2].split(',') ]
tmpcats = [ l.strip('\r\n') for l in lines[1].split(',') ]

bdtcuts = {}
category_cuts = {}
for icat, cat_ in enumerate(tmpcats):
    bdtcuts['2glbTrk_'+cat_] = " bdt < "+tmpcuts[icat]+" && bdt > "+tmpcuts[icat+3]
    if 'A' in cat_: category_cuts['2glbTrk_'+cat_] = " category==0 "
    if 'B' in cat_: category_cuts['2glbTrk_'+cat_] = " category==1 "
    if 'C' in cat_: category_cuts['2glbTrk_'+cat_] = " category==2 "

filename = 'inputdata/T3MMiniTree_xgboost_setting1_2018UL.root'

bdt_name = "bdt"
categ_name = "category"
MClabel_name = "dataMCType"
weight_name = "eventWeight"

mass = ROOT.RooRealVar(args.mass, args.mass, 38, 1.62, 2.0, 'GeV')
roobdt = ROOT.RooRealVar(bdt_name, bdt_name, -2, 2);
roocategory = ROOT.RooRealVar(categ_name, categ_name, 0, 2); #mass resolution category 0=A, 1=B, 2=C
roomc = ROOT.RooRealVar(MClabel_name, MClabel_name, 0, 4); #0=data, 1=Ds, 2=B0, 3=Bp, 4=W
rooweight = ROOT.RooRealVar(weight_name, weight_name, 0, 1); #normalisation of MC including corrections i.e. PU reweighting

mass.setRange('unblinded', 1.62, 2.0)

category = args.category

mass_range_left = {
        '2glbTrk_A1': [1.62, 1.75],
        '2glbTrk_A2': [1.62, 1.75],
        '2glbTrk_B1': [1.62, 1.74],
        '2glbTrk_B2': [1.62, 1.74],
        '2glbTrk_C1': [1.62, 1.73],
        '2glbTrk_C2': [1.62, 1.73]
        }

mass_range_right = {
        '2glbTrk_A1': [1.80, 2.0],
        '2glbTrk_A2': [1.80, 2.0],
        '2glbTrk_B1': [1.82, 2.0],
        '2glbTrk_B2': [1.82, 2.0],
        '2glbTrk_C1': [1.83, 2.0],
        '2glbTrk_C2': [1.83, 2.0]
        }

mc_cut = {
        '2glbTrk_A1': ' dataMCType>0 ',
        '2glbTrk_A2': ' dataMCType>0 ',
        '2glbTrk_B1': ' dataMCType>0 ',
        '2glbTrk_B2': ' dataMCType>0 ',
        '2glbTrk_C1': ' dataMCType>0 ',
        '2glbTrk_C2': ' dataMCType>0 '
        }

data_cut = {
        '2glbTrk_A1': ' dataMCType==0 ',
        '2glbTrk_A2': ' dataMCType==0 ',
        '2glbTrk_B1': ' dataMCType==0 ',
        '2glbTrk_B2': ' dataMCType==0 ',
        '2glbTrk_C1': ' dataMCType==0 ',
        '2glbTrk_C2': ' dataMCType==0 '
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
  c_bernstein = [ ROOT.RooRealVar('c_Bernstein{}{}'.format(i, j), 'c_Bernstein{}{}'.format(i, j), 0.01, -10, 10) for j in range(1,i+1)]
  c_chebychev = [ ROOT.RooRealVar('c_Chebychev{}{}'.format(i, j), 'c_Chebychev{}{}'.format(i, j), 0.01, -10, 10) for j in range(1,i+1)]
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

data = ROOT.RooDataSet('data', '', tree, variables, data_cut[category]+"&&"+category_cuts[category]+"&&"+bdtcuts[category],"eventWeight")#.binnedClone('data')
hist = data.binnedClone('histo')
getattr(wspace, 'import')(data)

frame = wspace.var(args.mass).frame()
wspace.data('data').plotOn(frame)

envelope = ROOT.RooArgList("envelope")

can = ROOT.TCanvas()
leg = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)

gofmax  = 0
bestfit = None
families = ['Bernstein', 'Chebychev', 'Exponential']
allpdfs_list = ROOT.RooArgList(pdfs.allPdfs())
allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]
chi2Map = {}
for j, fam in enumerate(families):
  pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
  mnlls    = []
  for i, pdf in enumerate(pdf_list):
    norm = ROOT.RooRealVar("nev", "", 0, 1e+3)
    ext_pdf = ROOT.RooAddPdf(pdf.GetName()+"_ext", "", ROOT.RooArgList(pdf), ROOT.RooArgList(norm))
    results = ext_pdf.fitTo(data,  ROOT.RooFit.Save(True), ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'), ROOT.RooFit.Extended(True))
    #chi2Map[fam] = ROOT.RooChi2Var("chi2"+pdf.GetName(), "", pdf, hist)
    chi2 = ROOT.RooChi2Var("chi2"+pdf.GetName(), "", pdf, hist)
    mnll = results.minNll()+(i+1)

    gof_prob = 0
    #gof_prob = ROOT.TMath.Prob(chi2Map[fam].getVal(), hist.numEntries()-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
    gof_prob = ROOT.TMath.Prob(chi2.getVal(), hist.numEntries()-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
    fis_prob = ROOT.TMath.Prob(2.*(mnlls[-1]-mnll), 1) if len(mnlls) else 0
    
    mnlls.append(mnll)

    print(">>>", pdf.GetName(), gof_prob, fis_prob)

    if gof_prob > 0.01 and fis_prob < 0.1:
      if gof_prob > gofmax:
        gofmax = gof_prob
        bestfit = pdf.GetName()
      envelope.add(pdf)
      pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()), ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'))
    del chi2 # RooChi2Var makes the code crash at the end of the execution. This line makes it crash faster.
for pdf in [envelope.at(i) for i in range(envelope.getSize())]:
  leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (bestfit)" if bestfit==pdf.GetName() else pdf.GetName(), "l")



can.SetTitle("Category %s" % category);     
can.SetMinimum(0.01);
can.SetMaximum(1.40*can.GetMaximum());
can.GetXaxis().SetTitle("m_{3mu} [GeV]");

ctmp_sig = TCanvas("Category %s" % category,"Categories",0,0,660,660);
ctmp_sig.SetFrameLineWidth(3);
ctmp_sig.SetTickx();
ctmp_sig.SetTicky();

can.Update()
can.Modified()
can.Print();
can.Draw("SAME");

leg.SetBorderSize(0);
leg.SetFillStyle(0);
leg.SetTextSize(0.029);
leg.Draw("SAME");  
ctmp_sig.SaveAs("plots/MultiPdf_category_%s_SplusB.png" % category);

cat = ROOT.RooCategory("roomultipdf_cat", "")

multipdf = ROOT.RooMultiPdf("multipdf", "", cat, envelope)
cat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(bestfit))
outerspace = ROOT.RooWorkspace('ospace')
getattr(outerspace, 'import')(envelope)
getattr(outerspace, 'import')(multipdf)
getattr(outerspace, 'import')(data)

if not os.path.exists('MultiPdfWorkspaces'):
  os.makedirs("MultiPdfWorkspaces")
outerspace.writeToFile("MultiPdfWorkspaces/"+args.category+".root")

print("\nExecution is complete. I may crash in peace\n")
import pdb; pdb.set_trace()
