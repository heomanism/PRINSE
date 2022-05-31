import sys,re,os,string,glob

def getTrimmomaticID(Sample_List):
    with open(Sample_List) as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]

    Trim_ID_list = list()
    for sample in lines:
        tmp_ID = sample.split('/')[5].split('.')[0]
        Trim_ID_list.append(tmp_ID)

    return Trim_ID_list

def getID(Sample_List):
    with open(Sample_List) as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]

    ID_list = list()
    for sample in lines:
        tmp_ID_list = sample.split('/')[5].split('_')
        tmp_ID = tmp_ID_list[0] + "_" + tmp_ID_list[1] + "_" + tmp_ID_list[2]
        ID_list.append(tmp_ID)

    return ID_list

def getFASTQ(Sample_List):
    with open(Sample_List) as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    return lines

def MakeTmpDir(TMP_DIR,ID_list):
    os.chdir(TMP_DIR)

    for i in range(0,len(ID_list),2):
        os.makedirs(ID_list[i],exist_ok=True)

