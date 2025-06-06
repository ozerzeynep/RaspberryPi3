# 🌐 IoT Tabanlı Gerçek Zamanlı Sensör Verisi Toplama ve AWS MQTT ile Bulut Entegrasyonu

Bu proje, **Raspberry Pi** üzerinde çalışan bir Python uygulaması ile **DHT11** (sıcaklık ve nem) ve **PZEM-004T** (gerilim, akım, güç, enerji) sensörlerinden gerçek zamanlı veri toplayarak bu verileri hem **lokal bir zaman serisi veritabanında (InfluxDB)** saklamayı hem de **AWS IoT Core** üzerinden **MQTT protokolü** ile buluta iletmeyi amaçlamaktadır. Görselleştirme işlemleri **Grafana** arayüzü ile sağlanmaktadır. Bu sistem, uzaktan izlenebilirlik, enerji takibi ve çevresel izleme uygulamaları için temel bir altyapı sunar.

---

## 🚀 Kullanılan Teknolojiler ve Bileşenler

- 🧠 **Raspberry Pi** – Merkezi kontrol birimi, veri okuma ve aktarımı
- 🌡️ **DHT11** – Ortam sıcaklık ve nem sensörü
- ⚡ **PZEM-004T v3.0** – Elektriksel parametreleri ölçen enerji modülü
- 🐍 **Python 3** – Sensör okuma, MQTT mesajlaşma, veri işleme
- 💾 **InfluxDB** – Hafif ve hızlı zaman serisi veritabanı
- 📊 **Grafana** – Gerçek zamanlı panellerle izleme arayüzü
- 📡 **MQTT (Paho MQTT + Mosquitto Broker)** – Yerel haberleşme protokolü
- ☁️ **AWS IoT Core** – MQTT üzerinden bulut tabanlı veri gönderimi ve işlenmesi
- 🛡️ **AWS Sertifikaları (.pem/.key)** – Güvenli MQTT bağlantısı için kimlik doğrulama
- 🖼️ **Graphviz** / mimari diyagramlar – Sistem akışını açıklayan şema

---

## 🧩 Sistem Mimarisi

Aşağıdaki görsel, veri akışını sensörlerden buluta kadar olan tüm süreciyle gösterir:

📷 `bulutbilişim-proje.jpeg` dosyasına göz atabilirsiniz.

---

## 📂 Dosya ve Klasör Açıklamaları

| Dosya/Klasör           | Açıklama                                                                 |
|------------------------|--------------------------------------------------------------------------|
| `example2.py`          | DHT11'den sıcaklık ve nem verisi alır, verileri InfluxDB ve AWS MQTT ile iletir. |
| `okuyucu.py`           | PZEM-004T modülünden elektriksel verileri (akım, voltaj vb.) alır ve gönderir.   |
| `requirements.txt`     | Proje için gerekli olan tüm Python bağımlılıklarını içerir.              |
| `bulutbilişim-proje.jpeg` | Mimari tasarımı içeren sistem şeması.                                      |
| `/certs/`              | AWS IoT Core için gerekli olan güvenlik sertifikalarının saklandığı dizin.   |

---

## ⚙️ Kurulum Adımları

1. Python bağımlılıklarını yükleyin:
   ```bash
   pip install -r requirements.txt
