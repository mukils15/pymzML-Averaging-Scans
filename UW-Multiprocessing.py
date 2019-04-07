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

def getSpectralAverageAndWriteToFile(filepathPair):
    #print ("Time when function actually called:" ,time.time())
    filepath = filepathPair[0]
    num = filepathPair[1]
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
    # print (mz_i_tuples)
    #trace = go.Scatter(x=spectrum.mz, y=avg_i)
    #data = [trace]
    #py.iplot(data, filename = filepath + ' .png')
    plt.plot(spectrum.mz, avg_i)
    plt.xlabel("m/z")
    plt.ylabel('Intensity')

    # write spectra to another file
    # run = pymzml.run.Reader(filepath, MS1_Precision = 5e-6, MSn_Precision = 20e-6)
    # write_run = pymzml.run.Writer(filename='write_test.mzML', run=run , overwrite=True)

    plt.savefig(filepath + str(num) + '.png')


if __name__ == '__main__':
    text_file_path = "C:\\Bruker Files"
    mzml_file1 = os.path.join(text_file_path, "MS2-ESI-ISO.mzML")
    mzml_file2 = os.path.join(text_file_path, "MS2-ESI-ISO2.mzML")
    mzml_file3 = os.path.join(text_file_path, "MS3-ETD-CID.mzML")
    x = 1
    lowest_time = 100000;
    print ("CPU Count ", multiprocessing.cpu_count())


    mzmlFileArray = []


    fileArrayLen = 0
    
    while fileArrayLen < 100:
        listToExtend = [[mzml_file1, fileArrayLen*3],[mzml_file2, fileArrayLen*3+1], [mzml_file3, fileArrayLen*3+2]]
        mzmlFileArray.extend(listToExtend)
        fileArrayLen += 1

    #print(mzmlFileArray)

    #exit
    
    #t_init = time.time()
    #for index in range(len(mzmlFileArray)):
    #   getSpectralAverageAndWriteToFile(mzmlFileArray[index])
    #t_fin = time.time()
    #avg_time = (t_fin-t_init)
    #print("Average time for non-parallel processing: ", avg_time)
    #print ("Average time per file: ", (avg_time/(len(mzmlFileArray))))

    while x<5:
       p = Pool(x)

       t4 = time.time()
       p.map(getSpectralAverageAndWriteToFile, mzmlFileArray)
       t5 = time.time()
       time_elapsed3 = t5-t4
       print ("Time elapsed: ", time_elapsed3, " for ", x, "processes with no chunks")
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
       #    print("The new lowest time is ", time_elapsed, " for ", x, " processes")
        #   lowest_time = time_elapsed
       x = x+1

 




