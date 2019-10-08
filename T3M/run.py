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
    args = parser.parse_args()

    command="root -b -q 'createDataCards.cxx(\" " + args.input_file+ "\" )';"
    command +="cd datacards; combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt CMS_T3MSignal_13TeV_B1.txt CMS_T3MSignal_13TeV_B2.txt  CMS_T3MSignal_13TeV_C1.txt CMS_T3MSignal_13TeV_C2.txt > CMS_T3MSignal_13TeV_Combined.txt;"


    print command
    os.system(command)
