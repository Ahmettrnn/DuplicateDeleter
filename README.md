# Duplicate File Finder Tool

Bu araç, belirtilen dizinde dosya kopyalarını bulur ve kullanıcıdan onay alarak veya zorla bu kopyaları siler. Dosyalar, SHA-256 hash algoritması kullanılarak karşılaştırılır.

## Gereksinimler

Bu aracı çalıştırmak için aşağıdaki gereksinimlerin yüklü olması gerekmektedir:

- Python 3.x
- `tqdm` kütüphanesi

## Kurulum

1. Bu repo'yu klonlayın veya ZIP dosyası olarak indirin:
2. git clone https://github.com/Ahmettrnn/DuplicateDeleter.git
3. cd DuplicateDeleter
4. pip3 install -r requirements.txt

### Parametreler

- `<directory>`: Arama yapılacak dizin.
- `-ext`, `--extensions`: İzin verilen dosya uzantıları (örneğin: `.txt .jpg .iso`).
- `--all`: Tüm uzantıları tarar.
- `--force`: Tüm dosyaları sormadan siler.
- `--tenmb`: 10 MB ve üstü dosyaları tarar.
- `--fiftymb`: 50 MB ve üstü dosyaları tarar.
- `--hundredmb`: 100 MB ve üstü dosyaları tarar.
- `--twohundredmb`: 200 MB ve üstü dosyaları tarar.
- `--fivehundredmb`: 500 MB ve üstü dosyaları tarar.
- `--onegb`: 1 GB ve üstü dosyaları tarar.

### Örnek Kullanım

Home klasöründeki .txt uzantısına sahip ve 50 MB'tan büyük dosyaları taramak için:

python3 DuplicateDeleter.py  /home  -ext  .txt  --fiftymb


