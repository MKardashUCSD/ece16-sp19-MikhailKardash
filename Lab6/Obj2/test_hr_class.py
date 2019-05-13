# -*- coding: utf-8 -*-
"""
Created on Sun May 12 22:45:11 2019

@author: Michael K
"""

from Hr_basic import Hr
import numpy as np

hr = Hr("ir_data_train.csv")

data_time_val, data_ir_val = np.loadtxt("ir_data_validation.csv", delimiter=",", skiprows=1, unpack=True)

hr.plot_histo(data_ir_val)
hr.plot_labels(data_time_val, data_ir_val)