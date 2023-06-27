mkdir June_2023/
mkdir June_2023/2018/
mkdir June_2023/2018/tauh/
mkdir June_2023/2018/tauh/datacards/
mkdir June_2023/2018/tauh/workspaces/
mkdir June_2023/2018/tauh/plots/
mkdir June_2023/2018/taumu/
mkdir June_2023/2018/taumu/datacards/
mkdir June_2023/2018/taumu/workspaces/
mkdir June_2023/2018/taumu/plots/
mkdir June_2023/2018/taue/
mkdir June_2023/2018/taue/datacards/
mkdir June_2023/2018/taue/workspaces/
mkdir June_2023/2018/taue/plots/


./run.py -i inputdata/Combine_Tree_ztau3mutau.root -c model_card_ZTT.rs --run 2018 --type threeGlobal -v 2 -s configs/config_ZTT_tauh_2018.txt 2>&1 | tee out.log
cd datacards/
combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt > CMS_T3MSignal_13TeV_Combined.txt
cd ../
cp -r datacards/*.txt June_2023/2018/tauh/datacards/
cp -r workspaces/*.root June_2023/2018/tauh/workspaces/
cp threeGlobal_2018_yields.txt June_2023/2018/tauh/
cp -r plots/*.png June_2023/2018/tauh/plots/

./run.py -i inputdata/Combine_Tree_ztau3mutau.root -c model_card_ZTT.rs --run 2018 --type threeGlobal -v 2 -s configs/config_ZTT_taumu_2018.txt 2>&1 | tee out.log
cd datacards/
combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt > CMS_T3MSignal_13TeV_Combined.txt
cd ../
cp -r datacards/*.txt June_2023/2018/taumu/datacards/
cp -r workspaces/*.root June_2023/2018/taumu/workspaces/
cp threeGlobal_2018_yields.txt June_2023/2018/taumu/
cp -r plots/*.png June_2023/2018/taumu/plots/

./run.py -i inputdata/Combine_Tree_ztau3mutau.root -c model_card_ZTT.rs --run 2018 --type threeGlobal -v 2 -s configs/config_ZTT_taue_2018.txt 2>&1 | tee out.log
cd datacards/
combineCards.py CMS_T3MSignal_13TeV_A1.txt CMS_T3MSignal_13TeV_A2.txt > CMS_T3MSignal_13TeV_Combined.txt
cd ../
cp -r datacards/*.txt June_2023/2018/taue/datacards/
cp -r workspaces/*.root June_2023/2018/taue/workspaces/
cp threeGlobal_2018_yields.txt June_2023/2018/taue/
cp -r plots/*.png June_2023/2018/taue/plots/