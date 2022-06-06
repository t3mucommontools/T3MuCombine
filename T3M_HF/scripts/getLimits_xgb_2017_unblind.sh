./run.py -i inputdata/T3MMiniTree_xgboost_setting1_2018UL.root -s config_xgboost_TwoGlobalTracker_2018.txt -v 2 -t twoGlobalTracker -c model_card_v2.rs -r 2018;
mkdir  plots/2018_twoGlobalTracker_xgb_setting1_unblinded
mv plots/*png plots/2018_twoGlobalTracker_xgb_setting1_unblinded
mv datacards/*txt datacards/2018_twoGlobalTracker_xgb_setting1_unblinded
cp -r plots/2018_twoGlobalTracker_xgb_setting1_unblinded /eos/user/b/bjoshi/www/Tau23Mu/Preapproval/
