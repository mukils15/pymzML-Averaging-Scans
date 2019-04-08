import multiprocessing
import os.path
import time
import pymzml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import plotly.plotly as py
import plotly.graph_objs as go
import time
import argparse
import sys

def create_arg_parser():
    #Creates and returns the ArgumentParser object, which defines the arguments to the script
    parser = argparse.ArgumentParser(description='Description of your app.')

    #Argument for the file input directory
    parser.add_argument('inputDirectory',
                    help='Path to the input directory.')
    #Argument for the file output directory - optional
    parser.add_argument('--outputDirectory',
                    help='Path to the output that contains the resumes.')
    #Argument for the number of processes to be used - optional
    parser.add_argument('--numProcesses',
                        help='Number of processes used for multiprocessing')
    #Argument for the chunk size - optional
    parser.add_argument('--chunkSize',
                        help='Chunk size used for multiprocessing map')
    return parser


def getSpectralAverageAndWriteToFile(inputFilepath):
    #Initalize mzml reader for given file path
    msrun = pymzml.run.Reader(inputFilepath, MS_precisions={1:5e-6, 2:20e-6, 3:20e-6})

    # Get length of any one spectrum
    spec_length = len(msrun[2].mz)

    # initialize list to hold averages
    total_i = [0] * spec_length

    # initialize var to count number of spectra in file
    numspectra = 0

    #Initialize reader
    msrun2 = pymzml.run.Reader(inputFilepath, MS_precisions={1:5e-6, 2:20e-6, 3:20e-6})

    # compute number of spectra in file and store total intensity at each point in single list
    for spectrum in msrun2:
        numspectra += 1
        x = 0
        while x < spec_length:
            total_i[x] = total_i[x] + spectrum.i[x]
            x += 1


    # compute average intensity at each point across all spectra
    avg_i = [item / numspectra for item in total_i]
    mz_i_tuples = list(zip(spectrum.mz, avg_i))

    #Create plot for the average mz/i for the given file
    plt.clf()
    plt.plot(spectrum.mz, avg_i)
    plt.xlabel("m/z")
    plt.ylabel('Intensity')

    #Save plot to output file
    plt.savefig(inputFilepath + '.png')


if __name__ == '__main__':
    ## Enstantiating arg_parser to get arguments from user in command prompt
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    #Save the input directory given by user as variable to be used
    mzmlInputDir = parsed_args.inputDirectory

    #Make sure that directory exists
    if os.path.exists(mzmlInputDir):
        print("File exists")


    # Because numProcesses is an optional argument, check first if it is not None. If not none, then save the value by user as variable to be used. If none, default to 3 processes
    if parsed_args.numProcesses is not None:
        nP = int(parsed_args.numProcesses)
    else:
        nP = 3

    # Because chunkSize is an optional argument, check first if it is not None. If not none, then save the value by user as variable to be used. If none, default to 5 files
    if parsed_args.chunkSize is not None:
        nC = int(parsed_args.chunkSize)
    else:
        nC = 5

    # Because outputDirectory is an optional argument, check first if it is not None. If not none, then save the value by user as variable to be used. If none, default to inputDirectory
    # Still in progress
    if parsed_args.outputDirectory is not None:
        oD = parsed_args.outputDirectory
    else:
        oD = mzmlInputDir


    #Create array of file paths with every file from input file directory
    #This array will be used to map in multiprocessing
    mzmlFileArray = []
    for root, dirs, files in os.walk(mzmlInputDir):
        for file in files:
            if file.endswith(".mzML"):
                full_file_path = os.path.join(root,file)
                print(full_file_path)
                mzmlFileArray.append(full_file_path)


    # Test print to check how many logical processors the machine has
    print ("CPU Count ", multiprocessing.cpu_count())

    #Begin multiprocessing - start by creating pool with numProcesses different processes
    p = Pool(nP)

    # Map the getSpectralAverageAndWriteToFile function to every file in mzmlFileArray, which contains every file in the input directory. Use chunk size nC
    # Measure total time it took as a measure of effectiveness of multiprocessing
    t0 = time.time()
    p.map(getSpectralAverageAndWriteToFile, mzmlFileArray, nC)
    t1 = time.time()
    time_elapsed1 = t1-t0

    # Print statements to check results
    print ("Time elapsed: ", time_elapsed1, " for ", nP, "processes with chunk size=", nC)
    print ("Average time per file: ", (time_elapsed1/(len(mzmlFileArray))))





 




