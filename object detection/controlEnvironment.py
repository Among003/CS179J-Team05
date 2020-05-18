# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:11:15 2020

@author: tyler
"""

import os, json, sys, time, cv2
import requests as req
import tkinter as tk
import hand_detection
import coordinates
cwd = os.path.dirname(os.path.abspath(__file__))
print(cwd)
os.chdir(os.path.join(cwd, '../client'))
import client
os.chdir(cwd)

#url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"

def main(video1, video2, Verbose=False, Testing=False):
    print("starting control environment")
    GRAPH_PATH = os.path.join(os.getcwd(), "inference_graph/frozen_inference_graph.pb")
    LABEL_PATH = os.path.join(os.getcwd(), "training\labelmap.pbtxt")
    
    #if Testing:
        #t = tk.Tk()
        #label = tk.Label(t, text='Sending Data')
        #t.mainloop()
    
    Video1 = cv2.VideoCapture(video1)
    Video2 = cv2.VideoCapture(video2)
    
    coors = coordinates.coordinates()
    obj_detect = hand_detection.Object_Detection(coors, GRAPH_PATH, LABEL_PATH, Video1, Video2, Verbose=Verbose)
    
    print("starting detection")
    
    while(Video1.isOpened() and Video2.isOpened()):
        
        results = obj_detect.Detect()
        
        if results is None: break
    
        if Verbose: print(results["coors"][0], results["coors"][1], results["coors"][2], results["hand_val"])
        
        client.postData(results["coors"][0], results["coors"][1], results["coors"][2], results["hand_val"])
    
    Video1.release()
    Video2.release()
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #main(0, 1)
    main(1, 0, Verbose=True, Testing=True)