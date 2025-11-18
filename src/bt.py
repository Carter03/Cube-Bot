import serial
import struct

class SerialReceiver:
    def __init__(self, port, baud, img_path):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud, timeout=10)
        self.img_path = img_path
    
    def receive_imgs(self):
        i = 0

        while True:
            header = self.ser.read(3)
            if header == b"IMG" or header == b"CFG":
                length_bytes = self.ser.read(4)
                if len(length_bytes) < 4:
                    print("Incomplete length header")
                    break
                img_len = struct.unpack('<I', length_bytes)[0]
                img_data = self.ser.read(img_len)
                if len(img_data) != img_len:
                    print("Image incomplete")
                    break

                filename = f"{self.img_path}/{str(header)}_{i}.jpg"
                with open(filename, "wb") as f:
                    f.write(img_data)
                i += 1
            elif header == b"END":
                break

    def transmit_start(self):
        self.ser.write(b"main\x00")

    def transmit_config(self):
        self.ser.write(b"config\x00")

    def transmit_soln(self, soln):
        self.ser.write(soln.encode())
