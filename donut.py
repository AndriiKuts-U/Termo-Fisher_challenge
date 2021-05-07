import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
from scipy import signal
from skimage import exposure
# import os
from os import listdir
from os.path import isfile, isdir, join
import csv
# Let's load a simple image with 3 black squares
# image = cv2.imread('1.tiff')
# cv2.waitKey(0)
def fit(file_name):
    image = cv2.imread(file_name, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_GRAYSCALE)

    def find_ellipses( ct): #img is grayscale image of what I want to fit
        # ret,th = cv2.threshold(img,127,255, 0)
        # contours,hierarchy = cv2.findContours(th, 2,1)
        elipses = []
        # print(contours)
        if len(ct) != 0:
            for cont in ct:
                if len(cont) < 5:
                    break
                elps = cv2.fitEllipse(cont)
                elipses.append(elps)
                #only returns one ellipse for now
        return elipses

    img_contrast = exposure.rescale_intensity(image, in_range=tuple(np.percentile(image, (5.0, 90.0))))

    # fig, axes = plt.subplots(2, 1, figsize=(20,20))
    # axes[0].imshow(img_contrast, cmap='gray') #gray, twilight, plasma, binary
    # axes[0].axis('on')
    # axes[1].imshow(image, cmap='gray')
    # axes[1].axis('on')
    # plt.tight_layout()
    # plt.show()

    img_con = signal.convolve(img_contrast, [[-1.], [-1.], [-1.],
                                            [-1.], [8.], [-1.],
                                            [-1.], [-1.], [-1.]])
    # img_con = signal.convolve(img_contrast, [[1., -1.], [-1., 1.]])
    # img_con = signal.convolve(img_contrast, [[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    # mask = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # img_con1 = exposure.rescale_intensity(img_con, in_range=tuple(np.percentile(img_con, (5.0, 90.0))))
    img_con1 = exposure.rescale_intensity(img_con, in_range=tuple(np.percentile(img_con, (1.0, 95.0))))
    # img_con1 = exposure.rescale_intensity(img_con, in_range=tuple(np.percentile(img_con, (1.0, 90.0))))
    img_con3 = exposure.rescale_intensity(img_con, in_range=tuple(np.percentile(img_con, (1.0, 95.0))))
    # fig, axes = plt.subplots(3, 1, figsize=(20,20))
    # axes[0].imshow(img_con1, cmap='gray') #gray, twilight, plasma, binary
    # axes[0].axis('on')
    # # axes[1].imshow(img_con2, cmap='gray')
    # # axes[1].axis('on')
    # axes[2].imshow(img_con3, cmap='gray')
    # axes[2].axis('on')
    # plt.tight_layout()
    # plt.show()



    # print(img_con1[img_con1 < np.max(img_con1)])
    # plt.imshow(img_con1 > (np.mean(img_con1)))
    # # plt.imshow(img_con1 < np.max(img_con1))
    # plt.show()


    img_con_next = signal.convolve(img_con1, [[-1.], [1.],
                                            [1.], [-1.]])

    img_con_next1 = exposure.rescale_intensity(img_con1, in_range=tuple(np.percentile(img_con_next, (1.0, 95.0))))

    v = np.max(img_con_next1)

    # print(img_con_next1)
    img_con_next1 = img_con_next1 < 0
    # print(img_con_next1)
    # plt.imshow(img_con_next1)
    # plt.show()
    # cv2.erode( img_con_next1, img_con_next1, 0, 4)

    img_con_next1 = img_con_next1.astype(np.uint8)

    # kernel = np.ones((5, 5), np.uint8)
    # img_con_next1 =  cv2.erode(img_con_next1, kernel)
    # plt.imshow(img_con_next1)
    # plt.show()




    # cv2.imshow('ssda', edged)
    dotts = []
    for i in range(0,len(img_con_next1)):
        for j in range(0,len(img_con_next1[i])):
            if  img_con_next1[i][j] == True:
                dotts.append([[j,i]])
            # else:
            #    img_con_next1[i][j] = False 


    # edged = cv2.Canny(img_con_next1,0,15)

    contour = np.array(dotts)
    # print(contour)

    img_con_next1*=255
    # print(img_con_next1)




    # imgray = cv2.cvtColor(img_con_next1, cv2.COLOR_BGR2GRAY)

    # ret, thresh = cv2.threshold(img_con_next1, 127, 255, 0)
    # contour1,hierarchy = cv2.findContours(img_con_next1,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ellipse = find_ellipses([contour])
    for i in ellipse:
        cv2.ellipse(img_con_next1,i,0,2)
    # ellipse.append(np.shape(image))
    # print(ellipse)

    # plt.imshow(img_con_next1)
    # plt.show()
    return ellipse, np.shape(image)



def test(folder):
    with open("results.csv", mode="a", encoding='utf-8',newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",")
        # file_writer.writerow(["filename","gt_ellipse_center_x","gt_ellipse_center_y","gt_ellipse_majoraxis","gt_ellipse_minoraxis","gt_ellipse_angle","image_width","image_height"])
        filenames = [f for f in listdir(folder) if isfile(join(folder, f)) and f.rsplit('.', 1)[1] == 'tiff']
        print(filenames)
        for filename in filenames:
            if filename is None:
                continue
            ellpse, size = fit(join(folder,filename))
            if(ellpse is not None and ellpse != []):
                file_writer.writerow([filename,ellpse[0][0][0],ellpse[0][0][1],ellpse[0][1][1]/2,ellpse[0][1][0]/2,round(ellpse[0][2]),size[0],size[1]])
            else:
                file_writer.writerow([filename,'','','','','',size[0],size[1]])


if __name__ == '__main__':
    test("./data/test/")
