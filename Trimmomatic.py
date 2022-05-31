import sys,re,os,string,glob,subprocess
import queue,threading,time

os.getcwd()
def Trimmomatic(NUM_THREAD,FASTQ_DIR,FASTQ_list,Trimm_id_list,paired_dir,unpaired_dir,adapter,SeedMismatches,PalindromClipThreshold,SimpleClipThreshold,LEADING,TRAILING,Windowsize,ReQuiredQuality,MINLEN,TRIM_DIR,ID_list):
    # Investigating Target Samples
    os.chdir(TRIM_DIR)

    TRIM_FILE_LIST = list()
    TRIM_FILE_PE_LIST = list()
    for i in range(0,len(Trimm_id_list),2):
        fastq_file_1 = FASTQ_list[i]
        fastq_file_2 = FASTQ_list[i+1]

        file_1= TRIM_DIR + "/Paired/" + Trimm_id_list[i] + ".paired.fq.gz"
        file_2= TRIM_DIR + "/Paired/" + Trimm_id_list[i+1] + ".paired.fq.gz"

        if((os.path.exists(fastq_file_1) == False) | (os.path.exists(fastq_file_2) == False) | (os.path.exists(adapter) == False)):
            print("You have inappropriate %s's input. Please check your fastq file or adapter." %(ID_list[i]))
        else:
            if((os.path.exists(file_1) == False) & (os.path.exists(file_2) == False)):
                TRIM_FILE_LIST.append(ID_list[i])
                TRIM_FILE_PE_LIST.append(Trimm_id_list[i])
                TRIM_FILE_PE_LIST.append(Trimm_id_list[i+1])
                print("Start %s's Trimming Process\n"%(ID_list[i]))
            else:
                print("%s is existed, Skip Trimming Process\n"%(ID_list[i]))

    print("Target Samples : %s\n" % (TRIM_FILE_LIST))

    if(len(TRIM_FILE_LIST)!=0):
        PER_THREAD = NUM_THREAD//len(TRIM_FILE_LIST)
        print("You have %s Samples.\n" % (len(TRIM_FILE_LIST)))
        print("Threads for Trimming Process per sample : %s\n"%(PER_THREAD))
        # Execution
        processes=[]

        start=time.time()
        for i in range(0,len(TRIM_FILE_LIST),1):
            # Trimmomatic cmd
            cmd ='java -jar /data/bin/trimmomatic-0.33.jar PE -threads %s -phred33 %s/%s.fastq.gz %s/%s.fastq.gz %s/%s.paired.fq.gz %s/%s.unpaired.fq.gz %s/%s.paired.fq.gz %s/%s.unpaired.fq.gz ILLUMINACLIP:%s:%s:%s:%s LEADING:%s TRAILING:%s SLIDINGWINDOW:%s:%s MINLEN:%s 2> %s/%s.log'%(PER_THREAD,FASTQ_DIR,TRIM_FILE_PE_LIST[2*i],FASTQ_DIR,TRIM_FILE_PE_LIST[2*i+1], paired_dir,TRIM_FILE_PE_LIST[2*i], unpaired_dir,TRIM_FILE_PE_LIST[2*i], paired_dir,TRIM_FILE_PE_LIST[2*i+1], unpaired_dir,TRIM_FILE_PE_LIST[2*i+1],adapter,SeedMismatches,PalindromClipThreshold,SimpleClipThreshold,LEADING,TRAILING,Windowsize,ReQuiredQuality,MINLEN,TRIM_DIR,TRIM_FILE_LIST[i])
            processes.append(subprocess.Popen([cmd],shell=True))

        for proc in processes:
            proc.communicate()

        end=time.time()

        print("Finished in %.3f seconds" % (end-start))

    else:
        print("Trimming proceess is already done. Please check your Trimming output file.")
