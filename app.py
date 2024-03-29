# coding: utf-8

from flask import Flask, request, make_response, jsonify, render_template, render_template_string
import pandas as pd
from pathlib import PurePath
from datetime import datetime
import os, sys
import csv, json
import chardet
import werkzeug
import requests
try:
  import MecabSimilar
except:
  from CosineSimilarity import CosineSimilarity


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

def req_pair(key, text):
  try:
    result = MecabSimilar.sentence_similarity(key, text)
  except:
    cos = CosineSimilarity()
    result = cos(key, text)
  return result

# ------------------------------------------------------------------
@app.route('/')
def main_page():
  return render_template("index.html")

@app.route('/data/upload', methods=['POST'])
def upload_multipart():
  sys.stderr.write("*** upload_multipart *** start ***\n")
  _keyword = request.form["keyword"]
  sys.stderr.write("Got Keyword : {} \n".format(_keyword))
  if 'uploadFile' not in request.files:
    make_response(jsonify({'result':'uploadFile is required.'}))

  upload_files = request.files.getlist('uploadFile_aa')
  sys.stderr.write("len(upload_files) = %d\n" % len(upload_files))

  result = pd.DataFrame(index=[], columns=["Keyword", "Volume", "Position History"])

  # 読み込んだCSVを処理
  for file in upload_files:
    fileName = file.filename
    sys.stderr.write("fileName = " + fileName + "\n")
    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
        + werkzeug.utils.secure_filename(fileName)

    # サーバ上にCSVを保存
    file_path = os.path.join(UPLOAD_DIR / saveFileName)
    file.save(file_path)
    enc_code = get_enc(file_path)

    # CSVを読み込む
    df = pd.read_csv(file_path, sep='\t', encoding=enc_code)
    df = df[df["Keyword"].isnull() == False].sort_values("Position History Date")
    df = df.drop_duplicates(subset='Keyword').reset_index(drop=True)
    result = result.append(df[["Keyword", "Volume", "Position History", "Traffic (desc)", "CPC", "SERP Features"]]).reset_index(drop=True)

  unique_lis = result["Keyword"].value_counts()
  print(unique_lis)
  result["順位取得率（％）"] = [int(unique_lis[word] / len(upload_files) * 100) for word in result["Keyword"]]
  sys.stderr.write("*** upload_multipart *** end ***\n")

  # 重複したもののうち、Traffic (desc)の高いものを取り出す
  result = result.sort_values("Traffic (desc)", ascending=False)
  is_complete_duplicate_keep_first = result.duplicated(keep='first')
  result = result[~is_complete_duplicate_keep_first]

  result = result.sort_values("Position History")[result['Position History'] < 11]
  result["Score"] = [req_pair(_keyword, text) for text in result["Keyword"]]

  return render_template("result_pandas.html", table=result[result["Score"] > 0.59].to_html(index=False))

# ------------------------------------------------------------------
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
  print("werkzeug.exceptions.RequestEntityTooLarge")
  return 'result : file size is overed.'

# ------------------------------------------------------------------
if __name__ == "__main__":
  app.debug = True
  app.run(host='localhost', port=3000)
