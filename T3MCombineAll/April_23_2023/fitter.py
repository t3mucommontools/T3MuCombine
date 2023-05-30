import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input' , required=True)
parser.add_argument('--output', default="scan.pdf")
parser.add_argument('--min'   , default=0.2)
parser.add_argument('--max'   , default=0.3)
parser.add_argument('--cl'    , default=0.9)
args = parser.parse_args()

file = ROOT.TFile.Open(args.input, 'READ')
tree = file.Get("limit")
graph = ROOT.TGraphErrors()

for i,pt in enumerate(tree):
  '''
  in the output tree, limit is the value of r, quantileExpected the pvalue and 
  limitErr the error on the pvalue?
  '''
  x = pt.limit
  y = pt.quantileExpected
  if y == 0.5: continue
  e = pt.limitErr 
  print(x,y)
  graph.SetPoint(i,x,y)
  graph.SetPointError(i,0,e)

fitf = ROOT.TF1("fitf", "expo", args.min, args.max)
graph.Fit(fitf, "LR")
can = ROOT.TCanvas()
graph.SetTitle(";r;p-value (CLs)")
graph.Draw("AP")
fitf.Draw("SAME")

import math
p = (math.log(1-args.cl)-fitf.GetParameter(0))/fitf.GetParameter(1) if fitf.GetParameter(1) else -99
xline = ROOT.TLine(0, 1, 0.1, 0.1)
yline = ROOT.TLine(p, 0, p, 1)
xline.SetLineColor(ROOT.kRed)
yline.SetLineColor(ROOT.kRed)
xline.Draw("SAME")
yline.Draw("SAME")
can.Update()
can.Modified()
can.SaveAs(args.output, args.output.split('.')[-1])

print("r < "+str(p))