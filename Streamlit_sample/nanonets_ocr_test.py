# import requests, os, json
  
# url = "https://app.nanonets.com/api/v2/OCR/Model/"
# # api_key = os.environ.get('NANONETS_API_KEY')
# api_key = '72decf1a-3823-11ef-8e55-b6da12066c86'

# ##
# payload = "{\"categories\" : [\"number_plate\"], \"model_type\": \"ocr\"}"
# headers = {'Content-Type': "application/pdf",}

# response = requests.request("POST", url, headers=headers, auth=requests.auth.HTTPBasicAuth(api_key, ''), data=payload)
# model_id = json.loads(response.text)["model_id"]

# print("NEXT RUN: export NANONETS_MODEL_ID=" + model_id)
# print("THEN RUN: python ./code/upload-training.py")

import requests
import pandas as pd
import base64
import json
import bb_to_csv as bb_to_csv

url = "https://app.nanonets.com/api/v2/OCR/FullText"

def get_ocr_df(file, filename = 'CBP_Manual_1948_part1-pages.pdf'):
  print("file = ", filename)
  payload={}
  # files=[('file',('FILE_NAME',open(filename,'rb'),'application/pdf'))]
  headers = {}

  inputpdf = file
  files=[('file',('FILE_NAME',inputpdf,'application/pdf'))]
  response = requests.request("POST", url, headers=headers, data=payload, files=files, auth=requests.auth.HTTPBasicAuth('72decf1a-3823-11ef-8e55-b6da12066c86', ''))

  # Convert the JSON string to a Python dictionary
  response_dict = json.loads(response.text)

  print(response_dict)

  # print(response_dict)

  # print('-----------------------')

  # print(response.text)

  # with open('nanoresponse.json', 'w') as json_file:
  #     json.dump(response_dict, json_file, indent=4)
  ocr_df = bb_to_csv.convert_json_to_df(response_dict)

  print(ocr_df.head())

  return ocr_df

# get_ocr_df()
