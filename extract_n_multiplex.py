# python code
# what it does - 
# 1. extract variable regions based on given primer set from given multifasta file
# 2. multiplex each region sequence by random times
# 3. do multiplexing in given iterations

# Author - Dattatray Suresh Mongad
# Date - 06/08/18
# Place - National Centre for Microbial Resource
# list of definitions
# 1. qw
# 2. getpos
# 3. extract_subseq
# 4. make_randint_list
# 5. select_random_index
# 6. mutate_list

#importing required modules
from optparse import OptionParser
import os
import re
import random
from random import shuffle
from Bio import SeqIO

#definitions
def qw(s):
    return tuple(s.split())

def getpos(forward_primer,reverse_primer):
    #commands for fuzznuc
    cmd = "fuzznuc -sequence tmp.fasta -pattern "+forward_primer+" -complement Y -rformat excel -outfile f.fuzznuc"
    os.system(cmd)
    cmd = "fuzznuc -sequence tmp.fasta -pattern "+reverse_primer+" -complement Y -rformat excel -outfile r.fuzznuc"
    os.system(cmd)
    fwd = open("f.fuzznuc","r")
    line = fwd.readlines()
    if len(line) > 1:
        start = int(line[1].split()[1])
    else:
        start = 0
    fwd.close()
    rev = open("r.fuzznuc","r")
    line = rev.readlines()
    if len(line) > 1:
        end = int(line[1].split()[2])
    else:
        end = 0
    rev.close()
    return start,end

def extract_subseq(seq,start,end):
    return seq[start:end]

#random integers list
def make_randint_list(n):
    randintlist_1_to_10 = []
    for i in range(1,n+1,1):
        randintlist_1_to_10.append(random.randint(1,10))
    return randintlist_1_to_10

#random index from list
def select_random_index(list,percent):
    randindex = []
    for i in range(1,int(len(list)*percent/100),1):
        randindex.append(random.randint(0,len(list)))
    return randindex

#mutate list
def mutate_list(intlist,indexlist,sum):
    for i in range(1,len(indexlist),1):
        intlist[i] = intlist[i] * random.randint(1,100)
        temp = 0
        for i in intlist:
            temp = temp + i
        if temp < sum:
            continue
        else:
            break
    return intlist

#getting options
required = qw("forward_primer reverse_primer seqdata")
parser = OptionParser()
parser.add_option("-f",dest="forward_primer",help="forward-primer")
parser.add_option("-r",dest="reverse_primer",help="reverse-primer")
parser.add_option("-n",dest="niter",default=1,help="(default 1) number of iterations to repeat random multiplexing of extracted sequences")
parser.add_option("-d",dest="seqdata",help="multifasta sequence file from which regions will be extracted")

options,args = parser.parse_args()

# #checking if required arguments are passed
for r in required:
    if options.__dict__[r] is None:
        parser.error("parameter %s required "%r)
#capturing given arguments
forward_primer = options.forward_primer
reverse_primer = options.reverse_primer
seqdata = options.seqdata
if options.__dict__["niter"] is not None:
    niter = options.niter
else:
    niter = 1


################## running code to extract seqs ################

#extract seq and write in file
fout = open("variable_regions.fasta","a") 
fout2 = open("failed.fasta","a")
noOfSeqWritten = 0
for record in SeqIO.parse(seqdata,"fasta"):
    ftmp = open("tmp.fasta","w")
    seq = str(record.seq)
    id = str(record.id) + " " + str(record.description)
    ftmp.write(">" + id + "\n" + seq)
    ftmp.close()
    header = id
    start,end = getpos(forward_primer,reverse_primer)
    if start > 0 and end > 0:
        vregion = extract_subseq(seq,start,end)
        seq = ">"+header+"\n"+vregion+"\n"
        fout.write(seq)
        noOfSeqWritten = noOfSeqWritten + 1
    else:
        fout2.write(">"+header)
        fout2.write(seq)    
fout.close()
os.remove("tmp.fasta")
print("No. of seq written",noOfSeqWritten)

for i in range(int(niter)):
    n = i + 1
    fout = "multiplexed_ite_" + str(n)
    fout = open(fout,"a")
    fstat = "multiplexed_count_ite_" + str(n)
    fstat = open(fstat,"a")
    fstat.write("header\tcount\n")
    #making random multipliers
    intlist = make_randint_list(noOfSeqWritten)
    indexlist = select_random_index(intlist,90)
    intlist = mutate_list(intlist,indexlist,500000)
    shuffle(intlist)
    fseq = open("variable_regions.fasta","r")
    fiter = iter(fseq)
    index = 0
    for line in fiter:
        header = line
        seq = next(fiter)
        print(intlist)
        copyNumber = intlist[index]
        fstat.write(header.strip()+"\t")
        fstat.write(str(copyNumber)+"\n")
        index = index + 1
        for j in range(0,copyNumber):
            fout.write(header)
            fout.write(seq)
    fout.close()
    fstat.close()

