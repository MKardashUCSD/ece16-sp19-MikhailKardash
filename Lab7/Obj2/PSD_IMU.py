# -*- coding: utf-8 -*-
"""
Created on Sun May 19 22:46:36 2019

@author: Michael K
"""

import scipy.signal as ss
import matplotlib.pyplot as plt


read_filename1 = "data_train_ax.csv"
read_filename2 = "data_train_ay.csv"
read_filename3 = "data_train_az.csv"
read_file1 = open(read_filename1, 'r')
read_file2 = open(read_filename2, 'r')
read_file3 = open(read_filename3, 'r')
read_file1.readline()
read_file2.readline()
read_file3.readline()

x_dat = []
t1_dat = []
y_dat = []
t2_dat = []
z_dat = []
t3_dat = []

for line in read_file1:
    t, y, imu = line.split(',')                
    x_dat.append(float(imu.strip()))
    t1_dat.append(float(t.strip()))
    
for line in read_file2:
    t, y, imu = line.split(',')                
    y_dat.append(float(imu.strip()))
    t2_dat.append(float(t.strip()))
    
for line in read_file3:
    t, y, imu = line.split(',')                
    z_dat.append(float(imu.strip()))
    t3_dat.append(float(t.strip()))
    

plt.figure()

plt.subplot(3,1,1)
f, Pxx_den = ss.welch(x_dat,20)
plt.plot(f, Pxx_den)
plt.title("ax")

plt.subplot(3,1,2)
f, Pxx_den = ss.welch(y_dat,20)
plt.plot(f, Pxx_den)
plt.title("ay")

plt.subplot(3,1,3)
f, Pxx_den = ss.welch(z_dat,20)
plt.plot(f, Pxx_den)
plt.title("az")