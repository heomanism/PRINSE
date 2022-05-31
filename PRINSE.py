import sys,re,os,string,glob,argparse
import queue, threading,time
os.getcwd()
sys.path.append("/home2/mheo/RNA_seq_Pre_preprocessing")
import GetID
import Trimmomatic
import HISAT2
import SamtoolsIndexing
import Quantification

## 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description='Whole Genome Sequencing Germline Variant Calling made by Min Heo')

## 입력받을 인자값 등록 , 필수 값은 required=True해야함
parser.add_argument('-Dp', required=True, help='RNA seq pre-processing Directory')
parser.add_argument('-Ds', required=True, help='Input Sample list: txt file')
parser.add_argument('-Df', required=True, help='FASTQ DIRECTORY')
parser.add_argument('-t', required=True, help='Threads Number')
parser.add_argument('-a', required=True, help='Adapter file for Trimmomatic')
parser.add_argument('-I', required=True, help='Reference HISAT2 INDEX')
parser.add_argument('-an', required=True, help='Annotation file in FeatureCounts')

parser.add_argument('--p', required=False, default='33', help='Tophred number (33)')
parser.add_argument('--m', required=False, default='2', help="Trimmomatic's mismatch numbers (2)")
parser.add_argument('--pthr', required=False, default='30', help="Trimmomatic's Palindrome Clip Threshold (30)")
parser.add_argument('--sthr', required=False, default='10', help="Trimmomatic's Simple Clip Threshold (10)")
parser.add_argument('--l', required=False, default='3', help="Trimmomatic's Leading (3)")
parser.add_argument('--trail', required=False, default='3', help="Trimmomatic's Trailing (3)")
parser.add_argument('--w', required=False, default='4', help="Trimmomatic's Window Sliding Size (4)")
parser.add_argument('--q', required=False, default='15', help="Trimmomatic's requiredQuality (15)")
parser.add_argument('--ml', required=False, default='36', help="Trimmomatic's MINLENGTH (36)")

parser.add_argument('--strand',required=False, default=' ', help="HISAT2's --rna-strandness (none)")

parser.add_argument('--strandFeature',required=False, default='0', help="FeatureCounts's -s (0)")
## 입력받은 인자값을 args에 저장 (type: namespace)

## 작업할 때.
#args_str="-Dp /home/ubuntu/Variant_Calling/Python_Version/toy/Toy_Pipeline -Df /data/WGS_Toy_data -t 10 -a /program/Trimmomatic-0.39/adapters/TruSeq3-PE-2.fa -R /data/WGS_Reference/hg19/ucsc.hg19.chr.only.fasta -Ri /data/WGS_Reference/hg19/ucsc.hg19.chr.only.fasta.fai -K /data/WGS_Reference/hg19/dbsnp_151.hg19.vcf"
#args,_= parser.parse_known_args(args=args_str.split())

args=parser.parse_args()

##########################################
#        Step 0. Pre-Processing          #
##########################################
# Making Directory
WORK_DIRCTROY = args.Dp
os.chdir(WORK_DIRCTROY)

dirs=["0.TMP","1.Trimmomatic",
"2.Mapping","3.Converting_Sorting",
"4.Indexing","5.Quantification",
"1.Trimmomatic/Paired","1.Trimmomatic/Unpaired"]

for dir in dirs:
    os.makedirs(dir,exist_ok=True)

# Variables for Pipeline
# Necessary Args.
PIPELINE_DIR = args.Dp
SAMPLE_LIST = args.Ds
FASTQ_DIR = args.Df
NUM_THREAD = int(args.t)

Adapter = args.a
INDEX_FILE = args.I

# Unnecessary Args.
## Trimmomatic
TophredNumber = args.p
SeedMismatches = args.m
PalindromClipThreshold = args.pthr
SimpleClipThreshold = args.sthr
LEADING = args.l
TRAILING = args.trail
Windowsize = args.w
ReQuiredQuality = args.q
MINLEN = args.ml

## HISAT2
if args.strand == ' ':
    RNA_strandness = args.strand
else:
    RNA_strandness = ' --rna-strandness ' + args.strand + ' '

## FeatureCounts
ANNOTATION_FILE = args.an
RNA_strandness_Feature = args.strandFeature

# Dir Args.
TMP_DIR =PIPELINE_DIR + "/" + dirs[0]
TRIM_DIR =PIPELINE_DIR + "/" + dirs[1]
MAPPING_DIR =PIPELINE_DIR + "/" + dirs[2]
Conv_Sort_DIR =PIPELINE_DIR + "/" + dirs[3]
INDEXING_DIR = PIPELINE_DIR + "/" + dirs[4]
Quantification_DIR =PIPELINE_DIR + "/" + dirs[5]
paired_dir =PIPELINE_DIR + "/" + dirs[6]
unpaired_dir =PIPELINE_DIR + "/" + dirs[7]

# Get Sample ID 
Trimm_id_list =GetID.getTrimmomaticID(SAMPLE_LIST) # Trimmomatic ID list
ID_list=GetID.getID(SAMPLE_LIST) # ID list
FASTQ_list = GetID.getFASTQ(SAMPLE_LIST) # FASTQ list
print(ID_list)

# Making TMP Dir for each sample
GetID.MakeTmpDir(TMP_DIR,ID_list)

##########################################
#          Step 1. Trimmomatic           #
########################################## 
Trimmomatic.Trimmomatic(NUM_THREAD,FASTQ_DIR,FASTQ_list,Trimm_id_list,paired_dir,unpaired_dir,Adapter,SeedMismatches,PalindromClipThreshold,SimpleClipThreshold,LEADING,TRAILING,Windowsize,ReQuiredQuality,MINLEN,TRIM_DIR,ID_list)

##########################################
#          Step 2. HISAT2                #
########################################## 
HISAT2.HISAT2(NUM_THREAD,RNA_strandness,INDEX_FILE,TRIM_DIR,ID_list,Trimm_id_list,paired_dir,MAPPING_DIR,Conv_Sort_DIR)

##########################################
#          Step 3. Indexing              #
########################################## 
SamtoolsIndexing.Indexing(Conv_Sort_DIR,INDEXING_DIR,NUM_THREAD,ID_list)

##########################################
#       Step 4. Quantification           #
########################################## 
Quantification.Quantification(Conv_Sort_DIR,INDEXING_DIR,Quantification_DIR,NUM_THREAD,ID_list,RNA_strandness_Feature,ANNOTATION_FILE)

