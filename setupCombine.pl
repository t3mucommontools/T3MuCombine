#! /usr/bin/perl
use Cwd;
use POSIX;
use POSIX qw(strftime);

#############################################
$numArgs = $#ARGV +1;
$ARGV[$argnum];

$UserID= POSIX::cuserid();

$CMSSWRel="11_3_4";
$ARCH="slc7_amd64_gcc700";
$time= strftime("%h_%d_%Y",localtime);

if($ARGV[0] eq "--help" || $ARGV[0] eq ""){

    printf("\n  This code requires one input option. The syntax is:./setupCombine.pl [OPTION]");
    printf("\n  Please choose from the following options:\n");
    printf("\n  ./setupCombine.pl --help                                   Prints this message");
    printf("\n  ./setupCombine.pl --Combine <workdir>                      Clone and compile HiggsCombine and Combine Harvester tools. Example: ./setupCombine --Combine workdir");
    printf("\n  ");

    exit(0);  
} 



if( $ARGV[0] eq "--Combine"){
    $currentdir=getcwd;
    if($ARGV[1] ne ""){
        $basedir=$ARGV[1];
    }
    else{
        printf("\n<workdir> is required. Please follow the syntax:./setupCombine.pl --Combine <workdir> ");
        printf("\nFor more details use: ./setupCombine.pl --help\n");
        exit(0);
    }
    printf("\nWorkingDir for Combine: $basedir");
    printf("\nCurrentDir is: $currentdir \n");

    system(sprintf("rm Install_Combine_$time"));


    system(sprintf("echo \"export SCRAM_ARCH=\\\"$ARCH\\\"\" >> Install_Combine_$time"));
    system(sprintf("echo \"source /cvmfs/cms.cern.ch/cmsset_default.sh\" >> Install_Combine_$time"));


    system(sprintf("echo \"mkdir $basedir\" >>  Install_Combine_$time"));
    system(sprintf("echo \"cd $basedir\" >>  Install_Combine_$time"));
    system(sprintf("echo \"cmsrel CMSSW_$CMSSWRel\" >>  Install_Combine_$time"));
    system(sprintf("echo \"cd CMSSW_$CMSSWRel/src\" >> Install_Combine_$time"));
    system(sprintf("echo \"cmsenv\" >> Install_Combine_$time"));
    system(sprintf("echo \"git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit\" >> Install_Combine_$time"));
    system(sprintf("echo \"cd HiggsAnalysis/CombinedLimit \" >> Install_Combine_$time"));

    system(sprintf("echo \"git fetch origin  \" >> Install_Combine_$time"));
    system(sprintf("echo \"git checkout v9.1.0  \" >> Install_Combine_$time"));
    system(sprintf("echo \"scram b clean; scram b -j 4  \" >> Install_Combine_$time"));

    system(sprintf("echo \"cd ../../ \" >> Install_Combine_$time"));

    system(sprintf("echo \"git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester\" >> Install_Combine_$time"));
    system(sprintf("echo \"scram b -j 4  \" >> Install_Combine_$time"));

    system(sprintf("echo \"cp -r ../../../T3M_INFN  CombineHarvester \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp -r ../../../T3M  CombineHarvester \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp -r ../../../T3MLimit  CombineHarvester \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp -r ../../../T3MCombineAll CombineHarvester \" >> Install_Combine_$time"));
    system(sprintf("echo \"mkdir  CombineHarvester/T3M/workspaces \" >> Install_Combine_$time"));
    system(sprintf("echo \"mkdir  CombineHarvester/T3M/plots \" >> Install_Combine_$time"));
    system(sprintf("echo \"mkdir  CombineHarvester/T3MLimit/workspaces \" >> Install_Combine_$time"));
    system(sprintf("echo \"mkdir  CombineHarvester/T3MLimit/plots \" >> Install_Combine_$time"));
    system(sprintf("echo \"mkdir  CombineHarvester/T3MLimit/datacards \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp  ../../../T3MLimit/CMS_lumi.py  CombineHarvester/T3MLimit/datacards \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp  ../../../T3MLimit/readLimit.py  CombineHarvester/T3MLimit/datacards \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp  ../../../T3MLimit/tdrstyle.py  CombineHarvester/T3MLimit/datacards \" >> Install_Combine_$time"));
    system(sprintf("echo \"cp -r ../../../T3M_HF  CombineHarvester \" >> Install_Combine_$time"));


    printf("\n\nInstructions:");
    printf("\nTo complete the installation do the following command (compilation might take some time ...):");
    printf("\nsource  Install_Combine_$time \n");

}


