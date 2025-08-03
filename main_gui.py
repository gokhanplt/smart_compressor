# akilli_sikistirma/main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading # Uzun süren işlemleri arayüzü dondurmadan yapmak için

# Diğer modüllerimizi içe aktarıyoruz
from .data_analyzer import analyze_file_properties
from .compressor_selector import CompressorSelector
from .compressors import Compressor # Tip ipucu için

class SmartCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Sıkıştırma Uygulaması")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.input_filepath = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.getcwd()) # Varsayılan çıktı dizini
        self.last_compressed_filepath = None # Yeni eklenen değişken

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="Giriş Dosyası Seçimi", padding="10")
        input_frame.pack(pady=10, fill=tk.X)

        ttk.Label(input_frame, text="Dosya Yolu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.input_filepath, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(input_frame, text="Gözat...", command=self._browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        input_frame.columnconfigure(1, weight=1)

        output_frame = ttk.LabelFrame(main_frame, text="Çıktı Dizini", padding="10")
        output_frame.pack(pady=10, fill=tk.X)

        ttk.Label(output_frame, text="Dizin Yolu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(output_frame, text="Gözat...", command=self._browse_output_dir).grid(row=0, column=2, padx=5, pady=5)
        output_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Sıkıştır", command=self._start_compress_thread, width=15).pack(side=tk.LEFT, padx=10)
        
        # 'Aç' butonu için özel bir metot ekliyoruz.
        # Bu metot, last_compressed_filepath'i kontrol edip input_filepath'i ayarlayacak.
        self.decompress_button = ttk.Button(button_frame, text="Aç", command=self._prepare_decompress, width=15)
        self.decompress_button.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(main_frame, text="Hazır...", anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="indeterminate", length=400)
        self.progress_bar.pack(pady=5)
        self.progress_bar.pack_forget()

    def _browse_input_file(self):
        filepath = filedialog.askopenfilename(
            title="Sıkıştırılacak/Açılacak Dosyayı Seçin",
            filetypes=[("Tüm Dosyalar", "*.*")]
        )
        if filepath:
            self.input_filepath.set(filepath)

    def _browse_output_dir(self):
        directory = filedialog.askdirectory(
            title="Çıktı Dizini Seçin"
        )
        if directory:
            self.output_dir.set(directory)

    def _update_status(self, message: str):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def _start_compress_thread(self):
        filepath = self.input_filepath.get()
        output_dir = self.output_dir.get()

        if not filepath:
            messagebox.showwarning("Uyarı", "Lütfen bir giriş dosyası seçin.")
            return
        if not os.path.exists(filepath):
            messagebox.showerror("Hata", f"Giriş dosyası bulunamadı: '{filepath}'")
            return
        
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        self._update_status("Sıkıştırma başlatılıyor...")

        thread = threading.Thread(target=self._run_compress, args=(filepath, output_dir))
        thread.start()

    def _run_compress(self, filepath: str, output_dir: str):
        try:
            analysis_results = analyze_file_properties(filepath)
            if not analysis_results:
                raise Exception("Dosya analizi başarısız oldu.")

            selector = CompressorSelector()
            selected_compressor: Compressor = selector.select_compressor(analysis_results)
            
            self._update_status(f"Seçilen algoritma: {selected_compressor.get_name()}. Sıkıştırma başlatılıyor...")

            with open(filepath, 'rb') as f:
                original_data = f.read()

            compressed_data = selected_compressor.compress(original_data)
            
            output_filename = os.path.basename(filepath) + f".{selected_compressor.get_name()}.comp"
            compressed_filepath = os.path.join(output_dir, output_filename)

            os.makedirs(output_dir, exist_ok=True)

            with open(compressed_filepath, 'wb') as f:
                f.write(compressed_data)
            
            original_size = len(original_data)
            compressed_size = len(compressed_data)
            compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
            
            # Sıkıştırma tamamlandığında son sıkıştırılan dosya yolunu kaydet
            self.last_compressed_filepath = compressed_filepath

            messagebox.showinfo(
                "Sıkıştırma Başarılı",
                f"Dosya başarıyla sıkıştırıldı!\n"
                f"Algoritma: {selected_compressor.get_name()}\n"
                f"Orijinal Boyut: {original_size} B\n"
                f"Sıkıştırılmış Boyut: {compressed_size} B\n"
                f"Sıkıştırma Oranı: {compression_ratio:.2f}x\n"
                f"Kaydedildi: '{compressed_filepath}'"
            )
            self._update_status("Sıkıştırma tamamlandı.")

        except Exception as e:
            messagebox.showerror("Sıkıştırma Hatası", f"Dosya sıkıştırılırken bir hata oluştu: {e}")
            self._update_status("Sıkıştırma başarısız oldu.")
            self.last_compressed_filepath = None # Hata olursa sıfırla
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def _prepare_decompress(self):
        """
        Açma işlemini başlatmadan önce, eğer mevcutsa en son sıkıştırılan dosyanın yolunu ayarlar.
        """
        if self.last_compressed_filepath and os.path.exists(self.last_compressed_filepath):
            self.input_filepath.set(self.last_compressed_filepath)
            self._update_status(f"Son sıkıştırılan dosya ('{os.path.basename(self.last_compressed_filepath)}') otomatik seçildi.")
            # Otomatik seçildikten sonra decompress thread'i başlat
            self._start_decompress_thread()
        else:
            # Eğer son sıkıştırılan dosya yoksa veya bulunamazsa, kullanıcıdan dosya seçmesini iste
            messagebox.showinfo("Bilgi", "En son sıkıştırılan dosya bulunamadı veya daha önce sıkıştırma yapılmadı. Lütfen açmak istediğiniz dosyayı manuel olarak seçin.")
            self._browse_input_file() # Dosya seçim penceresini aç
            # Kullanıcı dosya seçtikten sonra manuel olarak 'Aç' butonuna tekrar basması gerekecek.
            # Veya _browse_input_file içinden doğrudan _start_decompress_thread çağrılabilir.
            # Şimdilik kullanıcıdan tekrar basmasını bekleyelim, arayüz akışı için daha net olabilir.


    def _start_decompress_thread(self):
        filepath = self.input_filepath.get()
        output_dir = self.output_dir.get()

        if not filepath:
            messagebox.showwarning("Uyarı", "Lütfen bir giriş dosyası seçin.")
            return
        if not os.path.exists(filepath):
            messagebox.showerror("Hata", f"Giriş dosyası bulunamadı: '{filepath}'")
            return

        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        self._update_status("Açma başlatılıyor...")

        thread = threading.Thread(target=self._run_decompress, args=(filepath, output_dir))
        thread.start()

    def _run_decompress(self, filepath: str, output_dir: str):
        try:
            parts = os.path.basename(filepath).split('.')
            if len(parts) < 3 or parts[-1] != 'comp':
                raise ValueError("Geçersiz sıkıştırılmış dosya adı formatı. Beklenen format: 'orjinal_dosya_adi.algoritma_adi.comp'")
            
            compressor_name = parts[-2] 

            selector = CompressorSelector()
            selected_compressor_class = selector.available_compressors.get(compressor_name)

            if not selected_compressor_class:
                raise ValueError(f"Bilinmeyen sıkıştırma algoritması adı: '{compressor_name}'.")
            
            selected_compressor: Compressor = selected_compressor_class()
            self._update_status(f"Açma için seçilen algoritma: {selected_compressor.get_name()}.")

            with open(filepath, 'rb') as f:
                compressed_data = f.read()

            decompressed_data = selected_compressor.decompress(compressed_data)

            original_base_name = ".".join(parts[:-2])
            decompressed_filepath = os.path.join(output_dir, original_base_name)

            os.makedirs(output_dir, exist_ok=True)

            with open(decompressed_filepath, 'wb') as f:
                f.write(decompressed_data)
            
            messagebox.showinfo(
                "Açma Başarılı",
                f"Dosya başarıyla açıldı!\n"
                f"Algoritma: {selected_compressor.get_name()}\n"
                f"Kaydedildi: '{decompressed_filepath}'"
            )
            self._update_status("Açma tamamlandı.")

        except Exception as e:
            messagebox.showerror("Açma Hatası", f"Dosya açılırken bir hata oluştu: {e}")
            self._update_status("Açma başarısız oldu.")
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

def start_gui():
    root = tk.Tk()
    app = SmartCompressorApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()