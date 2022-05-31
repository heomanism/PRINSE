import sys,re,os,string,glob,subprocess
import queue,threading,time

os.getcwd()
def HISAT2(NUM_THREAD,RNA_strandness,INDEX_FILE,TRIM_DIR,ID_list,Trimm_id_list,paired_dir,MAPPING_DIR,Conv_Sort_DIR):
    # Investigating Target Samples
    os.chdir(MAPPING_DIR)

    MAP_FILE_LIST = list()

    for i in range(0,len(ID_list),2):
        file_1= TRIM_DIR + "/Paired/" + Trimm_id_list[i] + ".paired.fq.gz"
        file_2= TRIM_DIR + "/Paired/" + Trimm_id_list[i+1] + ".paired.fq.gz"

        Map_file = MAPPING_DIR + "/" + ID_list[i] + ".log"
        Sort_file = Conv_Sort_DIR + "/" + ID_list[i] + ".Sorted.bam"

        if((os.path.exists(file_1) == False) | (os.path.exists(file_2) == False)):
            print("You have inappropriate %s's input. Please check your paired fastq file or Reference files." %(ID_list[i]))
        else:
            if((os.path.exists(Map_file) == False) & (os.path.exists(Sort_file) == False)):
                print("Start %s's Mapping Process !!\n" % (ID_list[i]))
                MAP_FILE_LIST.append(ID_list[i])
            else:
                print("%s is existed, Skip Mapping Process\n"%(ID_list[i]))

    print("Target Samples : %s\n" % (MAP_FILE_LIST))

    if(len(MAP_FILE_LIST)!=0):
        PER_THREAD = NUM_THREAD//len(MAP_FILE_LIST)
        print("You have %s Samples.\n" % (len(MAP_FILE_LIST)))
        print("Threads for Mapping Process per sample : %s\n"%(PER_THREAD))
        # Set Memory 
        Memory=os.popen("free -m | grep ^Mem | awk '{print $7}'").read().strip().split('\n')
        Memory=int("".join(Memory))

        RealMemory = Memory//len(MAP_FILE_LIST)//NUM_THREAD//2

        # Execution
        processes=[]

        start=time.time()
        for i in range(0,len(MAP_FILE_LIST),1):
            # HISAT2 cmd
            cmd ='/data/bin/hisat2 -p %s%s-x %s -1 %s/%s.paired.fq.gz -2 %s/%s.paired.fq.gz 2> %s/%s.log | samtools view -b | /data/bin/samtools sort -m %sM -@ %s -o %s/%s.Sorted.bam '%(PER_THREAD,RNA_strandness,INDEX_FILE,paired_dir,Trimm_id_list[2*i],paired_dir,Trimm_id_list[2*i+1],MAPPING_DIR,MAP_FILE_LIST[i],RealMemory,PER_THREAD,Conv_Sort_DIR,MAP_FILE_LIST[i])
            processes.append(subprocess.Popen([cmd],shell=True))

        for proc in processes:
            proc.communicate()
        end=time.time()

        print("Finished in %.3f seconds" % (end-start))

    else:
        print("Mapping proceess is already done. Please check your Mapping output file.")     

