#!/usr/bin/env python

import os
import argparse
import ROOT
from ROOT import TFile
import math
import array
from datetime import datetime

def open_wp():
    fil = ROOT.TFile.Open("../workspaces/CMS_T3MBkg_13TeV.root", "READ")
    wsp = fil.Get("w_all")
    return wsp

def take_index_dp(catlist):
    wsp = open_wp()
    setparam = ["roomultipdf_cat_HF_{c}={i}".format(c=cat, i=wsp.pdf('multipdf_'+cat).getCurrentIndex() ) for cat in categorylist]
    return setparam

def take_paramsel_dp(catlist):
    wsp = open_wp()
    parameters  = [ROOT.RooArgList(wsp.pdf('multipdf_'+cat).getParameters(ROOT.RooArgSet(wsp.var("m3m"))))[i] for cat in catlist for i in range(ROOT.RooArgList(wsp.pdf('multipdf_'+cat).getParameters(ROOT.RooArgSet(wsp.var("m3m")))).getSize())] 
    parameters  = [p for p in parameters if not p.isConstant() and not 'roomultipdf_cat' in p.GetName()]
    parameters_selection = ['{P}={m},{M}'.format(P=p.GetName(), m=p.getMin(), M=p.getMax()) for p in parameters]
    return parameters_selection

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",help="input file. [Default: %(default)s] ", action="store", default = 'CMS_T3MSignal_13TeV_Combined.txt')
    parser.add_argument("-b", "--blind",help="blind option. [Default: %(default)s] ", action="store", default = 'true')
    parser.add_argument("-m", "--method",help="AsymptoticLimits or HybridNew. [Default: %(default)s] ", action="store", default = 'AsymptoticLimits')
    parser.add_argument("-c", "--categories", help="Comma separated list of categories. [Default: %(default)s] ", action="store", default = 'A1,B1,C1,A2,B2,C2,A3,B3,C3')
    parser.add_argument("-d", "--discrete", help="Use discrete profiling method. [Default: %(default)s] ", action="store_false", default=False)
    parser.add_argument("-t", "--type", help="specify type (threeGlobal/twoGlobalTracker)", action="store", default="threeGlobal")
    parser.add_argument("-r", "--run", help="Run (2017/2018)", action="store", default="2018")
    parser.add_argument("-q", "--quantile", help="set to compute the median expected and the 68% and 95% interval boundaries", action="store", default="0.5", choices=["0.025", "0.16", "0.5", "0.84", "0.975"])
    parser.add_argument("-s", "--submit", help="submit jobs to HTcondor", action="store", default="false")
    args = parser.parse_args()

    categorylist = args.categories.split(',')

    now = datetime.now()
    now = now.strftime("%b_%d_%Y_%H_%M_%S")

    command ="combineTool.py -M T2W -o workspace_"+now+".root -i "+args.input_file+";"
    if(args.method=='AsymptoticLimits'):
        if(args.blind=='true'):
            command +="combineTool.py -M "+args.method+" --run blind -d workspace_"+now+".root --cl 0.90 -m 1.777 --noFitAsimov"
        else:
            command +="combineTool.py -M "+args.method+" --run expected -d workspace_"+now+".root --cl 0.90 -m 1.777"
            command +="combineTool.py -M "+args.method+" --run observed -d workspace_"+now+".root --cl 0.90 -m 1.777"
    else: #toys
        command +="combineTool.py -M "+args.method+" --cl 0.90 -m 1.777 --testStat=LHC "
        command +=" --frequentist "+args.input_file+" -T 500 --plot=../plots/limit_combined_hybridnew_HF.pdf --rMin -1 --rMax 10 "
        command +=" --expectedFromGrid "+args.quantile
        if(args.blind=='true'):
            command +=" --fitNuisances=0"
        else:
            command +=" --fitNuisances=1"

        if(args.submit=='true'):
            command +=' --job-mode condor --task-name '+now+'_'+'Combined_v5_yesDPsimplified_500t_'+args.quantile
            #command +=' --job-mode condor --task-name '+now+'_'+categorylist[-1]+'_'+args.quantile+'_noDP'
            command +=' --sub-opts=\'+JobFlavour="nextweek"\nRequestCpus = 4\' '
    if(args.discrete=='true'):
        
        discrete_prof = take_index_dp(categorylist)
        discrete_prof = ','.join(discrete_prof)
        command += " --setParameters "+discrete_prof+" "


        parameter_selection =["bkg_norm_{c}={m},{M}".format(c=categ, m=0, M=1000000) for categ in categorylist]
        #parameter_selection += ["slope_{c}={m},{M}".format(c=categ, m=-1000, M=100) for categ in categorylist]
        parameter_selection += take_paramsel_dp(categorylist)
        parameters_selection  =  ':'.join(parameter_selection)
        command += " --setParameterRanges "+parameters_selection+" "
        ###freeze pdf index?
        paramlist = ["roomultipdf_cat_HF_{c}".format(c=cat) for cat in categorylist]
        paramlist = ','.join(paramlist)
        command += " --freezeParameters "+paramlist+" "
    else:
        parameter_selection = ["bkg_exp_slope_{c}={m},{M}".format(c=categ, m=-1000, M=100) for categ in categorylist]
        parameter_selection +=["bkg_norm_{c}={m},{M}".format(c=categ, m=0, M=1000000) for categ in categorylist]
        parameters_selection  =  ':'.join(parameter_selection)
        command += " --setParameterRanges "+parameters_selection+" "

    print command
    os.system(command)

