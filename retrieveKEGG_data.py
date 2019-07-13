import requests
import sys
import re
import pandas as pd

keggFile = sys.argv[1]
df = pd.DataFrame()

def countKO(reqObj):
    copyNumberDict = dict()
    for i in reqObj:
        matchObj = re.search("^.*\:(K\d+)",i)
        if(matchObj):
            ko = matchObj.group(1)
            copyNumberDict[ko] = copyNumberDict.get(ko,0)+1
    return copyNumberDict

count = 1
orgList = []
rrnaFile = open("16S_rRNA_seq.fasta",'w')
with open(keggFile,'r') as f:
    for i in f.readlines():
        orgCode = i.strip().split("\t")[1]
        orgName = i.strip().split("\t")[2]
        #make url for retriveing all genes
        url = "http://rest.kegg.jp/link/ko/" + orgCode
        req = requests.get(url).text.split("\n")
        countKO(req)
        #get gene for 16S rRNA gene
        r = re.compile("K01977")
        rRNA_16S = list(filter(r.search,req))[0].split('\t')[0]
        #retriev 16S rrna and make dataframe
        url = "http://rest.kegg.jp/get/" + rRNA_16S + "/ntseq"
        rRNASeq = requests.get(url).text
        if(len(rRNASeq) > 0):
            print(str(count) + " : " + orgCode + " : " + orgName)
            copyNumDict = countKO(req)
            df = df.append(copyNumDict,ignore_index=True)
            orgList.append(orgCode)
            #write seq in file
            rrnaFile.write(rRNASeq)
            count = count + 1
df.to_csv("copyNumbers.txt",sep='\t')
df.index = orgList
df.to_csv("copyNumbers_with_Names.txt",sep='\t')