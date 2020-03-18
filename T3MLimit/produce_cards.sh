#! /bin/bash


bdtpoints='-0.2 -0.15 -0.05 -0.04 -0.03 -0.02 -0.01 0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.11 0.12 0.13 0.14  0.15 0.16 0.17 0.18 0.19  0.2 0.21 0.22 0.23 0.24 0.25 0.26 0.27 0.28'

for wp in $bdtpoints
    do
    selection='bdt>'$wp
    ./makeTheCard.py --selection=$selection'& category==1 '  --category='Var2016A'$wp --datafile T3MMiniTree2016Vars.root
    ./makeTheCard.py --selection=$selection'& category==2 '  --category='Var2016B'$wp --datafile T3MMiniTree2016Vars.root
    ./makeTheCard.py --selection=$selection'& category==3 '  --category='Var2016C'$wp --datafile T3MMiniTree2016Vars.root
    done
