# Python-codes
1. extract_n_multiplex.py - to extract regions of sequences which can be amplified using specified primers and make multiple copies in multi-fasta file (multiplex) with random numbers for "n" times.

  Dependencies - fuzznuc (emboss-toolkit)

  Usage: python3.6 extract_n_multiplex.py [options]

    Options:

    -h, --help         show this help message and exit
  
    -f FORWARD_PRIMER  forward-primer
  
    -r REVERSE_PRIMER  reverse-primer
  
    -n NITER           (default 1) number of iterations to repeat random
                       multiplexing of extracted sequences
                     
    -d SEQDATA         multifasta sequence file from which regions will be
                       extracted
  
  2. seq_stat.py - extract count of each letters(nucleotide/amino acids) and seuence length in each sequence in fasta file.
  
   Dependencies - BioPython (In case you don't have BioPython, use https://github.com/drdee255/Perl-Bioinformatics/blob/master/seq_stat.pl)
    
   Usage: python3.6 seq_stat.py -i input.fasta -o output.txt
   
   Options:
   
    -h, --help            show this help message and exit.
    
    -i INPUTFILE, --input=INPUTFILE	input fasta/multi-fasta file (protein/nucleotide).
    
    -o OUTPUTFILE, --output=OUTPUTFILE	output file name(tab-separated).
  3. csv2LibSVM.R - convert .csv to .libsvm format
   
   Usage: csv2LibSVM.R inputFileName positiveClassName outFileName
    
