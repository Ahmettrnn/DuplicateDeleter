import os
import hashlib
from tqdm import tqdm
def print_title():
    title = """
███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗   ██╗     
████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝     
██╔████╔██║███████║██║  ██║█████╗      ██████╔╝ ╚████╔╝      
██║╚██╔╝██║██╔══██║██║  ██║██╔══╝      ██╔══██╗  ╚██╔╝       
██║ ╚═╝ ██║██║  ██║██████╔╝███████╗    ██████╔╝   ██║        
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝    ╚═╝        
                                                             
████████╗ █████╗ ███╗   ███╗██╗      █████╗ ████████╗ █████╗ 
╚══██╔══╝██╔══██╗████╗ ████║██║     ██╔══██╗╚══██╔══╝██╔══██╗
   ██║   ███████║██╔████╔██║██║     ███████║   ██║   ███████║
   ██║   ██╔══██║██║╚██╔╝██║██║     ██╔══██║   ██║   ██╔══██║
   ██║   ██║  ██║██║ ╚═╝ ██║███████╗██║  ██║   ██║   ██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
"""
    print(title)

def hash_file(file_path):
    """Dosyanın hash'ini SHA-256 ile hesapla."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except Exception as e:
        print(f"Hata oluştu: {file_path} - {str(e)}")
    return hasher.hexdigest()

def find_and_delete_copies(search_dir, allowed_extensions=None, min_size=0, force=False):
    """Verilen dizinde belirli uzantılara ve boyutlara sahip dosyaları bulur ve hash'e göre aynı dosyaları siler."""
    
    scanned_files = []
    
    for root, dirs, files in tqdm(os.walk(search_dir), desc="Dizinler taranıyor"):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                # Dosya boyutunu kontrol et, belirtilen boyuttan küçük dosyaları atla
                if os.path.getsize(file_path) < min_size:
                    continue

                # Sadece belirli uzantıları kontrol et (allowed_extensions yoksa tüm uzantılar taranır)
                if allowed_extensions and not file.lower().endswith(tuple(allowed_extensions)):
                    continue

                # Sembolik bağlantıları es geç (silinmez)
                if os.path.islink(file_path) or not os.path.isfile(file_path):
                    continue
                
                file_hash = hash_file(file_path)

                # Daha önce taranmış dosyalarla karşılaştır
                for original_file, original_hash in scanned_files:
                    if original_hash == file_hash:  # Aynı hash'e sahipse, potansiyel kopya
                        print(f"\nKopya dosya bulundu: {file_path}")
                        print(f"Asıl dosya: {original_file}")

                        if force:
                            # --force seçeneğiyle sormadan sil
                            os.remove(file_path)
                            print(f"Sorulmadan silindi: {file_path}")
                        else:
                            # Kullanıcıya dosyayı silmek istiyor musunuz? diye sor
                            user_input = input(f"Bu dosyayı silmek istiyor musunuz? [Y/n]: {file_path} ").strip().lower()
                            if user_input in ['', 'y']:  # Enter ya da Y/Y'e basarsa sil
                                os.remove(file_path)
                                print(f"Silindi: {file_path}")
                            elif user_input == 'n':  # N'ye basarsa geç
                                print(f"Silinmedi: {file_path}")

                # Taranan dosyayı listeye ekle
                scanned_files.append((file_path, file_hash))

            except (OSError, IOError) as e:
                print(f"Hata oluştu: {file_path} - {str(e)}")

def main(): 
    print_title()  # Başlık fonksiyonunu çağır
    import argparse
    parser = argparse.ArgumentParser(description="Belirtilen dizinde dosya kopyalarını bul ve sil.")
    parser.add_argument("directory", help="Arama yapılacak dizin")
    parser.add_argument("-ext", "--extensions", nargs="*", help="İzin verilen dosya uzantıları (örnek: .txt .jpg)", default=None)
    parser.add_argument("--all", action="store_true", help="Tüm uzantıları tarar")
    parser.add_argument("--force", action="store_true", help="Tüm dosyaları sormadan siler")

    # Dosya boyutlarını MB ve GB cinsinden filtrelemek için seçenekler ekleyelim
    parser.add_argument("--tenmb", action="store_true", help="10 MB ve üstü dosyaları tarar")
    parser.add_argument("--fiftymb", action="store_true", help="50 MB ve üstü dosyaları tarar")
    parser.add_argument("--hundredmb", action="store_true", help="100 MB ve üstü dosyaları tarar")
    parser.add_argument("--twohundredmb", action="store_true", help="200 MB ve üstü dosyaları tarar")
    parser.add_argument("--fivehundredmb", action="store_true", help="500 MB ve üstü dosyaları tarar")
    parser.add_argument("--onegb", action="store_true", help="1 GB ve üstü dosyaları tarar")

    args = parser.parse_args()

    # Boyut filtresi için bayrakları kontrol et ve byte cinsine çevir
    min_size = 0
    if args.tenmb:
        min_size = 10 * 1024 * 1024  # 10 MB
    elif args.fiftymb:
        min_size = 50 * 1024 * 1024  # 50 MB
    elif args.hundredmb:
        min_size = 100 * 1024 * 1024  # 100 MB
    elif args.twohundredmb:
        min_size = 200 * 1024 * 1024  # 200 MB
    elif args.fivehundredmb:
        min_size = 500 * 1024 * 1024  # 500 MB
    elif args.onegb:
        min_size = 1 * 1024 * 1024 * 1024  # 1 GB

    # --all seçeneği kullanıldığında tüm uzantılar taranır, uzantı filtresi devre dışı kalır
    if args.all:
        allowed_extensions = None
    else:
        allowed_extensions = args.extensions

    # Dosya tarama ve kopyaları bulma, --force seçeneği kontrol edilir
    find_and_delete_copies(args.directory, allowed_extensions, min_size, force=args.force)

if __name__ == "__main__":
    main()
