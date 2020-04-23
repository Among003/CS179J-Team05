# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:16:06 2020

@author: tyler
"""

import os, cv2, sys, json
sys.path.append('D:\school\CS179J\tensorflow\models')
sys.path.append('D:\school\CS179J\tensorflow\models\research')
sys.path.append('D:\school\CS179J\tensorflow\models\research\slim')
import numpy as np
import tensorflow as tf
nowdir = os.getcwd()
os.chdir('..')
import hand_detection
os.chdir(nowdir)

# tensorflow module for utilities using the models research repository
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

def CheckWrong(predicted, correct):
    for prediction in predicted:
        if prediction != correct:
            return False
    return True

def testVideoOnObjectDetection(testVideo):
    """
    

    Returns
    -------
    report : Dictionary
        Gives passing value, input, and output as dictionary to be aggregated

    """
    
    #VIDEO_PATH = os.path.join(os.getcwd(), "testing/video/test1.mp4")
    
    (category_index, graph, sess) = hand_detection.InitObjectDetection()
    
    video = cv2.VideoCapture(testVideo)
    
    results = hand_detection.Detect(video, category_index, graph, sess)
    
    correct = CheckWrong([result['classes'] for result in results], 'open hand')
    
    report = {"correct": correct, "output": results}
    #report = {"output": (boxes, scores, classes)}
    
    return report
    
    
def TestVideoHarness():
    """
    Specific harness for Video Object Detection, configures

    Returns
    -------
    None.

    """
    
    report = {}
    
    os.chdir('..')
    
    testVideo1 = os.path.join(os.getcwd(), "testing/video/test1.mp4")
    testVideo2 = os.path.join(os.getcwd(), "testing/video/test2.mp4")
    
    report["test1"] = testVideoOnObjectDetection(testVideo1)
    report["test2"] = testVideoOnObjectDetection(testVideo2)
    
    return report
    
if __name__ == '__main__':
    print('started testing object detection')
    report = TestVideoHarness()
    for test in report:
        print(test, " Report returned: ", report[test]["correct"])
    print(report)