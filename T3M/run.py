#!/usr/bin/env python

import os
import argparse
import ROOT
from ROOT import TFile
import math
import array


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",help="input file. [Default: %(default)s] ", action="store", default = 'input_histograms.root')
    parser.add_argument("-c", "--card-file",help="model card file. [Default: %(default)s] ", action="store", default = 'model_card.rs')
    parser.add_argument("-t", "--type", help="specify type (threeGlobal/twoGlobalTracker)", action="store", default="threeGlobal")
    parser.add_argument("-r", "--run", help="Run (2017/2018)", action="store", default="2018")
    parser.add_argument("-d", "--dimensions",help="Type of binning used (1 for 1D, 2 for 2D)", type=int, action="store",default=1)
    parser.add_argument("-v", "--version", help="Version of createDataCard.cxx",action="store", type=int, default=2)
    args = parser.parse_args()

    command = ""
    print(args.dimensions)

    if (args.dimensions==1):
        if args.version==1:
           command="root -b -q 'createDataCards.cxx(\"" + args.input_file+ "\", 0, false, \""+ args.card_file +"\",\""+args.type+"\",\""+args.run+"\")';"
           command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt"
           command +="  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt > CMS_T3MSignal_13TeV_Combined.txt;"
        elif args.version==2:
           command="root -b -q 'createDataCards_v2.cxx(\"" + args.input_file+ "\", 0, false, \""+ args.card_file +"\",\""+args.type+"\",\""+args.run+"\")';"
           command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt"
           command +="  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt > CMS_T3MSignal_13TeV_Combined.txt;"
        elif args.version==3:
           command="root -b -q 'createDataCards_v3.cxx(\"" + args.input_file+ "\", 0, false, \""+ args.card_file +"\",\""+args.type+"\",\""+args.run+"\")';"
           command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_A3.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt"
           command +=" CMS_T3MSignal_13TeV_B3.txt  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt CMS_T3MSignal_13TeV_C3.txt> CMS_T3MSignal_13TeV_Combined.txt;"
        elif args.version==4:
           command="root -b -q 'createDataCards_v4.cxx(\"" + args.input_file+ "\", 0, false, \""+ args.card_file +"\",\""+args.type+"\",\""+args.run+"\")';"
           command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_A3.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt"
           command +=" CMS_T3MSignal_13TeV_B3.txt  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt CMS_T3MSignal_13TeV_C3.txt> CMS_T3MSignal_13TeV_Combined.txt;"

    elif (args.dimensions==2):
        command="root -b -q 'create2DDataCards.cxx(\"" + args.input_file+ "\", 0, false, \""+ args.card_file +"\",\""+args.type+"\",\""+args.run+"\")';"
        command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A11.txt CMS_T3MSignal_13TeV_A12.txt CMS_T3MSignal_13TeV_A21.txt CMS_T3MSignal_13TeV_A22.txt "
        command +="CMS_T3MSignal_13TeV_B11.txt CMS_T3MSignal_13TeV_B12.txt CMS_T3MSignal_13TeV_B21.txt CMS_T3MSignal_13TeV_B22.txt "
        command +="CMS_T3MSignal_13TeV_C11.txt CMS_T3MSignal_13TeV_C12.txt CMS_T3MSignal_13TeV_C21.txt CMS_T3MSignal_13TeV_C22.txt > CMS_T3MSignal_13TeV_Combined.txt;"
    else:
        print("Invalid number of dimensions!")


    print command
    os.system(command)
