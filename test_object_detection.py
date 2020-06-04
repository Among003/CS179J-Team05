# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:16:06 2020

@author: tyler
"""

import os, cv2, sys, json, re, pytest
import numpy as np
import tensorflow as tf
import datetime as t
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(cwd,'..'))
print(os.getcwd())
import objectDetection.hand_detection as hand_detection
import objectDetection.coordinates as coordinates
import objectDetection.controlEnvironment as control
os.chdir(cwd)

# tensorflow module for utilities using the models research repository
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

p = re.compile('([ .:-])')
TEST_DUMP_FILE = "test_" + p.sub('', str(t.datetime.now()).split('.')[0])

# Video files for testing
testVideo1_1 = os.path.join(cwd, "testing/video/video1_test1.mp4")
testVideo2_1 = os.path.join(cwd, "testing/video/video2_test1.mp4")
testVideo1_2 = os.path.join(cwd, "testing/video/video1_test2.mp4")
testVideo2_2 = os.path.join(cwd, "testing/video/video2_test2.mp4")
testVideo1_3 = os.path.join(cwd, "testing/video/video1_test3.mp4")
testVideo2_3 = os.path.join(cwd, "testing/video/video2_test3.mp4")
testVideo1_4 = os.path.join(cwd, "testing/video/video1_test4.mp4")
testVideo2_4 = os.path.join(cwd, "testing/video/video2_test4.mp4")

def CheckWrong(predicted, correct):
    """
    Takes in array of predicted values and verifies that each prediction has the correct label.
    If any of the predictions are wrong, the test fails.

    Returns
    -------
    report : True or False

    """
    for prediction in predicted:
        if prediction != correct:
            print("Expected: ", correct," recieved: ", prediction)
            return False
    return True

@pytest.mark.parametrize('testVideo1,testVideo2,label',[(testVideo1_1,testVideo2_1,"open hand"),(testVideo1_2,testVideo2_2,"open hand"),(testVideo1_3,testVideo2_3,"closed hand"),(testVideo1_4,testVideo2_4,"closed hand")])
def testVideoOnObjectDetection(testVideo1, testVideo2, label):
    """
    Creates environment for object detection class to run and then runs the object detection module over the given video feed.

    Returns
    -------
    void

    """
    
    GRAPH_PATH = os.path.join(cwd, "ObjectDetection/inference_graph/frozen_inference_graph.pb")
    LABEL_PATH = os.path.join(cwd, "ObjectDetection/training/labelmap.pbtxt")
    
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
    
    assert correct == True
    
    report = {"correct": correct, "input": video1, "output": results}
    
    return
    #return report
    
    
# def TestVideoOnObjectDetectionHarness():
#     """
#     Specific harness for Video Object Detection, configures

#     Returns
#     -------
#     Report - Dictionary containing

#     """
    
#     report = {}
    
#     # report["test1"] = testVideoOnObjectDetection(testVideo1_1, testVideo2_1, "open hand")
#     # report["test2"] = testVideoOnObjectDetection(testVideo1_2, testVideo2_2, "open hand")
#     # report["test3"] = testVideoOnObjectDetection(testVideo1_3, testVideo2_3, "closed hand")
#     # report["test4"] = testVideoOnObjectDetection(testVideo1_4, testVideo2_4, "closed hand")
    
#     return report

def testControlEnvironment(video1, video2):
    """
    Tests the control environment of the system by verifying the execution of the program executes without exceptions

    Parameters
    ----------
    video1 : video file
        video feed of top webcam
    video2 : video file
        video feed of side webcam

    Returns
    -------
    bool
        Return false if any line of the control environment throws an exception

    """
    try:
        control.main(video1, video2, Verbose=True, Testing=True)
        return True
    except Exception:
        return False

@pytest.mark.parametrize('testInput,expected',[((testVideo1_1,testVideo2_1),True),((testVideo1_2,testVideo2_2),True),((testVideo1_3,testVideo2_3),True),((testVideo1_4,testVideo2_4),True)])
def testControlEnvironmentHarness(testInput, expected):
    assert testControlEnvironment(*testInput) == expected

# def runObjDetectTests():
#     print('started testing object detection')
#     report = TestVideoOnObjectDetectionHarness()
#     for test in report:
#         print(test, " Report returned: ", report[test]["correct"])
#     print(report)
#     with open(os.path.join(os.path.abspath('testing/logs'), TEST_DUMP_FILE), 'w+') as jF:
#         json.dump(str(report), jF)
        
# def runControlTests():
#     print('started testing control environment')
#     report = testControlEnvironmentHarness()
#     for test in report:
#         print(test, " Report returned: ", report[test]["correct"])
#     print(report)
#     with open(os.path.join(os.path.abspath('testing/logs'), TEST_DUMP_FILE), 'w+') as jF:
#         json.dump(str(report), jF)

def main():
    # runObjDetectTests()
    # runControlTests()
    return
    
if __name__ == '__main__':
   main()