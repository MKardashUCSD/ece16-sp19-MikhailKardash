from sklearn.neighbors import KNeighborsClassifier as KNN
import numpy as np
from Libraries.ListBuffer import ListBuffer
from statistics import mean
from math import ceil


class Pedometer:

# initial_steps is useful if you ever have to restart the pedometer
	def __init__(self, train_file_active, train_file_inactive, window_length=100, initial_steps=0):
		self.window_length = window_length
		self.steps = initial_steps
		self.knn = self.train(train_file_active, train_file_inactive)
	
	def extract_features(self, t, imu):
		# Split into 10 chunks
		j = 0
		oof = [0]*ceil(len(imu)/10)
		for i in range(0, len(imu),10):
		# Get the maxima of each chunk. The list comprehension is equivalent to a for-loop but cleaner!
			oof[j] = max(imu[i:i+10])
		# Return the average of these maxima
		result = mean(oof)
		return result
	
	
	
	def train(self, train_file_active, train_file_inactive):
		"""
		---------------------- DATA LOADING ----------------------
		"""
		# Load the data into numpy arrays. The data must only have two columns. Skip the labels row.
		t_active, data_active = np.loadtxt(train_file_active, delimiter=",", skiprows=1, usecols = [0,2], unpack=True)
		t_inactive, data_inactive = np.loadtxt(train_file_inactive, delimiter=",", skiprows=1, usecols = [0,2], unpack=True)
		
		# For both the active data and the inactive data, split it into windows of size window_length
		# Let's assume there are "num_window" windows
		
		#but like why tho?
		#Function that makes windows and extracts window features
		active_features = []
		inactive_features = []
		for i in range(0, len(t_active),self.window_length):
			active_features.append(self.extract_features(t_active[i:i + self.window_length], data_active[i:i + self.window_length]))
		for i in range(0,len(t_inactive),self.window_length):	
			inactive_features.append(self.extract_features(t_inactive[i:i + self.window_length], data_inactive[i:i + self.window_length]))
		
		# Extract features for each of these windows for both the active and active set
		# Do this by calling self.extra_features()
		# The result will be an array of num_window features for the active set, and a similar array for the inactive set
		
		# For both the active and the inactive set, split the features 50/50 into a training set and a validation set
		# The result will be an array of num_window//2 features for the active training set,
		# num_window//2 features for the active validation set, and something similar for the inactive set
		
		train_act = active_features[0:ceil(len(active_features)/2)]
		val_act = active_features[ceil(len(active_features)/2):len(active_features)]
		train_inact = inactive_features[0:ceil(len(inactive_features)/2)]
		val_inact = inactive_features[ceil(len(inactive_features)/2):len(inactive_features)]
		"""
		---------------------- TRAINING ----------------------
		"""
		
		# Create training data
		# (1) Merge your array of features for the active training set and the inactive training set into one array.
		#     Reshape to a 2D array (of many rows and 1 column). Let's call this array X.
		# (2) Create the correct labels for these features in a separate array Y. It will have the same dimensions as X.
		#     When the data came from the actve set, the corresponding label should 0. When it came from the inactive set, the
		#     corresponding label should be 1.
		
		X = np.asarray(train_act + train_inact)
		X = X.reshape(-1,1)
		Y = np.asarray([1]*len(train_act) + [0]*len(train_inact)) 
		#Y = Y.reshape(-1,1)
		# Instantiate KNN
		knn = KNN(weights = 'distance')
		
		# Train the KNN with X and Y
		knn.fit(X,Y)
		
		"""
		---------------------- VALIDATION ----------------------
		"""
		
		# Create the validation data in a similar way as was done with the training data.
		# This will result in an array X_val and Y_val, with the data and labels respectively.
		X_val = np.asarray(val_act + val_inact)
		X_val = X_val.reshape(-1,1)
		Y_val = np.asarray([1]*len(val_act) + [0]*len(val_inact)) 
		#Y_val = Y_val.reshape(-1,1)
		# Run KNN to predict the labels for validation data
		Y_predicted = knn.predict(X_val)
		# Find the accuracy by comparing Y_val with Y_predicted
		accum = 0
		for i in range(0,len(Y_val)):
			if Y_val[i] != Y_predicted[i]:
				accum = accum + 1

		accuracy = 1 - (accum/len(Y_val))

		# Print the accuracy to the terminal
		print(accuracy)
		# Return he KNN parameters
		return knn


# def process(self, t_data, imu_data):
#
#     # Return if we don't have enough data yet or were not given enough data
#     if len(t) < self.window_length:
#         return self.steps
#            
#     # Slice into just one window
#     t = t_data[-self.window_length:]
#     imu = imu_data[-self.window_length:]
#
#     # Use the KNN to determine if the instantaneous state is active or inactive
#     # call self.is_active(...)
#
#     # Implement your own step counter heuristic
#     # You can create new functions if you want
#
#     return self.steps
#
# def is_active(self, t, imu):
#
#     # Extract features for KNN
#     # call self.extract_features(...)
#            
#     # Classify using KNN
#            
#     # Return the result (labels) of the classification
#     return result
#
