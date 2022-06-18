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
parser.add_argument('-i', '--input_file', type=str,  default='../T3M_HF/inputdata/input.root',  help='input ttree'                    )
parser.add_argument("-t", "--type",       type=str,  default="threeGlobal", help="specify type (threeGlobal/twoGlobalTracker)", action="store")
parser.add_argument("-r", "--run",        type=str,  default="2018",        help="Run (2017/2018)", action="store")
parser.add_argument('-s', '--setting'   , type=str  , default='../T3M_HF/configs/config.txt', help='config file, same as createdatacards'  )
parser.add_argument('-M', '--max-order' , type=int  , default=6           , help='max pdf order to consider'          )
parser.add_argument('-U', '--unblind'   , action='store_true'             , help='don\'t use blinded ranges'          )
args = parser.parse_args()

filename = args.input_file

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
    #set of variables
    variables = ROOT.RooArgSet(mass);
    variables.add(roobdt)
    variables.add(roocategory)
    variables.add(roomc)
    variables.add(rooweight)

    category = '' #A, B, C
    for reso in category_cuts: 
        if reso in cat:
            category = reso

    mass.setRange('unblinded', 1.62, 2.0)
    mass.setRange('left', mass_range_left[category][0], mass_range_left[category][1])
    mass.setRange('right', mass_range_right[category][0], mass_range_right[category][1])

    #take rooDataSet from tree
    data = ROOT.RooDataSet('data_'+cat, '', tree, variables, data_cut+"&&"+category_cuts[category]+"&&"+bdt_cutlist[idx], weight_name)#.binnedClone('data')
    #debug
    print("category "+cat)
    print(data_cut+"&&"+category_cuts[category]+"&&"+bdt_cutlist[idx])

    #reduce to sidebands
    sidebands = "("+m3m_name+"<"+str(mass_range_left[category][1])+"&&"+m3m_name+">="+str(mass_range_left[category][0])+")||("+m3m_name+"<"+str(mass_range_right[category][1])+"&&"+m3m_name+">="+str(mass_range_right[category][0])+")"
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
    c_powerlaw = ROOT.RooRealVar("c_PowerLaw_{}".format(cat), "", 1, -100, 100)
    powerlaw = ROOT.RooGenericPdf("PowerLaw_{}".format(cat), "TMath::Power(@0, @1)", ROOT.RooArgList(mass, c_powerlaw))
    getattr(pdfs, 'import')(powerlaw)

    pdfs.factory("Exponential::Exponential_{C}({M}, slope_{C}[0, -1000, 100])".format(M=m3m_name, C=cat))
   
    # Bernstein: oder n has n+1 coefficients (starts from constant)
    for i in range(1, args.max_order+1):
      c_bernstein = '{'+','.join(['c_Bernstein{}{}_{}[.1, 0.0, 1.0]'   .format(i, j, cat) for j in range(i+1)])+'}'
      pdfs.factory('Bernstein::Bernstein{}_{}({}, {})'.format(i, cat, m3m_name, c_bernstein))

    ## Chebychev: order n has n coefficients (starts from linear)
    #for i in range(args.max_order):
    #  c_chebychev = '{'+','.join(['c_Chebychev{}{}_{}[.1, 0, 1]'.format(i+1, j, cat) for j in range(i+1)])+'}'
    #  pdfs.factory('Chebychev::Chebychev{}({}, {})'.format(i+1, m3m_name, c_chebychev)) 

    # Polynomial: order n has n coefficients (starts from constant)
    for i in range(1, args.max_order):
      c_polynomial = '{'+','.join(['c_Polynomial{}{}_{}[.1, -100, 100]'.format(i+1, j, cat) for j in range(i+1)])+'}'
      pdfs.factory('Polynomial::Polynomial{}_{}({}, {})'.format(i, cat, m3m_name, c_polynomial)) 

    wspace = ROOT.RooWorkspace('wspace')
    getattr(wspace, 'import')(mass)
    wspace.var(m3m_name).setBins(38)
    
    
    getattr(wspace, 'import')(data)
    
    frame = wspace.var(m3m_name).frame()
    frame.SetTitle(args.type+" "+args.run+" "+cat)
    wspace.data('data_'+cat).plotOn(frame)
    
    envelope = ROOT.RooArgList("envelope")
    
    can = ROOT.TCanvas()
    leg = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)
    
    gofmax  = 0
    bestfit = None
    #families = ['Bernstein', 'Chebychev', 'Exponential', 'PowerLaw']
    families = ['Polynomial', 'Exponential', 'PowerLaw']  
    allpdfs_list = ROOT.RooArgList(pdfs.allPdfs())
    allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]

    converged = 0
    for j, fam in enumerate(families):
      pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
      mnlls    = []
      for i, pdf in enumerate(pdf_list):
        norm = ROOT.RooRealVar("nbkg", "", 0, 1e+6)
        ext_pdf = ROOT.RooAddPdf(pdf.GetName()+"_ext", "", ROOT.RooArgList(pdf), ROOT.RooArgList(norm)) if not 'Bernstein' in pdf.GetName() else pdf
        #note: ROOT bug, see https://root-forum.cern.ch/t/problem-with-fit-in-range-with-roobernstein/41593
        results = ext_pdf.fitTo(data,  ROOT.RooFit.Save(True), ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'), ROOT.RooFit.Extended(not 'Bernstein' in pdf.GetName()))
        chi2 = ROOT.RooChi2Var("chi2"+pdf.GetName(), "", ext_pdf, hist, ROOT.RooFit.DataError(ROOT.RooAbsData.Expected))
        mnll = results.minNll()+0.5*(i)

        gof_prob = ROOT.TMath.Prob(chi2.getVal(), int(hist.sumEntries())-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
        fis_prob = ROOT.TMath.Prob(2.*(mnlls[-1]-mnll), i-converged) if len(mnlls) else 0
        if results.covQual()==3:
          mnlls.append(mnll)
          converged = i
        print(">>>", pdf.GetName(), " chi2 ", chi2.getVal())

        del chi2 # RooChi2Var makes the code crash at the end of the execution. This line makes it crash faster.
        #if gof_prob > 0.01 and fis_prob < 0.1 and results.covQual()==3:
        if fis_prob < 0.1 and results.covQual()==3:
          if gof_prob > gofmax:
            gofmax = gof_prob
            bestfit = pdf.GetName()
          envelope.add(pdf)

          print(">>>", pdf.GetName(), " added to envelope")
          print("gof_prob:", gof_prob, " fis_prob:", fis_prob, " mnll: ",mnll)

          #draw exponential contour
          if "Exponential" in pdf.GetName():
            pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()),
                       ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'), ROOT.RooFit.VisualizeError(results,2),
                       ROOT.RooFit.NormRange('unblinded' if args.unblind else 'left,right'),
                       ROOT.RooFit.FillColor(ROOT.kYellow), ROOT.RooFit.FillStyle(3001))
            pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()),
                       ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'), ROOT.RooFit.VisualizeError(results,1),
                       ROOT.RooFit.NormRange('unblinded' if args.unblind else 'left,right'),
                       ROOT.RooFit.FillColor(ROOT.kGreen ), ROOT.RooFit.FillStyle(3001))
          pdf.plotOn(frame, ROOT.RooFit.LineColor(envelope.getSize()), ROOT.RooFit.Name(pdf.GetName()),
                       ROOT.RooFit.NormRange('unblinded' if args.unblind else 'left,right'),
                       ROOT.RooFit.Range('unblinded' if args.unblind else 'left,right'))
        elif fis_prob >= 0.1:
          break
    for pdf in [envelope.at(i) for i in range(envelope.getSize())]:
      leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (bestfit)" if bestfit==pdf.GetName() else pdf.GetName(), "l")
    
    frame.Draw()
    leg.Draw("SAME")
    can.Update()
    can.Modified()
    roocat = ROOT.RooCategory("roomultipdf_cat_HF_{}".format(cat), "")
    
    multipdf = ROOT.RooMultiPdf("multipdf", "", roocat, envelope)
    #indexing Expo in the multipdf. Change line below to switch to "bestfit"
    roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index('Exponential_{}'.format(cat)))
    #roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(bestfit))
    outerspace = ROOT.RooWorkspace('ospace')
    getattr(outerspace, 'import')(envelope)
    getattr(outerspace, 'import')(multipdf)
    
    can.SaveAs("MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+"_plot.png")
    #can.SaveAs("MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+"_plot.pdf", "pdf")
    outerspace.writeToFile("MultiPdfWorkspaces/"+args.run+"_"+args.type+"_"+cat+".root")
    
    print("\nExecution is complete. I may crash in peace\n")
