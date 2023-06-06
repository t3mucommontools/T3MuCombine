./run.py -i inputdata/T3MMiniTree_xgboost_setting1_2017UL_dmc89.root -s config_xgboost_TwoGlobalTracker_2017.txt -v 2 -t twoGlobalTracker -c model_card_v2.rs -r 2017 -b;
mkdir  plots/2017_twoGlobalTracker_xgb_setting1_multipdf
mkdir  datacards/2017_twoGlobalTracker_xgb_setting1_multipdf
mkdir  workspaces/2017_twoGlobalTracker_xgb_setting1_multipdf

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

mv plots/*png plots/2017_twoGlobalTracker_xgb_setting1_multipdf
mv datacards/*txt datacards/2017_twoGlobalTracker_xgb_setting1_multipdf
mv workspaces/*root workspaces/2017_twoGlobalTracker_xgb_setting1_multipdf
cp -r plots/2017_twoGlobalTracker_xgb_setting1_multipdf /eos/user/b/bjoshi/www/Tau23Mu/Preapproval/
