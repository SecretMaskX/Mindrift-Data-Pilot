import time
from google import genai
from google.genai import errors

client = genai.Client(api_key="AIzaSyAN33SBeVStj6efnidij5U2texrSAmol9A")

# Örnek veriyi 10'arlı gruplara bölelim (kotayı yormamak için)
cekilen_sozler = [
    # Buraya Selenium'dan gelen 100 söz listesini koyduğunu varsayıyoruz
    "The world as we have created it is a process of our thinking.",
    "It is our choices, Harry, that show what we truly are.",
    # ... devamı
]

print("Yapay zeka verileri işlemeye başlıyor (Kota kontrolü ile)...")

def analiz_et(veri_parçası):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Bu sözleri kısaca temalarına ayır:\n{veri_parçası}"
        )
        print(response.text)
    except errors.ClientError as e:
        if "429" in str(e):
            print("Kota doldu, 60 saniye dinleniyoruz...")
            time.sleep(60) # Bir dakika bekle ve tekrar dene
            analiz_et(veri_parçası)

# Verileri küçük gruplar halinde gönder (Daha güvenli)
for i in range(0, len(cekilen_sozler), 25):
    grup = cekilen_sozler[i:i+10]
    analiz_et(grup)
    time.sleep(20) # Her grup arasında 5 saniye nefes payı
