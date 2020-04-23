# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:16:06 2020

@author: tyler
"""

import os, cv2, sys, json, re
sys.path.append('D:\school\CS179J\tensorflow\models')
sys.path.append('D:\school\CS179J\tensorflow\models\research')
sys.path.append('D:\school\CS179J\tensorflow\models\research\slim')
import numpy as np
import tensorflow as tf
import datetime as t
nowdir = os.getcwd()
os.chdir('..')
import hand_detection
os.chdir(nowdir)

# tensorflow module for utilities using the models research repository
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

p = re.compile('([ .:-])')
#test = p.sub('', str(t.datetime.now()).split('.')[0])
TEST_DUMP_FILE = "test_" + p.sub('', str(t.datetime.now()).split('.')[0])

def CheckWrong(predicted, correct):
    for prediction in predicted:
        if prediction != correct:
            return False
    return True

def testVideoOnObjectDetection(testVideo, label):
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
    
    correct = CheckWrong([result['classes'] for result in results], label)
    
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
    testVideo3 = os.path.join(os.getcwd(), "testing/video/test3.mp4")
    testVideo4 = os.path.join(os.getcwd(), "testing/video/test4.mp4")
    
    report["test1"] = testVideoOnObjectDetection(testVideo1, "open hand")
    report["test2"] = testVideoOnObjectDetection(testVideo2, "open hand")
    report["test3"] = testVideoOnObjectDetection(testVideo3, "closed hand")
    report["test4"] = testVideoOnObjectDetection(testVideo4, "closed hand")
    
    return report
    
if __name__ == '__main__':
    print('started testing object detection')
    report = TestVideoHarness()
    for test in report:
        print(test, " Report returned: ", report[test]["correct"])
    print(report)
    with open(os.path.join(os.path.abspath('testing/logs'), TEST_DUMP_FILE), 'w+') as jF:
        json.dump(str(report), jF)
    #print(report)