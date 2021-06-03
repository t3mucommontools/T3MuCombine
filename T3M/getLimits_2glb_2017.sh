for card in BPH_vars_twoGlobalTracker; do
   echo $card
   ./run.py -i inputdata/input_histograms_2glbTrk_$card\.root -c model_card_twoGlobalTracker.rs -t twoGlobalTracker -r 2017 > 2017_2glbTrk_$card\.log 
   mkdir plots/2017_2glbTrk_$card;
   mv plots/*.png plots/2017_2glbTrk_$card;
   cat datacards/CMS_T3MSignal_13TeV_Combined.txt | grep rate;
   mkdir datacards/2017_2glbTrk_$card;
   cp datacards/CMS_*.txt datacards/2017_2glbTrk_$card;
   cd datacards; ./runLimit.py; cd ..;
   mkdir workspaces/2017_2glbTrk_$card;
   cp workspaces/*.root workspaces/2017_2glbTrk_$card
done
