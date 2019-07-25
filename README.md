# T3MuCombine

# Creating Datacards for T3Mu analysis
```
 git clone git@github.com:t3mucommontools/T3MuCombine.git
``` 

The script setupCombine.pl will clone and compile HiggsAnalysisTools and CombineHarvester. 
Run ./setupCombine.pl  for an instruction




The following settings will be used by default:

    SCRAM_ARCH=slc6_amd64_gcc530	
    CMSSW_8_1_0	


After compilation:

cd CombineHarvester/T3M

 combineTool.py -M T2W -o workspace.root -i datacard.dat

 combineTool.py -M AsymptoticLimits -d workspace.root



The script writedatacard.py suppose to create data cards automatically by CombineHarvester by running: 

./writedatacard.py -i inputdata/input_histograms.root

However, something is not right, the Harvester is happy with this script and gives a meaninfull print out, but no actual data card is produced (to be fixed)


Some documentation:  https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development
