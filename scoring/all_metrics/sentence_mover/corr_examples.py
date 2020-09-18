import numpy as np
import sys
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import Levenshtein


def read_normal_file(file1):
    with open(file1, 'r') as f1:
        f1Lines = f1.readlines()[2:]  # ignore 2 header lines
    list1 = []
    for i in range(len(f1Lines)):
        ind1, val1 = f1Lines[i].split("\t")
        list1.append(float(val1.strip()))
    return list1


def read_rouge_wmd_file(file1):
    with open(file1, 'r') as f1:
        f1Lines = f1.readlines()
    rougeList = []
    wmdList = []
    newSection = 0
    for line in f1Lines:
        if (":" in line) or ("=" in line):
            newSection += 1
        elif newSection == 1:
            wmdList.append(float(line.strip()))
        elif newSection == 2:
            rougeList.append(float(line.strip()))
        if newSection == 3:
            newSection = -1
    return rougeList, wmdList


def process_files(keep_file, file1, file2=None):
    # don't need keep file anymore
    # with open(keep_file,"r") as keep:
     #    keepList = [int(x.strip()) for x in keep.readlines()]
#    print(len(keepList))
    dataDict = {"wmd1": [], "wmd2": [], "rouge1": [], "rouge2": [], "normal1": [], "normal2": []}
    if "rouge" in file1:
        rouge1, wmd1 = read_rouge_wmd_file(file1)
        dataDict["rouge1"] = [x for x in rouge1]  # used to be a negation here. not any more.
        dataDict["wmd1"] = wmd1
    elif "human" in file1:
        dataDict["normal1"] = [x for x in read_normal_file(file1)]  # removed negation
    else:
        dataDict["normal1"] = read_normal_file(file1)
    if file2:
        if "rouge" in file2:
            rouge2, wmd2 = read_rouge_wmd_file(file2)
            dataDict["rouge2"] = [x for x in rouge2]  # removed negation
            dataDict["wmd2"] = wmd2
        elif "human" in file2:
            dataDict["normal2"] = [x for x in read_normal_file(file2)]  # removed negation
        else:
            dataDict["normal2"] = read_normal_file(file2)
    # ignore the entries from the reference model
    # don't need this anymore
    # for k in list(dataDict.keys()):
    #    if dataDict[k] != []:
    #        dataDict[k] = [i for j, i in enumerate(dataDict[k]) if j in keepList]
    for v in dataDict.values():
        if v != 0:
            print(len(v))
    return dataDict


def get_examples(data, percentile, orig_data_file, keep_file, dataSource1, dataSource2, AisSim, BisSim):
    odfLines = []
    with open(orig_data_file, 'r') as odf:
        odfLines = odf.readlines()
    # don't need keep_file anymore
    # with open(keep_file,"r") as keep:
    #    keepList = [int(x.strip()) for x in keep.readlines()]
    dataA = data[dataSource1]
    dataB = data[dataSource2]
    assert(len(odfLines) == len(dataA))
    assert(len(odfLines) == len(dataB))
    print("MAX A: " + "\t" + str(np.max(dataA)) + "\t" + odfLines[dataA.index(np.max(dataA))].split("\t")[1])
    print("MIN A: " + "\t" + str(np.min(dataA)) + "\t" + odfLines[dataA.index(np.min(dataA))].split("\t")[1])
    print("MAX B: " + "\t" + str(np.max(dataB)) + "\t" + odfLines[dataB.index(np.max(dataB))].split("\t")[1])
    print("MIN B: " + "\t" + str(np.min(dataB)) + "\t" + odfLines[dataB.index(np.min(dataB))].split("\t")[1])

    lowSimThreshA = np.percentile(dataA, percentile)
    highSimThreshA = np.percentile(dataA, 100 - percentile)
    lowSimThreshB = np.percentile(dataB, percentile)
    highSimThreshB = np.percentile(dataB, 100 - percentile)
    print(lowSimThreshA, highSimThreshA, lowSimThreshB, highSimThreshB)
    AsimBdif = []
    AdifBsim = []
    AsimBsim = []
    AdifBdif = []
    for i in range(len(dataA)):
        # higher numbers = higher sim, lower dif, once I switched everything to similarity
        if dataA[i] <= lowSimThreshA:
            if dataB[i] <= lowSimThreshB:
                AdifBdif.append(i)
            elif dataB[i] > highSimThreshB:
                AdifBsim.append(i)
        elif dataA[i] > highSimThreshA:
            if dataB[i] > highSimThreshB:
                AsimBsim.append(i)
            elif dataB[i] < lowSimThreshB:
                AsimBdif.append(i)
    print("AsimBdif: ",len(AsimBdif))
    print("AdifBsim: ",len(AdifBsim))
    print("AsimBsim: ",len(AsimBsim))
    print("AdifBdif: ",len(AdifBdif))
    #AscoreDist={}
    #for x in dataA:
    #    if x not in AscoreDist:
    #        AscoreDist[x] = 1
    #    else:
    #        AscoreDist[x] += 1
    #print(AscoreDist)
    # Bscores3 = [0,0,0]  # top percentile, mid, bottom
    # Bscores0 = [0,0,0]  # top, mid, bottom
    #
    # for i in range(len(dataA)):
    #     if dataA[i] == 3.:
    #         if dataB[i] <=lowSimThreshB:
    #             Bscores3[2] += 1
    #         elif dataB[i] > highSimThreshB:
    #             Bscores3[0] += 1
    #         else:
    #             Bscores3[1] += 1
    #     elif dataA[i] == 0.:
    #         if dataB[i] <=lowSimThreshB:
    #             Bscores0[2] += 1
    #         elif dataB[i] > highSimThreshB:
    #             Bscores0[0] += 1
    #             print(i)
    #         else:
    #             Bscores0[1] += 1
    # print("scores of best essays: ", Bscores3)
    # print("scores of worst essays: ", Bscores0)

    # #get threshold scores for 0,1,2,3
    # counts = [39, 646, 1303]  #last 423 are 3
    # sortedB = dataB[:]
    # sortedB.sort()
    # minScores = [sortedB[x] for x in counts]  # where 0 is the lowest score to get a 1, 1 is the lowest to get a 2, and 2 to get a 3
    # confusionMatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]  # confusion matrix at [i,j] is human=i, pred=j
    # for i in range(len(dataA)):
    #     a = int(dataA[i])
    #     if dataB[i] >= minScores[2]:
    #         confusionMatrix[a][3] += 1
    #     elif dataB[i] >= minScores[1]:
    #         confusionMatrix[a][2] += 1
    #     elif dataB[i] >= minScores[0]:
    #         confusionMatrix[a][1] += 1
    #     else:
    #         confusionMatrix[a][0] += 1
    # for a in confusionMatrix:
    #     print(a)
    # to see examples of all categories:
    # for l in [AsimBdif, AdifBsim, AsimBsim, AdifBdif]:
    # to see examples of differing judgments:
    avgSimWordsA = 0.
    avgDifWordsA = 0.
    avgSimWordsB = 0.
    avgDifWordsB = 0.
    #with open("length.values",'w') as outF:
    for l in [AsimBdif, AdifBsim]:
        print("**************************")
        for i in l:
        #for i in range(len(dataA)):
            ref, hyp = odfLines[i].split("\t")
            #num_words = word_tokenize(hyp)
            #outF.write(str(i)+"\t"+str(len(num_words))+"\n")
            # ref, hyp = odfLines[keepLines[i]].split("\t")
            # convert back to positive if sim
            aScore = dataA[i]
            bScore = dataB[i]
            # removed below because all are sim now
            #if AisSim:
            #    aScore = -aScore
            #if BisSim:
            #    bScore = -bScore
            print(str(i+1) + "\n" + ref + "\n" + hyp + "\n" + str(aScore)+"\t"+str(bScore))
    return "Done!"


def get_overlap_examples(data, percentile, orig_data_file, keep_file, dataSource1, dataSource2, AisSim, BisSim):
    with open(orig_data_file, 'r') as odf:
        odfLines = odf.readlines()
    with open(keep_file,"r") as keep:
        keepList = [int(x.strip()) for x in keep.readlines()]
    refList = [x.split("\t")[0] for x in odfLines]
    hypList = [y.split("\t")[1].strip() for y in odfLines]
    print(len(odFLines))
    print(len(keepList))
    print(len(refList))
    print(len(hypList))
    assert len(refList) == len(hypList)
    levenList = [Levenshtein.distance(refList[keepList[z]], hypList[keepList[z]]) for z in range(len(keepList))]
    lowLevenThresh = np.percentile(levenList, percentile)
    highLevenThresh = np.percentile(levenList, 100 - percentile)
    dataA = data[dataSource1]
    dataB = data[dataSource2]
    highEdit = []
    lowEdit = []
    for elt_id in range(len(dataA)):
        if levenList[elt_id] <= lowLevenThresh:
            lowEdit.append(elt_id)
        elif levenList[elt_id] >= highLevenThresh:
            highEdit.append(elt_id)
    print(len(lowEdit))
    print(len(highEdit))
    lowA = []
    highA = []
    lowB = []
    highB = []
    isLow = True
    for l in [lowEdit, highEdit]:
        print("**************************")
        count = 0
        for e_id in l:
            if count < 100000:  # show this many examples
                ref, hyp = odfLines[keepList[e_id]].split("\t")
                #ref_doc = [sent for sent in nltk.sent_tokenize(ref)]
                #ref_doc = [[t for t in nltk.word_tokenize(sent) if t.isalpha()] for sent in ref_doc]
                #ref_doc = [x for x in ref_doc if x != []][:3]
                #ref_doc = [" ".join(x) for x in ref_doc]
                #print("REF: "+" ".join(ref_doc)+"\tHYP: "+hyp[:-1])
                # convert back to positive if sim
                print("REF: "+ref+"\tHYP: "+hyp[:-1])
                aScore = dataA[e_id]
                bScore = dataB[e_id]
                # removed negation below
                # if AisSim:
                #     aScore = -aScore
                # if BisSim:
                #     bScore = -bScore
                if isLow:
                    lowA.append(aScore)
                    lowB.append(bScore)
                else:
                    highA.append(aScore)
                    highB.append(bScore)                
                print(str(levenList[e_id])+"\t"+str(aScore)+"\t"+str(bScore))
                count += 1
        isLow = False
    print("average low A: ", np.mean(lowA))
    print("average low B: ", np.mean(lowB))
    print("average high A: ", np.mean(highA))
    print("average high B: ", np.mean(highB))
    print("correlation on low edit distance (high similarity): ",np.corrcoef(lowA,lowB)[0][1])
    print("correlation on high edit distance (low similarity): ",np.corrcoef(highA,highB)[0][1])
    return "Done!"


if __name__ == "__main__":
    percentile = sys.argv[1]
    orig_data = sys.argv[2]
    keep_indices = sys.argv[3]
    data1 = sys.argv[4]
    data2 = sys.argv[5]
    files = sys.argv[6:]
    # switched these to always be true since now calculating similarity
    AisSim = True
    BisSim = True
    if data1 == "rouge1":
        AisSim = True
    if data2 == "rouge2":
        BisSim = True
    for i in range(len(files)):
        if "human" in files[i]:
            if i == 0:
                AisSim = True
            else:
                BisSim = True
    if len(files) == 2:
        dataDict = process_files(keep_indices, files[0], files[1])
    else:
        dataDict = process_files(keep_indices, files[0])
    get_examples(dataDict, int(percentile), orig_data, keep_indices, data1, data2, AisSim, BisSim)
    # get_overlap_examples(dataDict, int(percentile), orig_data, keep_indices, data1, data2, AisSim, BisSim)
