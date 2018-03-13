# Loading binary vectors

import word2vec
import itertools
import numpy as np
import sys
import random
import os,glob
dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
from scipy.spatial.distance import cosine

RELEVANTS = [1,2,4,8]
TOTAL_Ns = [0] * len(RELEVANTS)
TOTAL_Cs = [0] * len(RELEVANTS)
TOTAL_NsT = [0] * len(RELEVANTS)
TOTAL_CsT = [0] * len(RELEVANTS)
RELEVANTS.sort()
# MAX_RELEVANTS = max(RELEVANTS)

# print("ARG 2 [folder name] [filename]")
name = sys.argv[1]
# folder = sys.argv[1]

filename = name.split("/")[-1].split(".")[0].split("_")[0]
subname = name.split("/")[-2]
filepath = dir_path + "/dataparsed/{0}.csv".format(filename)
filepathresults = dir_path + "/results/{0}/{1}".format(subname,name.split("/")[-1].split(".")[0])

print(name,filename,filepath)
# evaluator/vectors/mitdwhdata_v200_n10_i10_csv.bin

print("LOADING MODULE")
model = word2vec.load(name)
print("VOCAB SIZE: ",len(model.vocab))
print("MODEL LOADED")

def similar(t,val):
    # for t in table:
    if val in t:
        return 1
    return 0

# ~R!RR*~
def lTable(table):
    global TOTAL_Ns
    global TOTAL_Cs
    global RELEVANTS
    # global RELEVAN

    if len(table) == 0:
        return
    (r,c) = (len(table),len(table[0]))
    #Create column arrays
    # print("FLIPPING TABLE")
    rTable = list(zip(*table))
    # print("FLIPPED TABLE")
    rang = range(c)
    for i in range(r):
        if random.randint(1,10) > 1:
            continue
        if i % 1000 == 0:
            print("Viewed Approximately",i/10,"lines")
            for ind in range(len(RELEVANTS)):
                if TOTAL_CsT[ind] > 0:
                    print(RELEVANTS[ind],TOTAL_NsT[ind]*100/TOTAL_CsT[ind],"%")
                    # fh.write(" ".join([str(RELEVANTS[ind]),str(TOTAL_NsT[ind]/TOTAL_CsT[ind]*100),"%\n"]))
                    # fh.flush()

        for j in [random.choice(rang),random.choice(rang)]:
            val = table[i][j]
            # print(val)
            if len(val) == 0:
                continue
            try:
                indexes, metrics = model.cosine(val, n=RELEVANTS[-1])
                res = model.generate_response(indexes, metrics).tolist()
                y = 0
                ind = 0
                for rr in range(len(res)):
                    resp = res[rr]
                    l = similar(table[i],resp[0])
                    y += max(l,similar(rTable[j],resp[0]))
                    if rr + 1 == RELEVANTS[ind]:
                        TOTAL_Ns[ind] += y
                        TOTAL_Cs[ind] += RELEVANTS[ind]
                        TOTAL_NsT[ind] += y
                        # if y == 1:
                        #     print("RELEVANT",resp)
                        TOTAL_CsT[ind] += RELEVANTS[ind]
                        ind += 1
            except:
                # print(val)
                # print(e)
                pass
import csv
fh = open(filepathresults + ".log", "w")
with open(filepath, 'r') as csvfile:
    reader = csv.reader(csvfile)
    # print(reader)
    table = []
    tablenum = 0
    for row in reader:
        # print(row)
        if row[0] == "~R!RR*~":
            if len(table) == 0:
                continue
            #We now have a 2-D
            TOTAL_NsT = [0] * len(RELEVANTS)
            TOTAL_CsT = [0] * len(RELEVANTS)
            fh.write("New Table -- {0}, length: {1} x {2}\n".format(tablenum,len(table),len(table[0])))
            print("Processing Table")
            lTable(table)
            table = []
            # print("update accurates")
            for ind in range(len(RELEVANTS)):
                if TOTAL_CsT[ind] > 0:
                    print(RELEVANTS[ind],TOTAL_NsT[ind]*100/TOTAL_CsT[ind],"%")
                    fh.write(" ".join([str(RELEVANTS[ind]),str(TOTAL_NsT[ind]*100/TOTAL_CsT[ind]),"%\n"]))
            fh.write("--\n")
            fh.flush()
            print("DONE with TABLE",tablenum)
            tablenum += 1
        else:
            table.append(row)
            if len(table) % 10000 == 0:
                print("LOADED",len(table),"lines")
    print("---END---")
    flog = open(filepathresults + ".res","w")
    flog.write("#ACCURACY FILE running ~1/10 every row and 2 random colmuns each time \n")
    flog.write("TOTAL TABLES: {0}\n".format(tablenum))
    for ind in range(len(RELEVANTS)):
        print(RELEVANTS[ind],TOTAL_Ns[ind]*100/TOTAL_Cs[ind],"%")
        fh.write(" ".join([str(RELEVANTS[ind]),str(TOTAL_Ns[ind]*100/TOTAL_Cs[ind]),"%\n"]))
        fh.flush()
        flog.write(" ".join([str(RELEVANTS[ind]),str(TOTAL_Ns[ind]*100/TOTAL_Cs[ind]),"%\n"]))
        flog.flush()