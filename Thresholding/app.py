import gui
from PyQt5 import QtWidgets
import time
import sys
import cv2
import matplotlib.pyplot as plt
from src.threshold import global_threshold, local_threshold
from src.agglomerative import agglomerative
from src.kmeans import kmeans
from src.meanshift import meanshift
from src.regionGrowing import region_growing
from src.luv import rgb_luv,luv_rgb

class MainWindow(QtWidgets.QMainWindow , gui.Ui_MainWindow):
    # resized = QtCore.pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.widgets = [self.input_img,self.output_img,self.input_img_2,self.output_img_2]
        self.widget_configuration()
        self.default_img()
        self.open_button.clicked.connect(self.open_image)
        self.open_button_2.clicked.connect(self.open_image)
        self.comboBox_2.currentIndexChanged.connect(self.show_clustering_inputs, self.comboBox_2.currentIndex())
        self.apply_button.clicked.connect(self.apply_threshold)
        self.apply_button_2.clicked.connect(self.apply_clustering)
    

    def open_image(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',"", "Image Files (*.png *jpeg *.jpg)")
        if self.tabWidget.currentIndex( ) == 0:
            self.threshold_img = cv2.imread(self.file_path)
            self.img_rgb = cv2.cvtColor(self.threshold_img, cv2.COLOR_BGR2RGB)
            self.apply_button.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.radio_global.setEnabled(True)
            self.radio_local.setEnabled(True)
            self.size_input.setEnabled(True)
            self.display(self.img_rgb,self.widgets[0])
            self.output_img.clear()
        else:
            self.clustering_img = cv2.imread(self.file_path)
            self.img_rgb = cv2.cvtColor(self.clustering_img, cv2.COLOR_BGR2RGB)
            self.apply_button_2.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.show_clustering_inputs(_)
            self.display(self.img_rgb,self.widgets[2])
            self.output_img.clear()


    def apply_threshold(self):
        start = time.time()
        if self.comboBox.currentText() == "Optimal Thresholding":
            if self.radio_global.isChecked():
                self.threshold_output = global_threshold(self.threshold_img,"optimal")
            else:
                self.threshold_output = local_threshold(self.threshold_img,int(self.size_input.text()),"optimal")
        elif self.comboBox.currentText() == "Otsu Thresholding":
            if self.radio_global.isChecked():
                self.threshold_output = global_threshold(self.threshold_img,"otsu")
            else:
                self.threshold_output = local_threshold(self.threshold_img,int(self.size_input.text()),"otsu")
        else:
            if self.radio_global.isChecked():
                self.threshold_output = global_threshold(self.threshold_img,"spectral")
            else:
                self.threshold_output = local_threshold(self.threshold_img,int(self.size_input.text()),"spectral")
        end = time.time()
        self.threshold_output = cv2.cvtColor(self.threshold_output, cv2.COLOR_BGR2RGB)
        self.display(self.threshold_output,self.widgets[1])
        self.time_label.setText(str("{:.3f}".format(end-start)) + " Seconds")

    def apply_clustering(self):
        RGB = True
        start = time.time()
        if self.comboBox_2.currentText() == "K-Means":
            self.clustering_output = luv_rgb(kmeans(rgb_luv(self.clustering_img), int(self.cluster_input.text())))
        elif self.comboBox_2.currentText() == "Mean-Shift":
            self.clustering_output = luv_rgb(meanshift(rgb_luv(self.clustering_img), int(self.bandwidth_input.text())))
        elif self.comboBox_2.currentText() == "Agglomerative":
            # op = cv2.cvtColor(self.clustering_img,cv2.COLOR_RGB2LUV)
            self.clustering_output = agglomerative(self.clustering_img, int(self.cluster_input.text()))
            RGB = False
        else:
            seeds = [[10, 10],[82, 150],[20, 300]]
            self.clustering_output = region_growing(self.clustering_img, seeds, int(self.threshold_input.text()))
            RGB = False

        end = time.time()
        self.clustering_output = cv2.cvtColor(self.clustering_output, cv2.COLOR_BGR2RGB) if RGB else self.clustering_output
        self.display(self.clustering_output,self.widgets[3])
        self.time_label_2.setText(str("{:.3f}".format(end-start)) + " Seconds")

    def show_clustering_inputs(self, index):
        if self.comboBox_2.currentText() == "K-Means" or self.comboBox_2.currentText() == "Agglomerative":
            self.cluster_input.setEnabled(True)
            self.bandwidth_input.setEnabled(False)
            self.threshold_input.setEnabled(False)
        elif self.comboBox_2.currentText() == "Mean-Shift":
            self.threshold_input.setEnabled(False)
            self.cluster_input.setEnabled(False)
            self.bandwidth_input.setEnabled(True)
        else:
            self.cluster_input.setEnabled(False)
            self.bandwidth_input.setEnabled(False)
            self.threshold_input.setEnabled(True)

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