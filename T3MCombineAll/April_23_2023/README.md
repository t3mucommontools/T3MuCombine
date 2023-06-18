datacards and workspaces created in Combine v9

to run the condor toy generation, use 
```bash
combineTool.py -d CMS_T3MSignal_13TeV_Run2.root \
    -M HybridNew                                  \
    --job-mode condor                             \
    --sub-opts=$T3M_CONDOROPTIONS                 \
    --X-rtd MINIMIZER_freezeDisassociatedParams   \
    --cminDefaultMinimizerStrategy 0              \
    --cl 0.90                                     \
    -m 1.777                                      \
    --generateNuisances=1                         \
    --generateExternalMeasurements=0              \
    --fitNuisances=1                              \
    --testStat LHC                                \
    --clsAcc 0                                    \
    -T $T3M_TOYSPERJOB                            \
    -s -1                                         \
    --singlePoint $T3M_INTERVAL                   \
    --saveHybridResult                            \
    --saveToys                                    \
    --task-name Run2T3M                           \
    --setParameterRanges=\"$Run2\"
```
specifying the number of toys per job, the condor cfg options (if any) and the single point intervals in the form MIN:MAX:STEP.
Each command runs one jobs submmission per point with the specified number of toys. Run as many time as needed to produce a large number of toys.

Merge the result with
```bash
hadd grid.root input_root_files*.root
```
and compute the limit with

```bash
combine -M HybridNew CMS_T3MSignal_13TeV_Run2.root --readHybridResult --grid=grid.root -m 1.777 --expectedFromGrid 0.5 --plot EXP.pdf --cl 0.9 --saveGrid
```
Use fitter.py to extrapolate the limit at a given CL
```bash
python fitter.py --input combine_output.root
```
