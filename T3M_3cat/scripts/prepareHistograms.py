#!/usr/bin/env python

import os
import argparse
import ROOT
from ROOT import TFile
import math
import array


MAX = 2.0
MIN = 1.5
NCat = 3

categories = [ ]
categories.append(["A",[0.0, 0.15]]) 
categories.append(["B",[0.0, 0.15]]) 
categories.append(["C",[0.05, 0.1]]) 

samples = [ ]
samples.append(["Data",1])
samples.append(["MC2",1])  # Ds  -> Tau
samples.append(["MC3",1])  # B_0 -> Tau
samples.append(["MC4",1])  # B_p -> Tau


histo_prefix = "signalselector_default_TauMass_allVsBDT"


def get_histogram(path):
    input_file_path, histogram_path = path.split(":")
    input_file = ROOT.TFile(input_file_path, "OPEN")
    histogram = input_file.Get(histogram_path)
    histogram.SetDirectory(0)
    input_file.Close()
    return histogram


def get_projection(histo,a,b):
    axis = histo.GetYaxis()
    mvamin = axis.FindBin(a)
    mvamax = axis.FindBin(b)
    if b==-1: 
        mvamax = b
    return histo.ProjectionX("huy",mvamin, mvamax, "")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",help="input file. [Default: %(default)s] ", action="store", default = 'LOCAL_COMBINED_signalselector_default_LumiScaled.root')
    args = parser.parse_args()
    
    histosData = []
    histosBkg = []
    histosMC   = []

    for c in categories:
        for s in samples:
#            print histo_prefix+c[0]+s
           
            if s[0] =="Data":
                histo1 = get_projection(get_histogram(args.input_file+":"+histo_prefix+c[0]+s[0]), c[1][1], -1)
                histo1.SetName("background"+c[0]+"1")
                histo2 = get_projection(get_histogram(args.input_file+":"+histo_prefix+c[0]+s[0]), c[1][0], c[1][1])
                histo2.SetName("background"+c[0]+"2")

                histosBkg.append(histo1)
                histosBkg.append(histo2)

            if s[0] =="Data":
                histo1 = get_projection(get_histogram(args.input_file+":"+histo_prefix+c[0]+s[0]),c[1][1], -1)
                histo1.SetName("data_obs"+c[0]+"1")
                histo2 = get_projection(get_histogram(args.input_file+":"+histo_prefix+c[0]+s[0]),c[1][0], c[1][1])
                histo2.SetName("data_obs"+c[0]+"2")

                histosData.append(histo1)
                histosData.append(histo2)



            if s[0]!="Data":
                histo1 = get_projection(get_histogram(args.input_file+":"+histo_prefix+c[0]+s[0]),c[1][1], -1)
                histo1.SetName(s[0]+c[0]+"1")
                histo1.Scale(s[1])

                histo2 = get_projection(get_histogram(args.input_file+":"+histo_prefix+c[0]+s[0]),c[1][0], c[1][1])
                histo2.SetName(s[0]+c[0]+"2")
                histo2.Scale(s[1])


                histosMC.append(histo1)
                histosMC.append(histo2)



    f = TFile( 'test.root', 'recreate' )
    for h in histosData:
        h.Write()

    for h in histosBkg:
        h.Write()

#    for h in histosMC:
#        h.Write()
#       print h.GetName()

    histoSubCategory1 =[]
    histoSubCategory2 =[]
    for c in categories:
        for h in histosMC:
            if c[0]+"1" in h.GetName():
                histoSubCategory1.append(h)
            if c[0]+"2" in h.GetName():
                histoSubCategory2.append(h)

                

    print histoSubCategory1
    print histoSubCategory2



    histoMCA1 = []
    histoMCA2 = []
    histoMCB1 = []
    histoB2 = []
    histoA1 = []
    histoA1 = []
    histoA1 = []
    SignalA1 = histosMC[0]

    SignalA1.SetName("signalA1")
    SignalA1.Add(histosMC[2])
    SignalA1.Add(histosMC[4])
    SignalA1.Write()

    SignalA2 = histosMC[1]
    SignalA2.SetName("signalA2")
    SignalA2.Add(histosMC[3])
    SignalA2.Add(histosMC[5])
    SignalA2.Write()

    SignalB1 = histosMC[6]
    SignalB1.SetName("signalB1")
    SignalB1.Add(histosMC[8])
    SignalB1.Add(histosMC[10])
    SignalB1.Write()

    SignalB2 = histosMC[7]
    SignalB2.SetName("signalB2")
    SignalB2.Add(histosMC[9])
    SignalB2.Add(histosMC[11])
    SignalB2.Write()

    SignalC1 = histosMC[12]
    SignalC1.SetName("signalC1")
    SignalC1.Add(histosMC[14])
    SignalC1.Add(histosMC[16])
    SignalC1.Write()

    SignalC2 = histosMC[13]
    SignalC2.SetName("signalC2")
    SignalC2.Add(histosMC[15])
    SignalC2.Add(histosMC[17])

    SignalC2.Write()



