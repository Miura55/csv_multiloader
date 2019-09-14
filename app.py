# coding: utf-8

from flask import Flask, request, make_response, jsonify, render_template
from pathlib import PurePath
import os
import sys
import csv
import chardet
import werkzeug
from datetime import datetime

# flask
app = Flask(__name__)

# limit upload file size : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = PurePath("./files")

def get_enc(file):
    with open(file, "rb") as f:
        res = chardet.detect(f.read())
        enc = res["encoding"]
    return enc

# ------------------------------------------------------------------
@app.route('/')
def main_page():
  return render_template("index.html")

@app.route('/data/upload', methods=['POST'])
def upload_multipart():
  sys.stderr.write("*** upload_multipart *** start ***\n")
  if 'uploadFile' not in request.files:
    make_response(jsonify({'result':'uploadFile is required.'}))

  upload_files = request.files.getlist('uploadFile_aa')
  sys.stderr.write("len(upload_files) = %d\n" % len(upload_files))
  for file in upload_files:
    fileName = file.filename
    sys.stderr.write("fileName = " + fileName + "\n")
    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
        + werkzeug.utils.secure_filename(fileName)

    # サーバ上にCSVを保存
    file_path = os.path.join(UPLOAD_DIR / saveFileName)
    file.save(file_path)
    enc_code = get_enc(file_path)
    with open(file_path, encoding=enc_code) as f:
      reader = csv.reader(f)
      for row in reader:
        print(row)

  sys.stderr.write("*** upload_multipart *** end ***\n")
  return make_response(jsonify({'result':'upload OK.'}))

# ------------------------------------------------------------------
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
  print("werkzeug.exceptions.RequestEntityTooLarge")
  return 'result : file size is overed.'

# ------------------------------------------------------------------
# main
if __name__ == "__main__":
  print(app.url_map)
  app.run(host='localhost', port=3000)
