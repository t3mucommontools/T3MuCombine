#! /bin/bash


bdtA1='0.171'
bdtA2='0.102'
bdtB1='0.205'
bdtB2='0.118'
bdtC1='0.219'
bdtC2='0.120'

#phivetoes='(abs(m12-1.020)>0.025)&(abs(m13-1.020)>0.025)'  # phi mass veto
#omegavetoes='&abs(m12-0.782)>0.04&fabs(m13-0.782)>0.04&'   # omega mass veto

phivetoes='((m12<0.96|m12>1.07)&(m13<0.96|m13>1.07))'  # phi mass veto
omegavetoes='&((m12<0.77|m12>0.812)&(m12<0.76|m12>0.812))&'   # omega mass veto

#phivetoes=''  # phi mass veto
#omegavetoes=''   # omega mass veto



./makeTheCard.py --selection=$phivetoes$omegavetoes'bdt >'$bdtA1'& category==1 '                  --category='V2018A1' --varset="TrainWoVetosWithMass"  --datafile T3MMiniTree_train_wo_vetos_withmasses.root
./makeTheCard.py --selection=$phivetoes$omegavetoes'bdt >'$bdtA2'&bdt<'$bdtA1'& category==1 '     --category='V2018A2' --varset="TrainWoVetosWithMass"  --datafile T3MMiniTree_train_wo_vetos_withmasses.root
./makeTheCard.py --selection=$phivetoes$omegavetoes'bdt >'$bdtB1'& category==2 '                  --category='V2018B1' --varset="TrainWoVetosWithMass"  --datafile T3MMiniTree_train_wo_vetos_withmasses.root
./makeTheCard.py --selection=$phivetoes$omegavetoes'bdt >'$bdtB2'&bdt<'$bdtB1'& category==2 '     --category='V2018B2' --varset="TrainWoVetosWithMass"  --datafile T3MMiniTree_train_wo_vetos_withmasses.root
./makeTheCard.py --selection=$phivetoes$omegavetoes'bdt >'$bdtC1'& category==3 '                  --category='V2018C1' --varset="TrainWoVetosWithMass"  --datafile T3MMiniTree_train_wo_vetos_withmasses.root
./makeTheCard.py --selection=$phivetoes$omegavetoes'bdt >'$bdtC2'&bdt<'$bdtC1'& category==3 '     --category='V2018C2' --varset="TrainWoVetosWithMass"  --datafile T3MMiniTree_train_wo_vetos_withmasses.root


