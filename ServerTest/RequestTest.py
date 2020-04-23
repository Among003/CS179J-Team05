import os
import requests as req
import sys
import time

#URL FOR SERVER

url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"

if len(sys.argv) < 4:
	print("Enter three arguments")
	sys.exit()

x_val = sys.argv[1]
y_val = sys.argv[2]
hand_val = bool(int(sys.argv[3]))

r = req.post(url + "/postData/", json={'x': x_val, 'y': y_val, 'hand': hand_val})

time.sleep(2)

data = 0
r = req.get(url + "/getData/",  headers={'Cache-Control': 'no-cache'})

if r.ok:
	data = r.json()
	xVal = int(data['x'])
	yVal = int(data['y'])
	handVal = bool(data['hand'])
	print("x: " + str(xVal) + " y: " + str(yVal) + " hand: " + str(handVal))
    
	r.close()

try:                                                              
	assert xVal == int(sys.argv[1]) and yVal == int(sys.argv[2]) and handVal == int(sys.argv[3]) 
except:                                                                                                                                                                                                                         
	print("Warning, assertion failed on values: "+ sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + "\n" + "Recieved: " + str(xVal) + " " + str(yVal) +  " " + str(handVal) + " instead") 




