import cv2

def detect_faces(img,scale_factor,minNeighbors,thickness):
    # Loading the required haar-cascade xml classifier file
    face_cascade = cv2.CascadeClassifier('./resources/haarcascade_frontalface_default.xml')  
    # Converting image to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applying the face detection method on the grayscale image
    faces = face_cascade.detectMultiScale( gray_image , scale_factor , minNeighbors )
    #drawing rectangles around the detected faces
    for( x , y , width , height ) in faces:
        cv2.rectangle(img , (x,y) , (x+width , y+height) , (255 , 0 , 0 ),thickness)
    return img


