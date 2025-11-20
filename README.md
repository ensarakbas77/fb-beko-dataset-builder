# Fenerbahçe Beko Dataset Builder

## Proje Hakkında
Fenerbahçe Beko basketbol takımıyla ilgili haber ve istatistik verilerini toplamak için geliştirilmiş bir projedir. Veriler, **EuroLeague** ve **Eurohoops** web sitelerinden otomatik olarak çekilmektedir. Bu proje, veri analizi, görselleştirme ve makine öğrenimi gibi çeşitli uygulamalar için zengin bir veri seti sunar.

## Özellikler
- **Haber Verileri**: Fenerbahçe Beko ile ilgili haberler JSON ve CSV formatlarında kaydedilir.
- **İstatistik Verileri**: Takımın sezonluk performans istatistikleri CSV formatında saklanır.
- **Kolay Kullanım**: Veri çekme işlemleri otomatikleştirilmiştir ve kolayca çalıştırılabilir.

## Kurulum
Projeyi yerel makinenize kurmak için şu adımları izleyin:

1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/ensarakbas77/fb-beko-dataset-builder.git
   ```

2. Proje dizinine gidin:
   ```bash
   cd fb-beko-dataset-builder
   ```

3. Bir sanal ortam (.venv) oluşturun:
   ```bash
   python -m venv .venv
   ```

4. Sanal ortamı aktif hale getirin:
     ```bash
     .venv\Scripts\activate
     ```
5. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım
Veri çekme işlemlerini başlatmak için aşağıdaki adımları takip edin:

### Haber Verilerini Çekme
Fenerbahçe Beko ile ilgili haberleri çekmek için şu komutu çalıştırın:
```bash
python ScrapingText.py
```
Bu işlem, haberleri JSON ve CSV formatlarında kaydedecektir.

### İstatistik Verilerini Çekme
Takımın sezonluk istatistiklerini çekmek için şu komutu çalıştırın:
```bash
python ScrapingStatistics.py
```
Bu işlem, istatistikleri CSV formatında kaydedecektir.

## Dosya Açıklamaları
- **ScrapingText.py**: Fenerbahçe Beko ile ilgili haberleri web sitelerinden çekmek için kullanılan Python betiği.
- **ScrapingStatistics.py**: Takımın sezonluk istatistiklerini çekmek için kullanılan Python betiği.
- **DataVisualization.ipynb**: Verilerin görselleştirilmesi için kullanılan Jupyter Notebook dosyası. Grafikler ve analizler içerir.
- **TextVisualization.ipynb**: Metin verilerinin görselleştirilmesi ve analiz edilmesi için kullanılan Jupyter Notebook dosyası.
- **DataPreprocessing.ipynb**: Veri temizleme ve ön işleme adımlarını içeren Jupyter Notebook dosyası.
- **TextPreprocessing.ipynb**: Metin verilerinin temizlenmesi ve ön işlenmesi için kullanılan Jupyter Notebook dosyası.

## Veri Seti
Toplanan veriler aşağıdaki dizinlerde saklanır:
- **Haber Verileri**: `Texts-JSON/` ve `Texts-CSV/` dizinlerinde.
- **İstatistik Verileri**: `Dataset/` dizininde.
