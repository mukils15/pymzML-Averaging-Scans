# pymzML-Averaging-Scans
Using the pymzML moldule to process raw mass spectroscopy data in the form of mzml files. The goal is to produce mzml files with average scans from the initial mzml files, which had multiple scans. 

Usage: 
The script is called UW_Multiprocessing.py and takes a mandatory argument for the input file directory where all fo the mzml files to be analyzed reside, as well as optional arguments for the number of processes to be used in the multiprocessing logic which computes averages of the spectra in each file and generates a plot. Another optional argument is the chunk size indicating how many files are to be allotted to each process at a time. THe output files are written to the same directory as the input files as of now, but I am working on adding an additional optional argument to allow the user to specify the output file directory. 

C:\Users\Mukil>python C:\Users\Mukil\PycharmProjects\Test\UW-Multiprocessing.py "C:\Bruker Files" --numProcesses 5 --chunkSize 10
File exist
C:\Bruker Files\MS2-ESI-ISO.mzML
C:\Bruker Files\MS2-ESI-ISO2.mzML
C:\Bruker Files\MS3-ETD-CID.mzML
CPU Count  4
Time elapsed:  7.357267379760742  for  5 processes with chunk size= 10
Average time per file:  2.4524224599202475


