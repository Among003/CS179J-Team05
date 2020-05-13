# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:01:01 2020

@author: tyler
"""

import testmuh
import cv2
import numpy as np
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

def changeIt(frame, cat_i, classes, boxes, scores):
    return vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            cat_i,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)

boxy = [np.array([.1, .1, .9, .9]),
        np.array([.2, .1, .9, .9]),
        np.array([.3, .1, .9, .9]),
        np.array([.4, .1, .9, .9]),
        np.array([.4, .1, .9, .9]),
        np.array([.4, .2, .9, .9]),
        np.array([.4, .3, .9, .9]),
        np.array([.4, .4, .9, .9]),
        np.array([.4, .4, .9, .9]),
        np.array([.4, .4, .8, .9]),
        np.array([.4, .4, .7, .9]),
        np.array([.4, .4, .6, .9]),
        np.array([.4, .4, .6, .9]),
        np.array([.4, .4, .6, .8]),
        np.array([.4, .4, .6, .7]),
        np.array([.4, .4, .6, .6]),
         ]

report, cat_i, classes, boxes, scores = testmuh.TestVideoHarness()

video = cv2.VideoCapture(0)

for box in boxy:
    ret, frame = video.read()
    boxes[0][0] = box
    new_frame = changeIt(frame, cat_i, classes, boxes, scores)
    cv2.imshow('onj', new_frame)
    cv2.waitKey(2000)

cv2.destroyAllWindows()
    
