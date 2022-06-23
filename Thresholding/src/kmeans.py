import numpy as np
from .utils import euclidean_distances
import cv2
# TODO:
# Add loss function (intertia) and iterate for different seeds 
class KMeans():
    def __init__(self, K:int=2, initial_centroids:np.ndarray|None=None ,max_iter:int =100, tolerance:float=1e-4, verbose:bool= False) -> None:
        self.K = K
        self.max_iter = max_iter
        self.verbose = verbose
        self.initial_centroids = initial_centroids
        self.tolerance = tolerance

    def __check_params(self):
        if self.K < 2:
            raise ValueError(f"K must be greater than or equal 2")
        if self.max_iter < 1:
            raise ValueError(f"max_iter must be greater than or equal 1")
    
    # for each point
    # calculate the distance to each centroid
    # assign the point to cluster k based on least centroid
    # update centroid to mean of points in k
    def fit(self, X: np.ndarray):
        self.__check_params()
        self.__init_centroids(X)
        
        for i in range(self.max_iter):            
            self.labels = self.__assign_labels(X)

            old_centroids = self.centroids.copy()
            self.__update_centroids(X,self.labels)

            if np.allclose(old_centroids,self.centroids,rtol=self.tolerance,atol=0):
                if self.verbose:
                    print(f"converged at iteration #{i+1}")
                return self

            if self.verbose:
                print(f"iteration #{i+1}:")
                [print(f"\tcentroid {j+1}: {k}") for j,k in enumerate(self.centroids)]
        
        return self

    def __update_centroids(self, X: np.ndarray, labels:np.ndarray):
        for k in range(self.K):
            x = X[np.where(labels==k)[0]]
            if x.shape[0]:
                self.centroids[k] = x.mean(axis=0)

    def __assign_labels(self, X: np.ndarray)-> np.ndarray:
        distances = np.ndarray((self.K,X.shape[0]))
        for i,c in enumerate(self.centroids):
            distances[i] = euclidean_distances(X, c)

        return np.argmin(distances,axis=0)

    def __init_centroids(self, X):
        # check if user supplied initial centroid else
        # initialize random centroids from the observations
        if type(self.initial_centroids) == np.ndarray:
            if self.initial_centroids.shape == (self.K, X.shape[1]):
                self.centroids = self.initial_centroids
            else:
                raise ValueError(f"Expected shape({self.K}, {X.shape[1]}), found {self.initial_centroids.shape}") 
        else:
            self.centroids = np.array([X[np.random.randint(0,X.shape[0])] for _ in range(self.K)])
        

        if self.verbose:
            [print(f"initial centroid {i+1}: {k}") for i,k in enumerate(self.centroids)]

def kmeans(image, K):

    pixel_vals = image.reshape((-1,3))

    # Convert to float type
    pixel_vals = np.float32(pixel_vals)

    m = KMeans(K=K,max_iter=10).fit(pixel_vals)

    # convert data into 8-bit values
    centers = np.uint8(m.centroids)
    segmented_data = centers[m.labels.flatten()]
    
    # reshape data into the original image dimensions
    return segmented_data.reshape((image.shape))
    
if __name__ == "__main__":
    import cv2
    import sys

    if len(sys.argv) != 3:
        print("Must supply path to image file and number of clusters")

    try:
        img = cv2.imread(sys.argv[1])
        K = int(sys.argv[2])

        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        pixel_vals = image.reshape((-1,3))

        # Convert to float type
        pixel_vals = np.float32(pixel_vals)

        m = KMeans(K=K,max_iter=100).fit(pixel_vals)

        # convert data into 8-bit values
        centers = np.uint8(m.centroids)
        segmented_data = centers[m.labels.flatten()]
    
        # reshape data into the original image dimensions
        segmented_image = segmented_data.reshape((image.shape))
    
        cv2.imshow("original",img)
        cv2.imshow("segmented",segmented_image)
        cv2.waitKey(0)
    except cv2.error:
        print("Must supply valid image path")