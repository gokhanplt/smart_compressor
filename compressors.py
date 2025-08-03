# akilli_sikistirma/compressors.py

import zlib
import lzma
import bz2
import brotli
import zstandard

class Compressor:
    """
    Farklı sıkıştırma algoritmaları için temel bir arayüz sağlar.
    """
    def __init__(self, name: str):
        self.name = name

    def compress(self, data: bytes) -> bytes:
        """Veriyi sıkıştırır."""
        raise NotImplementedError("Bu metodun alt sınıflarda uygulanması gerekir.")

    def decompress(self, data: bytes) -> bytes:
        """Veriyi açar."""
        raise NotImplementedError("Bu metodun alt sınıflarda uygulanması gerekir.")

    def get_name(self) -> str:
        """Kompresörün adını döndürür."""
        return self.name

class ZlibCompressor(Compressor):
    def __init__(self):
        super().__init__("zlib")
    def compress(self, data: bytes) -> bytes:
        return zlib.compress(data)
    def decompress(self, data: bytes) -> bytes:
        return zlib.decompress(data)

class LzmaCompressor(Compressor):
    def __init__(self):
        super().__init__("lzma")
    def compress(self, data: bytes) -> bytes:
        return lzma.compress(data)
    def decompress(self, data: bytes) -> bytes:
        return lzma.decompress(data)

class BZ2Compressor(Compressor):
    def __init__(self):
        super().__init__("bz2")
    def compress(self, data: bytes) -> bytes:
        return bz2.compress(data)
    def decompress(self, data: bytes) -> bytes:
        return bz2.decompress(data)

class BrotliCompressor(Compressor):
    def __init__(self):
        super().__init__("brotli")
    def compress(self, data: bytes) -> bytes:
        return brotli.compress(data, quality=8)
    def decompress(self, data: bytes) -> bytes:
        return brotli.decompress(data)

class ZstandardCompressor(Compressor):
    def __init__(self):
        super().__init__("zstandard")
    def compress(self, data: bytes) -> bytes:
        return zstandard.compress(data, level=3)
    def decompress(self, data: bytes) -> bytes:
        return zstandard.decompress(data)

if __name__ == "__main__":
    print("--- compressors.py Modül Testleri ---")

    original_data = b"Bu bir deneme metnidir. Tekrar eden kelimeler icermektedir. Deneme deneme." * 10

    compressors_to_test = [
        ZlibCompressor(),
        LzmaCompressor(),
        BZ2Compressor(),
        BrotliCompressor(),
        ZstandardCompressor()
    ]

    for comp in compressors_to_test:
        print(f"\n--- {comp.get_name()} ile Test ---")
        try:
            compressed_data = comp.compress(original_data)
            decompressed_data = comp.decompress(compressed_data)

            print(f"  Orjinal Boyut: {len(original_data)} bayt")
            print(f"  Sıkıştırılmış Boyut: {len(compressed_data)} bayt")
            print(f"  Sıkıştırma Oranı: {len(original_data) / len(compressed_data):.2f}x")

            if original_data == decompressed_data:
                print("  Sıkıştırma ve Açma BAŞARILI: Veri bütünlüğü korundu.")
            else:
                print("  HATA: Veri bütünlüğü KORUNAMADI!")

        except Exception as e:
            print(f"  {comp.get_name()} testi sırasında hata oluştu: {e}")