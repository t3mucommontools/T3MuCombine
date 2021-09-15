#!/usr/bin/env python

import os
import argparse
import ROOT
from ROOT import TFile
import math
import array

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",help="input file. [Default: %(default)s] ", action="store", default = 'CMS_T3MSignal_13TeV_Combined.txt')
    parser.add_argument("-b", "--blind",help="blind option. [Default: %(default)s] ", action="store", default = 'true')
    args = parser.parse_args()
    command ="combineTool.py -M T2W -o workspace.root -i "+args.input_file+";"
    if(args.blind=='true'):
        command +="combineTool.py -M AsymptoticLimits  --run blind  -d workspace.root --cl 0.90 -m 1.777 --noFitAsimov;"
    else:
        command +="combineTool.py -M AsymptoticLimits --run expected -d workspace.root --cl 0.90 -m 1.777;"
        command +="combineTool.py -M AsymptoticLimits --run observed -d workspace.root --cl 0.90 -m 1.777;"

    print command
    os.system(command)
