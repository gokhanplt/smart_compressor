# akilli_sikistirma/compressor_selector.py

from .compressors import ZlibCompressor, LzmaCompressor, BZ2Compressor, BrotliCompressor, ZstandardCompressor, Compressor
from typing import Dict, Any, Type

class CompressorSelector:
    """
    Dosya analiz sonuçlarına göre en uygun sıkıştırma algoritmasını seçer.
    Kural tabanlı bir seçim yapar.
    """
    def __init__(self):
        self.available_compressors: Dict[str, Type[Compressor]] = {
            "zlib": ZlibCompressor,
            "lzma": LzmaCompressor,
            "bz2": BZ2Compressor,
            "brotli": BrotliCompressor,
            "zstandard": ZstandardCompressor
        }

    def select_compressor(self, analysis_results: Dict[str, Any]) -> Compressor:
        """
        Analiz sonuçlarına göre en uygun sıkıştırma algoritmasını seçer.
        """
        file_size = analysis_results.get('file_size', 0)
        entropy = analysis_results.get('entropy', 0.0)
        file_extension = analysis_results.get('file_extension', '')
        
        # Güncellenmiş Kural Seti:
        if file_size < 1000: # 1KB'tan küçük dosyalar
            print(f"  [Seçim]: Çok küçük dosya ({file_size}B). Hızlı Zstandard seçildi.")
            return self.available_compressors["zstandard"]()

        if entropy > 7.5: # Yüksek entropili dosyalar
            print(f"  [Seçim]: Yüksek entropili dosya ({entropy:.2f} bit/bayt). LZMA deneniyor (maksimum sıkıştırma).")
            return self.available_compressors["lzma"]()

        if file_extension in ['.html', '.css', '.js', '.json', '.xml']:
            print(f"  [Seçim]: Web veya yapısal metin dosyası ({file_extension}). Brotli seçildi.")
            return self.available_compressors["brotli"]()
        
        if file_extension in ['.txt', '.log', '.csv', '.py', '.md']:
            print(f"  [Seçim]: Genel metin/kod dosyası ({file_extension}). Zstandard (hız ve oran dengesi) seçildi.")
            return self.available_compressors["zstandard"]()

        if entropy < 4.0: # Çok düşük entropili (çok tekrar eden) veriler
            print(f"  [Seçim]: Çok düşük entropili dosya ({entropy:.2f} bit/bayt). LZMA (yüksek sıkıştırma oranı) seçildi.")
            return self.available_compressors["lzma"]()

        # Varsayılan veya bilinmeyen dosya tipleri için Zstandard iyi bir genel çözümdür.
        print(f"  [Seçim]: Genel dosya tipi. Zstandard varsayılan olarak seçildi.")
        return self.available_compressors["zstandard"]()

if __name__ == "__main__":
    from .data_analyzer import analyze_file_properties # Bu satır, paketin içinden doğru import için gerekli
    import os

    print("--- compressor_selector.py Modül Testleri ---")

    selector = CompressorSelector()

    test_files = {
        "text_file.txt": "Bu bir test metnidir. Tekrar eden kelimeler icermektedir. test test test." * 50,
        "high_entropy_binary.bin": bytes([i % 256 for i in range(2000)]),
        "low_entropy_binary.bin": b'\x00' * 5000 + b'\xFF' * 5000,
        "small_file.txt": "kisa metin",
        "web_page.html": "<html><body><h1>Merhaba Dünya</h1><p>Bu bir deneme HTML sayfasıdır. Sayfa içeriği.</p></body></html>" * 20,
        "javascript.js": "function greet(name) { console.log('Hello, ' + name + '!'); } greet('World');" * 30
    }

    for filename, content in test_files.items():
        file_path = filename
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(file_path, mode) as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                f.write(content)

        print(f"\nDosya: '{file_path}'")
        analysis = analyze_file_properties(file_path)
        if analysis:
            print(f"  Boyut: {analysis['file_size']}B, Entropi: {analysis['entropy']:.2f}, Uzantı: {analysis['file_extension']}")
            selected_compressor = selector.select_compressor(analysis)
            print(f"  Seçilen Algoritma: {selected_compressor.get_name()}")
        
        os.remove(file_path)
    
    print("\nTest dosyaları temizlendi.")