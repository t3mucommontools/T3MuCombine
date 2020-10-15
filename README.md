# T3MuCombine

# Creating Datacards for T3Mu analysis
```
 git clone git@github.com:t3mucommontools/T3MuCombine.git
``` 

The script setupCombine.pl will clone and compile HiggsAnalysisTools and CombineHarvester. 
Run ./setupCombine.pl  for an instruction


```sh 
./setupCombine.pl --help
```

There is just one option to it --Combine, do:

```sh
./setupCombine --Combine MyWorkDir
```
This will produce text file that you need to source to setup everything (just pay attention to the instruction on your screen)


The following settings will be used by default:

    SCRAM_ARCH=slc6_amd64_gcc530	
    CMSSW_8_1_0	


After compilation:
```
cd /MyWorkDir/CMSSW_8_1_0/src/CombineHarvester/
```
And choose your working area; The place for combining all categories is /MyWorkDir/CMSSW_8_1_0/src/CombineHarvester/T3MCombineAll



For UF people: the working area is T3MLimit
```
./makeTheCard.py --help for an instruction 
```

(or ```./run.py```  with default root file)







Some documentation:  https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development
https://arxiv.org/pdf/1007.1727.pdf

https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki
