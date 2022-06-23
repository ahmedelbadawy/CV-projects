import gui
from PyQt5 import QtWidgets
import time
import sys
import cv2
import matplotlib.pyplot as plt
from src.face_recog import Face_recognition
from src.face_detection import detect_faces


class MainWindow(QtWidgets.QMainWindow , gui.Ui_MainWindow):
    # resized = QtCore.pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.widgets = [self.input_img,self.input_img_2,self.output_img_2]
        self.widget_configuration()
        self.default_img()
        self.open_button.clicked.connect(self.open_image)
        self.open_button_2.clicked.connect(self.open_image)
        self.apply_button.clicked.connect(self.apply_detection)
        self.apply_button_2.clicked.connect(self.recog_img)
    

    def open_image(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',"", "Image Files (*.png *jpeg *.jpg)")
        if self.file_path != "":
            if self.tabWidget.currentIndex( ) == 0:
                self.input_img = cv2.imread(self.file_path)
                self.apply_detection()
                self.apply_button.setEnabled(True)
                self.scale_factor.setEnabled(True)
                self.thickness.setEnabled(True)
                self.min_size.setEnabled(True)
            else:
                
                self.img = cv2.imread(self.file_path)
                self.img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                self.display(self.img_rgb,self.widgets[1])
                self.widgets[2].clear()
                self.eigen_num.setEnabled(True)
                self.apply_button_2.setEnabled(True)
    def apply_detection(self):
        start = time.time()
        detect_img = detect_faces(self.input_img,float(self.scale_factor.text()),int(self.min_size.text()),int(self.thickness.text()))
        end = time.time()
        self.time_label.setText(str("{:.3f}".format(end-start)) + " Seconds")
        self.img_rgb = cv2.cvtColor(detect_img, cv2.COLOR_BGR2RGB)
        self.display(self.img_rgb,self.widgets[0])
    
    def recog_img(self):
        model = Face_recognition(int(self.eigen_num.text()),2250)
        start = time.time()
        model.train("Dataset/train")
        end = time.time()
        self.time_label_2.setText(str("{:.3f}".format(end-start)) + " Seconds")
        start = time.time()
        detected, matched_img,person = model.recognize(self.img)
        end = time.time()
        self.time_label_3.setText(str("{:.3f}".format(end-start)) + " Seconds")
        if detected:
            self.matched_person.setText(person)
            matched_img_rgb = cv2.cvtColor(matched_img, cv2.COLOR_BGR2RGB)
        else:
            self.matched_person.setText("UNKNOWN")
            matched_img_rgb = plt.imread("images/unknown.jpeg")
        self.display(matched_img_rgb,self.widgets[2])
        

    def display(self , data , widget):
            data = cv2.transpose(data)
            widget.setImage(data)
            widget.view.setLimits(xMin=0, xMax=data.shape[0], yMin= 0 , yMax= data.shape[1])
            widget.view.setRange(xRange=[0, data.shape[0]], yRange=[0, data.shape[1]], padding=0)    

    def widget_configuration(self):

        for widget in self.widgets:
            widget.ui.histogram.hide()
            widget.ui.roiBtn.hide()
            widget.ui.menuBtn.hide()
            widget.ui.roiPlot.hide()
            widget.getView().setAspectLocked(False)
            widget.view.setAspectLocked(False)

    def default_img(self):
        defaultImg = plt.imread("images/default-image.jpg")
        for widget in self.widgets:
            self.display(defaultImg,widget)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()