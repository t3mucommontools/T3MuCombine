#!/usr/bin/env python

import os
import argparse
import ROOT
from ROOT import TFile
import math
import array

def load_dp(path):
    fil = ROOT.TFile.Open(path, "READ")
    wsp = fil.Get("ospace")
    return wsp

def take_index(cat, typ, year):
    wsp = load_dp("../../python/MultiPdfWorkspaces/"+year+"_"+typ+"_"+cat+".root") 
    return wsp.pdf("bkg").getCurrentIndex()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",help="input file. [Default: %(default)s] ", action="store", default = 'CMS_T3MSignal_13TeV_Combined.txt')
    parser.add_argument("-b", "--blind",help="blind option. [Default: %(default)s] ", action="store", default = 'true')
    parser.add_argument("-m", "--method",help="AsymptoticLimits or HybridNew. [Default: %(default)s] ", action="store", default = 'AsymptoticLimits')
    parser.add_argument("-c", "--categories", help="Comma separated list of categories. [Default: %(default)s] ", action="store", default = 'A1,B1,C1,A2,B2,C2,A3,B3,C3')
    parser.add_argument("-d", "--discrete", help="Use discrete profiling method. [Default: %(default)s] ", action="store", default = 'false')
    parser.add_argument("-t", "--typ", help="specify type (threeGlobal/twoGlobalTracker)", action="store", default="threeGlobal")
    parser.add_argument("-r", "--run", help="Run (2017/2018)", action="store", default="2018")
    args = parser.parse_args()

    categorylist = args.categories.split(',')
    command ="combineTool.py -M T2W -o workspace.root -i "+args.input_file+";"
    if(args.method=='AsymptoticLimits'):
        if(args.blind=='true'):
            command +="combineTool.py -M "+args.method+" --run blind -d workspace.root --cl 0.90 -m 1.777 --noFitAsimov;"
        else:
            command +="combineTool.py -M "+args.method+" --run expected -d workspace.root --cl 0.90 -m 1.777;"
            command +="combineTool.py -M "+args.method+" --run observed -d workspace.root --cl 0.90 -m 1.777;"
    else: #toys
        command +="combineTool.py -M "+args.method+" --cl 0.90 -m 1.777 --testStat=LHC "
        command +="--frequentist "+args.input_file+" -T 3000 --expectedFromGrid 0.5 --plot=../plots/limit_combined_hybridnew_HF.pdf --rMin -1 --rMax 10 "
        if(args.discrete=='true'):
            
            discrete_prof = ["roomultipdf_cat_HF_{c}={i}".format(c=categ, i=take_index(categ, args.typ, args.run)) for categ in categorylist]
            discrete_prof = ','.discrete_prof
            command += "--setParameters "+discrete_prof+" "

            parameter_selection = ["slope_{c}={m},{M}".format(c=categ, m=-1000, M=100) for categ in categorylist]
            parameter_selection +=["bkg_norm_dp_{c}={m},{M}".format(c=categ, m=0, M=1000000) for c in categorylist]
            parameters_selection  =  ':'.join(parameter_selection)
            command += "--setParameterRanges "+parameters_selection+" "
        else:
            parameter_selection = ["bkg_exp_slope_{c}={m},{M}".format(c=categ, m=-1000, M=100) for categ in categorylist]
            parameter_selection +=["bkg_exp_offset_{c}={m},{M}".format(c=categ, m=0, M=1000000) for categ in categorylist]
            parameters_selection  =  ':'.join(parameter_selection)
            command += "--setParameterRanges "+parameters_selection+" "
        if(args.blind=='true'):
            command +="--fitNuisances=0"
        else:
            command +="--fitNuisances=1"
    print command
    os.system(command)


