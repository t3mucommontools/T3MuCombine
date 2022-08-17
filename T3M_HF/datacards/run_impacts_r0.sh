RANGES="\
bkg_exp_slope_A1=-1000,1000:\
bkg_exp_slope_A2=-1000,1000:\
bkg_exp_slope_A3=-1000,1000:\
bkg_exp_slope_B1=-1000,1000:\
bkg_exp_slope_B2=-1000,1000:\
bkg_exp_slope_B3=-1000,1000:\
bkg_exp_slope_C1=-1000,1000:\
bkg_exp_slope_C2=-1000,1000:\
bkg_exp_slope_C3=-1000,1000"

echo "Run FitDiagnostics"
echo "combine -M FitDiagnostics -t -1 --expectSignal 0 -d CMS_T3MSignal_13TeV_Combined.txt --plots --rMin -1 --rMax 10 --setParameterRanges \"$RANGES\" --minos all -v 3"
combine -M FitDiagnostics -t -1 --expectSignal 0 -d CMS_T3MSignal_13TeV_Combined.txt --plots --rMin -1 --rMax 10 --setParameterRanges \"$RANGES\" --minos all -v 3 > fitDiagnostics_r0.txt 2>&1
sleep 1

echo "Compute diffNuisances"
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnosticsTest.root -g plots_r0.root
sleep 1

echo "Do initial fits"
combineTool.py -M Impacts \
-d workspace.root \
-m 1.777 \
--cminDefaultMinimizerPrecision 0.00000001 \
--doInitialFit \
--rMin -1 --rMax 10 \
-t -1 --expectSignal 0 --saveToys \
--setParameterRanges \"$RANGES\" \
--robustFit 1
sleep 1

#bug fix
scp higgsCombine_initialFit_Test.MultiDimFit.mH1.777.123456.root higgsCombine_initialFit_Test.MultiDimFit.mH1.777.root
sleep 1

echo "Fit the nuisances"
combineTool.py -M Impacts \
-d workspace.root \
-m 1.777 \
--cminDefaultMinimizerPrecision 0.00000001 \
--doFits \
--rMin -1 --rMax 10 \
-t -1 --expectSignal 0 \
--setParameterRanges \"$RANGES\" \
--robustFit 1 \
--parallel 10
sleep 1

echo "Collect outputs"
combineTool.py -M Impacts -d workspace.root -m 1.777 -t -1 --expectSignal 0 -o impacts_r0.json --cminDefaultMinimizerPrecision 0.00000001
sleep 1

echo "Plot"
plotImpacts.py -i impacts_r0.json -o impacts_r0 --per-page 11
