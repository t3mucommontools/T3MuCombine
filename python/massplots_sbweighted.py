import ROOT
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
    self.e = e
    self.ns = s
    self.nb = b
  def weight(self, w):
    ''' create a weight of value w and add it to the dataset.
    the dataset is not weighted at this point but contains the info
    '''
    self.wgt  = ROOT.RooRealVar("wgt", '', w)
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
  for cat in categories:
    cat.weight(1./cat.e/norm)
#    cat.weight(cat.ns/cat.nb/norm)
  merged = ROOT.RooDataSet('merged', '', categories[0].rds.get())
  for i, cat in enumerate(categories):
    merged.append(cat.rds)
  wdata  = ROOT.RooDataSet(merged.GetName(), merged.GetTitle(), merged, merged.get(), "", 'wgt')
  sigs = ROOT.RooArgList()
  wgts = ROOT.RooArgList()
  for cat in categories:
    sigs.add(cat.sig)
    wgts.add(cat.wgt)
  sums = ROOT.RooAddPdf('sums', '', sigs, wgts)
  signorm = sum(c.ns*c.wgt.getValV() for c in categories)
  plot  = categories[0].x.frame(40)
  wdata.plotOn(plot)
  sums.plotOn(plot, ROOT.RooFit.Normalization(signorm,ROOT.RooAbsReal.NumEvent), ROOT.RooFit.LineColor(ROOT.kRed))
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
  category(name='B3GL_A117', fileb=B3GL_2017, files=S3GL_2017, e=23.0, s=1.04, b=0.79, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B3GL_B117', fileb=B3GL_2017, files=S3GL_2017, e=21.9, s=1.50, b=2.49, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B3GL_C117', fileb=B3GL_2017, files=S3GL_2017, e=33.6, s=1.99, b=13.0, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B3GL_A217', fileb=B3GL_2017, files=S3GL_2017, e=17.0, s=4.27, b=18.9, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B3GL_B217', fileb=B3GL_2017, files=S3GL_2017, e=20.5, s=2.88, b=12.5, wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B3GL_C217', fileb=B3GL_2017, files=S3GL_2017, e=47.7, s=3.57, b=107 , wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  category(name='B3GL_A317', fileb=B3GL_2017, files=S3GL_2017, e=22.8, s=7.88, b=135 , wspacel='w_all', datal='data_obs_A3', sigl='SignalModel_A3'),
  category(name='B3GL_B317', fileb=B3GL_2017, files=S3GL_2017, e=18.8, s=12.5, b=243 , wspacel='w_all', datal='data_obs_B3', sigl='SignalModel_B3'),
  category(name='B3GL_C317', fileb=B3GL_2017, files=S3GL_2017, e=108., s=2.79, b=343 , wspacel='w_all', datal='data_obs_C3', sigl='SignalModel_C3'),
  # 3GL 2018
  category(name='B3GL_A118', fileb=B3GL_2018, files=S3GL_2018, e=12.3, s=4.60, b=10.0, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B3GL_B118', fileb=B3GL_2018, files=S3GL_2018, e=17.2, s=2.42, b=4.94, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B3GL_C118', fileb=B3GL_2018, files=S3GL_2018, e=17.9, s=2.60, b=5.95, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B3GL_A218', fileb=B3GL_2018, files=S3GL_2018, e=12.9, s=9.42, b=59.7, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B3GL_B218', fileb=B3GL_2018, files=S3GL_2018, e=10.0, s=12.8, b=59.4, wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B3GL_C218', fileb=B3GL_2018, files=S3GL_2018, e=21.3, s=4.84, b=37.3, wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  category(name='B3GL_A318', fileb=B3GL_2018, files=S3GL_2018, e=18.1, s=16.7, b=393 , wspacel='w_all', datal='data_obs_A3', sigl='SignalModel_A3'),
  category(name='B3GL_B318', fileb=B3GL_2018, files=S3GL_2018, e=13.5, s=33.8, b=944 , wspacel='w_all', datal='data_obs_B3', sigl='SignalModel_B3'),
  category(name='B3GL_C318', fileb=B3GL_2018, files=S3GL_2018, e=28.4, s=10.7, b=346 , wspacel='w_all', datal='data_obs_C3', sigl='SignalModel_C3'),
  # 2GL 2017
  category(name='B2GL_A117', fileb=B2GL_2017, files=S2GL_2017, e=48.8, s=0.65, b=2.08, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B2GL_B117', fileb=B2GL_2017, files=S2GL_2017, e=59.4, s=1.28, b=9.93, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B2GL_C117', fileb=B2GL_2017, files=S2GL_2017, e=143., s=0.34, b=6.30, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B2GL_A217', fileb=B2GL_2017, files=S2GL_2017, e=62.2, s=1.36, b=26.7, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B2GL_B217', fileb=B2GL_2017, files=S2GL_2017, e=72.2, s=3.31, b=224 , wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B2GL_C217', fileb=B2GL_2017, files=S2GL_2017, e=225., s=0.50, b=47.5, wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  # 2GL 2018
  category(name='B2GL_A118', fileb=B2GL_2018, files=S2GL_2018,  e=35.5, s=1.09, b=6.49, wspacel='w_all', datal='data_obs_A1', sigl='SignalModel_A1'),
  category(name='B2GL_B118', fileb=B2GL_2018, files=S2GL_2018,  e=26.2, s=4.61, b=54.4, wspacel='w_all', datal='data_obs_B1', sigl='SignalModel_B1'),
  category(name='B2GL_C118', fileb=B2GL_2018, files=S2GL_2018,  e=45.6, s=2.43, b=42.0, wspacel='w_all', datal='data_obs_C1', sigl='SignalModel_C1'),
  category(name='B2GL_A218', fileb=B2GL_2018, files=S2GL_2018,  e=55.0, s=1.63, b=31.0, wspacel='w_all', datal='data_obs_A2', sigl='SignalModel_A2'),
  category(name='B2GL_B218', fileb=B2GL_2018, files=S2GL_2018,  e=45.5, s=8.12, b=487 , wspacel='w_all', datal='data_obs_B2', sigl='SignalModel_B2'),
  category(name='B2GL_C218', fileb=B2GL_2018, files=S2GL_2018,  e=80.0, s=4.12, b=339 , wspacel='w_all', datal='data_obs_C2', sigl='SignalModel_C2'),
  # W 2017
  category(name='W_A17', fileb=BW_A17, files=SW_A17, e=22.4, s=0.14, b=1.4, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_B17', fileb=BW_B17, files=SW_B17, e=25.7, s=0.17, b=4.1, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_C17', fileb=BW_C17, files=SW_C17, e=67.6, s=0.06, b=2.0, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  # W 2018
  category(name='W_A18', fileb=BW_A17, files=SW_A17, e=12.0, s=0.26, b=1.6, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_B18', fileb=BW_B17, files=SW_B17, e=16.6, s=0.16, b=0.7, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
  category(name='W_C18', fileb=BW_C17, files=SW_C17, e=46.4, s=0.11, b=4.4, wspacel='t3m_shapes', datal='data_obs', sigl='sig'),
]
can, leg = merge_and_plot(categories_expweighted)
for cat in categories_expweighted:
  print('{}\t{}'.format(cat.n, round(cat.wgt.getValV(),4)))


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
#  latex.DrawLatex(posx, posy-1.2*cmstextsize*tt, "Preliminary")
title = "weighted_massplot.pdf".format(category, '17' if '2017' in lumitext else '18')
leg.Draw()
can.SaveAs(title, "pdf")
