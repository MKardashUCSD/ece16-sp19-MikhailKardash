import numpy as np
from Libraries.ListBuffer import ListBuffer
from sklearn.mixture import GaussianMixture as GM
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab


class Hr:

    def __init__(self, train_file, plot=False):
        self.plot = plot
        self.model = None
        self.train(train_file)
        
    def _normalize(self, data):
        return np.nan_to_num((data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data)))

    def train(self, train_file):
        # Load training data. train_file must be in the same folder as the script implementing this class.
        train_t, train_ir = np.loadtxt(train_file, delimiter=",", skiprows=1, unpack=True)
        # Reshape training data to be a 2D array
        # Unit normalize
        train_ir = self._normalize(train_ir)
        # Create GMM object
        gmm = GM(n_components=2)
        # Find parameters for GMM based on training data
        self.model = gmm.fit( train_ir.reshape(-1,1))
        if self.plot:
            self.plot_histo(train_ir)
            self.plot_labels(train_t,train_ir )
        
    def plot_histo(self, ir):
         # Retrieve Gaussian parameters
         mu0 = self.model.means_[0]
         mu1 = self.model.means_[1]
         sig0 = np.sqrt(self.model.covariances_[0])
         sig1 = np.sqrt(self.model.covariances_[1])
         w0 = self.model.weights_[0]
         w1 = self.model.weights_[1]
         
         ir = self._normalize(ir)
    
         # Create an "x" vector from which to compute normal distribution curves
         sizeI = np.shape(ir)
         x = np.reshape((np.linspace(np.min(ir), np.max(ir), sizeI[0])), [sizeI[0], 1])
         #
         # Compute normal curves
         oof1 = w1 * mlab.normpdf(x, mu1, sig1)
         oof0 = w0 * mlab.normpdf(x, mu0, sig0)
         
         plt.figure()
         plt.hist(ir, bins = 50, density = True)
         plt.plot(x, oof0)
         plt.plot(x, oof1)
    
         # Plot histograms and sum of curves
         plt.show(block=False)
    
    def plot_labels(self, t, ir):
        ir = self._normalize(ir)
        bias_point1 = np.min(ir)
        multiplier1 = np.max(ir) - np.min(ir)
        labels = self.model.predict(ir.reshape(-1,1))
        # Plot t, ir and labels
        plt.figure()
        plt.plot(t,ir)
        plt.plot(t,labels*multiplier1 + bias_point1)
        plt.show(block=False)
    
    # Process the IR data to get a heart rate estimate
    # t_data: numpy array with timestamps
    # ir_data: numpy array with IR data
    # returns: heart rate hr estimate in bpm (returns None if not valid) and the time t_hr for that hr estimate
    def process(self, t_data, ir_data):
         # Reshape and normalize your data
         # Use GMM to label beats
         ir_data = self._normalize(ir_data)
         labels = self.model.predict(ir_data.reshape(-1,1))
    
         # Apply beat heuristics
         # You may want to wrap this in a try/except clause to avoid issues like 0 heartbeat giving a divide by zero error
         t_hr, hr = self.hr_heuristics(t_data, labels)
    
         return t_hr, hr
    
    # Process the label data to get a hr estimate
    # t: numpy array with timestamps
    # labels: numpy array with corresponding GMM labels of the data
    # returns: heart rate hr estimate in bpm (returns None if not valid) and the time t_hr for that hr estimate
    def hr_heuristics(self, t, labels):
         k = np.diff(labels)
         k = np.append(k,[-1])
         diffs = np.where(k > 0,t, 0)
         t_hr = diffs[np.nonzero(diffs)]
         hr = 60/np.diff(t_hr)
         t_hr = t_hr[1:]
         return t_hr, hr
