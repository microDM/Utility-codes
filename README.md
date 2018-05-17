# Python-codes
1. extract_n_multiplex.py - to extract regions of sequences which can be amplified using specified primers and make multiple copies in multi-fasta file (multiplex) with random numbers for "n" times.
Usage: python3.6 extract_n_multiplex.py [options]
Options:
  -h, --help         show this help message and exit
  -f FORWARD_PRIMER  forward-primer
  -r REVERSE_PRIMER  reverse-primer
  -n NITER           (default 1) number of iterations to repeat random
                     multiplexing of extracted sequences
  -d SEQDATA         multifasta sequence file from which regions will be
                     extracted
