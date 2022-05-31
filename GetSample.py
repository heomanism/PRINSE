import sys,re,os,string,glob

DIRECTORY = sys.argv[1]
NUM_SAMPLE = sys.argv[2]
OUTPUT_DIR = sys.argv[3]
OUTPUT_NAME = sys.argv[4]


os.chdir(DIRECTORY)
id_list=glob.glob("*.fastq.gz")

new_id_list=list()

for raw_id in id_list:
    id=  DIRECTORY + "/" +raw_id
    new_id_list.append(id)

new_id_list.sort()

if (len(new_id_list)//2)%int(NUM_SAMPLE) == 0:
    Cluster = range(0,(len(new_id_list)//2//NUM_SAMPLE))
else:
    Cluster = range(0,(len(new_id_list)//2//NUM_SAMPLE) + 1)

for i in Cluster:
    file_name = OUTPUT_DIR + "/" + OUTPUT_NAME + "_v" + str(i+1)+ ".txt"
    file = open(file_name,"w")
    for fq in new_id_list[(2*i*int(NUM_SAMPLE)):(2*(i+1)*int(NUM_SAMPLE))]:
        file.write(fq+'\n')
    file.close()
