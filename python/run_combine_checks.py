from __future__ import print_function
import os
import sys
import argparse
parser = argparse.ArgumentParser('''
This script runs the following checks on the specified datacard:
- impact computation
- significance estimation for discovery (with toys)
- significance estimation for discovery (with asymptitic formulae)
- upper limits
- log-likelihood profiles vs. parameters
Details of the commands in the code.''')
parser.add_argument('-d', '--datacard', required=True           , help='path to the combine datacard to open' )
parser.add_argument('-p', '--pranges' , default=''              , help='parameter ranges to use in the form "par1=min,max:par2=min,max"')
parser.add_argument('-e', '--expected', default='0'             , help='expected signal strength for the Asimov generation')
parser.add_argument('-l', '--label'   , default='combine_checks', help='used to label the output directory')
parser.add_argument('-r', '--rmin'    , default='0'             , help='lower boundary for r')
parser.add_argument('-R', '--rmax'    , default='10'            , help='higher boundary for r')
parser.add_argument('-t', '--toys'    , default='10000'         , help='toys to use to compute the significance or the upper limit')
parser.add_argument('-U', '--unblind' , action='store_true'     , help='run unblinded tests')
parser.add_argument(      '--log'     , action='store_true'     , help='store stdout and stderr in log files instead of printing them')
parser.add_argument('-I', '--impacts' , action='store_true'     , help='run the impacts computation')
parser.add_argument('-A', '--sig-asym', action='store_true'     , help='run the significance computation using asymptotic formulae')
parser.add_argument('-T', '--sig-toys', action='store_true'     , help='run the significance computation using toys')
parser.add_argument('-L', '--lhscan'  , action='store_true'     , help='run the likelihood scan')
parser.add_argument(      '--lhparams', default='r'             , help='parameters to run the likelihood scan in the form "par1 par2 par3"')
parser.add_argument(      '--limit'   , action='store_true'     , help='run the upper limit with toys')
parser.add_argument(      '--cl'      , default='0.9'           , help='confidence level used for the upper limit')
parser.add_argument(      '--grid'    , default='0.5'           , help='quantile considered for the upper limit computation')

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
PARAMETERS = '--setParameterRanges "{}"'.format(args.pranges) if args.pranges!='' else ''
BLINDER    = '-t -1 --expectSignal {EXP}'.format(EXP=args.expected) if not args.unblind else ''

OUTPUT = os.path.abspath('_'.join([args.label, 'rMin'+args.rmin, 'rMax'+args.rmax]+['unblinded' if args.unblind else 'rAsimov'+args.expected]))
OUTPUT_IMPACTS  = OUTPUT+'/impacts'
OUTPUT_SIG_TOYS = OUTPUT+'/significance_toys'
OUTPUT_SIG_ASYM = OUTPUT+'/significance_asymptotic'
OUTPUT_LHSCAN   = OUTPUT+'/lh_scan'
OUTPUT_LIMIT    = '_'.join([OUTPUT+'/limit', 'CL'+args.cl, 'grid'+args.grid.replace('.','p')])

CMD_IMPACTS = '\n'.join([
  'combine -M FitDiagnostics -d {DAT} {B} --plots --rMin "{r}" --rMax "{R}" --minos all {PAR}',
  'python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics.root -g plots.root',
  'text2workspace.py {DAT} -m 1.777 -o {WSP} -D data_obs',
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

CMD_SIGNIFICANCE_TOYS = '\n'.join([
  'combine -M HybridNew -d {DAT} --LHCmode LHC-significance --saveToys --fullBToys --saveHybridResult  -T {T} {PAR}',
]).format(
  T  =args.toys ,
  DAT=DATACARD  ,
  PAR=PARAMETERS,
).split('\n')

CMD_SIGNIFICANCE_ASYM = '\n'.join([
  'combine -M Significance -d {DAT}',
]).format(
  DAT=DATACARD
).split('\n')

CMD_LHSCAN = '\n'.join([
  'text2workspace.py {DAT} -m 1.777 -o {WSP} -D data_obs',
  'for nui in {NUI}; do \
    echo scanning $nui;\
    combine {WSP} -M MultiDimFit --algo grid --points 20 {PAR} -m 1.777 --rMin "{r}" --rMax "{R}" -P $nui -n scan_$nui;\
    plot1DScan.py higgsCombinescan_$nui.MultiDimFit.mH1.777.root --POI  \"$nui\" --output plot_$nui;\
  done'
]).format(
  DAT=DATACARD  ,
  WSP=WORKSPACE ,
  PAR=PARAMETERS,
  r  =args.rmin ,
  R  =args.rmax ,
  NUI=args.lhparams,
).split('\n')

CMD_LIMIT = '\n'.join([
  'text2workspace.py {DAT} -m 1.777 -o {WSP} -D data_obs',
  "combine -M HybridNew --testStat=LHC --fitNuisances={BLI} --frequentist {WSP} -T {TOY} --expectedFromGrid {CI} -C {CL}  --plot='limit_combined_hybridnew_{CL}.pdf' --rMin {r} --rMax {R} {PAR}"
]).format(
  DAT=DATACARD ,
  WSP=WORKSPACE,
  TOY=args.toys,
  CI =args.grid,
  CL =args.cl  ,
  r  =args.rmin,
  R  =args.rmax,
  PAR=PARAMETERS,
  BLI=1 if args.unblind else 0,
).split('\n')

impacts_cmd  = Command('Impacts'                , CMD_IMPACTS           , OUTPUT_IMPACTS ).run(args.impacts )
sig_asym_cmd = Command('Asymptotic significance', CMD_SIGNIFICANCE_ASYM , OUTPUT_SIG_ASYM).run(args.sig_asym)
sig_toys_cmd = Command('Toys significance'      , CMD_SIGNIFICANCE_TOYS , OUTPUT_SIG_TOYS).run(args.sig_toys)
lhscan_cmd   = Command('LHScan'                 , CMD_LHSCAN            , OUTPUT_LHSCAN  ).run(args.lhscan  )
lhscan_cmd   = Command('Upper limit'            , CMD_LIMIT             , OUTPUT_LIMIT   ).run(args.limit   )