import ROOT
import json
import argparse
parser = argparse.ArgumentParser('''
>> python3 rename_systematics.py --input Run2_workspace.root --output Run2_workspace_legacy.root --maps W_map.json HF_map.json 2016_map.json
''')
parser.add_argument('--input'     , required=True           , help='input .root file containing the workspace')
parser.add_argument('--output'    , required=True           , help='output .root file')
parser.add_argument('--workspace' , default='w'             , help='input workspace name')
parser.add_argument('--maps'      , required=True, nargs='+', help='list of input json file with the name map')

args = parser.parse_args()

ifile   = ROOT.TFile.Open(args.input, "READ")
wspace  = ifile.Get(args.workspace)
jsons   = [json.load(open(m, 'r')) for m in args.maps]

jmap = {}
for j in jsons:
  jmap = {**j, **jmap}

variables = [v.GetName() for v in wspace.allVars()]

for old, new in jmap.items():
  if not old in variables:
    print("WARNING: {} not found in the workspace. Skipping.".format(old))
    continue
  wspace.var(old).SetName(new)
  
ofile = ROOT.TFile.Open(args.output, "RECREATE")
ofile.cd()
wspace.Write()
ofile.Close()
print("{} file created".format(args.output))