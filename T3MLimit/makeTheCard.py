#! /bin/env python


import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
from numpy import *
import math
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--selection'      ,  help="Introduce your selection; [Default: %(default)s] "               , dest='selection'         , default='bdt > 0.1')
parser.add_argument('--signalnorm'     ,  help="Signal Normalization; [Default: %(default)s] "                   , dest='signalnorm'        , type = float, default=0.001)
parser.add_argument('--category'       ,  help="Category; [Default: %(default)s] "                               , dest='category'          , default='A')
parser.add_argument('--varset'         ,  help="BDTVariable set; [Default: %(default)s] "                        , dest='varset'            , default='Vars2016')
parser.add_argument('--datafile'       ,  help="Input Mini Tree; [Default: %(default)s] "                        , dest='datafile'          , default='T3MMiniTree.root')
parser.add_argument('--nbins'          ,  help="Number of bins in the mass spectra; [Default: %(default)s] "     , dest='nbins'             , type = int  , default=40)
parser.add_argument('--signal_range_lo',  help="Signal mass window low edge; [Default: %(default)s] "            , dest='signal_range_lo'   , default=1.73)
parser.add_argument('--signal_range_hi',  help="Signal mass window high edge; [Default: %(default)s] "           , dest='signal_range_hi'   , default=1.82)
parser.add_argument('--fit_range_lo'   ,  help="Overal fit range, low edge; [Default: %(default)s] "             , dest='fit_range_lo'      , default=1.65)
parser.add_argument('--fit_range_hi'   ,  help="Overal fit range, high edge; [Default: %(default)s] "            , dest='fit_range_hi'      , default=1.98)
parser.add_argument('--blinded'        ,  help="Blind the signal range; [Default: %(default)s] "                 , dest='blinded'           , action='store_true', default = True )
parser.add_argument('--unblinded'      ,                                                                           dest='blinded'           , action='store_false')

parser.set_defaults(blinded=True)

args = parser.parse_args() 

blinded         = args.blinded
selection       = args.selection
nbins           = args.nbins
signal_range_lo = double(args.signal_range_lo)
signal_range_hi = double(args.signal_range_hi)
fit_range_lo    = double(args.fit_range_lo)
fit_range_hi    = double(args.fit_range_hi)
minitree        = args.datafile

print "selection: ", selection

ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()


if len(args.category)>0:
    args.category = '_'+args.category

gaus = ROOT.TF1('signalgaus', 'gaus', 1.7, 1.86)
MiniTreeFile = ROOT.TFile.Open(args.datafile)
MiniTreeFile.cd()
tree = MiniTreeFile.Get('T3MMiniTree')


mass_histo_mc = ROOT.TH1F('mass_histo_mc', 'mass_histo_mc', nbins, 1.6, 2.)
#tree.Draw('m3m>>mass_histo_mc', '(' + selection + '& dataMCtype !=1 ' + ') * event_weight * %f' %args.signalnorm)
tree.Draw('m3m>>mass_histo_mc', '(' + selection + '& dataMCtype !=1 ' + ') * event_weight')
#print "INTEGRAL ",mass_histo_mc.Integral()



m3m          = ROOT.RooRealVar('m3m'                , '3#mu mass'           , fit_range_lo, fit_range_hi, 'GeV')
bdt          = ROOT.RooRealVar('bdt'                , 'bdt'                 , -1 , 1)
m12          = ROOT.RooRealVar('m12'                , 'm12'                 ,  0 , 2)
m13          = ROOT.RooRealVar('m13'                , 'm13'                 ,  0 , 2)
event_weight = ROOT.RooRealVar('event_weight'       , 'event_weight'        ,  0,  5)  # this weight includes also the scale  mc signal scale
category     = ROOT.RooRealVar('category'           , 'category'            ,  0,  5)
dataMCtype   = ROOT.RooRealVar('dataMCtype'         , 'dataMCtype'          ,  0,  100)
scale        = ROOT.RooRealVar('scale'              , 'scale'               ,  args.signalnorm)  # reserved but not used

print dataMCtype.getVal()

m3m.setRange('left' , fit_range_lo    , signal_range_lo)
m3m.setRange('right', signal_range_hi , fit_range_hi)
m3m.setRange('full' , fit_range_lo    , fit_range_hi)



slope = ROOT.RooRealVar('slope', 'slope', -0.001, -5, 5)
expo  = ROOT.RooExponential('bkg_expo', 'bkg_expo', m3m, slope)

slope2 = ROOT.RooRealVar('slope2', 'slope2', -0.001, -5, 5)
# expo2  = ROOT.RooExponential('bkg_expo2', 'bkg_expo2', mass, slope2)
expo2  = ROOT.RooExponential('bkg_expo2', 'bkg_expo2', m3m, slope)

# number of background events
nbkg = ROOT.RooRealVar('nbkg', 'nbkg', 1000, 0, 550000)
expomodel = ROOT.RooAddPdf('bkg_extended_expo', 'bkg_extended_expo', ROOT.RooArgList(expo), ROOT.RooArgList(nbkg))


mean  = ROOT.RooRealVar('mean' , 'mean' ,   1.78, 1.6, 1.9)
width = ROOT.RooRealVar('width', 'width',   0.02, 0.0, 0.1)
gaus  = ROOT.RooGaussian('sig_gaus', 'sig_gaus', m3m, mean, width)


cbwidth = ROOT.RooRealVar('cbwidth','cbwidth', 0.02, 0.0, 0.1)
cbalpha = ROOT.RooRealVar('cbalpha','cbalpha', 1.00, -20, 20 )
cbn     = ROOT.RooRealVar('cbn'    ,'cbn'    , 2,    0  , 5  )
cb      = ROOT.RooCBShape('cb'     ,'cb'     , m3m, mean, cbwidth, cbalpha, cbn)


fraction    = ROOT.RooRealVar('fraction' , 'fraction',   0.01, 0, 0.1)
#combined_model = ROOT.RooAddPdf("combined_model", "g+a", ROOT.RooArgList(gaus,cb), ROOT.RooArgList(gs_fraction,cb_fraction))
combined_model = ROOT.RooAddPdf("combined_model", "g+a", ROOT.RooArgList(gaus,cb), ROOT.RooArgList(fraction))




variables = ROOT.RooArgSet()
variables.add(m3m)
variables.add(bdt)
variables.add(m12)
variables.add(m13)
variables.add(event_weight)
variables.add(category)
variables.add(dataMCtype)
variables.add(scale)


MCSelector = ROOT.RooFormulaVar('MCSelector', 'MCSelector', selection + ' & dataMCtype !=1 ', ROOT.RooArgList(variables))
fullmc = ROOT.RooDataSet('mc', 'mc', tree, variables, MCSelector,'event_weight')


frame = m3m.frame()
frame.SetTitle('')

fullmc.plotOn(frame, 
              ROOT.RooFit.Binning(nbins), 
              ROOT.RooFit.XErrorSize(0), 
              ROOT.RooFit.LineWidth(2),
              ROOT.RooFit.MarkerStyle(6),
              ROOT.RooFit.MarkerColor(ROOT.kCyan + 2),
              ROOT.RooFit.MarkerSize(0.75),
              ROOT.RooFit.FillColor(ROOT.kCyan  + 2),
)

#print " ", fullmc.sumEntries()
results_cb   = cb.fitTo(fullmc, ROOT.RooFit.Range(signal_range_lo, signal_range_hi), ROOT.RooFit.Save())
results_cb.Print()
results_gaus = gaus.fitTo(fullmc, ROOT.RooFit.Range(signal_range_lo, signal_range_hi), ROOT.RooFit.Save())
results_gaus.Print()

results_combined_pdf = combined_model.fitTo(fullmc, ROOT.RooFit.Range(signal_range_lo, signal_range_hi), ROOT.RooFit.Save())
results_combined_pdf.Print()


#results_gaus = gaus.fitTo(fullmc, ROOT.RooFit.Save(), ROOT.RooFit.SumW2Error(True))
#results_gaus = gaus.chi2FitTo(fullmc, ROOT.RooFit.Save())

#gaus.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed +2 ))
cb.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kMagenta +2 ))
#combined_model.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kCyan +2 ))



frame.Draw()
cmd = 'mkdir plots/%s;'%args.varset + 'mkdir datacards/%s;'%args.varset + 'mkdir workspaces/%s;'%args.varset
os.system(cmd)
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextFont(42)
latex.SetTextAlign(31)
latex.DrawLatex(0.57, 0.85, 'taushape%s_%dbins'%(args.category, nbins))

ROOT.gPad.SaveAs('plots/%s/taushape%s_%dbins.png'%(args.varset,args.category, nbins))


DataSelector      = ROOT.RooFormulaVar('DataSelector', 'DataSelector', selection + ' & dataMCtype == 1', ROOT.RooArgList(variables))
BlindDataSelector = ROOT.RooFormulaVar('DataSelector', 'DataSelector', selection + ' & dataMCtype == 1 &  abs(m3m  - 1.776) > %s' %( (signal_range_hi -signal_range_lo)/2) , ROOT.RooArgList(variables))




if blinded:
    print 'BLIND'
    fulldata     = ROOT.RooDataSet('data', 'data', tree,  variables, BlindDataSelector)
else:
    fulldata     = ROOT.RooDataSet('data', 'data', tree,  variables, DataSelector)



fulldata.plotOn(frame, 
                ROOT.RooFit.Binning(nbins),
                ROOT.RooFit.MarkerStyle(21),
                ROOT.RooFit.MarkerColor(ROOT.kBlack), 
                ROOT.RooFit.MarkerSize(0.75))


if blinded:
    results_expo = expomodel.fitTo(fulldata, ROOT.RooFit.Range('left,right'), ROOT.RooFit.Save())
else:
    results_expo = expomodel.fitTo(fulldata, ROOT.RooFit.Range('full'), ROOT.RooFit.Save())


expomodel.plotOn(frame, 
                 ROOT.RooFit.LineColor(ROOT.kBlack))





ctmp_canvas = ROOT.TCanvas('Category %s' %args.category,"Categories",0,0,700,500);
ctmp_canvas.SetFrameLineWidth(3);
ctmp_canvas.SetTickx();
ctmp_canvas.SetTicky();




frame.Draw()
legend = ROOT.TLegend(0.12,0.70,0.43,0.86)
legend.AddEntry(frame.getObject(1),"Signal model gauss","L")
legend.AddEntry(frame.getObject(4),"data model exp","L")
#legend.Draw()


latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextFont(42)
latex.SetTextAlign(31)
latex.DrawLatex(0.57, 0.85, 'mass_fit%s_%dbins'%(args.category, nbins))


ROOT.gPad.SaveAs('plots/%s/massfit_%s_%dbins.png'%(args.varset,args.category, nbins))


output = ROOT.TFile.Open('workspaces/%s/workspace%s.root' %(args.varset,args.category), 'recreate')
seldata = ROOT.RooDataSet('data', 'data', tree, variables, DataSelector)
selsignal = ROOT.RooDataSet('mc', 'mc', tree, variables, MCSelector)



data =  ROOT.RooDataSet(
    'data_obs', 
    'data_obs',
    seldata, 
    ROOT.RooArgSet(m3m)
)

mc =  ROOT.RooDataSet(
    'mc', 
    'mc',
    selsignal, 
    ROOT.RooArgSet(m3m)
)


# create workspace

print 'creating workspace'
cb_fraction    = ROOT.RooRealVar('cb_fraction' , 'cbfraction' ,   1-fraction.getVal(), 1- fraction.getVal() , 1- fraction.getVal())
gs_fraction    = ROOT.RooRealVar('gs_fraction' , 'gs_fraction',   fraction.getVal(), fraction.getVal(), fraction.getVal())

workspace = ROOT.RooWorkspace('t3m_shapes')

workspace.factory('m3m[%f, %f]' % (fit_range_lo, fit_range_hi))
workspace.factory("Exponential::bkg(m3m, a0%s[%f,%f,%f])" %(args.category, slope.getVal(), slope.getError(), slope.getError()) )  


workspace.factory('cb_fraction[%f]'  % cb_fraction.getVal())
workspace.factory('gs_fraction[%f]'  % gs_fraction.getVal())
workspace.factory('mean[%f]'  % mean .getVal())
workspace.factory('sigma[%f]' % width.getVal())
workspace.factory('RooGaussian::sig(m3m, mean, sigma)')

workspace.factory('cbsigma[%f]' % cbwidth.getVal())
workspace.factory('cbalpha[%f]' % cbalpha.getVal())
workspace.factory('cbn[%f]' % cbn.getVal())
workspace.factory('RooCBShape::cbsig(m3m, mean, cbsigma, cbalpha, cbn)')



it = workspace.allVars().createIterator()
all_vars = [it.Next() for _ in range( workspace.allVars().getSize())]
for var in all_vars:
    if var.GetName() in ['mean', 'sigma','cb_fraction','gs_fraction','cbsigma','cbalpha','cbn']:
        var.setConstant()

combined_model_fit = ROOT.RooAddPdf("combined_model_fit", "g+a", ROOT.RooArgList(gaus,cb), ROOT.RooArgList(gs_fraction,cb_fraction), False)
#combined_model_fit = ROOT.RooAddPdf("combined_model_fit", "g+a", ROOT.RooArgList(gaus,cb), fraction, False)
getattr(workspace,'import')(combined_model_fit)


getattr(workspace,'import')(data)
getattr(workspace,'import')(mc)
workspace.Write()
output.Close()



# make  the datacard
with open('datacards/%s/CMS_T3MSignal_13TeV%s.txt' %(args.varset,args.category), 'w') as card:
   card.write(
'''
# HF Tau to three mu
imax 1 number of bins
jmax * number of processes minus 1
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes background    category{cat}       ../../workspaces/{wdir}/workspace{cat}.root t3m_shapes:bkg
shapes signal        category{cat}       ../../workspaces/{wdir}/workspace{cat}.root t3m_shapes:cbsig
shapes data_obs      category{cat}       ../../workspaces/{wdir}/workspace{cat}.root t3m_shapes:data_obs
--------------------------------------------------------------------------------
bin               category{cat}
observation       {obs:d}
--------------------------------------------------------------------------------

bin                                     category{cat}       category{cat}
process                                 signal              background
process                                 0                   1
rate                                   {signal:.4f}        {bkg:.4f}
--------------------------------------------------------------------------------
lumi              lnN                       1.025               -   
BRDToTau_13TeV    lnN                       1.03                -
BRDsPhiPi_13TeV   lnN                       1.08                -
BRBtoTau_13TeV    lnN                       1.11                -
BRBtoD_13TeV      lnN                       1.16                -
fUnc_13TeV        lnN                       1.11                -
DpmScaling_13TeV  lnN                       1.03                -
BsScaling_13TeV   lnN                       1.12                -
DsNorm_13TeV      lnN                       1.05                -
UncTrigger_13TeV  lnN                       1.12                -
UncRatioAcc_13TeV lnN                       1.01                -
UncMuonEff_13TeV  lnN                       1.015               -
MuES_13TeV        lnN                       1.007               -
MuRes_13TeV       lnN                       1.025               -

--------------------------------------------------------------------------------
'''.format(
         cat      = args.category,
         wdir      = args.varset,
         obs      = fulldata.numEntries() if blinded==False else -1,
#         signal   = mass_histo_mc.Integral(),   # the histogramm integral returns a screwed value, no clue why, to be sorted later
         signal   = fullmc.sumEntries(),         # use the ArgDataSet entries instead
         bkg      = nbkg.getVal(),
         )
)
