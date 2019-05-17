import requests

temperature = 38 
humidity = 40

API = "PVCA3FPHOCRUUJ10" #API Key Here

data = {
    'api_key':API,
    'field1': ,  #需要輸入想傳送上平台的變數名字
    "field2":
} 

res = requests.post("https://api.thingspeak.com/update.json",data=data)
