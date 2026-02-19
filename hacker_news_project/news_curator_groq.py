import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from groq import Groq
import time

# 1. Groq Kurulumu (Güvenli Yöntem)
# API anahtarını doğrudan koda yazmıyoruz, sistem değişkeninden çekiyoruz.
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def haberleri_topla():
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Haberler {url} adresinden çekiliyor...")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haber_listesi = []
    haberler = soup.find_all('tr', class_='athing')
    
    for haber in haberler:
        id_ = haber.get('id')
        baslik_tag = haber.find('span', class_='titleline').find('a')
        baslik = baslik_tag.text
        link = baslik_tag.get('href')
        
        haber_listesi.append({
            'ID': id_,
            'Başlık': baslik,
            'Link': link
        })
    return haber_listesi

def groq_analiz_et(baslik):
    prompt = f"""
    Analyze this tech headline: "{baslik}"
    Provide the result in Turkish with these fields:
    - Kategori (AI, Software, Hardware, Security)
    - Teknik Derinlik (1-10)
    - Kısa Özet (Tek cümle)
    """
    try:
        # Llama 3 8b modeli hem çok hızlı hem de ücretsiz kota için çok cömerttir
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Hata: {e}"

if __name__ == "__main__":
    ham_veriler = haberleri_topla()
    zengin_liste = []
    
    print(f"\nGroq ile {len(ham_veriler)} haber analiz ediliyor. Gözlerini kırpma, çok hızlı olacak!")
    
    for haber in ham_veriler[:20]: # İlk 20 haber için test yapalım
        analiz_sonucu = groq_analiz_et(haber['Başlık'])
        haber['Analiz'] = analiz_sonucu
        zengin_liste.append(haber)
        print(f"Bitti: {haber['Başlık'][:40]}...")
        # Groq çok hızlıdır ama saniyede 1-2 saniye beklemek her zaman iyidir
        time.sleep(1)

    # Veriyi Kaydet
    df = pd.DataFrame(zengin_liste)
    df.to_csv('hacker_news_groq_enriched.csv', index=False)
    
    print("\n--- İŞLEM TAMAM ---")
    print("Sonuçlar 'hacker_news_groq_enriched.csv' dosyasına kaydedildi.")
