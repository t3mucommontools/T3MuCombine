#!/usr/bin/env python
import os, sys


if (len(sys.argv)<2): print "No input files given"
input_files = [ sys.argv[i] for i in range(1, len(sys.argv)) ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-file",help="output file. [Default: %(default)s] ", action="store", default = 'HF_CMS_T3MSignal_13TeV_Combined.txt')
    args = parser.parse_args()

#combineCards.py ../ThreeGlobal/2017/CMS_T3MSignal_13TeV_Combined.txt ../TwoGlobalTracker/2017/CMS_T3MSignal_13TeV_Combined.txt > HF_CMS_T3MSignal_13TeV_Combined_2017.txt
#combineCards.py ../ThreeGlobal/2018/CMS_T3MSignal_13TeV_Combined.txt ../TwoGlobalTracker/2018/CMS_T3MSignal_13TeV_Combined.txt > HF_CMS_T3MSignal_13TeV_Combined_2018.txt
