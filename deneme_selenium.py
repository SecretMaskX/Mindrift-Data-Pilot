from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time

chrome_options = Options()
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
    options=chrome_options
)

try:
    # Test için sonsuz kaydırma olan bir siteye gidelim
    driver.get("https://quotes.toscrape.com/scroll")
    print("Site açıldı, kaydırma başlıyor...")

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Sayfayı en aşağı kaydır
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Yeni verilerin yüklenmesi için bekle (AJAX yüklemesi)
        time.sleep(2)

        # Yeni sayfa yüksekliğini hesapla ve eskisiyle karşılaştır
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break # Artık yeni veri gelmiyorsa dur
        last_height = new_height
        print("Sayfa aşağı kaydırıldı, yeni veriler yükleniyor...")

    # Tüm veriler yüklendikten sonra sözleri çekelim
    sozler = driver.find_elements("class name", "quote")
    print(f"\nToplam {len(sozler)} adet söz bulundu!")
    
    for soz in sozler[:5]: # İlk 5 tanesini örnek olarak basalım
        print(f"-> {soz.text[:50]}...")

finally:
    driver.quit()

