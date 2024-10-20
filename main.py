import requests
import datetime
import logging
import time
import json
import os
import sys

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s', encoding='utf-8')
sys.tracebacklimit = 0 

def trendyol_express():
      teslimatNumarasi = int(input("Teslimat No: "))

      headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0","Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Cache-Control": "no-cache"}
      cookies = {'cookie_name': 'cookie_value',}

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
      ordernumber = veri['orderNumber']

      os.system("cls")
      print(
            f"Takip Numarası: {takipNumarasi}\n"
            f"Teslimat Numarası: {ordernumber}\n"
            f"Gönderi Bilgi: {message}\n"
            f"Gönderi Durumu: {desc}\n")

      logging.info(f"[{datetime.datetime.now():%Y, %m, %d %H:%M}] Teslimat No: {teslimatNumarasi}, Takip No: {takipNumarasi}, Message: {message}, Status: {desc}")

def aras_kargo(): 
      os.system("cls")
      takipNo = int(input("Teslimat No: "))

      BaseUrl = "https://kurumsalwebservice.araskargo.com.tr/api"
      ShipmentInfoURL = f"{BaseUrl}/getShipmentByTrackingNumber"
      ShipmentNotDeliveredURL = f"{BaseUrl}/getShipmentNotDeliveredByTrackingNumberWeb"
      CargoTransactionURL = f"{BaseUrl}/getCargoTransactionByTrackingNumber"

      headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
         "Accept": "application/json, text/plain, */*",
         "Content-Type": "application/json; charset=utf-8"
         }

      ShipmentInfoData = {
         "TrackingNumber": f"{takipNo}",
         "IsWeb": True,
         "UniqueCode": "29786c54-3a38-4ddf-8c08-46eb2b1489f2",
         "SecretKey": "8at5zc", #Geçerlilik Süresi 1 Gün, 1 kere sitedeki captchayı çözüp body kısmını buraya atmalısınız.
         "LanguageCode": "tr"
         }
      TrackingInfoData = {
         "TrackingNumber":f"{takipNo}",
         "LanguageCode":"tr"
         }
      os.system("cls")
      
      print("[1] Gönderi Bilgileri")
      print("[2] Kargo Hareketleri")
      print("[3] Kargo Durum Bilgisi (Teslim Edildiyse/Teslim Edilmediyse)")
      secim = int(input("\nSeçiminiz: ")) 
      if secim == 1:
           ShipmentInfoResponse = requests.post(ShipmentInfoURL, headers=headers, json=ShipmentInfoData)
           if ShipmentInfoResponse.status_code != 200: {print(f"Hata. {ShipmentInfoResponse}")}
           else:
            veri = ShipmentInfoResponse.json()['Responses'][0]
            os.system("cls")
            baslik = {
                    "Gönderi Tarihi": veri['WaybillDate'],
                    "Alıcı Adı Soyadı: ": veri['ReceiverAccountAddressName'],
                    "Gönderici Adı Soyadı: ": veri['SenderAccountAddressName'],
                    "Tahmini Teslim Tarihi": veri['PlannedDeliveryDate'],
                    "Takip Numarası": veri['TrackingNumber'],
                    "Sipariş Durumu": veri['LovShipmentStatusName'],
                    "Teslimat İl": veri['DeliveryCity'],
                    "Teslimat İlçe": veri['DeliveryTown'],
                    "Siparişin Geldiği İl": veri['SourceCity'],
                    "Siparişin Geldiği İlçe": veri['SourceTown'],
                    "Teslim Şubesi: ": veri['DeliveryUnitName'],
                    "Çıkış Şubesi: ": veri['SourceUnitName'],
                    "Kargo Tipi: ": veri['LovPackTypeName'],
                    "Kargo Desisi: ": veri['TotalVolume'],
                    "Kargo Adeti: ": veri['PieceCount'],
                    "Ödeme Tipi: ": veri['LovPayorTypeName'],
                    }   
            
            for key, value in baslik.items():
                print(f"{key}: {value}")
            time.sleep(10)

      elif secim == 2:
           CargoTransactionResponse = requests.post(CargoTransactionURL, headers = headers, json = TrackingInfoData)
           #ekleme yapilacak
      elif secim == 3:
           ShipmentNotDeliveredResponse = requests.post(ShipmentNotDeliveredURL, headers = headers, json = TrackingInfoData)
           #ekleme yapilacak
      else:
           print("Hatali girdi.")     

def secenekler():
      print("[1] Trendyol Express")
      print("[2] Aras Kargo")


if __name__ == "__main__":
    while True:  
        secenekler()
        try:
            secim = int(input("\nSeçiminiz: "))

            if secim < 1 or secim > 3:  
                print("Seçiminiz 1-3 Arası Olmalıdır.")
            else:
                if secim == 1:
                    os.system("cls") 
                    trendyol_express()
                    time.sleep(15)
                    os.system('cls')  
                elif secim == 2:
                    aras_kargo()
                    time.sleep(15)
                    os.system('cls') 
                elif secim == 3:
                    sys.exit(0)
        except Exception as e:
            os.system("cls") 
            print(e)





