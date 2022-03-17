from __future__ import print_function
import os
import sys
import argparse
parser = argparse.ArgumentParser('''
This script runs the following checks on the specified datacard:
- impact computation
- significance estimation for discovery (with toys)
- significance estimation for discovery (with asymptitic formulae)
Details of the commands in the code.''')
parser.add_argument('-d', '--datacard', required=True           , help='path to the combine datacard to open' )
parser.add_argument('-p', '--pranges' , default=''              , help='parameter ranges to use in the form "par1=min,max:par2=min,max"')
parser.add_argument('-e', '--expected', default='0'             , help='expected signal strength for the Asimov generation')
parser.add_argument('-l', '--label'   , default='combine_checks', help='used to label the output directory')
parser.add_argument('-r', '--rmin'    , default='0'             , help='lower boundary for r')
parser.add_argument('-R', '--rmax'    , default='10'            , help='higher boundary for r')
parser.add_argument('-t', '--toys'    , default='1000'          , help='toys to use to compute the significance')
parser.add_argument('-U', '--unblind' , action='store_true'     , help='run unblinded tests')
parser.add_argument('-L', '--log'     , action='store_true'     , help='store stdout and stderr in log files instead of printing them')
parser.add_argument('-I', '--impacts' , action='store_true'     , help='run the impacts computation')
parser.add_argument('-A', '--sig-asym', action='store_true'     , help='run the significance computation using asymptotic formulae')
parser.add_argument('-T', '--sig-toys', action='store_true'     , help='run the significance computation using toys')

args = parser.parse_args()

class Command:
  WARNING = lambda self, msg: print("\033[93m[WARNING] "+ msg + "\033[0m")
  ERROR   = lambda self, msg: print("\033[91m[ERROR] "  + msg + "\033[0m")
  INFO    = lambda self, msg: print("\033[92m[INFO]  "  + msg + "\033[0m")
  CODE    = lambda self, msg: print("\033[95m" + msg + "\033[0m")
  def __init__(self, name, commands, output):
    self.n = name
    self.o = output
    self.c = commands
    self.w = os.getcwd()
    self.f = False  #failed
  
  def run(self, runme=True):
    if not runme: return

    self.INFO("running task {}".format(self.n))
    self.INFO("the output directory is")
    print(self.o)

    if not os.path.exists(self.o):
      os.makedirs(self.o)

    os.chdir(self.o)
    for i, cmd in enumerate(self.c):
      cmd = cmd+'>{X} {O}/LOGFILE.txt'.format(X='>' if i>0 or args.log else '', O=self.o) if args.log else cmd

      self.CODE(">> "+cmd)
      if args.log:
        self.INFO("logging stdout and stderr into")
        print(self.o+'/LOGFILE.txt')

      if args.log:
        os.system('echo \>\> %s\n' %cmd)
      ret = os.system(cmd)
      if ret:
        self.ERROR("an error was encountered when running the last command")
        self.f = True
    
    if self.f:
      self.WARNING("the {} task encountered some errors".format(self.n))
    else:
      self.INFO("task {} run succesfully".format(self.n))
    os.chdir(self.w)

DATACARD   = os.path.abspath(args.datacard)
WORKSPACE  = os.path.basename(args.datacard).replace('.txt', '.root')
PARAMETERS = '--setParameterRanges '+args.pranges if args.pranges!='' else ''
BLINDER    = '-t -1 --expectSignal {EXP}'.format(EXP=args.expected) if not args.unblind else ''

OUTPUT = os.path.abspath('_'.join([args.label, 'rMin'+args.rmin, 'rMax'+args.rmax]+['unblinded' if args.unblind else 'rAsimov'+args.expected]))
OUTPUT_IMPACTS  = OUTPUT+'/impacts'
OUTPUT_SIG_TOYS = OUTPUT+'/significance_toys'
OUTPUT_SIG_ASYM = OUTPUT+'/significance_asymptitic'

CMD_IMPACTS = '\n'.join([
  'combine -M FitDiagnostics -d {DAT} {B} --plots --rMin "{r}" --rMax "{R}" --minos all {PAR}',
  'python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics.root -g plots.root',
  'text2workspace.py {DAT} -m 1.777 -o {WSP}',
  'combineTool.py -M Impacts -d {WSP} -m 1.777 {B} --doInitialFit --robustFit=1 --rMin "{r}" --rMax "{R}"',
  'combineTool.py -M Impacts -d {WSP} -m 1.777 {B} --doFits --parallel 5 --rMin "{r}" --rMax "{R}"',
  'combineTool.py -M Impacts -d {WSP} -m 1.777 {B} --rMin "{r}" --rMax "{R}" -o impacts.json',
  'plotImpacts.py -i impacts.json -o impacts',
]).format(
  DAT=DATACARD      ,
  EXP=args.expected ,
  r  =args.rmin     ,
  R  =args.rmax     ,
  RAN=args.pranges  ,
  WSP=WORKSPACE     ,
  PAR=PARAMETERS    ,
  B  =BLINDER       ,
).split('\n')

CMD_SIGNIFICANCE_TOYS = ' && '.join([
  'combine -M HybridNew -d {DAT} --LHCmode LHC-significance --saveToys --fullBToys --saveHybridResult  -T {T} {PAR}',
]).format(
  T  =args.toys ,
  DAT=DATACARD  ,
  PAR=PARAMETERS,
).split('\n')

CMD_SIGNIFICANCE_ASYM = ' && '.join([
  'combine -M Significance -d {DAT}',
]).format(
  DAT=DATACARD
).split('\n')

impacts_cmd  = Command('Impacts'                , CMD_IMPACTS           , OUTPUT_IMPACTS ).run(args.impacts )
sig_asym_cmd = Command('Asymptotic significance', CMD_SIGNIFICANCE_ASYM , OUTPUT_SIG_ASYM).run(args.sig_asym)
sig_toys_cmd = Command('Toys significance'      , CMD_SIGNIFICANCE_TOYS , OUTPUT_SIG_TOYS).run(args.sig_toys)