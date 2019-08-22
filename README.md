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

 combineTool.py -M T2W -o workspace.root -i outcard.dat

 combineTool.py -M AsymptoticLimits -d workspace.root


To create the datacard use writedatacard.py

./writedatacard.py -i inputdata/input_histograms.root

So far it creates a dummy card out of dummy distributions in input_histograms.root.


Some documentation:  https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development
