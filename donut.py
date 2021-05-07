import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
from scipy import signal
from skimage import exposure
from os import listdir
from os.path import isfile, isdir, join
import csv
import time

def fit(file_name):
    image = cv2.imread(file_name, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_GRAYSCALE)
    start = time.time()
    def find_ellipses( ct): 
        elipses = []
        if len(ct) != 0:
            for cont in ct:
                if len(cont) < 5:
                    break
                elps = cv2.fitEllipse(cont)
                elipses.append(elps)
        return elipses

    img_contrast = exposure.rescale_intensity(image, in_range=tuple(np.percentile(image, (5.0, 90.0))))

    img_con = signal.convolve(img_contrast, [[-1.], [-1.], [-1.],
                                            [-1.], [8.], [-1.],
                                            [-1.], [-1.], [-1.]])
    img_con1 = exposure.rescale_intensity(img_con, in_range=tuple(np.percentile(img_con, (1.0, 95.0))))

    img_con_next = signal.convolve(img_con1, [[-1.], [1.],
                                            [1.], [-1.]])

    img_con_next1 = exposure.rescale_intensity(img_con1, in_range=tuple(np.percentile(img_con_next, (1.0, 95.0))))

    v = np.max(img_con_next1)
    img_con_next1 = img_con_next1 < 0
    img_con_next1 = img_con_next1.astype(np.uint8)

    dotts = []
    for i in range(0,len(img_con_next1)):
        for j in range(0,len(img_con_next1[i])):
            if  img_con_next1[i][j] == True:
                dotts.append([[j,i]])

    contour = np.array(dotts)
    img_con_next1*=255
    ellipse = find_ellipses([contour])
    for i in ellipse:
        cv2.ellipse(img_con_next1,i,0,2)
    end = time.time()
    # print((end - start) * 1000)
    return ellipse, (end - start) * 1000



def test(folder):
    with open("results.csv", mode="a", encoding='utf-8',newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",")
        # file_writer.writerow(["filename","gt_ellipse_center_x","gt_ellipse_center_y","gt_ellipse_majoraxis","gt_ellipse_minoraxis","gt_ellipse_angle","image_width","image_height"])
        filenames = [f for f in listdir(folder) if isfile(join(folder, f)) and f.rsplit('.', 1)[1] == 'tiff']
        print(filenames)
        for filename in filenames:
            if filename is None:
                continue
            ellpse, elapsed_time = fit(join(folder,filename))
            if(ellpse is not None and ellpse != []):
                file_writer.writerow([filename,ellpse[0][0][0],ellpse[0][0][1],ellpse[0][1][1]/2,ellpse[0][1][0]/2,round(ellpse[0][2]),elapsed_time])
            else:
                file_writer.writerow([filename,'','','','','',elapsed_time])
