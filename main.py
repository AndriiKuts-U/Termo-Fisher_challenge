import csv

from os import listdir
from os.path import isfile, isdir, join

import evaluate_ellipse_fit as ev_el_fit
import donut

def get_ellipses():
    '''
    get all *.tiff files and fit an ellipse on each of them.
    Then will write it to file 'results.csv'
    '''
    onlydirs = [f for f in listdir("./") if isdir(join("./", f)) and f != '__pycache__']
    with open("results.csv", mode="w", encoding='utf-8',newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",")
        file_writer.writerow(["filename","ellipse_center_x","ellipse_center_y","ellipse_majoraxis","ellipse_minoraxis","ellipse_angle","elapsed_time"])
    for dir in onlydirs:
        donut.test('./'+dir+'/')


def my_evaluation(csv_filepath, csv_ground_filepath):
    lst = []

    # csv_filepath = 'ground_truths_train.csv'

    with open(csv_filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['ellipse_center_x'] == '':
                        gt_ellipse = None
                else:
                        gt_ellipse = {'center': (float(row['ellipse_center_x']), float(row['ellipse_center_y'])),
                                      'axes': (float(row['ellipse_majoraxis']), float(row['ellipse_minoraxis'])),
                                      'angle': int(round(float(row['ellipse_angle'])))}
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
    # This Function will rewrite file with results of fitting.
    # get_ellipses()

    evaluations = my_evaluation('results.csv', 'ground_truths_train.csv')
    n = len(evaluations)
    s = 0
    for i in evaluations:
        print(i)
        s += i[1]

    print()
    # sum: 23.093911148881034 mean: 0.2960757839600133
    if n != 0:
        mean = s/n
    print('sum:', s, 'mean:', mean)


# 2 2

