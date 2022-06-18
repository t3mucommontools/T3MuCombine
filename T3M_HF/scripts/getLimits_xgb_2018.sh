./run.py -i inputdata/T3MMiniTree_xgboost_setting1_2018UL.root -s config_xgboost_TwoGlobalTracker_2018.txt -v 2 -t twoGlobalTracker -c model_card_v2.rs -r 2018 -b;
mkdir  plots/2018_twoGlobalTracker_xgb_setting1
mkdir  datacards/2018_twoGlobalTracker_xgb_setting1
mkdir  workspaces/2018_twoGlobalTracker_xgb_setting1

'''
cd datacards/;
echo "==================================="
echo "         Printing Limits           "
echo "==================================="

echo "-----------------------------------"
echo "            Combined               "
echo "-----------------------------------"
./runLimit.py -i CMS_T3MSignal_13TeV_Combined.txt

for cat in A B C; do
   for sub in 1 2; do
      echo "-----------------------------------"
      echo "               ${cat}${sub}                  "
      echo "-----------------------------------"
      ./runLimit.py -i CMS_T3MSignal_13TeV_${cat}${sub}.txt
   done
done

cd -;
'''
mv plots/*png plots/2018_twoGlobalTracker_xgb_setting1
mv datacards/*txt datacards/2018_twoGlobalTracker_xgb_setting1
mv workspaces/*root workspaces/2018_twoGlobalTracker_xgb_setting1
cp -r plots/2018_twoGlobalTracker_xgb_setting1 /eos/user/b/bjoshi/www/Tau23Mu/Preapproval/
