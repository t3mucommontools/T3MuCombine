createDataCards.cxx
- reads input TTree (plain ntuples)
- imports wp shapes and parameters from model_card.rs file
- fits bkg and signal shapes
- writes the workspaces
- writes the datacards

inputs to be provided:
- configuration file with format:
```
OutputTree,tripletMass,bdt_cv,category,isMC,weight,dimu_OS1,dimu_OS2
A1,B1,C1,A2,B2,C2,A3,B3,C3
0.9325,0.9525,0.8375,0.7925,0.9025,0.4125,0.2475,0.4575,0.1375
```

First line: comma separated list of names for reading the ntuples
1) name of the TTree in the input file
2) branch name for m(3#mu) variable in GeV
3) branch name for bdt score
4) branch name for mass resolution category (integer, 0:A, 1:B, 2:C)
5) branch name for MC lable (MC==0 is data, MC>0 are signals, no limit on the number of signal samples)
6) branch name for event weight (includes MC normalisation and correction factors, is supposed to be 1 for data)
7) branch name for m(#mu#mu) - first OS pair
8) branch name for m(#mu#mu) - second OS pair

Second line: comma separated list of categories

Third line: comma separated list of bdt values which define the categories (same order must be used)

model_card.rs can be customised based on number of categories and/or channel (threeGlobal, twoGlobalTracker)

example input TTree can be found at:
```
scp -r /afs/cern.ch/user/f/fsimone/public/Tau3mu/inputdata .
``` 

--run argument (2017 or 2018) will affect the systematic uncertainties in the datacards

example call for 9 event categories, threeGlobal channel:
```./run.py -i inputdata/dataset_UL2017_ThreeGlobal_outputTree.root -c model_card_v3.rs --run 2017 --type threeGlobal -v 3 -s config_ThreeGlobal_2017.txt```

```./run.py -i inputdata/dataset_UL2018_ThreeGlobal_outputTree.root -c model_card_v3.rs --run 2018 --type threeGlobal -v 3 -s config_ThreeGlobal_2018.txt```

example call for 6 event categories, twoGlobalTracker:  
```./run.py -i inputdata/dataset_UL2017_TwoGlobalTracker_outputTree.root -c model_card_v2.rs --run 2017 --type twoGlobalTracker -v 2 -s configs/config_TwoGlobalTracker_2017.txt```

```./run.py -i inputdata/dataset_UL2018_TwoGlobalTracker_outputTree.root -c model_card_v2.rs --run 2018 --type twoGlobalTracker -v 2 -s configs/config_TwoGlobalTracker_2018.txt```

