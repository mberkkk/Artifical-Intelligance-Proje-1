#RANDOM FOREST
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from ucimlrepo import fetch_ucirepo
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_validate

  
# dataset sisteme yüklenir 
breast_cancer_wisconsin_diagnostic = fetch_ucirepo(id=17) 
  
# data (as pandas dataframes) 
X = breast_cancer_wisconsin_diagnostic.data.features 
y = breast_cancer_wisconsin_diagnostic.data.targets.values.ravel()

#Random Forest ile Sınıflandırma yapacağımız fonksiyon bir değişkene atanır  
rfc = RandomForestClassifier(random_state=0)

X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.7, test_size = 0.3, random_state = 0, stratify = y)

# Eğitim Verisi ile eğitimi gerçekleştiriyoruz
rfc.fit(X_train,y_train)

#Sonucu alıp yazdıralım
test_sonuc = rfc.predict(X_test)
print(test_sonuc)

#Bir confusion matrixi oluşturalım
cm = confusion_matrix(y_test, test_sonuc)
print(cm)
#Oluşturulan confusion matrixi ayrı bir pencerede görselleştirilir
plt.matshow(cm)
plt.title('Confusion matrix')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()


#İki adet örnek veri oluşturulup bu veri setilerin hangi sınıfa ait olduğu bulunur
test_ornek = ([17.52,19.51,99.84,564.7,0.1132,0.2338,0.1325,0.08356,0.1499,0.08892,0.7891,1.968,4.373,50.78,0.007907,0.05756,0.06443,0.01623,0.02947,0.006643,15.43,24.71,103.1,856.5,0.1146,0.4762,0.4922,0.1685,0.2334,0.09032],
              [16.44,18.24,90.77,516.9,0.1002,0.1339,0.29966,0.09064,0.1216,0.04396,0.4175,1.3772,4.184,62.76,0.006808,0.06612,0.04646,0.01848,0.02121,0.003321,18.34,22.22,119.4,873.6,0.1607,0.6830,0.3104,0.1697,0.2851,0.03473])
ornek_sonucu = rfc.predict(test_ornek)
print(ornek_sonucu)

#Accuracy,Precision ve Recall değerlerini kıyaslayalım
scoring = ["accuracy",'precision_macro', 'recall_macro']
#10 katmanlı cross validation gerçekleştirilir
scores = cross_validate(rfc, X, y, scoring=scoring, cv = 10)
sorted(scores.keys())
["accuracy", 'test_precision_macro', 'test_recall_macro']

#Sonuçların ortalama değeri alınır
accuracy_mean = scores['test_accuracy'].mean()
precision_mean = scores['test_precision_macro'].mean()
recall_mean = scores['test_recall_macro'].mean()

#Sonuçlar formatlanarak yazdırılır
print("Accuracy: {:.2f}".format(accuracy_mean))
print("Precision: {:.2f}".format(precision_mean))
print("Recall: {:.2f}".format(recall_mean))
