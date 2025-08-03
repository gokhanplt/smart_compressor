# akilli_sikistirma/data_analyzer.py

import os
import collections
import math

def analyze_file_properties(filepath: str) -> dict or None:
    """
    Belirtilen dosyanın temel istatistiksel özelliklerini analiz eder.
    Bayt frekansı, Shannon entropisi ve dosya uzantısı gibi bilgileri döner.

    Args:
        filepath (str): Analiz edilecek dosyanın yolu.

    Returns:
        dict or None: Analiz sonuçlarını içeren bir sözlük veya hata durumunda None.
                      Sözlük şu anahtarları içerir:
                      'file_size': Dosyanın bayt cinsinden boyutu.
                      'entropy': Dosyanın Shannon entropisi (bit/bayt).
                      'byte_frequencies': Her bayt değerinin frekans dağılımı.
                      'file_extension': Dosyanın uzantısı (küçük harf).
    """
    if not os.path.exists(filepath):
        print(f"Hata: Dosya bulunamadı - '{filepath}'")
        return None

    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        file_size = len(content)
        if file_size == 0:
            return {
                'file_size': 0,
                'entropy': 0.0,
                'byte_frequencies': {},
                'file_extension': os.path.splitext(filepath)[1].lower()
            }

        byte_counts = collections.Counter(content)
        byte_frequencies = {k: v / file_size for k, v in byte_counts.items()}

        entropy = 0.0
        for freq in byte_frequencies.values():
            if freq > 0:
                entropy -= freq * math.log2(freq)

        file_extension = os.path.splitext(filepath)[1].lower()

        analysis_results = {
            'file_size': file_size,
            'entropy': entropy,
            'byte_frequencies': byte_frequencies,
            'file_extension': file_extension
        }
        return analysis_results

    except Exception as e:
        print(f"Dosya analiz edilirken beklenmeyen bir hata oluştu: {e}")
        return None

if __name__ == "__main__":
    print("--- data_analyzer.py Modül Testleri ---")

    test_text_path = "test_text.txt"
    with open(test_text_path, "w", encoding="utf-8") as f:
        f.write("Bu bir deneme metnidir. Tekrar eden kelimeler içermektedir. Deneme deneme.")
    
    print(f"\n'{test_text_path}' analizi:")
    text_analysis = analyze_file_properties(test_text_path)
    if text_analysis:
        print(f"  Dosya Boyutu: {text_analysis['file_size']} bayt")
        print(f"  Entropi: {text_analysis['entropy']:.4f} bit/bayt")
        print(f"  Uzantı: {text_analysis['file_extension']}")

    test_binary_path = "test_binary.bin"
    try:
        import random
        with open(test_binary_path, "wb") as f:
            f.write(bytes([random.randint(0, 255) for _ in range(1024)]))
        
        print(f"\n'{test_binary_path}' analizi:")
        binary_analysis = analyze_file_properties(test_binary_path)
        if binary_analysis:
            print(f"  Dosya Boyutu: {binary_analysis['file_size']} bayt")
            print(f"  Entropi: {binary_analysis['entropy']:.4f} bit/bayt")
            print(f"  Uzantı: {binary_analysis['file_extension']}")
    except Exception as e:
        print(f"'{test_binary_path}' oluşturulurken veya analiz edilirken hata: {e}")

    test_empty_path = "test_empty.txt"
    with open(test_empty_path, "w") as f:
        pass
    
    print(f"\n'{test_empty_path}' analizi:")
    empty_analysis = analyze_file_properties(test_empty_path)
    if empty_analysis:
        print(f"  Dosya Boyutu: {empty_analysis['file_size']} bayt")
        print(f"  Entropi: {empty_analysis['entropy']:.4f} bit/bayt")
        print(f"  Uzantı: {empty_analysis['file_extension']}")

    try:
        os.remove(test_text_path)
        os.remove(test_binary_path)
        os.remove(test_empty_path)
        print("\nTest dosyaları temizlendi.")
    except OSError as e:
        print(f"Test dosyaları silinirken hata: {e}")