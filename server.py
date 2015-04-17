from flask import request, Flask, redirect, url_for, render_template
import json
# from werkzeug import secure_filename
import numpy as np
import pandas as pd 
from os import path 

import pysax

app = Flask(__name__)

UPLOAD_FOLDER = "static/upload/"
DEFAULT_STRIDE = 10
DEFAULT_ALPHABET = "ABCD"
DEFAULT_NBINS = 7

DATA = [""]
s1 = pd.read_table(open('static/data/chfdb_chf01_275_arti.txt',"r"), header = None,  names = ['y'])
s2 = pd.read_table(open('static/data/chfdb_chf01_275_arti_2.txt',"r"), header = None,  names = ['y'])
s = s1

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@app.route('/get_ts', methods=["GET"])
def get_ts():
	d = request.args["dataSource"]
	if d == "ECG1":
		return json.dumps([{'x': x, 'y': y} for x, y in enumerate(s1.y)])
	elif d == "ECG2":
		s = s2
		return json.dumps([{'x': x, 'y': y} for x, y in enumerate(s2.y)])

@app.route("/search", methods=["POST"])
def search_pattern():
	print request.get_json()
	target_start = int(request.get_json()["target_start"])
	target_end = int(request.get_json()["target_end"])
	stride = int(request.get_json()["stride"]) or DEFAULT_STRIDE
	nbins = int(request.get_json()["nbins"]) or DEFAULT_NBINS
	alphabet = request.get_json()["alphabet"] or DEFAULT_ALPHABET
	threshold = float(request.get_json()["threshold"]) or 0.1
	sax = pysax.SAXModel(stride = stride, nbins = nbins, alphabet=alphabet)
	found = sax.search_pattern(s.y, target_start, target_end, threshold)
	print found
	return json.dumps(list({"start": i[0].start, "stop": i[0].stop} for i in found))

# @app.route("/rules")

if __name__ == '__main__':
	# app.run(debug = True, port = 5001)
	app.run(debug = True, port = 5004)