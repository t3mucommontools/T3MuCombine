#!/usr/bin/env python

import ROOT
from ROOT import TFile, TTree, TCanvas, TGraph, TMultiGraph, TGraphErrors, TLegend, TPaveLabel, TPaveText, TLatex
import CMS_lumi, tdrstyle
import subprocess # to execute shell command
import argparse

ROOT.gROOT.SetBatch(ROOT.kTRUE)
 
# CMS style
CMS_lumi.cmsText = ""
CMS_lumi.extraText = ""
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()
 

 
# EXECUTE datacards
def executeDataCards(labels,values, cardprefix):
 
    for value in values:
        label = "%s" % (value)
        combine_command = "combineTool.py -M AsymptoticLimits  -n %s -d %s" % (cardprefix+label,cardprefix+label+'.txt')
        print ""
        print ">>> " + combine_command
        p = subprocess.Popen(combine_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line.rstrip("\n")
        print ">>>   higgsCombine"+cardprefix+label+".Asymptotic.mH125.root created"
        retval = p.wait()
 
 
# GET limits from root file
def getLimits(file_name):
 
    file = TFile(file_name)
    tree = file.Get("limit")
 
    limits = [ ]
    for quantile in tree:
        limits.append(tree.limit)
        print ">>>   %.2f" % limits[-1]
 
    return limits[:6]
 
 
# PLOT upper limits
def plotUpperLimits(labels,values,prefix,outputLabel):
 
    N = len(labels)
    yellow = TGraph(2*N)   
    green = TGraph(2*N)    
    median = TGraph(N)     
 
    up2s = [ ]
    upm  = [ ]
    text_limits=open("TextLimits%s"%(prefix)+outputLabel+".txt","w")
    for i in range(N):
        file_name = "higgsCombine"+prefix+labels[i]+".AsymptoticLimits.mH120.root"
        print "filename:  ", file_name
        limit = getLimits(file_name)
        up2s.append(limit[4])
        upm.append(limit[2])
        yellow.SetPoint(    i,    values[i], limit[4]) # + 2 sigma
        green.SetPoint(     i,    values[i], limit[3]) # + 1 sigma
        median.SetPoint(    i,    values[i], limit[2]) #    median
        green.SetPoint(  2*N-1-i, values[i], limit[1]) # - 1 sigma
        yellow.SetPoint( 2*N-1-i, values[i], limit[0]) # - 2 sigma
        text_limits.write("bdt %.2f     median exp %.2f\n"%(values[i],limit[2]))

    W = 800
    H  = 600
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W
    R = 0.04*W
    c = TCanvas("c","c",100,100,W,H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetGrid()
    c.SetFrameLineWidth(3);
    c.SetTickx();
    c.SetTicky();
    c.cd()
    frame = c.DrawFrame(1.4,0.001, 4.1, 10)
    frame.GetYaxis().CenterTitle()

    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(0.9)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetYaxis().CenterTitle(False)
    frame.GetYaxis().SetTitle("B(#tau #rightarrow #mu#mu#mu) #times 10^{-7}")
    frame.GetXaxis().SetTitle("bdt")




    frame.SetMinimum(0.5)
    frame.SetMaximum(10.)

    frame.GetXaxis().SetLimits(min(values),max(values)*1.2)


 
    yellow.SetFillColor(ROOT.kOrange)
    yellow.SetLineColor(ROOT.kOrange)
    yellow.SetFillStyle(1001)
#    yellow.Draw('F')
 
    green.SetFillColor(ROOT.kGreen+1)
    green.SetLineColor(ROOT.kGreen+1)
    green.SetFillStyle(1001)
#    green.Draw('Fsame')
 
    median.SetLineColor(1)
    median.SetLineWidth(2)
    median.SetLineStyle(2)
    median.Draw('Lsame')
    median.Draw()
 
    CMS_lumi.CMS_lumi(c,13,11)
    ROOT.gPad.SetTicks(1,1)
    frame.Draw('sameaxis')
 
    x1 = 0.15
    x2 = x1 + 0.24
    y2 = 0.76
    y1 = 0.60
    legend = TLegend(x1,y1,x2,y2)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.041)
    legend.SetTextFont(42)
    legend.AddEntry(median, "Asymptotic CL_{s} expected",'L')
#    legend.AddEntry(green, "#pm 1 std. deviation",'f')
#    legend.AddEntry(yellow,"#pm 2 std. deviation",'f')


    legend.Draw()
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextFont(42)
    latex.SetTextAlign(31)

    latex.DrawLatex(0.57, 0.85,prefix)
    latex.Draw('same') 
    print " "
    c.SaveAs("Limit"+prefix+outputLabel+".png")
    c.Close()
 
 
# RANGE of floats
def frange(start, stop, step):
    i = start
    while i <= stop:
        yield i
        i += step
 
 
# MAIN
def main():
 

    cuts=[-0.2, -0.15, -0.05, -0.04 ,-0.03, -0.02, -0.01, 0, 0.02,  0.04,  0.06,  0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14,  0.15, 0.16, 0.17, 0.18, 0.19,  0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26]
    prefixes = ['CMS_T3MSignal_13TeV_Var2016A','CMS_T3MSignal_13TeV_Var2016B','CMS_T3MSignal_13TeV_Var2016C']


    outputLabel = ''
    for prefix in prefixes:
        labels = [ ]
        values = [ ]

        for cl in cuts:
            values.append(cl)
            label = "%s" % (cl)
            labels.append(label)
        print values
        print labels
        print "prefix", prefix
        executeDataCards(labels,values,prefix)
        plotUpperLimits(labels,values,prefix,outputLabel)
 
 
 
if __name__ == '__main__':
    main()
