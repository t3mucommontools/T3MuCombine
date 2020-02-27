#! /bin/bash


datacard='datacards/CMS_T3MSignal_13TeV_A0.15.txt'

echo 'computing the 95% limit'
combineTool.py -M AsymptoticLimits  --run blind  -d  $datacard

    
