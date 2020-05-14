import os
import requests as req
import json
import sys
import time

url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"

def postData(x_val, y_val, z_val, hand_val):
    """
    Sends POST request to server and sends given data
    Returns
    -------
    None.
    """
    r = req.post(url + "/postData/", json={'x': x_val, 'y': y_val, 'z': z_val, 'hand': hand_val})

    try:
        r.raise_for_status()
    except r.exceptions.HTTPError as e:
        return "Error: " + str(e)


def getData():
    """
    Sends GET request to server and retrieves data from server.
    Returns
    -------
    Dictionary containing x,y,z and hand values. 
    """
    r = req.get(url + "/getData/",  headers={'Cache-Control': 'no-cache'})

    try:
        r.raise_for_status()
    except r.exceptions.HTTPError as e:
        return "Error: " + str(e)

    data = r.json()
    xVal = float(data['x'])
    yVal = float(data['y'])
    zVal = float(data['z'])
    handVal = data['hand']
    print("x: " + str(xVal) + " y: " + str(yVal) + " z: " + str(zVal)  + " hand: " + str(handVal))

    data = {'x': xVal, 'y': yVal, 'z': zVal, 'hand': handVal}

    return data



postData(0.12345, 0.65489, 0.147852, False)