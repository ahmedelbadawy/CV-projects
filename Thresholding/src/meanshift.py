# TODO:
# using a feature vector X e.g. RGB, HSV, ... and a window size
# for each point:
#   pick as the center or mean
#   estimate kde of the local neighbourhood
#   now we computed the mean shift vector or the step by which we need to move
#   update the mean by adding to it the mean shift vector
#   repeat until convergence

import numpy as np
from .utils import euclidean_distances, kernel_density_estimation

class MeanShift:
    def __init__(self, bandwidth: float, tolerance: float = 1e-2,verbose:bool = False) -> None:
        self.bandwidth = bandwidth
        self.tolerance = tolerance
        self.verbose = verbose

    def __check_params(self):
        if self.tolerance < 0:
            raise ValueError("tolerance must be greater than 0")
        if self.bandwidth < 0:
            raise ValueError("bandwidth must be greater than 0")

    def fit(self, X: np.ndarray):
        self.__check_params()
        self.labels = np.ndarray((X.shape[0],))
        self.centers = np.ndarray((0,X.shape[1]))
        for i,x in enumerate(X):
            center = x.copy()
            old_center = np.inf
            while not np.allclose(old_center,center,rtol=self.tolerance,atol=0):
                old_center = center.copy()
                neighbours = self.__get_neighbours(X, center)
                kde = kernel_density_estimation(neighbours - center)
                center = np.sum(kde * neighbours,axis=0)/np.sum(kde,axis=0)
            
            existing = False
            for j,c in enumerate(self.centers):
                if np.allclose(c, center,rtol=0.1,atol=1):
                    self.labels[i] = j
                    existing = True
            
            if not existing:
                self.centers = np.append(self.centers, [center],axis=0)
                self.labels[i] = self.centers.shape[0] - 1

        return self

    def __get_neighbours(self, X: np.ndarray, center: np.ndarray) -> np.ndarray:
        distances = euclidean_distances(X, center)
        return X[distances <= self.bandwidth]




def test_custom_data():
    from matplotlib import pyplot as plt
    from sklearn.datasets._samples_generator import make_blobs
    from mpl_toolkits.mplot3d import Axes3D

    # We will be using the make_blobs method
    # in order to generate our own data.
    clusters = [[2, 2,2],[8,14,1],[8,8,14],[12,12,12],[8,2,0]]

    X, _ = make_blobs(n_samples = 5000, centers = clusters,
    								cluster_std = 0.60)

    # # After training the model, We store the
    # # coordinates for the cluster centers
    ms = MeanShift(bandwidth=2)
    ms.fit(X)
    cluster_centers = ms.centers

    # Finally We plot the data points
    # and centroids in a 3D graph.

    fig = plt.figure()

    ax = fig.add_subplot(111,projection="3d")

    ax.scatter(X[:, 0], X[:, 1], X[:,2],marker ='o',c=ms.labels)
    ax.scatter(cluster_centers[:, 0], cluster_centers[:, 1], cluster_centers[:, 2], marker ='x', color ='red',
    		s = 300, linewidth = 5, zorder = 1)

    plt.show()

def meanshift(image, bandwidth):

    pixel_vals = image.reshape((-1,3))

    # Convert to float type
    pixel_vals = np.float32(pixel_vals)

    m = MeanShift(bandwidth=bandwidth).fit(pixel_vals)

    # convert data into 8-bit values
    centers = np.uint8(m.centers)
    segmented_data = centers[m.labels.astype(int)]
    
    # reshape data into the original image dimensions
    return segmented_data.reshape((image.shape))

if __name__ == "__main__":
    import cv2
    import sys

    if len(sys.argv) != 3:
        print("Must supply path to image file and bandwidth.")

    try:
        img = cv2.imread(sys.argv[1])
        
        bandwidth = int(sys.argv[2])
        
        segmented_image = meanshift(MeanShift, img, bandwidth)
    
        cv2.imshow("original",img)
        cv2.imshow("segmented",segmented_image)
        cv2.waitKey(0)
    except cv2.error:
        print("Must supply valid image path")