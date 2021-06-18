import os
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

import nettoyage

import cufflinks as cf

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

UPLOAD_FOLDER = 'C:\dataset'
output_file = 'C:\dataset\output4.csv'
ontoo = 'ontoo'

app = Flask(__name__)

CORS(app)
# hello.secret_key = "secret key"
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
      nettoyage.create_dataframe(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      nettoyage.clean()
      nettoyage.extraction()
      #csv2owl.write_ttl(ontoo)

      #csv2rdf.csv2rdf()
      errors['message'] = 'Extraction effectué avec succès'
      resp = jsonify(errors)
      resp.status_code = 500
      return resp
  if success:
    for file in files:
      nettoyage.create_dataframe(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      nettoyage.clean()
      nettoyage.extraction()
      #csv2rdf.csv2rdf()
      #csv2owl.write_ttl(ontoo)

      resp = jsonify({'message': 'Extraction effectué avec succès'})
      resp.status_code = 201
      return resp
  else:
    resp = jsonify(errors)
    resp.status_code = 500
    return resp

  # onto_path.append("C:\dataset\PersoDiagMedi.owl")
  # onto = get_ontology("C:\dataset\PersoDiagMedi.owl")
  # onto.load()


if __name__ == "__main__":
  app.run()

