# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:16:06 2020

@author: tyler
"""

import os, cv2, sys, json, re
import numpy as np
import tensorflow as tf
import datetime as t
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir('..')
import hand_detection
import coordinates
import controlEnvironment as control
os.chdir(cwd)

# tensorflow module for utilities using the models research repository
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

p = re.compile('([ .:-])')
TEST_DUMP_FILE = "test_" + p.sub('', str(t.datetime.now()).split('.')[0])

def CheckWrong(predicted, correct):
    for prediction in predicted:
        if prediction != correct:
            print("Expected: ", correct," recieved: ", prediction)
            return False
    return True

def testVideoOnObjectDetection(testVideo1, testVideo2, label):
    """
    

    Returns
    -------
    report : Dictionary
        Gives passing value, input, and output as dictionary to be aggregated

    """
    
    GRAPH_PATH = os.path.join(cwd, "../inference_graph/frozen_inference_graph.pb")
    LABEL_PATH = os.path.join(cwd, "../training\labelmap.pbtxt")
    
    video1 = cv2.VideoCapture(testVideo1)
    video2 = cv2.VideoCapture(testVideo2)
    
    coors = coordinates.coordinates()
    obj_detect = hand_detection.Object_Detection(coors, GRAPH_PATH, LABEL_PATH, video1, video2, Verbose=True)
    
    results = []
    
    while(video1.isOpened() and video2.isOpened()):
        output = obj_detect.Detect()
        if output is None: break
        else: results.append(output)
        
    cv2.destroyAllWindows()
    
    print(results)
    print([result for result in results])
    correct = CheckWrong([result["video1"]["classes"] for result in results], label)
    
    #print([])
    
    report = {"correct": correct, "input": video1, "output": results}
    #report = {"output": (boxes, scores, classes)}
    
    return report
    
    
def TestVideoOnObjectDetectionHarness():
    """
    Specific harness for Video Object Detection, configures

    Returns
    -------
    Report - Dictionary containing

    """
    
    report = {}
    
    os.chdir('..')
    
    testVideo1_1 = os.path.join(cwd, "testing/video/video1_test1.mp4")
    testVideo2_1 = os.path.join(cwd, "testing/video/video2_test1.mp4")
    testVideo1_2 = os.path.join(cwd, "testing/video/video1_test2.mp4")
    testVideo2_2 = os.path.join(cwd, "testing/video/video2_test2.mp4")
    testVideo1_3 = os.path.join(cwd, "testing/video/video1_test3.mp4")
    testVideo2_3 = os.path.join(cwd, "testing/video/video2_test3.mp4")
    testVideo1_4 = os.path.join(cwd, "testing/video/video1_test4.mp4")
    testVideo2_4 = os.path.join(cwd, "testing/video/video2_test4.mp4")
    
    report["test1"] = testVideoOnObjectDetection(testVideo1_1, testVideo2_1, "open hand")
    report["test2"] = testVideoOnObjectDetection(testVideo1_2, testVideo2_2, "open hand")
    report["test3"] = testVideoOnObjectDetection(testVideo1_3, testVideo2_3, "closed hand")
    report["test4"] = testVideoOnObjectDetection(testVideo1_4, testVideo2_4, "closed hand")
    
    return report

def testControlEnvironment(video1, video2, correct):
    
    control.main(video1, video2, Verbose=True, Testing=True)
    
    # try:
    #     control.main(video1, video2)
    # except Exception:
    #     print
    #     return {"correct": False}
    
    return {"correct": True}

def testControlEnvironmentHarness():
    
    report = {}
    
    os.chdir('..')
    
    testVideo1_1 = os.path.join(cwd, "testing/video/video1_test1.mp4")
    testVideo2_1 = os.path.join(cwd, "testing/video/video2_test1.mp4")
    testVideo1_2 = os.path.join(cwd, "testing/video/video1_test2.mp4")
    testVideo2_2 = os.path.join(cwd, "testing/video/video2_test2.mp4")
    testVideo1_3 = os.path.join(cwd, "testing/video/video1_test3.mp4")
    testVideo2_3 = os.path.join(cwd, "testing/video/video2_test3.mp4")
    testVideo1_4 = os.path.join(cwd, "testing/video/video1_test4.mp4")
    testVideo2_4 = os.path.join(cwd, "testing/video/video2_test4.mp4")
    
    report["test1"] = testControlEnvironment(testVideo1_1, testVideo2_1, "open hand")
    report["test2"] = testControlEnvironment(testVideo1_2, testVideo2_2, "open hand")
    report["test3"] = testControlEnvironment(testVideo1_3, testVideo2_3, "closed hand")
    report["test4"] = testControlEnvironment(testVideo1_4, testVideo2_4, "closed hand")
    
    return report

def runObjDetectTests():
    print('started testing object detection')
    report = TestVideoOnObjectDetectionHarness()
    for test in report:
        print(test, " Report returned: ", report[test]["correct"])
    print(report)
    with open(os.path.join(os.path.abspath('testing/logs'), TEST_DUMP_FILE), 'w+') as jF:
        json.dump(str(report), jF)
        
def runControlTests():
    print('started testing control environment')
    report = testControlEnvironmentHarness()
    for test in report:
        print(test, " Report returned: ", report[test]["correct"])
    print(report)
    with open(os.path.join(os.path.abspath('testing/logs'), TEST_DUMP_FILE), 'w+') as jF:
        json.dump(str(report), jF)

def main():
    runObjDetectTests()
    runControlTests()
    
if __name__ == '__main__':
   main()