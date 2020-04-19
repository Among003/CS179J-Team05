import os
from flask import Flask, render_template, flash, request, url_for, redirect, session, make_response

app = Flask(__name__) 

data={'x':0} 

@app.route('/',methods=['GET','POST'])
def index():
	if request.method =='POST':
		return 'Post Received'
	if request.method =='GET':
		return 'Get Received'
	return 'Success Logged In'

@app.route('/postfunct/<int:value>',methods=['GET','POST'])
def postfunct(value):
	
	if request.method == 'POST':
		data['x'] = value	

 
	return "Posted"


@app.route('/gets/',methods=['GET','POST'])
def gets():

	if request.method == 'GET':
		return str(data['x'])
	return 'Get'

 
@app.route('/delete-visits/')
def delete_visits():
	session.pop('visits', None) # delete visits
	return 'Visits deleted'

if __name__ == '__main__':
    app.run(debug=True)

