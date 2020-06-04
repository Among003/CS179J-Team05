import os
from flask import Flask, render_template, flash, request, url_for, redirect, session, make_response, jsonify

import json

app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

x = {'xValue':0} 
y = {'yValue':0}
handPosition = {'hand':0}
z = {'zValue':0}


data = {'x':0, 'y':0, 'hand':0, 'z':0}

@app.route('/postData/',methods=['POST'])
def postData():
	if request.method == 'POST':
		content = request.get_json(cache=False)
		data['x'] = content.get('x')
		data['y'] = content.get('y')
		data['hand'] = content.get('hand')
		data['z'] = content.get('z')		

		outfile = open("/home/ubuntu/CS179J-Team05/flaskapp/static/data.txt", 'w+');
		outfile.write(json.dumps(data))	
		return 'Posted'
	return 'Post'

@app.route('/getData/',methods=['GET','POST'])
def getData():
	if request.method == 'GET':
		infile = open("/home/ubuntu/CS179J-Team05/flaskapp/static/data.txt",'r+');
		tempDict = json.load(infile)
		return jsonify(tempDict)
		#return "TODO"
	return 'GET'

if __name__ == '__main__':
    app.run(debug=True)

