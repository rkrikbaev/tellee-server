import os
import cv2
import numpy
import random
from tqdm import tqdm

train_data = './data/train/'
test_data = './data/test1/'

def one_hot_label(img):
    label = img.split('.')[0]
    if label == 'normal':
        ohl = numpy.array([1, 0, 0, 0, 0])
    elif label == 'case1':
        ohl = numpy.array([0, 1, 0, 0, 0])
    elif label == 'case2':
        ohl = numpy.array([0, 0, 1, 0, 0])
    elif label == 'case3':
        ohl = numpy.array([0, 0, 0, 1, 0])
    elif label == 'case4':
        ohl = numpy.array([0, 0, 0, 0, 1])
    return ohl

def train_data_with_label():
    train_images = []
    for i in tqdm(os.listdir(train_data)):
        path = os.path.join(train_data, i)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28))
        img = numpy.float32(img)
        img = img.reshape(-1)       
        train_images.append([numpy.array(img, dtype=numpy.float32), one_hot_label(i)])
    random.shuffle(train_images)
    return train_images

def test_data_with_label():
    test_images = []
    for i in tqdm(os.listdir(test_data)):
        path = os.path.join(test_data, i)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28))
        img = numpy.float32(img)
        img = img.reshape(-1)
        test_images.append([numpy.array(img, dtype=numpy.float32), one_hot_label(i)])
    return test_images
