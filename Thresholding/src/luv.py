import numpy as np

def inverseGamma(t):
    if (t < 0.03928):
        return t/12.92
    else:
        return np.power(((t + 0.055)/1.055),2.4)


def gamma(d):
    if (d < 0.00304):
        return 12.92*d
    else:
        return 1.055*(np.power(d, 1/2.4))- 0.055

def gammaClip(g):
    if(g < 0):
        return 0
    elif(g > 1):
        return 1
    else:
        return g
def rgb_luv(inputImage):
    u_w = (4*0.95/(0.95+ 15 + 3*1.09))
    v_w = (9/(0.95+ 15 + 3*1.09))
    LRGB2XYZMatrix = [[0.412453, 0.357580, 0.180423],
                  [0.212671, 0.715160, 0.072169],
                  [0.019334, 0.119193, 0.950227]]
    rows, cols, bands = inputImage.shape # bands == 3
    LsRGBMatrix = np.zeros([rows, cols, bands], dtype=np.float16)

    for i in range(0, rows) :
        for j in range(0, cols) :
            b, g, r = inputImage[i, j]

            #sRGB to Non-Linear sRGB
            non_linear_B = b / 255.0
            non_linear_G = g / 255.0
            non_linear_R = r / 255.0

            #Non-Linear sRGB to Linear sRGB
            linear_B = inverseGamma(non_linear_B)
            linear_G = inverseGamma(non_linear_G)
            linear_R = inverseGamma(non_linear_R)


            LsRGBMatrix[i, j] = [linear_R, linear_G, linear_B]


    XYZMatrix = np.zeros([rows, cols, bands], dtype=np.float16)
    #Linear sRGB to XYZ
    for i in range(0, rows) :
        for j in range(0, cols) :
            RGB = LsRGBMatrix[i, j]
            XYZMatrix[i,j] = np.dot(LRGB2XYZMatrix, RGB)


    LuvMatrix = np.zeros([rows, cols, bands], dtype=np.float16)
    for i in range(0, rows) :
        for j in range(0, cols) :
            X, Y, Z = XYZMatrix[i, j]
            # Calculate the L
            L = 116 * np.power(Y, 1/3.0) - 16.0 if Y > 0.008856 else 903.3 * Y

            d = X + 15*Y + 3*Z
            if(d <= 0):
                d = 0.1

            # Calculate the u 
            u_temp = (4*X)/d
            u = 13*L*(u_temp - u_w)

            # Calculate the v
            v_temp = (9*Y)/d
            v = 13*L*(v_temp - v_w)

            LuvMatrix[i,j] = [L, u, v]
    return LuvMatrix



def luv_rgb(LuvMatrix):
    rows, cols, bands = LuvMatrix.shape # bands == 3
    u_w = (4*0.95/(0.95+ 15 + 3*1.09))
    v_w = (9/(0.95+ 15 + 3*1.09))
    XYZ2LRGBMatrix = [[3.240479, -1.53715, -0.498535],
                  [-0.969256, 1.875991, 0.041556],
                  [0.055648, -0.204043, 1.057311]]
    Luv2XYZMatrix = np.zeros([rows, cols, bands], dtype=np.float16)

    #Luv to XYZ conversion
    for i in range(0, rows) :
        for j in range(0, cols) :
            L, u, v = LuvMatrix[i, j]

            if(L == 0):
                u_temp = 0
                v_temp = 0
            else:
                u_temp = (u + 13*u_w*L)/(13*L)
                v_temp = (v + 13*v_w*L)/(13*L)

            if(L > 7.9996):
                Y = np.power((L + 16)/116, 3)
            else:
                Y = L/903.3

            if(v_temp == 0):
                X = 0
                Z = 0
            else:
                X = Y*2.25*(u_temp/v_temp)
                Z = (Y*(3 - 0.75*u_temp- 5*v_temp))/v_temp

            Luv2XYZMatrix[i,j] = [X, Y, Z]

    XYZ2LsRGBMatrix = np.zeros([rows, cols, bands], dtype=np.float16)
    LsRGB2NLsRGBMatrix = np.zeros([rows, cols, bands], dtype=np.float16)

    for i in range(0, rows) :
        for j in range(0, cols) :
            XYZ = Luv2XYZMatrix[i, j]
            #Linear RGB from XYZ
            XYZ2LsRGBMatrix[i, j] = np.dot(XYZ2LRGBMatrix, XYZ)

            R, G, B = XYZ2LsRGBMatrix[i, j]

            #Non Linear RGB from Linear RGB 
            non_linear_R = gammaClip(gamma(R))
            non_linear_G = gammaClip(gamma(G))
            non_linear_B = gammaClip(gamma(B))

            LsRGB2NLsRGBMatrix[i, j] = [non_linear_R, non_linear_G, non_linear_B]


    scaledOutput = np.zeros([rows, cols, bands], dtype=np.uint8)

    #final Scaled output in sRGB
    for i in range(0, rows) :
        for j in range(0, cols) :

            n_linear_R, n_linear_G, n_linear_B = LsRGB2NLsRGBMatrix[i, j]

            r = np.rint(n_linear_R*255)
            g = np.rint(n_linear_G*255)
            b = np.rint(n_linear_B*255)

            scaledOutput[i,j] = [b, g, r]

    return scaledOutput

if __name__ == "__main__":
    import cv2
    import sys

    if len(sys.argv) != 2:
        print("Must supply path to image file")

    try:
        inputImage = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
        print("rgb --> luv")
        luv = rgb_luv(inputImage)

        print("luv --> rgb")
        bgr = luv_rgb(luv)

        cv2.imshow('Input Image', inputImage)
        cv2.imshow('Scaled Output', bgr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except cv2.error:
        print("Must supply valid image path")