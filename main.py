import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import nettoyage
from owlready2 import *


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# get_ipython().run_line_magic('matplotlib', 'inline')
import tensorflow as tf
import cufflinks as cf

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
from sklearn.feature_extraction.text import CountVectorizer
import io
import time
from io import StringIO
import re
from nltk.corpus import stopwords
from PIL import *
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from ipywidgets import FileUpload
from IPython.display import display
import nltk
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import yake

UPLOAD_FOLDER = 'C:\\dataset'


app = Flask(__name__)




CORS(app)
# app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/multiple-files-upload', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def upload_file():

  # if 'files[]' not in request.files:
  if 'file' not in request.files:
    resp = jsonify({'message': 'No file part in the request'})
    resp.status_code = 400
    return resp
  # files = request.files.getlist('files[]')
  files = request.files.getlist('file')
  errors = {}
  success = False
  for file in files:
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      success = True
    else:
      errors[file.filename] = 'File type is not allowed'

  if success and errors:
    for file in files:
      nettoyage.function1(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      nettoyage.function2()
      nettoyage.function3()
      errors['message'] = 'Nettoyage effectué avec succès'
      resp = jsonify(errors)
      resp.status_code = 500
      return resp
  if success:
    for file in files:
      nettoyage.function1(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      nettoyage.function2()
      nettoyage.function3()
      resp = jsonify({'message': 'Nettoyage effectué avec succès'})
      resp.status_code = 201
      return resp
  else:
    resp = jsonify(errors)
    resp.status_code = 500
    return resp


if __name__ == "__main__":
  app.run()
