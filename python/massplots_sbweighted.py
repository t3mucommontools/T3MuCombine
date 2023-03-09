import ROOT
import math 
#ROOT.gROOT.SetBatch(True)

class category:
  ''' create a weighted category, where the weight is decided by the 
  argument weight function
  e = exp. upper limit (can be used or not)
  s = n. signal , b = n. background
  wspacel = wspace name in the root file
  datal = dataset name in the root file
  sigl = signal pdf name in the root file
  files = signal root file
  fileb = background root file
  name = name of the category
  '''
  def __init__(self, name, files, fileb, s, b, e, wspacel, datal, sigl):
    self.n = name
    self.fs = ROOT.TFile.Open(files, 'READ')
    self.fb = ROOT.TFile.Open(fileb, 'READ')
    self.wb = self.fb.Get(wspacel)
    self.ws = self.fs.Get(wspacel)
    self.rds = self.wb.obj(datal)
    if not self.rds.get().find('m3m'):
      self.rds.get().find('cand_refit_tau_mass').SetName('m3m')
    self.sig = self.ws.obj(sigl)
    self.x = self.rds.get().find('m3m')
    self.x.SetTitle('3#mu mass [GeV]')
    self.e = e*e
    self.ns = s
    self.nb = b
    self.ams = math.sqrt(2*( (float(s)+float(b)) * math.log( 1.0+float(s)/float(b) ) - float(s)))
  def weight(self, w):
    ''' create a weight of value w and add it to the dataset.
    the dataset is not weighted at this point but contains the info
    note: signal pdfs are weighted using sqrt(w and the signal yields
    '''
    self.wgt    = ROOT.RooRealVar("wgt", '', w)
    self.wgtsig = ROOT.RooRealVar("wgtsig", '', self.ns * math.sqrt(w))
    self.rds.addColumn(self.wgt)

B3GL_2017='ThreeGlobal/2017/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root'
B3GL_2018='ThreeGlobal/2018/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root'
B2GL_2017='TwoGlobalTracker/2017/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root'
B2GL_2018='TwoGlobalTracker/2018/unblind/multipdf/workspaces/CMS_T3MBkg_13TeV.root'

S3GL_2017='ThreeGlobal/2017/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root'
S3GL_2018='ThreeGlobal/2018/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root'
S2GL_2017='TwoGlobalTracker/2017/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root'
S2GL_2018='TwoGlobalTracker/2018/unblind/multipdf/workspaces/CMS_T3MSignal_13TeV.root'

BW_A17 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_A17.root'
BW_B17 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_B17.root'
BW_C17 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_C17.root'
BW_A18 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_A18.root'
BW_B18 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_B18.root'
BW_C18 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_C18.root'

SW_A17 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_A17.root'
SW_B17 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_B17.root'
SW_C17 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_C17.root'
SW_A18 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_A18.root'
SW_B18 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_B18.root'
SW_C18 = 'W/approved/unblinded/workspaces/CMS_T3M_13TeV_W_C18.root'

def merge_and_plot(categories):
  ''' normalize the weights of each category,
  merge the datasets, merge the signal pdfs,
  create a weighted data distribution, plot
  '''
  norm = sum(1./c.e for c in categories)
#  norm = sum(c.ns/c.nb for c in categories)
#  norm = sum(c.ams for c in categories)
  for cat in categories:
    cat.weight(1./cat.e/norm)
#    cat.weight(cat.ns/cat.nb/norm)
#    cat.weight(cat.ams/norm)
  merged = ROOT.RooDataSet('merged', '', categories[0].rds.get())

  for i, cat in enumerate(categories):
    merged.append(cat.rds)
  wdata  = ROOT.RooDataSet(merged.GetName(), merged.GetTitle(), merged, merged.get(), "", 'wgt')
  #wdata.Print("V")
 
  sigs = ROOT.RooArgList()
  wgts = ROOT.RooArgList()
  for cat in categories:
    sigs.add(cat.sig)
    wgts.add(cat.wgtsig)

  #setting recursiveFractions=ROOT.kTRUE, the coefficients will sum to 1
  sums = ROOT.RooAddPdf('sums', '', sigs, wgts)
  signorm =  sum(c.wgtsig.getValV() for c in categories)

  print('signorm ',signorm)
  print('norm ', norm)

  plot  = categories[0].x.frame(40)
  categories[0].x.setRange("fullRange",1.62,2.0)

  wdata.plotOn(plot)
  
  sums.plotOn(plot, ROOT.RooFit.Normalization(signorm,ROOT.RooAbsReal.NumEvent), ROOT.RooFit.Range("fullRange"), ROOT.RooFit.NormRange("fullRange"), ROOT.RooFit.LineColor(ROOT.kRed))
  plot.GetYaxis().SetTitle('Weighted entries / 10 MeV') 

  leg = ROOT.TLegend(0.48,0.60,0.86,0.78)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0)
  leg.SetTextFont(42)
  leg.AddEntry(plot.getObject(0), "Data", "PE")
  leg.AddEntry(plot.getObject(1), "Signal (B=10^{-7})", "L")

  can = ROOT.TCanvas("can", "", 50,50,800,800)
  can.SetFrameLineWidth(3)
  can.SetTickx()
  can.SetTicky()
  plot.SetMaximum(1.5*plot.GetMaximum())
  plot.SetTitle("")
  plot.Draw()
  plot.Print()
  plot.Draw("SAME")
  return can, leg

categories_expweighted = [
  # 3GL 2017
  category(name='B3GL_A117', fileb=B3GL_2017, files=S3GL_2017, e=2.30, s=1.0388 , b=1.05926, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B3GL_B117', fileb=B3GL_2017, files=S3GL_2017, e=2.19, s=1.50467, b=2.52061, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B3GL_C117', fileb=B3GL_2017, files=S3GL_2017, e=3.36, s=1.9952 , b=12.3963, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B3GL_A217', fileb=B3GL_2017, files=S3GL_2017, e=1.70, s=4.2737 , b=18.5647, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B3GL_B217', fileb=B3GL_2017, files=S3GL_2017, e=2.05, s=2.87582, b=12.4856, wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B3GL_C217', fileb=B3GL_2017, files=S3GL_2017, e=4.77, s=3.57411, b=107.263, wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  category(name='B3GL_A317', fileb=B3GL_2017, files=S3GL_2017, e=2.28, s=7.88048, b=139.2  , wspacel='w_all', datal='data_obs_A3', sigl='SignalModel_A3'),
  category(name='B3GL_B317', fileb=B3GL_2017, files=S3GL_2017, e=1.88, s=12.4699, b=250.512, wspacel='w_all', datal='data_obs_B3', sigl='SignalModel_B3'),
  category(name='B3GL_C317', fileb=B3GL_2017, files=S3GL_2017, e=10.8, s=2.78574, b=336.078, wspacel='w_all', datal='data_obs_C3', sigl='SignalModel_C3'),
  # 3GL 2018
  category(name='B3GL_A118', fileb=B3GL_2018, files=S3GL_2018, e=1.23, s=4.5975, b=10.0293, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B3GL_B118', fileb=B3GL_2018, files=S3GL_2018, e=1.72, s=2.4183, b=4.93178, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B3GL_C118', fileb=B3GL_2018, files=S3GL_2018, e=1.79, s=2.6001, b=5.91992, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B3GL_A218', fileb=B3GL_2018, files=S3GL_2018, e=1.29, s=9.4200, b=59.7067, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B3GL_B218', fileb=B3GL_2018, files=S3GL_2018, e=1.00, s=12.836, b=70.7446, wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B3GL_C218', fileb=B3GL_2018, files=S3GL_2018, e=2.13, s=4.8412, b=37.1054, wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  category(name='B3GL_A318', fileb=B3GL_2018, files=S3GL_2018, e=1.81, s=16.663, b=398.711, wspacel='w_all', datal='data_obs_A3', sigl='SignalModel_A3'),
  category(name='B3GL_B318', fileb=B3GL_2018, files=S3GL_2018, e=1.35, s=33.761, b=952.281, wspacel='w_all', datal='data_obs_B3', sigl='SignalModel_B3'),
  category(name='B3GL_C318', fileb=B3GL_2018, files=S3GL_2018, e=2.84, s=10.686, b=355.332, wspacel='w_all', datal='data_obs_C3', sigl='SignalModel_C3'),
  # 2GL 2017
  category(name='B2GL_A117', fileb=B2GL_2017, files=S2GL_2017, e=4.88, s=0.6578, b=2.08188, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B2GL_B117', fileb=B2GL_2017, files=S2GL_2017, e=5.94, s=1.2751, b=12.3156, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B2GL_C117', fileb=B2GL_2017, files=S2GL_2017, e=1.43, s=0.3390, b=6.77482, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B2GL_A217', fileb=B2GL_2017, files=S2GL_2017, e=6.22, s=1.3560, b=26.5756, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B2GL_B217', fileb=B2GL_2017, files=S2GL_2017, e=7.22, s=3.3052, b=244.133, wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B2GL_C217', fileb=B2GL_2017, files=S2GL_2017, e=22.5, s=0.5037, b=47.8639, wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  # 2GL 2018
  category(name='B2GL_A118', fileb=B2GL_2018, files=S2GL_2018,  e=3.55, s=1.0893, b=6.49795, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B2GL_B118', fileb=B2GL_2018, files=S2GL_2018,  e=2.62, s=4.6117, b=54.9399, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B2GL_C118', fileb=B2GL_2018, files=S2GL_2018,  e=4.56, s=2.4258, b=42.4175, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B2GL_A218', fileb=B2GL_2018, files=S2GL_2018,  e=5.50, s=1.6259, b=31.0139, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B2GL_B218', fileb=B2GL_2018, files=S2GL_2018,  e=4.55, s=8.1209, b=496.256, wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B2GL_C218', fileb=B2GL_2018, files=S2GL_2018,  e=8.00, s=4.1222, b=337.312, wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  # W 2017
  category(name='W_A17', fileb=BW_A17, files=SW_A17, e=2.24, s=1.4, b=1.4, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_B17', fileb=BW_B17, files=SW_B17, e=2.57, s=1.7, b=4.1, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_C17', fileb=BW_C17, files=SW_C17, e=6.76, s=0.6, b=2.0, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  # W 2018
  category(name='W_A18', fileb=BW_A17, files=SW_A17, e=1.20, s=2.6, b=1.6, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_B18', fileb=BW_B17, files=SW_B17, e=1.66, s=1.6, b=0.7, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_C18', fileb=BW_C17, files=SW_C17, e=4.64, s=1.1, b=4.4, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
]
can, leg = merge_and_plot(categories_expweighted)
for cat in categories_expweighted:
  print('{}\t{}\t{}\t{}'.format(cat.n, round(cat.wgt.getValV(),4), round(cat.e,4), round(cat.ams,4)))


lumitext="2017+2018, 97.8 fb^{-1} (13 TeV)"
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)
ll = can.GetLeftMargin()
tt = can.GetTopMargin()
rr = can.GetRightMargin()
bb = can.GetBottomMargin()
lumitextsize = 0.5
lumitextoffset = 0.2

latex.SetTextFont(42)
latex.SetTextAlign(31)
latex.SetTextSize(lumitextsize*tt)
latex.DrawLatex(1-rr, 1-tt+lumitextoffset*tt, lumitext)

cmstextfont = 61
cmstextsize = 0.65
extratextfont = 52
relposx = 0.045
relposy = 0.035
posx = ll+0.05*(1-ll-rr)
posy = 0.95-tt-relposy*(1-tt-bb)

latex.SetTextFont(cmstextfont)
latex.SetTextSize(cmstextsize*tt)
latex.SetTextAlign(12)
latex.DrawLatex(posx, posy, "CMS")

latex.SetTextSize(cmstextsize*tt*0.8)
#latex.DrawLatex(0.5, posy, "W Category {}".format(category))

latex.SetTextFont(extratextfont)
latex.SetTextSize(cmstextsize*tt)
#latex.DrawLatex(posx, posy-1.2*cmstextsize*tt, "Preliminary")
title = "weighted_massplot".format(category, '17' if '2017' in lumitext else '18')
leg.Draw()
can.SaveAs(title+".pdf", "pdf")
can.SaveAs(title+".root", "root")
