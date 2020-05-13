# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:11:15 2020

@author: tyler
"""

import os, json, sys, time
import requests as req
import hand_detection
cwd = os.getcwd()
os.chdir('../client')
import client
os.chdir(cwd)

def main(video1, video2):
    GRAPH_PATH = os.path.join(os.getcwd(), "inference_graph/frozen_inference_graph.pb")
    LABEL_PATH = os.path.join(os.getcwd(), "training\labelmap.pbtxt")
    
    Video1 = cv2.VideoCapture(testVideo1)
    Video2 = cv2.VideoCapture(testVideo2)
    
    while(Video1.isOpened() and Video2.isOpened()):
        
        coors = coordinates.coordinates()
        obj_detect = hand_detection.Object_Detection(coors, GRAPH_PATH, LABEL_PATH, Video1, Video2)
        
        results = obj_detect.Detect()
        
        client.

if __name__ == '__main__':
    main(0, 1)