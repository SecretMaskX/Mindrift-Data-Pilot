import requests
from bs4 import BeautifulSoup
import pandas as pd
from google import genai 

def haberleri_topla():
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'} # Bot engeline takılmamak için
    
    print(f"Haberler {url} adresinden çekiliyor...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haber_listesi = []
    
    # Hacker News yapısı: 'athing' class'lı her <tr> bir haberdir
    haberler = soup.find_all('tr', class_='athing')
    
    for haber in haberler:
        id_ = haber.get('id')
        baslik_tag = haber.find('span', class_='titleline').find('a')
        baslik = baslik_tag.text
        link = baslik_tag.get('href')
        
        # Puan bilgisini bir alt satırdan çekelim
        alt_bilgi = soup.find('td', id=f'score_{id_}')
        puan = alt_bilgi.text if alt_bilgi else "0 points"
        
        haber_listesi.append({
            'ID': id_,
            'Başlık': baslik,
            'Link': link,
            'Puan': puan
        })
    
    return haber_listesi

# Test çalışması
if __name__ == "__main__":
    veriler = haberleri_topla()
    df = pd.DataFrame(veriler)
    print(df.head()) # İlk 5 haberi terminalde göster
    df.to_csv('hacker_news_raw.csv', index=False)
    print("\nHam veriler 'hacker_news_raw.csv' olarak kaydedildi.")
def haberleri_zenginlestir(haberler):
    client = genai.Client(api_key="AIzaSyAN33SBeVStj6efnidij5U2texrSAmol9A")
    zengin_liste = []
    
    print("\nYapay zeka haberleri analiz ediyor (Kota dostu mod)...")
    
    # İlk 10 haberi analiz edelim (hem RAM hem kota için güvenli)
    for haber in haberler[:10]:
        prompt = f"""
        Bu teknoloji haberi başlığını analiz et: "{haber['Başlık']}"
        Şu bilgileri JSON formatında ver:
        - Kategori: (AI, Software, Hardware, Security)
        - Önem: (1-10 arası)
        - Özet: (Tek cümlelik profesyonel özet)
        """
        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            analiz = response.text
            haber.update({'Analiz': analiz})
            zengin_liste.append(haber)
            print(f"Analiz tamamlandı: {haber['Başlık'][:30]}...")
            time.sleep(10) # 429 hatası almamak için 10 saniye bekleme
        except Exception as e:
            print(f"Hata: {e}")
            
    return zengin_liste

# Ana çalıştırma kısmını güncelle
if __name__ == "__main__":
    ham_veriler = haberleri_topla()
    zengin_veriler = haberleri_zenginlestir(ham_veriler)
    
    df = pd.DataFrame(zengin_veriler)
    df.to_csv('hacker_news_enriched.csv', index=False)
    print("\nEfsane! 'hacker_news_enriched.csv' hazır. Artık gerçek bir veri küratörüsün.")

import time
from google.genai import errors

def analiz_yap_ve_bekle(client, prompt, retry_count=0):
    try:
        # Gemini 2.0 Flash daha hızlı ve ücretsiz kotaya daha uygun
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except errors.ClientError as e:
        if "429" in str(e):
            # Kota dolduğunda bekleme süresini her seferinde artır (1dk, 2dk...)
            wait_time = (2 ** retry_count) * 60 
            print(f"Kota doldu! {wait_time} saniye dinleniyoruz (Deneme: {retry_count + 1})...")
            time.sleep(wait_time)
            return analiz_yap_ve_bekle(client, prompt, retry_count + 1)
        else:
            print(f"Başka bir hata oluştu: {e}")
            return "Hata"
