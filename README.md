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
```
cd CombineHarvester/T3MLimit
```

```
./makeTheCard.py --help for an instruction 
```

(or ```./run.py```  with default root file)







Some documentation:  https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development
https://arxiv.org/pdf/1007.1727.pdf

https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki
