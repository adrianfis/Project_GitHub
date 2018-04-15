import glob, gzip
import matplotlib.pyplot as plt
import numpy as np

def Convolve(data, width):
  return np.convolve(data, np.ones((width,))/width)[width-1:]

def readTSVlc(filename):
  datafile = gzip.open(filename)
  time, rate, uncertainty = [], [], []
  for line in datafile:
    split = line.split()
    time.append(float(split[0]))
    rate.append(float(split[1]))
    uncertainty.append(float(split[2]))
  return time, rate, uncertainty

lcfiles = sorted(glob.glob('proc-1chan-4ms/*data.gz'),reverse=True)

for filename in lcfiles[:5]:
  time, rate, uncertainty = readTSVlc(filename)
  plt.plot(time, rate, label = 'original')
  plt.plot(time, Convolve(rate,100), label='convolve 100')
  plt.title(filename)
  plt.legend()
  plt.show()
