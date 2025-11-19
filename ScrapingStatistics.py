from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

base_url = "https://www.euroleaguebasketball.net/tr/euroleague/teams/fenerbahce-beko-istanbul/games/ulk/?season="

# sezonu için link oluştur
season = "2024-25"
team_name = "Fenerbahce Beko Istanbul"
link = base_url + season
print(f"İşlenecek link: {link}")

chrome_options = Options()

# webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

csv_filename = f"deneme_{season}.csv"
csv_headers = ["Date", "Opposing Team", "IsHome", "Points", "Performance Index Rating", "Two-point %", "Three-point %", "Free-throw %", "Offensive rebounds", "Defensive rebounds", "Total rebounds", "Assists", "Steals", "Blocks", "Turnovers"]

# CSV dosyasını oluştur
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_headers)

# İstatistikler
statistics_names = [
    "Points",
    "Performance Index Rating",
    "Two-point %",
    "Three-point %",
    "Free-throw %",
    "Offensive rebounds",
    "Defensive rebounds",
    "Total rebounds",
    "Assists",
    "Steals",
    "Blocks",
    "Turnovers"
]

def get_statistics_simple(driver, wait_obj, is_home):
    statistics = {}

    try:
        print(f"İstatistik çekiliyor... (IsHome: {is_home})")

        all_values = driver.find_elements(By.CSS_SELECTOR, 'div.font-bold.lg\\:text-base')

        if is_home == 1:
            target_indices = list(range(0, len(all_values), 2))
        else:
            target_indices = list(range(1, len(all_values), 2))

        # İstatistikleri çek
        for i, stat_name in enumerate(statistics_names):
            if i < len(target_indices):
                try:
                    idx = target_indices[i]
                    if idx < len(all_values):
                        stat_value = all_values[idx].text.strip()
                        if stat_value:
                            statistics[stat_name] = stat_value
                            print(f"  ✓ {stat_name}: {stat_value}")
                        else:
                            statistics[stat_name] = "N/A"
                    else:
                        statistics[stat_name] = "N/A"
                except Exception as e:
                    statistics[stat_name] = "N/A"
                    print(f"  ✗ {stat_name}: Hata")
            else:
                statistics[stat_name] = "N/A"

        success_count = len([v for v in statistics.values() if v != 'N/A'])
        print(f"Sonuç: {success_count}/{len(statistics_names)} başarılı")

    except Exception as e:
        print(f"İstatistik çekme hatası: {str(e)[:50]}")
        for stat_name in statistics_names:
            statistics[stat_name] = "N/A"

    return statistics

try:
    driver.get(link)
    time.sleep(15)

    # Maç linklerini bul
    articles = driver.find_elements(By.CSS_SELECTOR, 'article.relative.text-base.text-primary.font-normal.border.overflow-hidden.border-gray.rounded-lg.shadow-regular')

    print(f"Toplam {len(articles)} maç bulundu.")

    for i, article in enumerate(articles, 1):
        try:
            a_tag = article.find_element(By.CSS_SELECTOR, 'a.absolute.w-full.h-full.top-0.left-0.z-\\[1\\]')
            match_link = a_tag.get_attribute('href')

            span_tag = article.find_element(By.CSS_SELECTOR, 'span.visually-hidden_wrap__Ob8t3')
            match_title = span_tag.text.strip()

            print(f"Maç {i}: {match_title}")
            print(f"Link: {match_link}")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(match_link)

            time.sleep(3)

            try:
                date_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[1]/div[1]/div/p')
                date = date_element.text.strip()
            except Exception as e:
                print(f"Tarih bulunamadı: {e}")
                date = "N/A"

            try:
                team1_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[1]/div[1]/a[1]/div/p[1]')
                team1 = team1_element.text.strip()

                team2_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[1]/div[1]/a[2]/div/p[1]')
                team2 = team2_element.text.strip()

                if team_name in team1 or "FENERBAHCE" in team1.upper():
                    is_home = 1
                    opposing_team = team2
                elif team_name in team2 or "FENERBAHCE" in team2.upper():
                    is_home = 0
                    opposing_team = team1
                else:
                    print(f"Uyarı: Fenerbahçe takımı tespit edilemedi. Takımlar: {team1} vs {team2}")
                    is_home = 1
                    opposing_team = team2

            except Exception as e:
                print(f"Takım bilgileri alınamadı: {e}")
                opposing_team = "N/A"
                is_home = "N/A"

            print(f"Tarih: {date}")
            print(f"Rakip Takım: {opposing_team}")
            print(f"Ev Sahibi mi (1=Evet, 0=Hayır): {is_home}")

            try:
                team_stats_button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[2]/div[1]/div/div/span[4]/a')
                team_stats_button.click()
                time.sleep(5)
                print("Team Stats sayfasına geçildi")
            except Exception as e:
                print(f"Team Stats sayfasına geçilemedi: {e}")

            if is_home != "N/A":
                stats = get_statistics_simple(driver, wait, is_home)
            else:
                stats = {}
                for stat_name in statistics_names:
                    stats[stat_name] = "N/A"

            # CSV dosyasına veriyi ekle
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    date,
                    opposing_team,
                    is_home,
                    stats["Points"],
                    stats["Performance Index Rating"],
                    stats["Two-point %"],
                    stats["Three-point %"],
                    stats["Free-throw %"],
                    stats["Offensive rebounds"],
                    stats["Defensive rebounds"],
                    stats["Total rebounds"],
                    stats["Assists"],
                    stats["Steals"],
                    stats["Blocks"],
                    stats["Turnovers"]
                ])

            print("-" * 50)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Maç {i} için hata oluştu: {e}")
            try:
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            except:
                pass

except Exception as e:
    print(f"Ana hata: {e}")

finally:
    print("İşlem tamamlandı, tarayıcı kapatılıyor...")
    driver.quit()

    if os.path.exists(csv_filename):
        print(f"CSV dosyası başarıyla oluşturuldu: {csv_filename}")
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            row_count = sum(1 for row in reader)
            print(f"Toplam {row_count - 1} maç verisi kaydedildi (başlık hariç)")
    else:
        print("CSV dosyası oluşturulamadı!")
