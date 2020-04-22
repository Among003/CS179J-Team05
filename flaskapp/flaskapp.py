import os
from flask import Flask, render_template, flash, request, url_for, redirect, session, make_response

app = Flask(__name__) 

data={'x':0} 
data={'y':0}
data={'hand':False}

@app.route('/',methods=['GET','POST'])
def index():
	if request.method =='POST':
		return 'Post Received'
	if request.method =='GET':
		return 'Get Received'
	return 'Success Logged In'

@app.route('/postx/<int:value>',methods=['GET','POST'])
def postx(value):
	
	if request.method == 'POST':
		data['x'] = value	

 
	return "Posted"

@app.route('/posty/<int:value>',methods=['GET','POST'])
def posty(value):
	if request.method == 'POST':
		data['y'] = value

	return "Posted"

@app.route('/posthand/<int:value>',methods=['GET','POST'])
def posthand(value):
	if request.method == 'POST':
		data['hand'] = bool(value)

	return "Posted"

@app.route('/gets/',methods=['GET','POST'])
def gets():

	if request.method == 'GET':
		return str(data['x'])
	return 'Get'

if __name__ == '__main__':
    app.run(debug=True)

