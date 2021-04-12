#! /usr/bin/env python
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]

file1_list = []
file2_list = []

with open(file1) as file1_: 
    with open(file2) as file2_:
       lines1 = file1_.readlines()
       lines2 = file2_.readlines()
       file1_list = [ l.strip('\n').split('\t') for l in lines1 if 'run' not in l]
       file2_list = [ l.strip('\n').split('\t') for l in lines2 if 'run' not in l]

for rle1 in file1_list:
    for rle2 in file2_list:
        if (rle1[0]==rle2[0] and rle1[1]==rle2[1] and rle1[2]==rle2[2]): print rle1[0], rle1[1], rle1[2]
