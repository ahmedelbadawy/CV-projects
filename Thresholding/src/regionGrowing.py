import numpy as np
import cv2

class RegionGrowing :
    def __init__(self) -> None:
        self.finalImage = None

    def getGrayDiff(self,img, currentPoint, tmpPoint):
        return abs(int(img[currentPoint.x, currentPoint.y]) - int(img[tmpPoint.x, tmpPoint.y]))


    def selectConnects(self,p):
        if p != 0:
            connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1),
                        Point(0, 1), Point(-1, 1), Point(-1, 0)]
        else:
            connects = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
        return connects


    def fit(self, image, seeds, thresh, p=1):
        seeds = [Point(point[0],point[1]) for point in seeds]
        img = image
        height, weight = img.shape
        seedMark = np.zeros(img.shape)
        seedList = []
        for seed in seeds:
            seedList.append(seed)
        label = 1
        connects = self.selectConnects(p)
        while(len(seedList) > 0):
            currentPoint = seedList.pop(0)
            seedMark[currentPoint.x, currentPoint.y] = label
            for i in range(8):
                tmpX = currentPoint.x + connects[i].x
                tmpY = currentPoint.y + connects[i].y
                if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
                    continue
                grayDiff = self.getGrayDiff(img, currentPoint, Point(tmpX, tmpY))
                if grayDiff < thresh and seedMark[tmpX, tmpY] == 0:
                    seedMark[tmpX, tmpY] = label
                    seedList.append(Point(tmpX, tmpY))
        self.finalImage = seedMark

    def show_masked_image(self) :
        cv2.imshow('Output', self.finalImage)
        cv2.waitKey(0)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

def region_growing(image, seeds, threshold):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    region = RegionGrowing()
    region.fit(img, seeds, threshold)
    return region.finalImage

if __name__ == "__main__":
    seeds = [[10, 10],[82, 150],[20, 300]]
    image = cv2.imread("./images/Lenna_512.png")
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    region = RegionGrowing()
    region.fit(img, seeds, 6)
    region.show_masked_image()
