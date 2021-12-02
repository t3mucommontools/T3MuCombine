RANGES="\
a0_A17bdt0.991=-100,100:\
a0_B17bdt0.994=-100,100:\
a0_C17bdt0.992=-100,100:\
a0_A18bdt0.995=-100,100:\
a0_B18bdt0.998=-100,100:\
a0_C18bdt0.994=-100,100:\
bkgNorm_A17bdt0.991=0,1000000:\
bkgNorm_B17bdt0.994=0,1000000:\
bkgNorm_C17bdt0.992=0,1000000\
bkgNorm_A18bdt0.995=0,1000000:\
bkgNorm_B18bdt0.998=0,1000000:\
bkgNorm_C18bdt0.994=0,1000000:"

combine -M HybridNew --testStat=LHC --fitNuisances=0 --frequentist ../../workspaces/W/CMS_T3M_13TeV_W_Combined.root -T 5000 --expectedFromGrid 0.5 -C 0.9  --plot='{PDF}/limit_combined_hybridnew_{CL}_WP_{LABEL}.pdf' --rMin 0 --rMax 10 --setParameterRanges $RANGES >> result.txt