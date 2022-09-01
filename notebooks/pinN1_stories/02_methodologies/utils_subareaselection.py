import numpy as np

def fraction_nonnan(array_data):
    return np.sum(~np.isnan(array_data))/array_data.size