# I don't get the toy splitting done by combine, but this command follows the twiki prescription
# http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/#observed-significance
HERE=$PWD
WDIR=teststat_dist
CARD=/gwpool/users/lguzzi/Tau3Mu/2017_2018/combine_test/T3MuCombine/T3MCombineAll/August_18_2022/datacards/CMS_T3MSignal_13TeV_Combined_2017_2018.txt
mkdir $WDIR
cd $WDIR
ln -s $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/plotTestStatCLs.py .
for n in {1..100}; do
  echo $n
  echo ">> combine $CARD -M HybridNew --LHCmode "LHC-limits" --singlePoint 1 --saveToys --saveHybridResult -T 1000 --clsAcc 0 --setParameterRanges $WPARS:$HFPARS --freezeParameters $HFFROZEN -s -1 --expectSignal 1 --expectedFromGrid=0.5 > job_$n.txt 2>&1"
  echo ""
  combine $CARD -M HybridNew --LHCmode "LHC-limits" --singlePoint 1 --saveToys --saveHybridResult -T 1000 --clsAcc 0 --setParameterRanges \"$WPARS:$HFPARS\" --freezeParameters \"$HFFROZEN\" -s -1 --expectSignal 1 --expectedFromGrid=0.5 > job_$n.txt 2>&1
done

hadd grid.root *.root 
python plotTestStatCLs.py --input grid.root --poi r --val all --mass 120 -E -q 0.5
cd $HERE