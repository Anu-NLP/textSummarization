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
from transformers import BartForConditionalGeneration, BartTokenizer ,PegasusForConditionalGeneration, PegasusTokenizer


# Load the pre-trained BART model and tokenizer
fbmodel_name   = 'facebook/bart-large-cnn'
fbmodel        = BartForConditionalGeneration.from_pretrained(fbmodel_name)
fbtokenizer    = BartTokenizer.from_pretrained(fbmodel_name)

# Load the pre-trained Pegasus model and tokenizer
gcp_model_name = 'google/pegasus-xsum'
gcp_model      = PegasusForConditionalGeneration.from_pretrained(gcp_model_name)
gcp_tokenizer  = PegasusTokenizer.from_pretrained(gcp_model_name)

app = Flask(__name__)
app.secret_key = 'file_upload_key'
MYDIR = os.path.dirname(__file__)
print("MYDIR",MYDIR)


@app.route("/")
def render_default(): 
    return make_response(render_template('homelayout.html'),200)


def fb_summarize_chat(chat_text):
    inputs = fbtokenizer.encode("summarize: " + chat_text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = fbmodel.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = fbtokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def gcp_summarize_chat(chat_text):
    inputs = gcp_tokenizer.encode(chat_text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = gcp_model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = gcp_model.decode(summary_ids[0], skip_special_tokens=True)
    return summary




@app.route("/summarizeTranscript",methods=['GET', 'POST'] )    
def summarizeTranscript():
    Transcript  = request.form.get('Transcript')
    model       = request.form.get('model')
    summary     = ""
    if model    == "Facebook":
        summary = fb_summarize_chat(Transcript)
    elif model  == "Google" : 
        summary = gcp_summarize_chat(Transcript)
    d = {"error":"none","msg":summary}   
    return flask.jsonify(d)  

if __name__ == '__main__':
    app.debug = True
    app.run()

