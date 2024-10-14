import requests
import datetime
import logging
import json
import os
import sys

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s', encoding='utf-8')
sys.tracebacklimit = 0 

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0","Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Cache-Control": "no-cache"}
cookies = {'cookie_name': 'cookie_value',}


teslimatNumarasi = int(input("Teslimat No: "))
takipNumarasiResponse = requests.get(f"https://texpublic-mars.trendyol.com/delivery-lastmileplanning-cargo-tracking-service/api/tracks?trackingNumber={teslimatNumarasi}", headers=headers, cookies=cookies)
if takipNumarasiResponse.status_code != 200: 
      os.system("cls")  
      print(f"Hatali Takip Numarasi.\nStatus Code: {takipNumarasiResponse.status_code}")
else:      
      takipNumarasi = json.loads(takipNumarasiResponse.content.decode('utf-8'))[0]
      teslimatResponse = requests.get(f"https://texpublic-mars.trendyol.com/delivery-lastmileplanning-communication-service/api/chatbot/rule-result?deliveryNumber={takipNumarasi}&categoryId=chatbot.findDeliveryLocation")
      if teslimatResponse.status_code !=200:
            os.system("cls")
            print(f"Hata.\nStatus Code: {teslimatResponse.status_code}")
      else:
            veri = teslimatResponse.json()


message = veri['message']
desc = veri['progress']['desc']

os.system("cls")
print(
      f"Takip Numarası: {takipNumarasi}\n"
      f"Teslimat Numarası: {teslimatNumarasi}\n"
      f"Gönderi Bilgi: {message}\n"
      f"Gönderi Durumu: {desc}")

logging.info(f"[{datetime.datetime(2020, 5, 17)}]Teslimat No: {teslimatNumarasi}, Takip No: {takipNumarasi}, Message: {message}, Status: {desc}")






