# T3MuCombine

# Installing combine code for T3Mu analysis
```
 git clone git@github.com:t3mucommontools/T3MuCombine.git
``` 

The script setupCombine.pl will clone and compile HiggsAnalysisTools and CombineHarvester. 
Run ./setupCombine.pl  for an instruction

Please find information on latest releases here: https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/

```sh 
./setupCombine.pl --help
```

There is just one option to it --Combine, do:

```sh
./setupCombine --Combine MyWorkDir
```
This will produce text file that you need to source to setup everything (just pay attention to the instruction on your screen)


The following settings will be used by default:

    SCRAM_ARCH=slc7_amd64_gcc700
    CMSSW_11_3_4


# Creating Datacards for T3Mu analysis
After compilation:
```
cd /MyWorkDir/CMSSW_11_3_4/src/CombineHarvester/
```
And choose your working area; The place for combining all categories is /MyWorkDir/CMSSW_11_3_4/src/CombineHarvester/T3MCombineAll



For UF people: the working area is T3MLimit
```
./makeTheCard.py --help for an instruction 
```

(or ```./run.py```  with default root file)



# Running limits with toys and hybrid-bayesian

1) Run ```text2workspace.py``` with --X-assign-flatParam-prior flag 

```ssh
text2workspace.py mydatacard.txt -o myworkspace.root --X-assign-flatParam-prior
```

2) [Recommended] Define reasonable ranges for all ranges in your datacard. Suggestion: use a script like ```python/generate_ranges_sh.py``` to define a list of parameter ranges (e.g. ```$RUN2_PARS```).

3) Run the limit. Note: the option ```MINIMIZER_freezeDisassociatedParams``` is required if you have discrete parameters in your datacards.

```ssh
combineTool.py -d myworkspace.root -M HybridNew --setParameterRanges $RUN2_PARS --rMin=-5 --rMax 10 --X-rtd MINIMIZER_freezeDisassociatedParams --cminDefaultMinimizerStrategy 0 --cl 0.90 -m 1.777 --generateNuisances=1 --generateExternalMeasurements=0 --fitNuisances=1 --testStat LHC
```

# Produce toys using condor/CRAB
see: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/runningthetool/#combinetool-for-job-submission
Example in ```T3MCombineAll/April_23_2023```


# Docs
https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki
http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/

