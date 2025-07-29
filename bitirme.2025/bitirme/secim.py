import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

# 1. Gerçek oy ve vekil verisi yükleniyor
df_oy = pd.read_csv(r"C:\Users\asus\Downloads\secim.csv", encoding="windows-1254", sep=";", header=1)
df_oy.columns = df_oy.columns.str.strip()
df_oy = df_oy[df_oy["İl Adı"].notna()]
df_oy = df_oy[~df_oy["İl Adı"].str.contains("TOPLAMI|OY ORANI", case=False, na=False)]
df_oy["il_adi_duz"] = df_oy["İl Adı"].str.extract(r"([^\d]+)")[0].str.strip().str.upper()

df_aday = pd.read_csv(r"C:\Users\asus\Downloads\SecilenAdaylar.csv", sep=";", skiprows=1)
df_aday["il_adi_duz"] = df_aday["Seçim Çevresi Adı"].str.extract(r"([A-ZÇĞİÖŞÜ ]+)-?\d*")[0].str.strip().str.upper()
milletvekili_sayilari = df_aday.groupby("il_adi_duz").size().reset_index(name="milletvekili_sayisi")

# 2. Oylar gruplanıyor
oy_partileri = df_oy.columns[6:-1]
df_oy_il = df_oy.groupby("il_adi_duz")[oy_partileri].sum().fillna(0).reset_index()
df_analiz = df_oy_il.merge(milletvekili_sayilari, how="left", on="il_adi_duz")
df_analiz = df_analiz[df_analiz["milletvekili_sayisi"].notna()]

# 3. Yöntem fonksiyonları
def dhondt(votes, seats):
    quotients = []
    for party, vote in votes.items():
        for d in range(1, seats + 1):
            quotients.append((vote / d, party))
    quotients.sort(reverse=True)
    allocation = defaultdict(int)
    for i in range(seats):
        _, p = quotients[i]
        allocation[p] += 1
    return dict(allocation)

def sainte_lague(votes, seats):
    quotients = []
    for party, vote in votes.items():
        for d in range(1, 2 * seats, 2):
            quotients.append((vote / d, party))
    quotients.sort(reverse=True)
    allocation = defaultdict(int)
    for i in range(seats):
        _, p = quotients[i]
        allocation[p] += 1
    return dict(allocation)

# 4. Analiz
rapor = []
toplam_dh = defaultdict(int)
toplam_sl = defaultdict(int)

for _, row in df_analiz.iterrows():
    il = row["il_adi_duz"]
    mv = int(row["milletvekili_sayisi"])
    oylar = row[oy_partileri].to_dict()
    oylar = {k: int(str(v).replace(".", "").replace(",", "").strip()) for k, v in oylar.items()}

    dag_dh = dhondt(oylar, mv)
    dag_sl = sainte_lague(oylar, mv)

    for parti in oylar:
        toplam_dh[parti] += dag_dh.get(parti, 0)
        toplam_sl[parti] += dag_sl.get(parti, 0)

    yorum = []
    for parti in oylar:
        fark = dag_sl.get(parti, 0) - dag_dh.get(parti, 0)
        if fark > 0:
            yorum.append(f"{parti}: +{fark} vekil (avantaj)")
        elif fark < 0:
            yorum.append(f"{parti}: -{abs(fark)} vekil (dezavantaj)")

    rapor.append({
        "il": il,
        "mv": mv,
        "dhondt": dag_dh,
        "saint": dag_sl,
        "yorum": yorum
    })

# 5. Seçili illeri yazdır
secili_iller = ["ADANA", "MERSİN", "TRABZON", "ESKİŞEHİR", "VAN", "AYDIN"]
print("\n🔍 SEÇİLİ 6 İL DETAYLI ANALİZ:\n" + "=" * 60)
for il_kaydi in rapor:
    if il_kaydi["il"].upper() in secili_iller:
        print(f"\n🏙️ {il_kaydi['il'].upper()}")
        print(f"Toplam MV: {il_kaydi['mv']}")
        print("D'Hondt:", il_kaydi["dhondt"])
        print("Sainte-Laguë:", il_kaydi["saint"])
        print("Yorumlar:")
        for y in il_kaydi["yorum"]:
            print(" -", y)

# 6. Türkiye geneli fark grafiği
partiler = sorted(toplam_dh.keys())
farklar = {p: toplam_sl[p] - toplam_dh[p] for p in partiler}

plt.figure(figsize=(12, 6))
bars = plt.bar(partiler, [farklar[p] for p in partiler])
plt.axhline(0, color='black')
plt.title("Sainte-Laguë - D'Hondt Farkı (Milletvekili Sayısı)")
plt.ylabel("Fark")
plt.xticks(rotation=45)
for bar, parti in zip(bars, partiler):
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y, f"{y:+}", ha="center", va="bottom" if y > 0 else "top")
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# 7. Türkiye geneli tablo
print("\n📊 TÜRKİYE GENELİ MİLLETVEKİLİ SİSTEM KARŞILAŞTIRMASI\n" + "-" * 60)
print("{:<25} {:>10} {:>15} {:>10}".format("Siyasi Parti", "D’Hondt", "Sainte-Laguë", "Değişim"))
print("-" * 60)
for parti in partiler:
    dh = toplam_dh[parti]
    sl = toplam_sl[parti]
    fark = sl - dh
    print("{:<25} {:>10} {:>15} {:>10}".format(parti, dh, sl, f"{fark:+}"))
import pandas as pd

# Ülke genelindeki toplam oy sayıları birbirine yakın olan iki partinin Saint League metodu uygulandığındaki mv sayılarındaki değişiminin analizi 
import pandas as pd

# Partiler
parti1 = "MHP"
parti2 = "YEŞİL SOL PARTİ"

# Veriler
il_listesi = []
mhp_dh_list = []
mhp_sl_list = []
mhp_fark_list = []
ysp_dh_list = []
ysp_sl_list = []
ysp_fark_list = []

for il in rapor:
    il_adi = il['il']
    dh1 = il["dhondt"].get(parti1, 0)
    sl1 = il["saint"].get(parti1, 0)
    fark1 = sl1 - dh1

    dh2 = il["dhondt"].get(parti2, 0)
    sl2 = il["saint"].get(parti2, 0)
    fark2 = sl2 - dh2

    if (dh1 or sl1 or dh2 or sl2):
        il_listesi.append(il_adi)
        mhp_dh_list.append(dh1)
        mhp_sl_list.append(sl1)
        mhp_fark_list.append(f"{fark1:+}" if fark1 != 0 else "0")
        ysp_dh_list.append(dh2)
        ysp_sl_list.append(sl2)
        ysp_fark_list.append(f"{fark2:+}" if fark2 != 0 else "0")

# DataFrame
df_karsilastirma = pd.DataFrame({
    "İl": il_listesi,
    "MHP D’Hondt": mhp_dh_list,
    "MHP S-Laguë": mhp_sl_list,
    "MHP Fark": mhp_fark_list,
    "YSP D’Hondt": ysp_dh_list,
    "YSP S-Laguë": ysp_sl_list,
    "YSP Fark": ysp_fark_list
})

# Toplamları hesapla
toplam_row = {
    "İl": "TOPLAM",
    "MHP D’Hondt": sum(mhp_dh_list),
    "MHP S-Laguë": sum(mhp_sl_list),
    "MHP Fark": f"{sum(sl - dh for sl, dh in zip(mhp_sl_list, mhp_dh_list)):+}",
    "YSP D’Hondt": sum(ysp_dh_list),
    "YSP S-Laguë": sum(ysp_sl_list),
    "YSP Fark": f"{sum(sl - dh for sl, dh in zip(ysp_sl_list, ysp_dh_list)):+}",
}

df_karsilastirma.loc[len(df_karsilastirma.index)] = toplam_row

# Yazdır
print("\n📊 MHP ve YEŞİL SOL PARTİ Karşılaştırmalı Tablo")
print(df_karsilastirma.to_string(index=False))
