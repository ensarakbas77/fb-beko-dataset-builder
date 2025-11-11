import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
import os

BASE_URL = "https://www.eurohoops.net/basket/fenerbahce/page/{}/?lang=tr"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/142.0.0.0 Safari/537.36"
}


def scrape_eurohoops_bs(start_page, end_page, delay=1.0):
    """
    Eurohoops Fenerbahçe haberlerini belirtilen sayfa aralığında çeker.
    start_page: başlanacak sayfa
    end_page: bitecek sayfa
    delay: istekler arası bekleme süresi (saniye)
    """
    all_articles = []

    for page in range(start_page, end_page + 1):
        url = BASE_URL.format(page)
        print(f"\n🔹 Sayfa {page} yükleniyor: {url}")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[⚠️ Sayfa yüklenemedi: {e}]")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.find_all("article")

        if not articles:
            print("⚠️ Bu sayfada hiç haber bulunamadı.")
            continue

        for idx, art in enumerate(articles, start=1 + (page - start_page) * 10):
            try:
                h2 = art.find("h2")
                a_tag = h2.find("a")
                title = a_tag.get_text(strip=True)
                link = a_tag["href"]

                # Haber sayfasını çek
                try:
                    news_resp = requests.get(link, headers=HEADERS, timeout=15)
                    news_resp.raise_for_status()
                except requests.RequestException as e:
                    print(f"[⚠️ Haber yüklenemedi: {title}] Hata: {e}")
                    continue

                news_soup = BeautifulSoup(news_resp.text, "html.parser")
                content_div = news_soup.find("div", class_="single__content")
                if not content_div:
                    print(f"[⚠️ Haber içeriği bulunamadı: {title}]")
                    continue

                # Metni temizle
                paragraphs = content_div.find_all(
                    ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"]
                )
                text = "\n".join(
                    [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                )

                print(f"{idx}. {title} (Haber uzunluğu: {len(text)} karakter)")

                all_articles.append({
                    "title": title,
                    "text": text,
                    "url": link
                })

                time.sleep(delay / 2)  # küçük gecikme (her haber arası)

            except Exception as e:
                print(f"[⚠️ Haber işlenemedi: {e}]")
                continue

        # sayfalar arası bekleme
        time.sleep(delay)

    # === JSON ve CSV olarak kaydet ===
    if all_articles:
        # Klasör yolları
        json_dir = "Texts-JSON"
        csv_dir = "Texts-CSV"

        # Klasörler yoksa otomatik oluştur
        os.makedirs(json_dir, exist_ok=True)
        os.makedirs(csv_dir, exist_ok=True)

        # Dosya isimleri
        json_name = os.path.join(json_dir, f"fenerbahce_news_{start_page}_{end_page}.json")
        csv_name = os.path.join(csv_dir, f"fenerbahce_news_{start_page}_{end_page}.csv")

        # JSON kaydet
        with open(json_name, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)
        print(f"\n✅ JSON dosyası kaydedildi: {json_name}")

        # CSV kaydet
        df = pd.DataFrame(all_articles)
        df.to_csv(csv_name, index=False, encoding="utf-8-sig")
        print(f"✅ CSV dosyası kaydedildi: {csv_name}")

    else:
        print("⚠️ Hiç haber metni kaydedilemedi.")


if __name__ == "__main__":
    # starg_page ve end_page arasındaki haberleri çek
    scrape_eurohoops_bs(start_page=1, end_page=10, delay=1.0)
