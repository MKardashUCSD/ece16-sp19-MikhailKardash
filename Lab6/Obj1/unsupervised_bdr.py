# ---------------------------------------- Import Libraries ---------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
from sklearn.mixture import GaussianMixture as GM
import matplotlib.mlab as mlab

# ---------- Import Your Modules HERE ---------- #


if (__name__ == "__main__"):
    
    ##########
    # Step 1 #
    ##########
    # ---------- Load training data ---------- #
    # Load training data
    data_time_tr, data_ir_tr = np.loadtxt("ir_data_train.csv", delimiter=",", skiprows=1, unpack=True)

    
    ##########
    # Step 2 #
    ##########
    i = 0;
    while 1:
        if data_time_tr[i] - data_time_tr[0] >= 5:
            break
        i = i + 1
    
    # ---------- Plot 5 sec of Raw Data ---------- #
    plt.figure()
    # PLOT HERE
    plt.plot(data_time_tr[0:i],data_ir_tr[0:i])
    plt.show()

    
    ##########
    # Step 3 #
    ##########
    # ---------- Plot Histogram ---------- #
    # Plot the histogram of your training dataset, here.
    plt.figure()
    plt.hist(data_ir_tr, 50)
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.title("IR Signal Histogram")
    
    
    numsamps = data_ir_tr.shape[0]

    ##########
    # Step 4 #
    ##########
    # ---------- Find GMM ---------- #
    # Create GMM object
    gmm = GM(n_components=2)
    # Fit 2 component Gaussian to the data
    gmm_fit = gmm.fit( data_ir_tr.reshape(-1, 1))                              # Pass correct parameters. Remember that this expects a 2D array.
    # Retrieve Gaussian parameters
    mu0 = gmm_fit.means_[0]
    mu1 = gmm_fit.means_[1]
    sig0 = np.sqrt(gmm_fit.covariances_[0])
    sig1 = np.sqrt(gmm_fit.covariances_[1])
    w0 = gmm_fit.weights_[0]
    w1 = gmm_fit.weights_[1]

    # ---------- Plot Gaussians sum over histogram ---------- #
    # Create an "x" array from which to compute the Gaussians
    temp = np.shape(data_ir_tr)
    print(temp)
    x = np.reshape((np.linspace(np.min(data_ir_tr), np.max(data_ir_tr),temp[0])), [temp[0], 1])
    plt.figure()
    plt.hist(data_ir_tr, bins=50, density=True)
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.title("IR Signal PDFs")
    #plt.plot(x, w1 * mlab.normpdf(x, mu1, sig1) + w0 * mlab.normpdf(x, mu0, sig0) )
    plt.plot(x, w1 * mlab.normpdf(x, mu1, sig1))
    plt.plot(x, w0 * mlab.normpdf(x, mu0, sig0))
    plt.show(block = False)
        
    # ---------- Plot two Gaussians over histogram ---------- #
    # Add the appropriate code
        
        
    ##########
    # Step 5 #
    ##########
    # ---------- Load validation data ---------- #
    # Load validation data
    data_time_va, data_ir_va = np.loadtxt("ir_data_validation.csv", delimiter=",", skiprows=1, unpack=True)
        
    # ---------- Predict Labels for training data ---------- #
    # Predict training labels
    train_pred_lbl = gmm_fit.predict(data_ir_tr.reshape(-1,1))                     # Pass correct parameters

    # ---------- Predict Labels for validation data ---------- #
    # Predict validation labels
    validation_pred_lbl = gmm_fit.predict(data_ir_va.reshape(-1,1))                # Pass correct parameters

    # ---------- Plot Training Set predictions ---------- #
    # Complete the code
    bias_point1 = np.min(data_ir_tr)
    multiplier1 = np.max(data_ir_tr) - np.min(data_ir_tr)
    plt.figure()
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.plot(data_time_tr,data_ir_tr)
    plt.plot(data_time_tr,train_pred_lbl*multiplier1 + bias_point1)
    plt.show()
        
    # ---------- Plot Validation Set predictions ---------- #
    # Complete the code
    bias_point2 = np.min(data_ir_va)
    multiplier2 = np.max(data_ir_va) - np.min(data_ir_va)
    plt.figure()
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.plot(data_time_va,data_ir_va)
    plt.plot(data_time_va,validation_pred_lbl*multiplier2 + bias_point2)
    plt.show()