import os
from flask import Flask, render_template, flash, request, url_for, redirect, session, make_response, jsonify

app = Flask(__name__) 

x = {'xValue':0} 
y = {'yValue':0}
handPosition = {'hand':0}



data = {'x':0, 'y':0, 'hand':0}

@app.route('/',methods=['GET','POST'])
def index():
	if request.method =='POST':
		return 'Post Received'
	if request.method =='GET':
		return 'Get Received'
	return 'Success Logged In'

@app.route('/postData/',methods=['POST'])
def postData():
	if request.method == 'POST':
		content = request.get_json()
		data['x'] = content.get('x')
		data['y'] = content.get('y')
		data['hand'] = content.get('hand')
		return 'Posted'
	return 'Post'


@app.route('/postx/<int:value>',methods=['GET','POST'])
def postx(value):
	
	if request.method == 'POST':
		x['xValue'] = value	

 
	return "Posted"

@app.route('/posty/<int:value>',methods=['GET','POST'])
def posty(value):
	if request.method == 'POST':
		y['yValue'] = value

	return "Posted"

@app.route('/posthand/<int:value>',methods=['GET','POST'])
def posthand(value):
	if request.method == 'POST':
		handPosition['hand'] = value

	return "Posted"

@app.route('/getData/',methods=['GET','POST'])
def getData():
	if request.methdod == 'GET':
		return jsonify(data)
		#return "TODO"
	return 'GET'

@app.route('/getx/',methods=['GET','POST'])
def getx():

	if request.method == 'GET':
	#	return str(x['xValue'])
		return jsonify(data)
	#	return jsonify({'x': x['xValue'], 'y': y['yValue'], 'hand': handPosition['hand']})
	return 'Get'


@app.route('/gety/',methods=['GET','POST'])
def gety():

        if request.method == 'GET':
                return str(y['yValue'])
        return 'Get'


@app.route('/gethand/',methods=['GET','POST'])
def gethand():

        if request.method == 'GET':
                return str(handPosition['hand'])
        return 'Get'



if __name__ == '__main__':
    app.run(debug=True)

