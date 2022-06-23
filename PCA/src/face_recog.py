import os
import cv2
import numpy as np
from sklearn import preprocessing
import math
class Face_recognition:

    def __init__(self, eigen_faces_num=50,threshold=2250):
        
        self.eigen_faces_num = eigen_faces_num
        self.threshold = threshold
        self.train_images = []
        self.images = []
        self.persons = []
        self.projections = []
    def train(self,data_path):
        self.data_path = data_path
        for filename in os.scandir(self.data_path):
            if filename.is_file():
                file = os.path.basename(filename.path)
                self.persons.append(file[:file.find("-")])
                img = cv2.imread(filename.path,cv2.IMREAD_GRAYSCALE)
                self.images.append(img)
                flatten_img = img.flatten()
                self.train_images.append(flatten_img)
        self.train_images = np.array(self.train_images)
        self.mean_img = np.sum(self.train_images,axis=0,dtype='float64')/self.train_images.shape[0]
        zero_mean_train = self.train_images - self.mean_img
        cov_matrix = zero_mean_train.dot(zero_mean_train.T)/self.train_images.shape[0]
        eigenvalues,eigenvectors = np.linalg.eig(cov_matrix)
        indices = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[indices]
        eigenvectors = eigenvectors[:,indices]
        images_projection = zero_mean_train.T.dot(eigenvectors)
        self.eigen_faces = preprocessing.normalize(images_projection.T)
        for i in range(self.train_images.shape[0]):
            self.projections.append(self.eigen_faces[:self.eigen_faces_num].dot(zero_mean_train[i]))
    def recognize(self,img):

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        flatten_img = img.flatten()
        zero_mean_test = flatten_img - self.mean_img
        E = self.eigen_faces[:self.eigen_faces_num].dot(zero_mean_test)
        test_projected = self.eigen_faces[:self.eigen_faces_num].T.dot(E)
        diff = zero_mean_test-test_projected
        beta = math.sqrt(diff.dot(diff))
        beta = math.sqrt(diff.dot(diff))
        if beta<self.threshold:
            face_detected = True
        else:
            face_detected = False
        smallest_dist = None 
        img_idx = 0 
        for z in range(len(self.projections)):
            diff = E-self.projections[z]
            imgs_dist = math.sqrt(diff.dot(diff))
            if smallest_dist==None:
                    smallest_dist=imgs_dist
                    img_idx = z
            if smallest_dist>imgs_dist:
                smallest_dist=imgs_dist
                img_idx=z
        return face_detected,self.images[img_idx],self.persons[img_idx]