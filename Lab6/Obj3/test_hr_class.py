# -*- coding: utf-8 -*-
"""
Created on Sun May 12 22:45:11 2019

@author: Michael K
"""

from Hr_basic import Hr
import numpy as np
import matplotlib.pyplot as plt

hr = Hr("ir_data_train.csv")

data_time_tr, data_ir_tr = np.loadtxt("ir_data_train.csv", delimiter=",", skiprows=1, unpack=True)
data_time_val, data_ir_val = np.loadtxt("ir_data_validation.csv", delimiter=",", skiprows=1, unpack=True)

#hr.plot_histo(data_ir_val)
#hr.plot_labels(data_time_val, data_ir_val)


i = 300
j = 0

while (data_time_tr[i] - data_time_tr[300] < 5):
    i = i + 1
    
while (data_time_val[j] - data_time_val[0] < 5):
    j = j + 1
    
[times, hr_rate] = hr.process(data_time_tr[300:i+1],data_ir_tr[300:i+1])
[times2, hr_rate2] = hr.process(data_time_val[0:j+1],data_ir_val[0:j+1])

plt.figure()
plt.plot(times,hr_rate)
plt.xlabel("Time")
plt.ylabel("BPM")

plt.figure()
plt.plot(times2,hr_rate2)
plt.xlabel("Time")
plt.ylabel("BPM")