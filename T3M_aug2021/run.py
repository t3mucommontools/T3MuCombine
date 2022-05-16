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
    parser.add_argument("-s", "--settings-file",help="txt file for settings/configuration. [Default: %(default)s] ", action="store", default = 'config.txt')
    parser.add_argument("-t", "--type", help="specify type (threeGlobal/twoGlobalTracker)", action="store", default="threeGlobal")
    parser.add_argument("-r", "--run", help="Run (2017/2018)", action="store", default="2018")
    parser.add_argument("-b", "--blind", help="blind signal region (true/false)", action="store_true")
    parser.add_argument("-v", "--version", help="-v 2 for 6 categories, -v 3 for 9 categories",action="store", type=int, default=2)
    args = parser.parse_args()

    command = ""

    isBlind = "false"
    if args.blind: isBlind = "true"

    if args.version==2:
           command="root -b -q 'createDataCards.cxx(\"" + args.input_file+ "\", 0, " + isBlind + ", \""+ args.card_file +"\",\""+ args.settings_file +"\",\""+args.type+"\",\""+args.run+"\")';"
           command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt"
           command +="  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt > CMS_T3MSignal_13TeV_Combined.txt;"
    elif args.version==3:
           command="root -b -q 'createDataCards.cxx(\"" + args.input_file+ "\", 0, " + isBlind + ", \""+ args.card_file +"\",\""+ args.settings_file +"\",\""+args.type+"\",\""+args.run+"\")';"
           command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_A3.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt"
           command +=" CMS_T3MSignal_13TeV_B3.txt  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt CMS_T3MSignal_13TeV_C3.txt> CMS_T3MSignal_13TeV_Combined.txt;"
    else:
        print("Invalid version")


    print command
    os.system(command)
