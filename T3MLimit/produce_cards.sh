#! /bin/bash


bdtpoints='-0.1 0 0.05 0.01 0.15 0.2'

for wp in $bdtpoints
    do
    selection='bdt>'$wp
    ./makeTheCard.py --selection=$selection'& category==1 '  --category='A'$wp
    ./makeTheCard.py --selection=$selection'& category==2 '  --category='B'$wp
    ./makeTheCard.py --selection=$selection'& category==3 '  --category='C'$wp
    done
