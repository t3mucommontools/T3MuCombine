for card in BPH_vars_twoGlobalTracker; do
   echo $card
   ./run.py -i inputdata/input_histograms_2017_2glbTrk_$card\.root -c model_card_v2.rs -t twoGlobalTracker -r 2017 > 2017_2glbTrk_$card\.log
   mkdir plots/2017_2glbTrk_$card;
   mv plots/*.png plots/2017_2glbTrk_$card;
   cat datacards/CMS_T3MSignal_13TeV_Combined.txt | grep rate;
   mkdir datacards/2017_2glbTrk_$card;
   cp datacards/CMS_*.txt datacards/2017_2glbTrk_$card;
   cd datacards; ./runLimit.py; cd ..;
   mkdir workspaces/2017_2glbTrk_$card;
   cp workspaces/*.root workspaces/2017_2glbTrk_$card
   rm datacards/*txt
   rm workspaces/*root
done

for card in BPH_vars_threeGlobal; do
   echo $card
   ./run.py -v 3 -i inputdata/datacardT3Mu_dataset_2017_may2021_newPhi_adjSB_v3.root -c model_card_v3.rs -t threeGlobal -r 2017 > 2017_3glb_$card\.log
   mkdir plots/2017_3glb_$card;
   mv plots/*.png plots/2017_3glb_$card;
   cat datacards/CMS_T3MSignal_13TeV_Combined.txt | grep rate;
   mkdir datacards/2017_3glb_$card;
   cp datacards/CMS_*.txt datacards/2017_3glb_$card;
   cd datacards; ./runLimit.py; cd ..;
   mkdir workspaces/2017_3glb_$card;
   cp workspaces/*.root workspaces/2017_3glb_$card
   rm datacards/*txt
   rm workspaces/*root
done
