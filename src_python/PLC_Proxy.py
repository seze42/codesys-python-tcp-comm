import socket
import xml.etree.ElementTree as ET
# import time

class PLCProxy:
    def __init__(self, ip, port, xml_path, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug
        self.vars = {}
        self.sock = None
        self._parse_xml(xml_path)
        self._connect()

    def _parse_xml(self, path):
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            ns = {'ns': 'http://www.3s-software.com/schemas/Symbolconfiguration.xsd'}
            # XML Yapısını tara
            for struct in root.findall(".//ns:TypeUserDef[@iecname='ST_Data']", ns):
                for elem in struct.findall("ns:UserDefElement", ns):
                    name = elem.get('iecname')
                    t_name = elem.get('type')
                    self.vars[name] = {
                        'offset': int(elem.get('byteoffset')),
                        'type': t_name,
                        'size': {'T_BOOL':1, 'T_INT':2, 'T_REAL':4, 'T_DINT':4}.get(t_name, 0)
                    }
            if self.debug: print(f"DEBUG: {len(self.vars)} değişken yüklendi.")
        except Exception as e:
            print(f"XML Hatası: {e}")

    def _connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(1.0) # 1 saniye timeout
            self.sock.connect((self.ip, self.port))
        except Exception as e:
            print(f"Bağlantı Hatası: {e}")

    def _exchange(self, msg):
        """PLC ile veri alışverişi yapan temel fonksiyon"""
        try:
            self.sock.sendall(msg.encode())
            data = self.sock.recv(1024).decode().strip()
            if self.debug: print(f"DEBUG: Giden {msg} -> Gelen {data}")
            return data
        except Exception as e:
            if self.debug: print(f"Haberleşme Hatası: {e}")
            return None

    def read(self, name):
            v = self.vars.get(name)
            if not v: return None
            
            # 3 kere deneme mekanizması (Haberleşme anlık koparsa diye)
            for _ in range(3):
                res = self._exchange(f"<R:{v['offset']}:{v['size']}>")
                if res and res != "None":
                    try:
                        if v['type'] == 'T_INT': return int(res)
                        if v['type'] == 'T_REAL': return float(res.replace(',', '.'))
                        if v['type'] == 'T_BOOL': return res.upper() == 'TRUE'
                        return res
                    except ValueError:
                        continue
                
            return None # Hala veri yoksa None dön

    def write(self, name, value):
        v = self.vars.get(name)
        if not v: return False
        val_str = "TRUE" if (isinstance(value, bool) and value) else ("FALSE" if isinstance(value, bool) else str(value))
        return self._exchange(f"<W:{v['offset']}:{v['size']}={val_str}>") == "OK"

    def __getattr__(self, name):
        if name in self.vars: return self.read(name)
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in ["ip", "port", "vars", "sock", "debug"]:
            super().__setattr__(name, value)
        elif hasattr(self, 'vars') and name in self.vars:
            self.write(name, value)
        else:
            super().__setattr__(name, value)

# ==========================================
# TEST SENARYOSU
# ==========================================
# if __name__ == "__main__":
#     # XML dosyanın yolu (Aynı klasörde olduğunu varsayıyoruz)
#     XML_FILE = r"C:\\Users\\Semih\\Documents\\PLC_PY_comm.Device.Application.xml"
    
#     plc = PLCProxy("127.0.0.1", 5000, XML_FILE)

#     print("\n--- Otomatik Değişken Erişim Testi ---")
#     # 1. Yazma Testi
#     print("Değerler yazılıyor...")
#     plc.Hiz_Setpoint = 200
#     plc.Motor_Run = False
#     plc.Sicaklik = 30.0
    
#     time.sleep(0.5) # PLC'nin işlemesi için kısa bir süre
    
#     # 2. Okuma Testi (Yazılanlar doğru gitmiş mi?)
#     print(f"Yeni Hız: {plc.Hiz_Setpoint}")
#     print(f"Yeni Motor Durumu: {plc.Motor_Run}")
#     print(f"Yeni Sıcaklık: {plc.Sicaklik}")
    


#     # Olmayan bir değişken testi
#     # print(plc.OlmayanDegisken)