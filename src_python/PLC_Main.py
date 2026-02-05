from PLC_Proxy import PLCProxy
import time
import os

def run_system_test():
    """
    PLC ile Python arasındaki senaryo tabanlı haberleşme testi.
    """
    # PLC Yapılandırma dosyasının yolu (Symbol Configuration sonucu oluşan XML)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    XML_FILE = os.path.join(BASE_DIR, "..", "src_plc", "PLC_PY_comm.Device.Application.xml")
        
    # PLC'ye bağlan (Varsayılan port 5000)
    plc = PLCProxy("127.0.0.1", 5000, XML_FILE)
    
    print("=== PLC Endüstriyel Haberleşme Testi Başladı ===")
    
    try:
        # Adım 1: PLC'ye Komut Gönderme 
        print("\n[Command] Hız setpoint değerleri gönderiliyor...")
        plc.Hiz_Setpoint1 = 45
        plc.Hiz_Setpoint2 = 65
        
        # PLC'nin tarama çevrimi için kısa bir bekleme
        time.sleep(0.5) 
        
        # Adım 2: PLC Kararlarını Okuma [cite: 2]
        print(f"[Feedback] Toplam Hesaplanan: {plc.Sonuc}")
        print(f"[Feedback] Motor Çalışma İzni: {'AKTİF' if plc.Motor_Run else 'PASİF'}")
        
        # Adım 3: Gerçek Zamanlı Veri İzleme (Sıcaklık) [cite: 2]
        print("\n[Monitor] 5 Saniye Boyunca Sıcaklık İzleniyor...")
        for _ in range(5):
            print(f">>> Anlık Sistem Sıcaklığı: {plc.Sicaklik:.2f} °C")
            time.sleep(1)
            
    except Exception as e:
        print(f"[Error] Haberleşme Hatası: {e}")
    finally:
        print("\n=== Test Tamamlandı ===")

if __name__ == "__main__":
    run_system_test()