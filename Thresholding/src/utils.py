from math import sqrt, pi
import numpy as np

def kernel_density_estimation(X:np.ndarray, kernel:str="gaussian", bandwidth: float=1):
    if kernel != "gaussian":
        raise NotImplementedError(f"'{kernel}' kernel hasn't been implemented yet. Use 'gaussian' instead")
    
    return 1/(bandwidth*sqrt(2*pi)) * np.exp(-0.5 * (X/bandwidth)**2)

def euclidean_distances(x1, x2):
    return np.linalg.norm(x1 - x2, ord=2, axis=1)