import requests

url = "http://127.0.0.1:5000/upload"

payload={}
files=[
  ('files[]',('1.jpg',open(r'D:\OCR Project\Data\1.jpg','rb'),'image/jpeg'),
  ('2.jpg',open(r'D:\OCR Project\Data\1.jpg','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
x = response.json
print(response.text)