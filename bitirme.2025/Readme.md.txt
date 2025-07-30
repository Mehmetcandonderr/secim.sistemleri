# Türkiye Seçim Simülasyonu  
**D'Hondt ve Sainte-Laguë Sistemleriyle Milletvekili Dağılımı Karşılaştırması**

Bu Python projesi, Türkiye'de yapılan milletvekili seçimlerini iki farklı dağıtım yöntemiyle simüle eder: **D'Hondt** ve **Sainte-Laguë**. Gerçek oy ve aday verileri kullanılarak partilere il bazında kaç vekil düştüğü hesaplanır ve sistem farkları analiz edilir.

---

## Ne Yapıyor Bu Proje?

- **Gerçek seçim verilerini** (oy sayıları + vekil sayıları) okur.
- İllerin milletvekili kontenjanlarına göre partilerin alacağı vekil sayısını **D’Hondt** ve **Sainte-Laguë** yöntemleriyle hesaplar.
- Her iki sistemin sonuçlarını karşılaştırır, farkları çıkarır.
- Türkiye geneli için **grafik** ve **tablo** oluşturur.
- 6 il (Adana, Mersin, Trabzon, Eskişehir, Van, Aydın) için özel analizler üretir.

---

##  Temel Bileşenler

- `secim.csv`: İllere göre partilerin aldığı oylar  
- `SecilenAdaylar.csv`: İllere göre vekil kontenjanları  
- `dhondt()` ve `sainte_lague()` fonksiyonları: İlgili dağıtım algoritmaları  
- `matplotlib`: Farkları grafiksel olarak göstermek için  
- `pandas`: Veri işleme ve tablo yapısı  

---

##  Örnek Çıktılar

### İl Bazında Karşılaştırma

```
 MERSİN
Toplam MV: 13
D'Hondt: {'AK PARTİ': 4, 'CHP': 5, 'MHP': 1, 'YSP': 3}
Sainte-Laguë: {'AK PARTİ': 3, 'CHP': 6, 'MHP': 1, 'YSP': 3}
Yorumlar:
 - CHP: +1 vekil (avantaj)
 - AK PARTİ: -1 vekil (dezavantaj)
```

### Türkiye Geneli Özet Tablosu

```
Siyasi Parti             D’Hondt   Sainte-Laguë    Değişim
----------------------------------------------------------
AK PARTİ                    268              258         -10
CHP                         169              177         +8
MHP                          50               44         -6
YSP                          61               68         +7
...
```

###  Grafik

- Her parti için iki sistem arasındaki farklar bar grafiğiyle görselleştirilir.

---

##  Nasıl Çalıştırılır?

1. Gerekli kütüphaneleri yükleyin:
   pip install pandas matplotlib
   

2. CSV dosyalarını `secim.csv` ve `SecilenAdaylar.csv` olarak script içinde belirtilen yollarla aynı klasöre koyun veya dosya yollarını güncelleyin.

3. Script'i çalıştırın:
   python secim.py

---

##  Notlar

- Veriler 2023 Türkiye seçim sonuçlarından alınmıştır.
- Sainte-Laguë sistemi küçük ve orta ölçekli partilere daha fazla şans tanırken, D’Hondt büyük partilere avantaj sağlar.
- Kod, görselleştirme ve karşılaştırma amacıyla akademik kullanıma uygundur. Gerçek resmi sonuçlar için YSK kaynakları esas alınmalıdır.

---

Bu proje kişisel, akademik ve görsel analiz amacıyla paylaşılmıştır. Herhangi bir siyasi kurumla bağlantısı yoktur.
