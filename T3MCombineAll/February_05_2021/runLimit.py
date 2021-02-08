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
    args = parser.parse_args()
    command ="combineTool.py -M T2W -o workspace.root -i "+args.input_file+";"
    os.system('pwd')
    path_to_file = args.input_file
    _ = [ str_ for str_ in path_to_file.split('/') if '.txt' not in str_ ]
    path_to_workspace = ''
    for i in xrange(len(_)): path_to_workspace += _[i]+'/'
    path_to_workspace += 'workspace.root'
    command += 'mv '+path_to_workspace+' .;'
    command +="combineTool.py -M AsymptoticLimits  --run blind  -d workspace.root --cl 0.90 -m 1.777;"


    print command
    os.system(command)
