from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

base_url = "https://www.euroleaguebasketball.net/tr/euroleague/teams/fenerbahce-beko-istanbul/games/ulk/?season="

# Sadece 2024-25 sezonu için link oluştur
season = "2024-25"
link = base_url + season
print(f"İşlenecek link: {link}")

# Chrome ayarlarını yapılandır
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Tarayıcıyı görünmez modda çalıştırmak için bu satırı açabilirsiniz

# WebDriver'ı, webdriver-manager kullanarak başlat
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

try:
    # Sayfaya git
    driver.get(link)
    time.sleep(3)  # Sayfanın yüklenmesi için bekle

    # Maç linklerini bul
    articles = driver.find_elements(By.CSS_SELECTOR, 'article.relative.text-base.text-primary.font-normal.border.overflow-hidden.border-gray.rounded-lg.shadow-regular')

    print(f"Toplam {len(articles)} maç bulundu.")

    # Her maç için bilgileri topla
    for i, article in enumerate(articles, 1):
        try:
            # Maç linkini al
            a_tag = article.find_element(By.CSS_SELECTOR, 'a.absolute.w-full.h-full.top-0.left-0.z-\\[1\\]')
            match_link = a_tag.get_attribute('href')

            # Maç başlığını al
            span_tag = article.find_element(By.CSS_SELECTOR, 'span.visually-hidden_wrap__Ob8t3')
            match_title = span_tag.text.strip()

            print(f"Link: {match_link}")

            # Her maç sayfasına git
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(match_link)

            # Burada maç detaylarını işleyebilirsiniz
            print(f"{driver.title}")
            time.sleep(2)  # Sayfanın yüklenmesini bekle
            print("-" * 50)

            # Ana pencereye geri dön ve yeni pencereyi kapat
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Hata oluştu: {e}")

except Exception as e:
    print(f"Ana hata: {e}")

finally:
    # Tarayıcıyı kapat
    print("İşlem tamamlandı, tarayıcı kapatılıyor...")
    driver.quit()
