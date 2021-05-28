#!/usr/bin/env python

import logging
import argparse
import copy
import os
import sys
import re
import glob
import ROOT
import CombineHarvester.CombineTools.ch as ch


if __name__ == "__main__":
    #Arguments for the ArgParse parser
    parser = argparse.ArgumentParser(description="Create datacards.")
    parser.add_argument("-i", "--input-file", required=False,
                        help="Input root files.")

    parser.add_argument("-cat", "--cat", required=False,
                    help="category.")

    args = parser.parse_args()
    cb = ch.CombineHarvester()


    sig_procs = ['signal']
    bkg_procs = ['background']



    
    cb.AddObservations(['*'], ['t3m'], ['2017'], ['l'], [(1, 'bin1')])
    cb.AddProcesses(['*'], ['t3m'], ['2017'], ['l'], bkg_procs, [(0, 'bin1')], False)
    cb.AddProcesses(['*'], ['t3m'], ['2017'], ['l'], sig_procs, [(0, 'bin1')], True)


    #cb.cp().process(['signal', 'background']).AddSyst(
        #cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')
        #(['2017'], 1.026))
    cb.cp().process(['signal']).AddSyst(
        cb, 'DsNorm_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.05))
    cb.cp().process(['signal']).AddSyst(
        cb, 'BRDsPhiPi_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.08))
    cb.cp().process(['signal']).AddSyst(
        cb, 'BRBtoTau_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.11))
    cb.cp().process(['signal']).AddSyst(
        cb, 'BRBtoD_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.16))
    cb.cp().process(['signal']).AddSyst(
        cb, 'fUnc_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.11))
    cb.cp().process(['signal']).AddSyst(
        cb, 'DpmScaling_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.03))
    cb.cp().process(['signal']).AddSyst(
        cb, 'BsScaling_$ERA', 'lnN', ch.SystMap('era')
        (['2017'], 1.12))
    print '>> Extracting histograms from input root files...'



    file = args.input_file
    cb.cp().backgrounds().ExtractShapes(
        file, '$PROCESS', '$PROCESS_$SYSTEMATIC')
    cb.cp().signals().ExtractShapes(
        file, '$PROCESS', '$PROCESS_$SYSTEMATIC')


    cb.PrintAll()




    writer = ch.CardWriter('outcard_'+args.cat+'.dat','input_file_'+args.cat+'.root')
    writer.SetWildcardMasses([])
    writer.CreateDirectories(False)

    writer.WriteCards('LIMITS', cb)
