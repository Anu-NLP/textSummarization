from flask import Flask, render_template, flash, url_for, request, make_response, jsonify, session,send_from_directory
from werkzeug.utils import secure_filename
import os, time
import io
import base64
import json
import datetime
import os, sys, glob
from flask import send_file
import time
import random
import pandas as pd
import flask



app = Flask(__name__)
app.secret_key = 'file_upload_key'
MYDIR = os.path.dirname(__file__)
print("MYDIR",MYDIR)


@app.route("/")
def render_default(): 
    return make_response(render_template('home.html'),200)
            

@app.route("/summarizeTranscript",methods=['GET', 'POST'] )    
def summarizeTranscript():
    Transcript  = request.form.get('Transcript')
    message     = """  Summary Block """
    d = {"error":"none","msg":Transcript}   
    return flask.jsonify(d)        

if __name__ == '__main__':
    app.debug = True
    app.run()

