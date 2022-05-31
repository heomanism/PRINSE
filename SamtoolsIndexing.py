import sys,re,os,string,glob,subprocess
import queue,threading,time

os.getcwd()
def Indexing(Conv_Sort_DIR,INDEXING_DIR,NUM_THREAD,ID_list):
    # Investigating Target Samples
    os.chdir(INDEXING_DIR)

    INDEX_FILE_LIST = list()

    for i in range(0,len(ID_list),2):
        Sort_file = Conv_Sort_DIR + "/" + ID_list[i] + ".Sorted.bam"

        INDEX_file= INDEXING_DIR + "/" + ID_list[i] + ".index"
        if((os.path.exists(Sort_file) == False)):
            print("You have inappropriate %s's input. Please check your paired Sorted bam file." %(ID_list[i]))
        else:
            if((os.path.exists(INDEX_file) == False)):
                print("Start %s's Indexing Process !!\n" % (ID_list[i]))
                INDEX_FILE_LIST.append(ID_list[i])
            else:
                print("%s is existed, Skip Indexing Process\n"%(ID_list[i]))

    print("Target Samples : %s\n" % (INDEX_FILE_LIST))

    if(len(INDEX_FILE_LIST)!=0):
        PER_THREAD = NUM_THREAD//len(INDEX_FILE_LIST)
        print("You have %s Samples.\n" % (len(INDEX_FILE_LIST)))
        print("Threads for Indexing Process per sample : %s\n"%(PER_THREAD))

        # Execution
        processes=[]

        start=time.time()
        for i in range(0,len(INDEX_FILE_LIST),1):
            # Samtools index cmd
            cmd ='/data/bin/samtools index %s/%s.Sorted.bam -@ %s -b %s/%s.index' % (Conv_Sort_DIR,INDEX_FILE_LIST[i],PER_THREAD,INDEXING_DIR,INDEX_FILE_LIST[i])

            processes.append(subprocess.Popen([cmd],shell=True))

        for proc in processes:
            proc.communicate()
        end=time.time()

        print("Finished in %.3f seconds" % (end-start))
    else:
        print("Indexing proceess is already done. Please check your Indexing output file.")
