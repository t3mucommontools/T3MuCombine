#! /bin/bash


bdtpoints='-0.2 -0.15 -0.05 -0.04 -0.03 -0.02 -0.01 0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.11 0.12 0.13 0.14 0.15 0.16 0.17'


wpA='0.07'
wpB='0.11'
wpC='0.18'
phivetoes='&(abs(m12-1.020)>0.025)&(abs(m13-1.020)>0.025)'
omegavetoes='&abs(m12-0.782)>0.04&fabs(m13-1.020)>0.04'


for wp in $bdtpoints
    do

    selection='bdt>'$wp$phivetoes$omegavetoes
#    selectionA=$selection'
#    selectionB=$selection'& bdt<'B
#    selectionC=$selection'& bdt<'$wpC

#    ./makeTheCard.py --selection=$selection'& category==1 &bdt <'$wpA  --category='Var2016ASubCategoryA'$wp  --varset="Vars2016"  --datafile T3MMiniTree2016Vars.root
#    ./makeTheCard.py --selection=$selection'& category==2 &bdt<'$wpB  --category='Var2016ASubCategoryB'$wp  --varset="Vars2016"  --datafile T3MMiniTree2016Vars.root
    ./makeTheCard.py --selection=$selection'& category==3 &bdt<'$wpC  --category='Var2016ASubCategoryC'$wp  --varset="Vars2016"   --datafile T3MMiniTree2016Vars.root
    done
