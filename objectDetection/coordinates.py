# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:30:08 2020

@author: tyler
"""

import math

OrientationLookup = {"top": 0,
                     "bottom": 2,
                     "left": 1,
                     "right": 3}

THRESHOLD_DISTANCE = 0.2


class coordinates:
    def __init__(self, filt="ED"):
        self.past = []
        self.filtering = self.EuclideanDistance
        
    def GetCoors(self, box1, box2):
        x_coor = (box1[OrientationLookup["left"]] + box1[OrientationLookup["right"]]) / 2
        y_coor = (box1[OrientationLookup["top"]] + box1[OrientationLookup["bottom"]]) / 2
        z_coor = (box2[OrientationLookup["top"]] + box2[OrientationLookup["bottom"]]) / 2
        return (x_coor, y_coor, z_coor)
    
    def Filter(self, coors):
        if self.filtering(coors):
            if self.past != []: self.past.pop(0)
            self.past.append(coors)
            return coors
        else:
            return None
        
    def EuclideanDistance(self, coors):
        if self.past == []: return True
        previous = self.past[len(self.past) - 1]
        now_x = coors[0]
        prev_x = previous[0]
        now_y = coors[1]
        prev_y = previous[1]
        now_z = coors[2]
        prev_z = previous[2]
        dist = math.sqrt((now_x - prev_x)**2 + (now_y - prev_y)**2 + (now_z - prev_z)**2)
        return dist < THRESHOLD_DISTANCE