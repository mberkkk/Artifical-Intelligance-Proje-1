from sklearn.preprocessing import StandardScaler
import numpy as np

#Örnek proje kağıdında örnek olarak verilen https://www.askpython.com/python/examples/standardize-data-in-python ile kendi örneğimiz olmak üzere iki farklı yolla yapılmıştır

#Örnek1
#1.Adım: Örnek bir veri oluşturalım

veri = ([2,9,3],[6,7,1],[5,4,7])

#Her bir sütunun yani aynı tipteki verinin ortalaması alınır
ortalama = np.mean(veri, axis = 0)

#for sütun in range(len(data[0])):
#   toplam = 0
#
#    for satır in range(len(data)):
#        toplam += data[satır][sütun]
#    ortalama[sütun] = toplam / len(data)
#ortalama yukarıdaki gibi de alınabilir ancak numpy kütüphanesi yardımıyla daha kolay almayı tercih ettik

#2.Adım: Veri setindeki aynı tipteki verilerin standart sapması hesaplanır
standart_sapma = np.std(veri,axis = 0)

#3.Adım: Standartization formulü olan "(Veri - Ortalama)/Standart Sapma" formulünden yola çıkılarak Standartization hesaplanır
standardize_veri = (veri - ortalama) / standart_sapma

#Aynı işlem for döngüsü ile aşağıdaki gibi de gerçekleştirilebilir
#satır = len(veri)
#column = len(veri[0])
#standardized_veri = []

#for i in range(satır):
#    row = []
#    for j in range(column):
#        row.append((veri[i][j] - ortalama[j]) / standart_sapma[j])
#    standardized_veri.append(row)

#4.Adım Sonuçların Yazdırılması

print("Veri:")
print(veri)

print("\nOrtalama:")
print(ortalama)

print("\nStandart Sapma:")
print(standart_sapma)

print("\nStandardize Edilmis Veri:")
print(standardize_veri)

#Örnek 2
#1.Adım StandardScaler bir değişkene atanır
scaler = StandardScaler()

#2.Adım 1.Örnekte oluşturulan data fit_transform metodu ile Standartize edilir
scaled_standardize_veri = scaler.fit_transform(veri)

#3.Adım Sonuç yazdırılır
print("\nStandardScaler Kullanılarak Standardize Edilmis Veri:")
print(scaled_standardize_veri)