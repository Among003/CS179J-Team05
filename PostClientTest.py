import os
import requests as req
import json
import sys
import time

url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"

if len(sys.argv) < 4:
	print("Enter three arguments")
	sys.exit()

x_val = sys.argv[1]
y_val = sys.argv[2]
hand_val = bool(int(sys.argv[3]))

data = json.dumps(tmp)

r = req.post(url + "/postData/", json={'x': x_val, 'y': y_val, 'hand': hand_val})

print(r.text)
