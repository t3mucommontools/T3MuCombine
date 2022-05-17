#!/usr/bin/env python

import os
import argparse
import ROOT
from ROOT import TFile
import math
import array
import subprocess
from itertools import product
import numpy

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--maxjobs'  , default = 5       , type = int)
parser.add_argument('--category' , default = 'B'        , type = str)
parser.add_argument('--outdir'   , default = 'scan_result', type = str)
parser.add_argument('--workdir'  , default = './', type = str)
parser.add_argument('--verbose'  , action = 'store_true')


COMBINE_CMD = 'combineCards.py {IN} > {OUT}'
RUN_COMBINE_ASYMPTOTIC_CMD = 'combineTool.py -M AsymptoticLimits  --run blind  -d  {CARD} --cl {CL} | grep "50.0%:" > "{RES}/limit_combined_asymptotic_CL_{CL}_WP_{LABEL}.txt"'
CMD = './run.py -i inputdata/dataset_UL2018_ThreeGlobal_outputTree.root -c model_card_v3.rs --run 2018 --type threeGlobal -v 3 -s {CONFIG}'

task_queue = []

DataCardsToCombine = []
args = parser.parse_args()
os.system('mkdir %s' %args.outdir)




def run_combined_datacards(list_of_cards):
    inputs = ''
    for sublist in list_of_cards:
        output_datacard = '/'.join([args.outdir,'Combined'+ sublist[0][45:-12]+args.category+'.txt'])
        inputs = ' '.join(sublist)
        os.system(COMBINE_CMD.format(IN = inputs, OUT = output_datacard))    
        os.system(RUN_COMBINE_ASYMPTOTIC_CMD.format(CL = 0.9, CARD = output_datacard, RES=args.outdir,LABEL=sublist[0][45:-12]+args.category))



sub_category_1 = numpy.arange(0.05,0.26,0.06)
sub_category_2 = numpy.arange(0.05,0.26,0.06)
sub_category_3 = numpy.arange(0.05,0.26,0.06)



for first, second, third in product(sub_category_1,sub_category_2, sub_category_3):
        if first >  second and first > third and second > third:
                CNFG_NAME = 'scan_config_cat%s_range_%.4f_%.4f_%.4f.txt' %(args.category,first, second, third)
                print CNFG_NAME
                with open(CNFG_NAME,'w') as scan_config_file:
                    if args.category=='A':
                        scan_config_file.write(
'''outputTree,tripletMass,bdt,category,isMC,weight
A1,B1,C1,A2,B2,C2,A3,B3,C3
{A1:.4f},0.2125,0.2475,{A2:.4f},0.1525,0.1925,{A3:.4f},0.0625,0.1125
'''.format(A1=first,A2=second,A3=third))

                    if args.category=='B':
                        scan_config_file.write(
'''outputTree,tripletMass,bdt,category,isMC,weight
A1,B1,C1,A2,B2,C2,A3,B3,C3
0.21168,{A1:.4f},0.2475,0.12208,{A2:.4f},0.1925,0.0575,{A3:.4f},0.1125
'''.format(A1=first,A2=second,A3=third))


                    if args.category=='C':
                        scan_config_file.write(
'''outputTree,tripletMass,bdt,category,isMC,weight
A1,B1,C1,A2,B2,C2,A3,B3,C3
0.21168,0.2125,{A1:.4f},0.12208,0.1525,{A2:.4f},0.0575,0.0625,{A3:.4f}
'''.format(A1=first,A2=second,A3=third))




                task_queue.append(CMD.format(CONFIG = CNFG_NAME))
                schedule   = [' & '.join(task_queue[jj:jj+args.maxjobs]) for jj in range(0, len(task_queue), args.maxjobs)]
                datacards=['datacards/CMS_T3MSignal'+CNFG_NAME[:-4]+'_13TeV_'+args.category+'1.txt','datacards/CMS_T3MSignal'+CNFG_NAME[:-4]+'_13TeV_'+args.category+'2.txt','datacards/CMS_T3MSignal'+CNFG_NAME[:-4]+'_13TeV_'+args.category+'3.txt']
                DataCardsToCombine.append(datacards)




for sch in schedule: 
    print '>>', sch
    process = subprocess.Popen(sch, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE) if not args.verbose else subprocess.Popen(sch, shell = True)
    stdout, stderr = process.communicate() 
    print stdout, '\n', stderr if args.verbose else stderr


run_combined_datacards(DataCardsToCombine)
os.system('rm scan_config_cat*')

print '[INFO] all processes ended'

results = os.listdir(args.outdir)
listof=[]
rdict = {}
for res in os.listdir(args.outdir): 
    if 'limit_combined_asymptotic' in res:
        limfile = open(args.outdir+'/'+res, 'r')
        line = limfile.readlines()
        line[0].strip()
        rdict[res] = float(line[0].split("<")[1][:-2])
        print  line[0].split("<")[1][:-2]

sorteddict =  sorted(rdict.items(), key=lambda x: x[1]) 
print sorteddict

