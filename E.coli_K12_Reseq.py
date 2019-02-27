
# coding: utf-8

# In[2]:


import os 
import argparse
import time
from Bio import SeqIO

#Gets the current directory of the user without any unwanted characters 
directory = os.popen('pwd').read().rstrip()

#Set the path to a variable which can be called later without having to write the entire path every time
current_direct = (directory + '/OptionA_Anusha_Gangani/')

#System command that allows the user to use the functionality in python to make the OptionA_Firstname_Lastname folder 
#using the variable created above for the pathway of the directory
os.system('mkdir ' + current_direct)

#Set the variable to the specified path 
os.chdir(current_direct)

#The os.system allows you to use the wget command to retrieve the illumina sequence reads from NCBI through an sra file.  
#The specific sequence is a single-end illumina read

os.system('wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra')
#Output: SRR8185310.sra
#This sra file is found in the OptionA_Anusha_Gangani folder


#Converts the SRA file retrieved from the wget command into a fastq file in order to run it on SPAdes
os.system('fastq-dump -I SRR8185310.sra')
#Output: SRR8185310.fastq
#This file is found in the OptionA_Anusha_Gangani folder

#Opens the tool SPAdes to assemble the genome using the converted fastq file. This tool can be used for single-celled
#or multiple celled bacterial data. The -k are parameters for the assembly, -t specifies the number of processors you want to use
#-s SRR8185310.fastq is the fastq file we 
#want to assemble and the -s specifies that the sequence is a single end read
#and -o provides the output directory, which is the variable that the path is set to so the output will dump 

os.system('spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o ' + current_direct)
#Output: Assembling finished. Used k-mer sizes: 55, 77, 99
#There are 6 output files retrieved from running SPAdes: contigs.fasta, scaffolds.fasta, assembly_graph.fastg, 
#assembly_graph_with_scaffolds.gfa, contigs.paths, scaffolds.paths

#Sets the string of the SPAdes command to a variabele and prints it
spades = 'spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o ' + current_direct
print(spades)

#Allows the user to write the SPAdes command into the log file with the 'w+'. This is also the first time in the code where the log file is created
#under the OptionA_First_Lastname folder. Once it outputs the SPAdes command into the log file, it ensures 
#that future items written in the same log file print on a new line

log_file = open(current_direct + 'OptionA.log', 'w+')
for x in range(1):
    log_file.write(spades + '\n')
#open the OptionA.log file to see the following (with the user's directory) in the first line: spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o /home/agangani/OptionA_Anusha_GanganiTEST/

    
#The following set of python code determines the number of contigs that are greater than 1000
#and writes it to a specified fasta file. The output of the command is then printed into the same log, OptionA.log, 
#that was created earlier after running the SPAdes command

#Open the contigs.fasta file, which was one of the files obtained from the output of running SPAdes
contigs = ('contigs.fasta')

#Creates an empty list that will store the contigs that are greater than 1000 once it runs through the for loop
Filtered_Length=[]

#Goes through each contig in the contigs.fasta file and if it is larger than 1000, it is added to the 
#Filtered_Lenth list 
for record in SeqIO.parse("contigs.fasta", "fasta"):
    if len(record)>1000:
        Filtered_Length.append(record)
#Outputs the integer from the Filtered_Length list and prints it
Filtered_contigs = "There are %i contigs > 1000 in the assembly." %len(Filtered_Length)
print(Filtered_contigs)
#Output: There are 150 contigs > 1000 in the assembly.

#Writes the list with the contigs greater than 1000 into a fasta file, which you can find in the OptionA_Anusha_Gangani directory
SeqIO.write(Filtered_Length,"Filtered_Length.fasta","fasta")

#Writes the output, which is in 'Filtered_contigs' to the log file.  
log_file = open(current_direct + 'OptionA.log', 'a+')
for x in range(1):
    log_file.write(Filtered_contigs + '\n')
#Go into the OptionA.log file to find the output of Filtered_contigs written below the SPAdes command line:
#spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o /home/agangani/OptionA_Anusha_GanganiTEST/
#There are 150 contigs > 1000 in the assembly.

 

#The following code takes the fasta file made from the previous step, which is Filtered_Length.fasta
#and counts the number of base pairs 

#Opens the file specified
assemble = ('Filtered_Length.fasta')
#Create two counters with 1 being temporary and 1 being the final one
Total = 0
temp = 0
#Splits up the record id and the sequence
for record in SeqIO.parse("Filtered_Length.fasta", "fasta"):
    #counts the number of bases in each of the sequences and adds it to the total length 
    temp = (len(record))
    Total += temp
#Prints the total length of base pairs in the file and prints it
Base_Pairs = "There are " + str(Total) + " base pairs in the assembly."
print(Base_Pairs)
#Output: There are 4535677 base pairs in the assembly.

#Prints the output to the log file in a new line 
log_file = open(current_direct + 'OptionA.log', 'a+')
for x in range(1):
    log_file.write(Base_Pairs + '\n')

#Go into the OptionA.log file to see the following thus far:
#spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o /home/agangani/OptionA_Anusha_GanganiTEST/
#There are 150 contigs > 1000 in the assembly.
#There are 4535677 base pairs in the assembly.



#This command runs the tool prokka which annotates the assembly using the file with contigs greater than 1000, which is 
#Filtered_Length.fasta. For prokka you have to specify an output directory where you want the results to go.
#In this case a new directory will be created under OptionA_Firstname_Lastname with the name of E.Coli_Annotation_Results, that 
#is where you will find the prokka .txt file along with other file types

os.system('prokka --outdir ' + current_direct + 'E.Coli_Annotation_Results --genus Escherichia --locustag ECOL Filtered_Length.fasta')
#Output: E.Coli_Annotation_Results. This is a new directory created containing the .txt file required.  

prok = 'prokka --outdir ' + current_direct + 'E.Coli_Annotation_Results --genus Escherichia --locustag ECOL Filtered_Length.fasta'
print(prok)

#prints the prokka command to the log file
log_file = open(current_direct + 'OptionA.log', 'a+')
for x in range(1):
    log_file.write(prok + '\n')
#Output of the OptionA.log file if you were to open  it at this point:
#spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o /home/agangani/OptionA_Anusha_GanganiTEST/
#There are 150 contigs > 1000 in the assembly.
#There are 4535677 base pairs in the assembly
#prokka --outdir /home/agangani/OptionA_Anusha_GanganiTEST/E.Coli_Annotation_Results --genus Escherichia --locustag ECOL Filtered_Length.fasta
#Prokka found 4088 more CDS and 4129 less tRNA than than the RefSeq.


#Since prokka generates the file by the date you ran it, the following code makes sure it is the current date 
#so that if you ran it a few days earlier, you can still use the file without having to run it again

#Gets rid of the unwanted characters and turns it into a string as 'date'
x = (time.strftime("%x"))
date = str(x)

#Replaces the / to a space 
date = date.replace("/", "")

#Putting the date into the correct format by adding '20' to '2019'
input_file = (date[0:4] + "20" + date[4:])

#Creating a prokka file with today's date 
prokka = "PROKKA_" + input_file + ".txt"
#print(prokka)


#Writes the prokka .txt file to the OptionA.log folder
with open(current_direct + 'E.Coli_Annotation_Results/' + prokka) as new:
    with open('OptionA.log', 'a+') as output:
        for line in new:
            output.write(line)
#Output if the user were to open the OptionA.log file:
#spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o /home/agangani/OptionA_Anusha_GanganiTEST/
#There are 150 contigs > 1000 in the assembly.
#There are 4535677 base pairs in the assembly
#organism: Escherichia species strain
#contigs: 150
#bases: 4535677
#CRISPR: 2
#tmRNA: 1
#CDS: 4218
#tRNA: 52
#prokka --outdir /home/agangani/OptionA_Anusha_GanganiTEST/E.Coli_Annotation_Results --genus Escherichia --locustag ECOL Filtered_Length.fasta




#The following code looks for any discrepancies in the CDS and the tRNA value of the prokka annotations in comparison to the values of the assembled
#genome in RefSeq E.Coli K12 (NC_000913)
#creates an empty list 'dataset' to extract the CDS value and tRNA value from the prokka file
dataset=[]
Prok_Annotate = open('E.Coli_Annotation_Results/'+ prokka)
for line in Prok_Annotate:
    if line.startswith("CDS"):
        dataset.append(line)        
    if line.startswith("tRNA"):
        dataset.append(line)
#print(dataset)
#save a variable from txt into list and then go through the index and save the number as a variable 
extract_trna = dataset[0]
extract_trna = extract_trna[5:]
extract_cds = dataset[1]
extract_cds = extract_cds[5:]

#The values for the assembled genome E.Coli K12 (NC_000913) which the user compares the prokka annotation to 
CDS = 4140
tRNA = 89

#comparisions start here

#Convers 'extract_cds' and 'extract_trna to an integer in order to do the comparisons of the discrepancies
extract_cds=int(extract_cds)
cds = CDS - extract_cds
extract_trna=int(extract_trna)
trna = tRNA - extract_trna

#these loops go through each possible scenrario of the prokka annotation values being greater than or equal to or less than or equal
#to or no discrepancies 
#and outputs the absolute value of the integer 
if trna>= 0 and cds >= 0:
    a= ("Prokka found " + str(abs(cds))+ " less CDS and " + str(abs(trna)) + " less tRNA than the RefSeq.")
elif trna >= 0 and cds <0:
    a =("Prokka found " + str(abs(cds))+ " less CDS and " + str(abs(trna)) + " more tRNA than the RefSeq.")
elif trna <0 and cds >= 0:
    a = ("Prokka found " + str(abs(cds))+ " more CDS and " + str(abs(trna)) + " less tRNA than the RefSeq.")
elif trna <0 and cds <0:
    a = ("Prokka found " + str(abs(cds))+ " more CDS and " + str(abs(trna)) + " more tRNA than the RefSeq.")

#Output: Prokka found 4088 more CDS and 4129 less tRNA than than the RefSeq.

#Appends the discprencies into the OptionA.log folder in a new line 
log_file = open(current_direct + 'OptionA.log', 'a+')
for x in range(1):
    log_file.write(a + '\n')

#Output of the log file at this point:
#spades -k 55,77,99,127 -t 5 --only-assembler -s SRR8185310.fastq -o /home/agangani/OptionA_Anusha_GanganiTEST/
#There are 150 contigs > 1000 in the assembly.
#There are 4535677 base pairs in the assembly
#organism: Escherichia species strain
#contigs: 150
#bases: 4535677
#CRISPR: 2
#tmRNA: 1
#CDS: 4218
#tRNA: 52
#prokka --outdir /home/agangani/OptionA_Anusha_GanganiTEST/E.Coli_Annotation_Results --genus Escherichia --locustag ECOL Filtered_Length.fasta
#Prokka found 4088 more CDS and 4129 less tRNA than than the RefSeq.
    
#Here we use the wget commmand used earlier to retrive the K-12 derivative BW38028 in the sra file format
os.system('wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR141/SRR1411276/SRR1411276.sra')
#Output: SRR1411276.sra

#The sra file must be converted to a fastq file in order to run it into tophat2 
os.system('fastq-dump -I SRR1411276.sra')
#Output: SRR1411276.fastq

#Retrieves the sequence for the completed annotated genome for E.Coli K-12, in which it will be mapped against the K-12 derivative sequence
os.system('wget ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna')
#Output: NC_000913.fna

#Creates the index to run tophat2
os.system('bowtie2-build NC_000913.fna EcoliK12')
#Output files:
#EcoliK12.1.bt2                   
#EcoliK12.2.bt2                      
#EcoliK12.3.bt2                   
#EcoliK12.4.bt2 
#EcoliK12.rev.1.bt2
#EcoliK12.rev.2.bt2


#The tool tophat2 aligns the genome sequence to the reference sequence
os.system('tophat2 --no-novel-juncs -o ' + current_direct + ' EcoliK12 SRR1411276.fastq')
#Output file: accepted_hits.bam


#Cufflinks assembles the reads from the output of tophat2
os.system('cufflinks -p 2 accepted_hits.bam')
#Ouput file: transcripts.gtf

