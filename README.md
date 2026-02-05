CODESYS-Python TCP Communication Bridge
Bu proje, CODESYS V3.5 tabanlı sanal PLC'ler ile Python arasında yüksek hızlı, esnek ve nesne yönelimli bir haberleşme köprüsü kurmanızı sağlar. Statik veri yapıları yerine CODESYS'in Symbol Configuration özelliğini kullanarak değişkenlerin bellek adreslerini (offset) dinamik olarak eşleştirir.

# 🚀 Özellikler

Dinamik Veri Eşleştirme: PLC tarafındaki ST_Data yapısı değişse bile Python tarafında kod değişikliği yapmadan veriye erişim.


Tip Güvenliği: BOOL, INT ve REAL veri tipleri için özel olarak optimize edilmiş parser yapısı. - FB içinde istenilen data tipine göre ekleme yapılabilir.


Hata Yönetimi: Bağlantı kopmaları ve geçersiz paketler için yerleşik hata kontrol mekanizması.


Performans: TCP protokolü üzerinden düşük gecikmeli veri transferi.

# 🛠 Gereksinimler
PLC Tarafı
CODESYS V3.5 veya üzeri.


CAA Net Base Services kütüphanesi (Haberleşme blokları için gereklidir).

Not: Library Manager üzerinden "CAA Net Base Services" kütüphanesini indirmeyi ve projenize eklemeyi unutmayın.

Python Tarafı
Python 3.x


PLCProxy kütüphanesi (Dosya içerisinde mevcuttur).

# 📦 Kurulum ve Kullanım
1. PLC Yapılandırması

ST_Data yapısını kendi ihtiyacınıza göre düzenleyin.


Symbol Configuration (Sembol Yapılandırması) nesnesini ekleyin ve ST_Data içerisindeki değişkenleri seçerek projeyi "Build" edin.

Oluşan .xml dosya yolunu Python içeriğindeki XML_PATH değişkenine yazılmalıdır; bu dosya Python tarafında değişken adreslerini bulmak için kullanılacaktır.

2. Python Bağlantısı
PLCProxy sınıfını kullanarak PLC'ye bağlanabilir ve değişkenlere doğrudan isimleri üzerinden erişebilirsiniz:

Python
from PLC_Proxy import PLCProxy

# Yapılandırma
XML_PATH = "C:\\path\\to\\your\\PLC_Config.xml"
plc = PLCProxy("127.0.0.1", 5000, XML_PATH)

# Veri Okuma/Yazma
plc.Hiz_Setpoint1 = 40  # Yazma
current_temp = plc.Sicaklik  # Okuma
📂 Proje Yapısı

/PLC: CODESYS projeleri ve FB_PythonComm kaynak kodları.


/Python: PLCManager ve örnek test scriptleri.


/Docs: Protokol detayları ve kurulum adımları.

