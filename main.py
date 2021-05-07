import csv

from os import listdir
from os.path import isfile, isdir, join

import evaluate_ellipse_fit as ev_el_fit
import donut

onlydirs = [f for f in listdir("./") if isdir(join("./", f)) and f != '__pycache__']


for dir in onlydirs:
    with open("results.csv", mode="w", encoding='utf-8',newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",")
        file_writer.writerow(["filename","ellipse_center_x","ellipse_center_y","ellipse_majoraxis","ellipse_minoraxis","ellipse_angle","elapsed_time"])
    donut.test('./'+dir+'/')



def my_evaluation(csv_filepath, csv_ground_filepath):
    lst = []

    # csv_filepath = 'ground_truths_train.csv'

    with open(csv_filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['gt_ellipse_center_x'] == '':
                        gt_ellipse = None
                else:
                        gt_ellipse = {'center': (float(row['gt_ellipse_center_x']), float(row['gt_ellipse_center_y'])),
                                      'axes': (float(row['gt_ellipse_majoraxis']), float(row['gt_ellipse_minoraxis'])),
                                      'angle': int(round(float(row['gt_ellipse_angle'])))
                                      }
                lst.append((row['filename'], gt_ellipse))


    evaluations = list()
    # csv_ground_filepath = 'ground_truths_train.csv'
    for image in lst:
        ev = ev_el_fit.evaluate_ellipse_fit(image[0], image[1], csv_ground_filepath)
        evaluations.append((image[0], ev))

    # for i in evaluations:
    #     print(i)

    return evaluations


if __name__ == "__main__":
    evaluations = my_evaluation('results.csv', 'ground_truths_train.csv')
    n = len(evaluations)
    s = 0
    for i in evaluations:
        print(i)
        s += i[1]

 
    # sum: 23.093911148881034 mean: 0.2960757839600133
    mean = 0
    if(n != 0):
        mean = s/n
    
    print('sum:', s, 'mean:', mean)
