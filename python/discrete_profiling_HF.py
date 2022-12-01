from __future__ import print_function
import ROOT
from ROOT import RooFit
import os
import time
import gc; gc.disable()

import argparse
parser = argparse.ArgumentParser('''
This script is a python adaptation of the HNL discrete profiling c++ code
https://github.com/BParkHNLs/flashggFinalFit/blob/mg-branch/Background/test/fTest.cpp
NOTE: the code will probably crash on exit. This is somehow related to the RooChi2Var object.
'''
)
parser.add_argument('-i', '--input_file', type=str,  default='input.root',  help='input ttree'                  )
parser.add_argument("-t", "--type",       type=str,  default="threeGlobal", help="specify type (threeGlobal/twoGlobalTracker)", action="store")
parser.add_argument("-r", "--run",        type=str,  default="2018",        help="Run (2017/2018)", action="store")
parser.add_argument('-s', '--setting'   , type=str  , default='config.txt', help='config file, same as createdatacards'  )
parser.add_argument('-M', '--max-order' , type=int  , default=6           , help='max pdf order to consider'    )
parser.add_argument('-U', '--unblind'   , action='store_true', default=False, help='don\'t use blinded ranges'  )
parser.add_argument('-F', '--unblindfit', action='store_true', default=False, help='don\'t show ranges'     )
args = parser.parse_args()

ROOT.gROOT.SetBatch(True)

filename = args.input_file

if(args.type=='threeGlobal'):
    filename = '/eos/user/f/fsimone/Tau23Mu_anatools/optim_Combine/T3MCombine/workdir/CMSSW_10_2_13/src/CombineHarvester/T3M_HF/inputdata/t3mminitree_xgb_'+args.run+'_22aug22.root'
    args.setting = '/eos/user/f/fsimone/Tau23Mu_anatools/optim_Combine/T3MCombine/workdir/CMSSW_10_2_13/src/CombineHarvester/T3M_HF/config_ThreeGlobal_'+args.run+'_22aug22.txt'

if(args.type=='twoGlobalTracker'):
    filename = '/eos/user/f/fsimone/Tau23Mu_anatools/optim_Combine/T3MCombine/workdir/CMSSW_10_2_13/src/CombineHarvester/T3M_HF/inputdata/T3MMiniTree_xgboost_setting2_'+args.run+'UL_v2_dimuonMass.root'
    args.setting = '/eos/user/f/fsimone/Tau23Mu_anatools/optim_Combine/T3MCombine/workdir/CMSSW_10_2_13/src/CombineHarvester/T3M_HF/config_xgboost_TwoGlobalTracker_'+args.run+'_v2.txt'

branch_names = []
cat_names = []
bdt_val = []

try:
    with open(args.setting, 'r') as f:
        lines = f.readlines()
        branch_names = (lines[0]).replace('\n', '').split(',')
        cat_names = (lines[1]).replace('\n', '').split(',')
        bdt_val = (lines[2]).replace('\n', '').split(',')
except IOError:
    print("Could not read file: "+args.setting)

tree_name = branch_names[0]
m3m_name = branch_names[1]
bdt_name = branch_names[2]
categ_name = branch_names[3]
MClabel_name = branch_names[4]
weight_name = branch_names[5]
dimu1_name = branch_names[6]
dimu2_name = branch_names[7]

omega_cut = " abs("+dimu1_name+"-0.782)>0.01 && abs("+dimu2_name+"-0.782)>0.01 "

bdt_cutlist = []
for idx,cat in enumerate(cat_names):
    if idx<3:
        bdt_cutlist.append(bdt_name+">"+bdt_val[idx])
    else:
        bdt_cutlist.append(bdt_name+"<="+bdt_val[idx-3]+"&&"+bdt_name+">"+bdt_val[idx])

mass_range_left = {
        'A': [1.62, 1.75],
        'B': [1.62, 1.74],
        'C': [1.62, 1.73]
        }

mass_range_right = {
        'A': [1.80, 2.0],
        'B': [1.82, 2.0],
        'C': [1.83, 2.0]
        }

data_cut = MClabel_name+'==0 '

category_cuts = {
        'A': categ_name+'==0',
        'B': categ_name+'==1',
        'C': categ_name+'==2',
        }

#open input file
rootfile = ROOT.TFile(filename, 'READ')
tree = rootfile.Get(tree_name)

for idx,cat in enumerate(cat_names): #loop on A1,A2,A3...C3
    mass = ROOT.RooRealVar(m3m_name, m3m_name, 38, 1.62, 2.0, 'GeV')
    roobdt = ROOT.RooRealVar(bdt_name, bdt_name, -2, 2);
    roocategory = ROOT.RooRealVar(categ_name, categ_name, 0, 2); #mass resolution category 0=A, 1=B, 2=C
    roomc = ROOT.RooRealVar(MClabel_name, MClabel_name, 0, 4); #0=data, 1=Ds, 2=B0, 3=Bp, 4=W
    rooweight = ROOT.RooRealVar(weight_name, weight_name, 0, 1); #normalisation of MC including corrections i.e. PU reweighting
    roodimu1 = ROOT.RooRealVar(dimu1_name, dimu1_name, 0.2, 1.8);
    roodimu2 = ROOT.RooRealVar(dimu2_name, dimu2_name, 0.2, 1.8);
    #set of variables
    variables = ROOT.RooArgSet(mass);
    variables.add(roobdt)
    variables.add(roocategory)
    variables.add(roomc)
    variables.add(rooweight)
    variables.add(roodimu1)
    variables.add(roodimu2)

    category = '' #A, B, C
    for reso in category_cuts: 
        if reso in cat:
            category = reso

    mass.setRange('unblinded', 1.62, 2.0)
    mass.setRange('left', mass_range_left[category][0], mass_range_left[category][1])
    mass.setRange('right', mass_range_right[category][0], mass_range_right[category][1])

    #debug
    print("category "+cat)
    print(data_cut+"&&"+category_cuts[category]+"&&"+bdt_cutlist[idx]+"&&"+omega_cut)

    #take rooDataSet from tree
    data = ROOT.RooDataSet('data_'+cat, '', tree, variables, data_cut+"&&"+category_cuts[category]+"&&"+bdt_cutlist[idx]+"&&"+omega_cut, weight_name)#.binnedClone('data')
    #data = ROOT.RooDataSet('data_'+cat, '', tree, variables, data_cut+"&&"+category_cuts[category]+"&&"+bdt_cutlist[idx], weight_name)#.binnedClone('data')

    #reduce to sidebands
    sidebands = "("+m3m_name+"<"+str(mass_range_left[category][1])+"&&"+m3m_name+">="+str(mass_range_left[category][0])+")||("+m3m_name+"<"+str(mass_range_right[category][1])+"&&"+m3m_name+">="+str(mass_range_right[category][0])+")"

    if(not args.unblindfit):
        data_toplot = data.reduce(ROOT.RooArgSet(mass), sidebands)
    else: data_toplot = data.reduce(ROOT.RooArgSet(mass))

    if(not args.unblind): 
        data = data.reduce(ROOT.RooArgSet(mass), sidebands)
    else: data = data.reduce(ROOT.RooArgSet(mass))


    #hist = ROOT.RooDataHist('histo_'+cat, 'histo_'+cat, ROOT.RooArgSet(mass), data)
    hist = data.binnedClone('histo_'+cat)

    #define maximum order for pdfs based on entries
    args.max_order = min(args.max_order, int(hist.sumEntries())-2)

    #define the set of pdfs
    pdfs = ROOT.RooWorkspace('pdfs_'+cat)
    getattr(pdfs, 'import')(mass)

    #power law
    c_powerlaw = ROOT.RooRealVar("c_PowerLaw_{}_{}_{}".format(args.run, args.type, cat), "", 1, -100, 100)
    powerlaw = ROOT.RooGenericPdf("PowerLaw_{}_{}_{}".format(args.run, args.type, cat), "TMath::Power(@0, @1)", ROOT.RooArgList(mass, c_powerlaw))
    getattr(pdfs, 'import')(powerlaw)

    pdfs.factory("Exponential::Exponential_{R}_{T}_{C}({M}, slope_{R}_{T}_{C}[0, -1000, 100])".format(M=m3m_name, R=args.run, T=args.type, C=cat))
   
    # Bernstein: oder n has n+1 coefficients (starts from constant)
    for i in range(1, args.max_order+1):
      c_bernstein = '{'+','.join(['c_Bernstein{}{}_{}_{}_{}[.1, 0.0, 1.0]'   .format(i, j, args.run, args.type, cat) for j in range(i+1)])+'}'
      pdfs.factory('Bernstein::Bernstein{}_{}_{}_{}({}, {})'.format(i, args.run, args.type, cat, m3m_name, c_bernstein))

    # Chebychev: order n has n coefficients (starts from linear)
    for i in range(args.max_order):
      c_chebychev = '{'+','.join(['c_Chebychev{}{}_{}_{}_{}[.1, 0.0, 10.0]'.format(i+1, j, args.run, args.type, cat) for j in range(i+1)])+'}'
      pdfs.factory('Chebychev::Chebychev{}_{}_{}_{}({}, {})'.format(i+1, args.run, args.type, cat, m3m_name, c_chebychev)) 

    # Polynomial: order n has n coefficients (starts from constant)
    for i in range(1, args.max_order):
      c_polynomial = '{'+','.join(['c_Polynomial{}{}_{}_{}_{}[.1, -100, 100]'.format(i+1, j, args.run, args.type, cat) for j in range(i+1)])+'}'
      pdfs.factory('Polynomial::Polynomial{}_{}_{}_{}({}, {})'.format(i, args.run, args.type, cat, m3m_name, c_polynomial)) 

    wspace = ROOT.RooWorkspace('wspace')
    getattr(wspace, 'import')(mass)
    wspace.var(m3m_name).setBins(38)
    
    
    getattr(wspace, 'import')(data)
    
    frame = wspace.var(m3m_name).frame()
    frame.SetTitle(args.type+" "+args.run+" "+cat)
    #wspace.data('data_'+cat).plotOn(frame)
    data_toplot.plotOn(frame)
    
    envelope = ROOT.RooArgList("envelope")
    
    can = ROOT.TCanvas()
    leg = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    
    gofmax  = 0
    bestfit = None
    #families = ['Bernstein', 'Chebychev', 'Exponential', 'PowerLaw']
    #families = ['Polynomial', 'Exponential', 'PowerLaw']  
    families = ['Exponential', 'PowerLaw', 'Bernstein']  
    allpdfs_list = ROOT.RooArgList(pdfs.allPdfs())
    allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]

    converged = 0
    norm = ROOT.RooRealVar("roomultipdf_{}_{}_{}_norm".format(args.run,args.type,cat), "", 0, 1e+6)
    for j, fam in enumerate(families):
      pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
      mnlls    = []
      for i, pdf in enumerate(pdf_list):
        ext_pdf = ROOT.RooAddPdf(pdf.GetName()+"_ext", "", ROOT.RooArgList(pdf), ROOT.RooArgList(norm))

        #note: ROOT bug, see https://root-forum.cern.ch/t/problem-with-fit-in-range-with-roobernstein/41593
        if (args.unblind):
            results = ext_pdf.fitTo(data,  ROOT.RooFit.Save(True), ROOT.RooFit.Extended(True))
        else:
            results = ext_pdf.fitTo(data,  ROOT.RooFit.Save(True), ROOT.RooFit.Range('left,right'), ROOT.RooFit.Extended(True))
        chi2 = ROOT.RooChi2Var("chi2"+pdf.GetName(), "", ext_pdf, hist, ROOT.RooFit.DataError(ROOT.RooAbsData.Expected))
        mnll = results.minNll()+0.5*(i)

        gof_prob = ROOT.TMath.Prob(chi2.getVal(), int(hist.sumEntries())-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
        fis_prob = ROOT.TMath.Prob(2.*(mnlls[-1]-mnll), i-converged) if len(mnlls) else 0
        if results.covQual()==3:
          mnlls.append(mnll)
          converged = i
        print(">>>", pdf.GetName(), " chi2 ", chi2.getVal())

        #if gof_prob > 0.01 and fis_prob < 0.1 and results.covQual()==3:
        if (fis_prob < 0.1 and results.covQual()==3) or ("Exponential" in pdf.GetName()):
          if gof_prob > gofmax:
            gofmax = gof_prob
            bestfit = pdf.GetName()
          envelope.add(pdf)

          print(">>>", pdf.GetName(), " added to envelope")
          print("gof_prob:", gof_prob, " fis_prob:", fis_prob, " mnll: ",mnll)

          #draw exponential contour
          if "Exponential" in pdf.GetName():
            ext_pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()),
                       ROOT.RooFit.Range('unblinded' if args.unblindfit else 'left,right'), ROOT.RooFit.VisualizeError(results,2),
                       ROOT.RooFit.NormRange('unblinded' if args.unblindfit else 'left,right'),
                       ROOT.RooFit.FillColor(ROOT.kYellow), ROOT.RooFit.FillStyle(3001))
            ext_pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()),
                       ROOT.RooFit.Range('unblinded' if args.unblindfit else 'left,right'), ROOT.RooFit.VisualizeError(results,1),
                       ROOT.RooFit.NormRange('unblinded' if args.unblindfit else 'left,right'),
                       ROOT.RooFit.FillColor(ROOT.kGreen ), ROOT.RooFit.FillStyle(3001))
          ext_pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()),
                       ROOT.RooFit.NormRange('unblinded' if args.unblindfit else 'left,right'),
                       ROOT.RooFit.Range('unblinded' if args.unblindfit else 'left,right'))
        elif fis_prob >= 0.1:
          break
        del chi2 # RooChi2Var makes the code crash at the end of the execution. This line makes it crash faster.
    for pdf in [envelope.at(i) for i in range(envelope.getSize())]:
      leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (bestfit)" if bestfit==pdf.GetName() else pdf.GetName(), "l")
   
    frame.GetYaxis().SetLimits(0.0, 1000)
    frame.Draw()
    leg.Draw("SAME")
    can.Update()
    can.Modified()
    roocat = ROOT.RooCategory("roomultipdf_cat_{}_{}_{}".format(args.run,args.type,cat), "")
    
    multipdf = ROOT.RooMultiPdf("roomultipdf_{}_{}_{}".format(args.run,args.type,cat), "", roocat, envelope)
    #indexing Expo in the multipdf. Change line below to switch to "bestfit"
    #roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index('Exponential_{}_{}_{}'.format(args.run, args.type, cat)))
    roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(bestfit))
    outerspace = ROOT.RooWorkspace('ospace')
    getattr(outerspace, 'import')(envelope)
    getattr(outerspace, 'import')(multipdf)
    getattr(outerspace, 'import')(norm)
   
    if(args.unblindfit):
        filename = "MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+"_plot_unblinded.png"
    else: 
        filename = "MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+"_plot.png"
    can.SaveAs(filename)
    #can.SaveAs("MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+"_plot.pdf", "pdf")
    outerspace.writeToFile("MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+".root")
    
    print("\nExecution is complete. I may crash in peace\n")
