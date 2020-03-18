#! /bin/bash


bdtA1='0.161179'
bdtA2='0.0739935'
bdtB1='0.182393'
bdtB2='0.0791633'
bdtC1='0.165342'
bdtC2='0.0566122'


./makeTheCard.py --selection='bdt >'$bdtA1'& category==1 '                  --category='2016A1'$wp   --datafile T3MMiniTree2016Vars.root
./makeTheCard.py --selection='bdt >'$bdtA2'&bdt<'$bdtA1'& category==1 '     --category='2016A2'$wp   --datafile T3MMiniTree2016Vars.root
./makeTheCard.py --selection='bdt >'$bdtB1'& category==2 '                  --category='2016B1'$wp   --datafile T3MMiniTree2016Vars.root
./makeTheCard.py --selection='bdt >'$bdtB2'&bdt<'$bdtB1'& category==2 '     --category='2016B2'$wp   --datafile T3MMiniTree2016Vars.root
./makeTheCard.py --selection='bdt >'$bdtC1'& category==3 '                  --category='2016C1'$wp   --datafile T3MMiniTree2016Vars.root
./makeTheCard.py --selection='bdt >'$bdtC2'&bdt<'$bdtC1'& category==3 '     --category='2016C2'$wp   --datafile T3MMiniTree2016Vars.root


