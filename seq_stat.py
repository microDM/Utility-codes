from collections import Counter
from Bio import SeqIO
from optparse import OptionParser

#inputFile,outputFile = "",""
parser = OptionParser()
parser.add_option("-i","--input",dest="inputFile",help="input fasta/multi-fasta file (protein/nucleotide)")
parser.add_option("-o","--output",dest="outputFile",help="output file name")
(options,args) = parser.parse_args()

inputFile = options.inputFile
outputFile = options.outputFile

out = open(outputFile,"w")

for record in SeqIO.parse(inputFile,"fasta"):
    header = record.id
    seq = str(record.seq)
    temp = Counter(seq)
    out.write(header+"\t")
    for i,j in temp.items():
        out.write(i+"="+str(j)+"\t")
    out.write("SeqLength="+str(len(seq))+"\n")
