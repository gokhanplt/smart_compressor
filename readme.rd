Akıllı Sıkıştırma Aracı
Bu proje, bir dosyanın içeriğini analiz ederek en uygun sıkıştırma algoritmasını otomatik olarak seçen ve uygulayan, Python tabanlı bir akıllı sıkıştırma aracıdır. Kullanıcı dostu bir grafik arayüzü (GUI) ile dosyaları kolayca sıkıştırabilir ve açabilirsiniz.

Neden Akıllı Sıkıştırma?
Farklı sıkıştırma algoritmaları, farklı dosya türlerinde (metin, ikili veri, web içeriği vb.) farklı performanslar gösterir. Örneğin, bir metin dosyasını sıkıştırmak için en iyi algoritma, rastgele baytlardan oluşan bir ikili dosyayı sıkıştırmak için en iyi algoritma olmayabilir. Bu araç, dosyanın boyutunu, dosya uzantısını ve entropi (bilgi miktarı) gibi istatistiksel özelliklerini analiz ederek en iyi sıkıştırma oranını veya en iyi hız/oran dengesini sunan algoritmayı dinamik olarak seçer.

Özellikler:

Akıllı Algoritma Seçimi: Dosya özelliklerine göre zlib, lzma, bz2, brotli ve zstandard gibi popüler kayıpsız sıkıştırma algoritmaları arasından en uygun olanını seçer.

Grafik Kullanıcı Arayüzü (GUI): Kullanımı kolay, sezgisel bir arayüz ile dosya seçme, sıkıştırma ve açma işlemlerini kolaylaştırır.

Detaylı Geri Bildirim: Sıkıştırma işlemi tamamlandığında, kullanılan algoritma, sıkıştırma oranı ve dosya boyutları gibi detaylı bilgileri sunar.

Kolay Kullanım: Sıkıştırılan dosyaları tek bir tıkla açabilir, bu sayede iş akışınızı hızlandırabilirsiniz.

Kurulum ve Çalıştırma
Projenin çalışabilmesi için Python 3'e ve bazı ek kütüphanelere ihtiyacınız olacaktır.

Adım 1: Gerekli Kütüphaneleri Yükleme
Terminalinizi açın ve aşağıdaki komutu çalıştırarak gerekli Python paketlerini yükleyin:

Bash

pip install brotli zstandard
Adım 2: Projeyi Çalıştırma
Projeniz bir Python paketi olarak yapılandırılmıştır. Bu nedenle, main_gui.py dosyasını doğrudan değil, bir modül olarak çalıştırmanız gerekir.

Terminalinizde, akilli_sikistirma klasörünün bir üst dizinine gidin. (Yani, akilli_sikistirma klasörünü içeren dizine.)

Aşağıdaki komutu çalıştırarak uygulamayı başlatın:

Bash

python -m akilli_sikistirma.main_gui
Bu komut, uygulamanın ana penceresini açacaktır.

Nasıl Kullanılır?
Sıkıştırma:

Giriş Dosyası bölümündeki "Gözat..." butonuna tıklayarak sıkıştırmak istediğiniz dosyayı seçin.

Çıktı Dizini bölümünden sıkıştırılmış dosyanın kaydedileceği yeri belirleyin (varsayılan olarak mevcut dizindir).

"Sıkıştır" butonuna tıklayın.

İşlem tamamlandığında, sıkıştırma oranları ve dosya yolu gibi bilgileri içeren bir bildirim alacaksınız.

Açma:

Eğer son sıkıştırdığınız dosyayı açmak istiyorsanız, "Aç" butonuna tıklamanız yeterlidir. Uygulama, sıkıştırılmış dosyayı otomatik olarak seçecek ve açacaktır.

Başka bir sıkıştırılmış dosyayı açmak için, Giriş Dosyası bölümünden .comp uzantılı dosyayı manuel olarak seçin ve "Aç" butonuna tıklayın.

Geliştirme ve Katkıda Bulunma
Bu proje açık kaynaklıdır ve katkılarınızı memnuniyetle karşılarız. Yeni sıkıştırma algoritmaları eklemek, kullanıcı arayüzünü iyileştirmek veya algoritma seçim mantığını daha da geliştirmek için fikirleriniz varsa lütfen iletişime geçin.
