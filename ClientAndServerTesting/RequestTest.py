import os
import requests as req
import sys
import time


#URL FOR SERVER

def serverAndClientTest(x, y, z, hand):
	url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"
	
	
	r = req.post(url + "/postData/", json={'x': x, 'y': y, 'z': z, 'hand': hand})
	time.sleep(2)

	
	r = req.get(url + "/getData/",  headers={'Cache-Control': 'no-cache'})

	if r.ok:
		data = r.json()
		xVal = float(data['x'])
		yVal = float(data['y'])
		zVal = float(data['z'])
		handVal = str(data['hand'])
		print("x: " + str(xVal) + " y: " + str(yVal) + " z: " + str(zVal) +" hand: " + str(handVal))
			
		r.close()

		try:                                                              
			assert (abs(float(xVal)-float(x)) < 0.001) and (abs(float(yVal)-float(y)) < 0.001) and (abs(float(zVal)-float(z)) < 0.001) and (handVal == hand) 
		except:                                                                                                                                                                                                                         
			print("Warning, assertion failed on values: "+ str(x) + " " + str(y) + " " + str(z) + " " + str(hand) + "\n" + "Recieved: " + str(xVal) + " " + str(yVal) +  " " + str(zVal) +   " " + str(handVal) +" instead") 
			print(hand," ",handVal)
			print(hand == handVal)
			return {"correct": False, "input" : (x,y,z,hand), "output": (xVal, yVal, zVal, handVal)} 
		
		return return {"correct": True, "input" : (x,y,z,hand), "output": (xVal, yVal, zVal, handVal)} ;

	



