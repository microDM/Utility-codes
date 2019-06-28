import sys
import argparse
import re
import pandas as pd
from Bio import SeqIO

parser = argparse.ArgumentParser(
    description="This script parses orthoMCL output to form count table"+
    ", presence-absence matrix and prints core, accessory and unique genes"+
    " in fasta file.")
parser.add_argument("-g",dest="groupFile",default="group.txt",help="Group file created by orthoMCL"+
                    ". Usually located at my_orthomcl_dir/groups/groups.txt")
parser.add_argument("-f",dest="fastaFile",default="goodProteins.fasta",help="goodProteins file"+
                    ". Usually located at my_orthomcl_dir/blast_dir/goodProteins.fasta")
parser.add_argument("-n",dest="nameFile",default="names.txt",help="List of names of genomes used by orthoMCL"+
                    ". List of names of genomes/organisms used while running orthomcl")
parser.add_argument("-s",dest="singletonFile",default="singletons.txt",help="Singletons file"+
                    ". Created by running orthomclSingletons")

if(len(sys.argv) == 1):
    parser.print_help(sys.stderr)
    sys.exit()

#parsing arguments
args = parser.parse_args()
groupFile = args.groupFile
fastaFile = args.fastaFile
nameFile = args.nameFile
singletonFile = args.singletonFile

############ definitions #######3
def addGenesToDict(dictToReturn,groupList,refDict):
    """
    :param groupList:
    :param refDict:
    :return:
    """
    for i in groupList:
        dictToReturn[i] = refDict[i]
    return dictToReturn

#make list of names
nameList = []
with open(nameFile,"r") as f:
    for i in f.readlines():
        nameList.append(i.strip())

#making group dictionary and empty dataframe
groupDict = dict()
df = pd.DataFrame()

with open(groupFile,"r") as f:
    for i in f.readlines():
        #make dummy dict
        dummyDict = {x:0 for x in nameList}
        members = i.split(":")[1].strip().split(" ") #all genes in group
        orthoGroup = i.split(":")[0] #ortho group name
        groupDict[orthoGroup] = members #insert into dictionary
        #calculate count
        temp = [re.sub("\|\S+","",x) for x in members]
        tempDict = {x:temp.count(x) for x in temp}
        dummyDict.update(tempDict)
        df = df.append(dummyDict,ignore_index=True)
df_index = list(groupDict.keys())
#add singletons to matrix
with open(singletonFile,"r") as f:
    for i in f.readlines():
        # make dummy dict
        dummyDict = {x: 0 for x in nameList}
        genome = i.strip().split("|")[0]
        dummyDict[genome] = 1
        df = df.append(dummyDict,ignore_index=True)
        gene = i.strip().split("|")[1]
        df_index.append(gene)

df.index = df_index
df.to_csv("count.txt",sep="\t") #count data
df[df>0] = 1
df.to_csv("presence_absence.txt",sep="\t")

#read goodproteins.fasta
seqDict = SeqIO.to_dict(SeqIO.parse(fastaFile,'fasta'))

coreGenes = dict()
accessoryGenes = dict()
uniqGenes = dict()

#print core and accessory genes
for i in df.index:
    if(df.loc[i].sum() == len(nameList)):
        coreGenes = addGenesToDict(coreGenes,groupDict[i],seqDict)
    elif(df.loc[i].sum() < len(nameList) and df.loc[i].sum() > 1):
        accessoryGenes = addGenesToDict(accessoryGenes,groupDict[i],seqDict)
#get uniq genes
with open(singletonFile,'r') as f:
    for i in f.readlines():
        uniqGenes[i.strip()] = seqDict[i.strip()]

#writing files
with open("core_genes.fasta",'w') as f:
    SeqIO.write(coreGenes.values(),f,'fasta')
with open('accessory_genes.fasta','w') as f:
    SeqIO.write(accessoryGenes.values(),f,'fasta')
with open('uniq_genes.fasta','w') as f:
    SeqIO.write(uniqGenes.values(),f,'fasta')

