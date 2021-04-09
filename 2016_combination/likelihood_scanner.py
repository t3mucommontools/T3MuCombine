import ROOT

file_envelope = ROOTTfile.Open('higgsCombineEnvelope.MultiDimFit.mH120.root', 'read')
tree_envelope = file_envelope.Get('limit')

file_pdf_bern = ROOTTfile.Open('higgsCombineIndex0.MultiDimFit.mH120.root', 'read')
tree_pdf_bern = file_pdf_bern.Get('limit')

file_pdf_expo = ROOTTfile.Open('higgsCombineIndex1.MultiDimFit.mH120.root', 'read')
tree_pdf_expo = file_pdf_expo.Get('limit')

file_pdf_pow  = ROOTTfile.Open('higgsCombineIndex2.MultiDimFit.mH120.root', 'read')
tree_pdf_pow  = file_pdf_pow.Get('limit')

c1 = ROOT.TCanvas('c1', '', 700, 700)
histo_envelope = ROOT.TH2F('envelope', '', 100, -0.1, 1.5, 1000, -31380, -31340)
histo_pdf_bern = ROOT.TH2F('bern'    , '', 100, -0.1, 1.5, 1000, -31380, -31340)
histo_pdf_expo = ROOT.TH2F('expo'    , '', 100, -0.1, 1.5, 1000, -31380, -31340)
histo_pdf_pow  = ROOT.TH2F('pow'     , '', 100, -0.1, 1.5, 1000, -31380, -31340)

histo_envelope.SetLineColor(ROOT.kBlack)
histo_pdf_bern.SetLineColor(ROOT.kBlue)
histo_pdf_expo.SetLineColor(ROOT.kRed)
histo_pdf_pow .SetLineColor(ROOT.kGreen)

histo_envelope.SetLineWidth(2)
histo_pdf_bern.SetLineWidth(2)
histo_pdf_expo.SetLineWidth(2)
histo_pdf_pow .SetLineWidth(2)

histo_envelope.GetXaxis().SetTitle('r')
histo_pdf_bern.GetXaxis().SetTitle('r')
histo_pdf_expo.GetXaxis().SetTitle('r')
histo_pdf_pow .GetXaxis().SetTitle('r')

histo_envelope.GetYaxis().SetTitle('2 #cdot Log(#mathcal{L}) + C')
histo_pdf_bern.GetYaxis().SetTitle('2 #cdot Log(#mathcal{L}) + C')
histo_pdf_expo.GetYaxis().SetTitle('2 #cdot Log(#mathcal{L}) + C')
histo_pdf_pow .GetYaxis().SetTitle('2 #cdot Log(#mathcal{L}) + C')

tree_envelope.Draw('2*(deltaNLL+nll+nll0):r', 'r>-0.1', 'lp')
tree_pdf_bern.Draw('2*(deltaNLL+nll+nll0):r', 'r>-0.1', 'lp')
tree_pdf_expo.Draw('2*(deltaNLL+nll+nll0):r', 'r>-0.1', 'lp')
tree_pdf_pow .Draw('2*(deltaNLL+nll+nll0):r', 'r>-0.1', 'lp')

histo_envelope.Draw('lp')
histo_pdf_bern.Draw('lp same')
histo_pdf_expo.Draw('lp same')
histo_pdf_pow .Draw('lp same')

c1.SaveAs('ll_scan.pdf')




