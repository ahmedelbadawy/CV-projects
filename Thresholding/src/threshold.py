import cv2
import numpy as np

def optimal_threshold(img):
    back_sum = []
    obj_sum = []
    prev_threshold = 0
    if len(img.shape)>2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if (row == 0 and col == 0) or (row == 0 and col == (img.shape[1]-1)) or (row == (img.shape[0] -1)  and col == 0) or (row == (img.shape[0] -1)  and col ==(img.shape[1] -1)):
                back_sum.append(img[row,col])
            else:
                obj_sum.append(img[row,col])
    back_avg = sum(back_sum)/len(back_sum)
    obj_avg = sum(obj_sum)/len(obj_sum)
    threshold = (back_avg + obj_avg)/2
    while threshold != prev_threshold:
        back_sum = []
        obj_sum = []
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                if img[row,col] < threshold:
                    back_sum.append(img[row,col])
                else:
                    obj_sum.append(img[row,col])
        back_avg = sum(back_sum)/len(back_sum)
        obj_avg = sum(obj_sum)/len(obj_sum)
        prev_threshold = threshold
        threshold = (back_avg + obj_avg)/2
    
    return threshold

def global_threshold(img,threshold_func):
    if len(img.shape)>2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    new_img = np.zeros_like(img)
    if threshold_func == "spectral":

        low_threshold ,high_threshold = spectral_threshold(img)
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                if img[row,col] < low_threshold:
                    new_img[row,col] = 0
                elif img[row,col] > high_threshold:
                    new_img[row,col] = 255
                else:
                    new_img[row,col] = 128
    else:
        if threshold_func == "otsu":
            threshold = otsu_threshold(img)
        elif threshold_func == "optimal":
            threshold = optimal_threshold(img)
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                if img[row,col] > threshold:
                    new_img[row,col] = 255
    return new_img

def local_threshold(img,kernal_size,threshold_func):
    row = 0
    col = 0 
    if len(img.shape)>2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    new_img = np.zeros_like(img)
    for row in range(0,img.shape[0],kernal_size):
        for col in range(0,img.shape[1],kernal_size):
            local_img = img[row:min((row+kernal_size),(img.shape[0])),col:min((col+kernal_size),(img.shape[1]))]
            new_img[row:min((row+kernal_size),(img.shape[0])),col:min((col+kernal_size),(img.shape[1]))] = global_threshold(local_img,threshold_func)
    return new_img
def otsu_threshold(img):
    if len(img.shape)>2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    width , height = img.shape
    image_size = width *height
    hist,_ = np.histogram(img.ravel(),256,[0,256])
    max_between_variance = 0 
    threshold = 1
    for i in range(1,256):
        # first divide Histogram_Array into two classes 
        class1 , class2 =np.split( hist , [i] )
        #claculate the two classes weight
        class1_weight = np.sum( class1 )/ image_size #class1 weight
        class2_weight = np.sum( class2 ) / image_size #class2 weight
        
        #claculate the two classes mean
        class1_mean=np.sum ([intensity * repeation for intensity,repeation in enumerate(class1)])/np.sum(class1)
        class2_mean=np.sum ([intensity * repeation for intensity,repeation in enumerate(class2,i)])/np.sum(class2)

        #calculate between class variance 
        between_variance = class1_weight * class2_weight * (class1_mean - class2_mean)**2

        if  between_variance > max_between_variance :
            max_between_variance = between_variance
            threshold = i

    return threshold

def spectral_threshold(img):  
    if len(img.shape)>2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    width , height = img.shape
    image_size = width *height
    hist,_ = np.histogram(img.ravel(),256,[0,256])
    max_between_variance = 0 
    low_threshold = 1
    high_threshold = 1
    total_mean=np.sum ([intensity * repeation for intensity,repeation in enumerate(hist)])/np.sum(hist)
    for threshold1 in range(1,255):
        for threshold2 in range(threshold1 + 1, 256):
            # first divide Histogram_Array into three classes 
            class1 ,sub_hist =np.split( hist , [threshold1])
            class2 ,class3=np.split( sub_hist , [threshold2 - threshold1] )            
            #claculate the three classes weight
            class1_weight = np.sum( class1 )/ image_size #class1 weight
            class2_weight = np.sum( class2 ) / image_size #class2 weight
            class3_weight = np.sum( class3 ) / image_size #class3 weight          
            #claculate the three classes mean
            class1_mean=np.sum ([intensity * repeation for intensity,repeation in enumerate(class1)])/np.sum(class1)
            class2_mean=np.sum ([intensity * repeation for intensity,repeation in enumerate(class2,threshold1)])/np.sum(class2)
            class3_mean=np.sum ([intensity * repeation for intensity,repeation in enumerate(class3,threshold2)])/np.sum(class3)

            # calculate between classes variance 
            between_variance = class1_weight * (total_mean - class1_mean)**2 +  class2_weight*(total_mean - class2_mean)**2  + class3_weight * (total_mean - class3_mean)**2
             
            if  between_variance > max_between_variance :
                max_between_variance = between_variance
                low_threshold = threshold1
                high_threshold = threshold2

    return low_threshold ,high_threshold
