# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:36:53 2019

@author: Michael K
"""

from Libraries.pedometer import Pedometer

read_filename1 = "data_train_sit.csv"
read_filename2 = "data_train_walk.csv"
#read_file1 = open(read_filename1, 'r')
#read_file2 = open(read_filename2, 'r')
#read_file1.readline()
#read_file2.readline()
#
#x_dat_sit = []
#t1_dat_sit = []
#x_dat_walk = []
#t2_dat_walk = []
#
#
#for line in read_file1:
#    t, y, imu = line.split(',')                
#    x_dat_sit.append(float(imu.strip()))
#    t1_dat_sit.append(float(t.strip()))
#    
#for line in read_file2:
#    t, y, imu = line.split(',')                
#    x_dat_walk.append(float(imu.strip()))
#    t2_dat_walk.append(float(t.strip()))
#    
ped = Pedometer(read_filename1, read_filename2)

