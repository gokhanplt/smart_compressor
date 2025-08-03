# akilli_sikistirma/main.py

import os
import sys
import argparse
from datetime import datetime

# Projenin diğer modüllerini içe aktarıyoruz
# Not: main.py bir paket içinde çalıştığı için bu göreceli içe aktarmalar doğru çalışır.
from .data_analyzer import analyze_file_properties
from .compressor_selector import CompressorSelector
from .compressors import Compressor # Tip ipucu için (bir sınıf türü, örnek değil)

def get_timestamp_filename(original_filepath: str, suffix: str = "") -> str:
    """
    Orijinal dosya adına zaman damgası ve bir sonek ekleyerek yeni bir dosya adı oluşturur.
    Örn: 'dosya.txt' -> 'dosya_20230726_143000_compressed.gz'
    """
    base_name, ext = os.path.splitext(original_filepath)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{suffix}{ext}"

def compress_file(filepath: str, output_dir: str = '.') -> str or None:
    """
    Bir dosyayı analiz eder, en uygun algoritmayı seçer ve sıkıştırır.
    Sıkıştırılmış dosyanın yolunu döndürür.
    """
    print(f"\n--- '{filepath}' dosyası sıkıştırılıyor ---")

    # 1. Dosya özelliklerini analiz et
    analysis_results = analyze_file_properties(filepath)
    if not analysis_results:
        print("Dosya analizi başarısız oldu. Sıkıştırma iptal edildi.")
        return None

    print(f"  Analiz Sonuçları: Boyut={analysis_results['file_size']}B, Entropi={analysis_results['entropy']:.2f}, Uzantı='{analysis_results['file_extension']}'")

    # 2. Sıkıştırıcıyı seç
    selector = CompressorSelector()
    selected_compressor: Compressor = selector.select_compressor(analysis_results)
    
    print(f"  Seçilen Sıkıştırma Algoritması: {selected_compressor.get_name()}")

    try:
        # Orijinal içeriği oku
        with open(filepath, 'rb') as f:
            original_data = f.read()

        # 3. Veriyi sıkıştır
        print(f"  {selected_compressor.get_name()} ile sıkıştırma başlatılıyor...")
        compressed_data = selected_compressor.compress(original_data)
        print(f"  Sıkıştırma tamamlandı. Orjinal: {len(original_data)}B, Sıkıştırılmış: {len(compressed_data)}B")
        print(f"  Sıkıştırma Oranı: {len(original_data) / len(compressed_data):.2f}x")

        # 4. Sıkıştırılmış veriyi diske yaz
        # Sıkıştırılmış dosya adı için algoritma adını da ekleyelim.
        # Örneğin: original.txt -> original_timestamp_zlib.txt.compressed
        # Veya sadece uzantısı değişebilir: original.txt -> original.gz
        # Şimdilik basitçe orijinal uzantısını koruyup sonuna .compressed ve algoritma adını ekleyelim.
        output_filename = os.path.basename(filepath) + f".{selected_compressor.get_name()}.comp"
        compressed_filepath = os.path.join(output_dir, output_filename)

        with open(compressed_filepath, 'wb') as f:
            f.write(compressed_data)
        
        print(f"  Sıkıştırılmış dosya kaydedildi: '{compressed_filepath}'")
        return compressed_filepath

    except Exception as e:
        print(f"  Sıkıştırma işlemi sırasında bir hata oluştu: {e}")
        return None

def decompress_file(filepath: str, output_dir: str = '.') -> str or None:
    """
    Sıkıştırılmış bir dosyayı açar. Hangi algoritmayla sıkıştırıldığını dosya adından varsayar.
    Açılmış dosyanın yolunu döndürür.
    """
    print(f"\n--- '{filepath}' dosyası açılıyor ---")

    # Dosya adından sıkıştırıcı bilgisini çıkar
    parts = os.path.basename(filepath).split('.')
    if len(parts) < 3 or parts[-1] != 'comp':
        print(f"Hata: Geçersiz sıkıştırılmış dosya adı formatı. '{filepath}'")
        print("Beklenen format: 'orjinal_dosya_adi.algoritma_adi.comp'")
        return None
    
    # Algoritma adını al
    # Örn: 'my_file.txt.zlib.comp' -> 'zlib'
    compressor_name = parts[-2] 

    # Seçiciyi kullanarak uygun sıkıştırıcıyı bul
    selector = CompressorSelector()
    selected_compressor_class = selector.available_compressors.get(compressor_name)

    if not selected_compressor_class:
        print(f"Hata: Bilinmeyen sıkıştırma algoritması adı '{compressor_name}'. Açma iptal edildi.")
        return None
    
    selected_compressor: Compressor = selected_compressor_class()
    print(f"  Açma için seçilen algoritma: {selected_compressor.get_name()}")

    try:
        # Sıkıştırılmış içeriği oku
        with open(filepath, 'rb') as f:
            compressed_data = f.read()

        # Veriyi aç
        print(f"  {selected_compressor.get_name()} ile açma başlatılıyor...")
        decompressed_data = selected_compressor.decompress(compressed_data)
        print("  Açma tamamlandı.")

        # Açılmış veriyi diske yaz (orijinal uzantısını geri alarak)
        # Örn: my_file.txt.zlib.comp -> my_file.txt
        original_base_name = ".".join(parts[:-2]) # 'my_file.txt' kısmı
        decompressed_filepath = os.path.join(output_dir, original_base_name)

        with open(decompressed_filepath, 'wb') as f:
            f.write(decompressed_data)
        
        print(f"  Açılmış dosya kaydedildi: '{decompressed_filepath}'")
        return decompressed_filepath

    except Exception as e:
        print(f"  Açma işlemi sırasında bir hata oluştu: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Akıllı Veri Sıkıştırıcı: Dosya tipini analiz eder ve en verimli algoritmayı kullanır.",
        formatter_class=argparse.RawTextHelpFormatter # Açıklamaların satır atlaması için
    )
    
    parser.add_argument('action', choices=['compress', 'decompress'], 
                        help="Yapılacak işlem: 'compress' (sıkıştır) veya 'decompress' (aç).")
    parser.add_argument('filepath', type=str, 
                        help="İşlem yapılacak dosyanın yolu.")
    parser.add_argument('-o', '--output', type=str, default='.',
                        help="Çıktı dosyasının kaydedileceği dizin. Varsayılan: Mevcut dizin.")
    
    args = parser.parse_args()

    # Çıktı dizininin var olduğundan emin ol
    if not os.path.isdir(args.output):
        os.makedirs(args.output)
        print(f"Çıktı dizini oluşturuldu: '{args.output}'")

    if args.action == 'compress':
        compress_file(args.filepath, args.output)
    elif args.action == 'decompress':
        decompress_file(args.filepath, args.output)

    print("\nİşlem tamamlandı.")

if __name__ == "__main__":
    # main.py'yi bir modül olarak çalıştırırken (python -m smart_compressor.main)
    # veya doğrudan betik olarak (ancak bu durumda göreceli importlar sorun yaratabilir)
    main()