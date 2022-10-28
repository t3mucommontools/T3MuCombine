export SIG_A17="\
HLT_Mu_A17=-5,5:\
HLT_TkMu_A17=-5,5:\
mc_stat_A17=-5,5:\
muonID_A17=-5,5"
export SIG_A18="\
HLT_Mu_A18=-5,5:\
HLT_TkMu_A18=-5,5:\
mc_stat_A18=-5,5:\
muonID_A18=-5,5"
export SIG_B17="\
HLT_Mu_B17=-5,5:\
HLT_TkMu_B17=-5,5:\
mc_stat_B17=-5,5:\
muonID_B17=-5,5"
export SIG_B18="\
HLT_Mu_B18=-5,5:\
HLT_TkMu_B18=-5,5:\
mc_stat_B18=-5,5:\
muonID_B18=-5,5"
export SIG_C17="\
HLT_Mu_C17=-5,5:\
HLT_TkMu_C17=-5,5:\
mc_stat_C17=-5,5:\
muonID_C17=-5,5"
export SIG_C18="\
HLT_Mu_C18=-5,5:\
HLT_TkMu_C18=-5,5:\
mc_stat_C18=-5,5:\
muonID_C18=-5,5"
export SIG_COMMON="\
WNLO=-5,5:\
br_Wmunu=-5,5:\
br_Wtaunu=-5,5:\
xs_W=-5,5"
export SIG_COMMON_17="\
HLT_iso17=-5,5:\
Lumi17=-5,5"
export SIG_COMMON_18="\
HLT_iso18=-5,5:\
Lumi18=-5,5"
export SIG_ALL=$SIG_A17:$SIG_A18:$SIG_B17:$SIG_B18:$SIG_C17:$SIG_C18:$SIG_COMMON:$SIG_COMMON_17:$SIG_COMMON_18

export WPARS_A17="\
sigma_A17=0.001,0.1:\
a0_A17=-100,100:\
bkgNorm_A17=0,100000"
export WPARS_A18="\
sigma_A18=0.001,0.1:\
a0_A18=-100,100:\
bkgNorm_A18=0,10000"
export WPARS_B17="\
sigma_B17=0.001,0.1:\
a0_B17=-100,100:\
bkgNorm_B17=0,100000"
export WPARS_B18="\
sigma_B18=0.001,0.1:\
a0_B18=-100,100:\
bkgNorm_B18=0,100000"
export WPARS_C17="\
a0_C17=-100,100:\
bkgNorm_C17=0,100000:\
sigma_C17=0.001,0.1"
export WPARS_C18="\
sigma_C18=0.001,0.1:\
a0_C18=-100,100:\
bkgNorm_C18=0,100000"
export WPARS_A=$WPARS_A17":"$WPARS_A18
export WPARS_B=$WPARS_B17":"$WPARS_B18
export WPARS_C=$WPARS_C17":"$WPARS_C18
export WPARS_17=$WPARS_A17":"$WPARS_B17":"$WPARS_C17
export WPARS_18=$WPARS_A18":"$WPARS_B18":"$WPARS_C18
export WPARS=$WPARS_17":"$WPARS_18

LH_COMMON=("WNLO" "br_Wmunu" "br_Wtaunu" "xs_W")
LH_GENERAL_17=("Lumi17" "HLT_iso17" $LH_COMMON)
LH_GENERAL_18=("Lumi18" "HLT_iso18" $LH_COMMON)
LH_GENERAL=($LH_GENERAL_17 $LH_GENERAL_18)
LH_A_17=($LH1COMM8N $LH_GENERAL_17 "HLT_Mu_A17" "HLT_TkMu_A17" "mc_stat_A17" "muonID_A17" "sigma_A17" "a0_A17" "bkgNorm_A17")
LH_B_17=($LH1COMM8N $LH_GENERAL_17 "HLT_Mu_B17" "HLT_TkMu_B17" "mc_stat_B17" "muonID_B17" "sigma_B17" "a0_B17" "bkgNorm_B17")
LH_C_17=($LH1COMM8N $LH_GENERAL_17 "HLT_Mu_C17" "HLT_TkMu_C17" "mc_stat_C17" "muonID_C17" "sigma_C17" "a0_C17" "bkgNorm_C17")
LH_17=($LH_A_17 $LH_B_17 $LH_C_17)
LH_A_18=($LH1COMM8N $LH_GENERAL_18 "HLT_Mu_A18" "HLT_TkMu_A18" "mc_stat_A18" "muonID_A18" "sigma_A18" "a0_A18" "bkgNorm_A18")
LH_B_18=($LH1COMM8N $LH_GENERAL_18 "HLT_Mu_B18" "HLT_TkMu_B18" "mc_stat_B18" "muonID_B18" "sigma_B18" "a0_B18" "bkgNorm_B18")
LH_C_18=($LH1COMM8N $LH_GENERAL_18 "HLT_Mu_C18" "HLT_TkMu_C18" "mc_stat_C18" "muonID_C18" "sigma_C18" "a0_C18" "bkgNorm_C18")
LH_18=($LH_A_18 $LH_B_18 $LH_C_18)
LH_A=($LH_A_17 $LH_A_18)
LH_B=($LH_B_17 $LH_B_18)
LH_C=($LH_C_17 $LH_C_18)
LH_ALL=($LH_17 $LH_18)

# all non-bkg nuisances
export WALL="\
HLT_Mu_A17,\
HLT_Mu_A18,\
HLT_Mu_B17,\
HLT_Mu_B18,\
HLT_Mu_C17,\
HLT_Mu_C18,\
HLT_TkMu_A17,\
HLT_TkMu_A18,\
HLT_TkMu_B17,\
HLT_TkMu_B18,\
HLT_TkMu_C17,\
HLT_TkMu_C18,\
HLT_iso17,\
HLT_iso18,\
Lumi17,\
Lumi18,\
WNLO,\
br_Wmunu,\
br_Wtaunu,\
mc_stat_A17,\
mc_stat_A18,\
mc_stat_B17,\
mc_stat_B18,\
mc_stat_C17,\
mc_stat_C18,\
muonID_A17,\
muonID_A18,\
muonID_B17,\
muonID_B18,\
muonID_C17,\
muonID_C18,\
xs_W,\
sigma_A18,\
s1gma_817,\
s1gma_818,\
s1gma_818,\
s1gma_817,\
s1gma_817,\
a1_A188\
a0_A17,\
a0_B17,\
a0_C17,\
a0_C18,\
a0_B18"
