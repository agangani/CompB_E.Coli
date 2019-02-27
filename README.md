# CompB_E.Coli

Previously, researchers have revisted sequencing of the E.coli K12 strain as it has evolved over time since when the whole genome was first sequenced. The purpose of this project is to resequence the E.coli K12 genome to see how it has evolved over time.

Here are the following tools you will need to have installed in order to successfully run the code on python3:
1. SPAdes v3.11.1
2. prokka 
3. tophat2 v2.1.1
4. cufflinks v2.2.1
5. SRA-tool kit
6. wget 

In general, the python3 code is a step by step guide to retrieving the required sequence, assembling the genome, annotating the assembly, analyzing the discprencies from the assembled genome in RefSeq for E.coli K-12 (NC_000913), building an index, aligning the genome sequence to the reference sequnce, and finally assembling the reads. 

According to the code, all the files will be located in OptionA_Anusha_Gangani, however, that can be modified in the code to fit the user's preferred folder name. In addition, there is an OptionA.log file under the OptionA_Anusha_Gangani directory where the user can find the following summary: 
1. SPAdes command
2. prokka command
3. # of contigs in the genome over 1000
4. # of base pairs in those contigs
5. Annotation results from prokka 
6. Discrepancies with the assembled genome E.coli K12 (NC_000913)


To download:
1. $git clone https://github.com/agangani/CompB_E.Coli.git
2. python3 E.coli_K12_Reseq.py




Author: Anusha Gangani

