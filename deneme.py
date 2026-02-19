import requests
from bs4 import BeautifulSoup
import pandas as pd # Veriyi tablo yapmak için

url = "https://www.scrapethissite.com/pages/simple/"
print(f"{url} adresinden veriler çekiliyor...")

try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ülke isimlerini ve başkentlerini çekelim
    ulke_listesi = []
    ulkeler = soup.find_all('div', class_='col-md-4 country')

    for ulke in ulkeler:
        isim = ulke.find('h3', class_='country-name').text.strip()
        baskent = ulke.find('span', class_='country-capital').text.strip()
        ulke_listesi.append({'Ülke': isim, 'Başkent': baskent})

    # Veriyi bir tabloya (DataFrame) dönüştür
    df = pd.DataFrame(ulke_listesi)

    # CSV olarak kaydet
    df.to_csv('ulkeler.csv', index=False, encoding='utf-8')
    print("\nBaşarılı! 'ulkeler.csv' dosyası oluşturuldu.")

except Exception as e:
    print(f"Hata: {e}")
