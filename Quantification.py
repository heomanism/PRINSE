import sys,re,os,string,glob,subprocess
import queue,threading,time

os.getcwd()

def Quantification(Conv_Sort_DIR,INDEXING_DIR,Quantification_DIR,NUM_THREAD,ID_list,RNA_strandness_Feature,ANNOTATION_FILE):
    # Investigating Target Samples
    os.chdir(Quantification_DIR)

    QUANT_FILE_LIST = list()

    for i in range(0,len(ID_list),2):
        Sort_file = Conv_Sort_DIR + "/" + ID_list[i] + ".Sorted.bam"
        INDEX_file= INDEXING_DIR + "/" + ID_list[i] + ".index"

        QUANTI_file = Quantification_DIR + "/" + ID_list[i] + "_counts.txt"
        if((os.path.exists(Sort_file) == False) | (os.path.exists(INDEX_file) == False)):
            print("You have inappropriate %s's input. Please check your input file." %(ID_list[i]))
        else:
            if((os.path.exists(QUANTI_file) == False)):
                print("Start %s's Quantification Process !!\n" % (ID_list[i]))
                QUANT_FILE_LIST.append(ID_list[i])
            else:
                print("%s is existed, Skip Quantification Process\n"%(ID_list[i]))

    print("Target Samples : %s\n" % (QUANT_FILE_LIST))

    if(len(QUANT_FILE_LIST)!=0):
        PER_THREAD = NUM_THREAD//len(QUANT_FILE_LIST)
        print("You have %s Samples.\n" % (len(QUANT_FILE_LIST)))
        print("Threads for Indexing Process per sample : %s\n"%(PER_THREAD))

        # Execution
        processes=[]

        start=time.time()
        for i in range(0,len(QUANT_FILE_LIST),1):
            # Samtools index cmd
            cmd ='/data/bin/subread/featureCounts -T %s -s %s -p -t exon -g gene_id -a %s -o %s/%s_counts.txt %s/%s.Sorted.bam'% (PER_THREAD,RNA_strandness_Feature,ANNOTATION_FILE,Quantification_DIR,QUANT_FILE_LIST[i],Conv_Sort_DIR,,QUANT_FILE_LIST[i])

            processes.append(subprocess.Popen([cmd],shell=True))

        for proc in processes:
            proc.communicate()
        end=time.time()

        print("Finished in %.3f seconds" % (end-start))
    else:
        print("Indexing proceess is already done. Please check your Indexing output file.")

