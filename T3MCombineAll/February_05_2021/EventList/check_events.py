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
       file2_idx = 0
       if 'run' in lines2[file2_idx]: file2_idx += 1
       for line1 in lines1:
           if 'run' in line1: continue
           if (file2_idx>=len(lines2)): break
           rle1 = line1.strip('\n').split('\t')
           rle2 = lines2[file2_idx].strip('\n').split('\t')
           if rle1[0]==rle2[1] and rle1[1]==rle2[1] and rle1[2]==rle2[2]: print rle1[0], rle1[1], rle1[2]
           if (rle1[0]<rle2[0]): continue
           for j in range(file2_idx, len(lines2)):
              j += 1
              rle2 = lines2[j].strip('\n').split('\t')
              if (rle2[0]>rle1[0]): break
           file2_idx = j
