import os
import hashlib
from tqdm import tqdm  # İlerleme çubuğu için tqdm kütüphanesi

def hash_file(file_path):
    """Dosyanın hash'ini hesapla."""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except Exception as e:
        print(f"Hata oluştu: {file_path} - {str(e)}")
    return hasher.hexdigest()

def find_and_delete_copies(target_path, search_dir):
    """Verilen dosyanın hash'ine göre aynı dosyaları bulur ve siler."""
    if not os.path.exists(target_path):
        print(f"Hedef dosya bulunamadı: {target_path}")
        return

    # Hedef dosyanın hash'ini hesapla
    target_hash = hash_file(target_path)

    # Tüm dosyaları tarar ve aynı hash'e sahip olanları bulur
    total_files = sum([len(files) for r, d, files in os.walk(search_dir)])  # Toplam dosya sayısını al
    with tqdm(total=total_files, desc="Taranıyor", unit="file") as pbar:
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Sembolik bağlantıları ve özel dosyaları es geç
                    if os.path.islink(file_path) or not os.path.isfile(file_path):
                        continue

                    if file_path != target_path:  # Hedef dosyayı tekrar silmemek için
                        if hash_file(file_path) == target_hash:
                            print(f"Siliniyor: {file_path}")
                            os.remove(file_path)
                except (OSError, IOError) as e:
                    print(f"Hata oluştu: {file_path} - {str(e)}")

                pbar.update(1)  # İlerleme çubuğunu güncelle

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Belirtilen dosyanın diğer kopyalarını sil.")
    parser.add_argument("target", help="Hedef dosyanın yolu")
    parser.add_argument("directory", help="Arama yapılacak dizin")
    args = parser.parse_args()

    find_and_delete_copies(args.target, args.directory)

if __name__ == "__main__":
    main()
