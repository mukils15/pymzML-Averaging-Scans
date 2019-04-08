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
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(description='Description of your app.')
    parser.add_argument('inputDirectory',
                    help='Path to the input directory.')
    parser.add_argument('--outputDirectory',
                    help='Path to the output that contains the resumes.')
    #parser.add_argument('--numProcesses',
                        #help='Number of processes used for multiprocessing')
    #parser.add_argument('--chunkSize',
                        #help='Chunk size used for multiprocessing map')
    return parser


def getSpectralAverageAndWriteToFile(filepath):
    #print ("Time when function actually called:" ,time.time())
    msrun = pymzml.run.Reader(filepath, MS_precisions={1:5e-6, 2:20e-6, 3:20e-6})
    # Get length of any one spectrum
    spec_length = len(msrun[2].mz)
    # print(spec_length)

    # initialize list to hold averages
    total_i = [0] * spec_length

    # initialize var to count number of spectra in file
    numspectra = 0

    # compute number of spectra in file and store total intensity at each point in single list
    msrun2 = pymzml.run.Reader(filepath, MS_precisions={1:5e-6, 2:20e-6, 3:20e-6})
    for spectrum in msrun2:
        numspectra += 1
        x = 0
        while x < spec_length:
            total_i[x] = total_i[x] + spectrum.i[x]
            x += 1

    # debug print
    #print(numspectra)

    # compute average intensity at each point across all spectra
    avg_i = [item / numspectra for item in total_i]
    mz_i_tuples = list(zip(spectrum.mz, avg_i))
    plt.plot(spectrum.mz, avg_i)
    plt.xlabel("m/z")
    plt.ylabel('Intensity')


    plt.savefig(filepath + '.png')


if __name__ == '__main__':
    ## Trying out the arg_parser to see if file paths can be passed from command-line
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    mzmlInputDir = parsed_args.inputDirectory
    if os.path.exists(mzmlInputDir):
        print("File exist")

    mzmlFileArray = []
    for root, dirs, files in os.walk(mzmlInputDir):
        for file in files:
            if file.endswith(".mzML"):
                full_file_path = os.path.join(root,file)
                print(full_file_path)
                mzmlFileArray.append(full_file_path)

    x = 1


    print ("CPU Count ", multiprocessing.cpu_count())


    while x<5:
        p = Pool(x)

        t4 = time.time()
        p.map(getSpectralAverageAndWriteToFile, mzmlFileArray)
        t5 = time.time()
        time_elapsed3 = t5-t4
        print ("Time elapsed: ", time_elapsed3, " for",x, "processes with no chunks")
        print ("Average time per file: ", (time_elapsed3/(len(mzmlFileArray))))
       
        t0 = time.time()
        p.map(getSpectralAverageAndWriteToFile, mzmlFileArray, 5)
        t1 = time.time()
        time_elapsed1 = t1-t0
        print ("Time elapsed: ", time_elapsed1, " for ", x, "processes with chunk size=5")
        print ("Average time per file: ", (time_elapsed1/(len(mzmlFileArray))))
       
        t2 = time.time()
        p.map(getSpectralAverageAndWriteToFile, mzmlFileArray, 10)
        t3 = time.time()
        time_elapsed2 = t3-t2
        print ("Time elapsed: ", time_elapsed2, " for ", x, "processes with chunk size=10")
        print ("Average time per file: ", (time_elapsed2/(len(mzmlFileArray))))
       
        #if time_elapsed<lowest_time:
        #   print("The new lowest time is ", time_elapsed, " for ", x, " processes")
        #   lowest_time = time_elapsed
        x = x+1

 




