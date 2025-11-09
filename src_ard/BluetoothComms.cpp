#include "BluetoothComms.h"
#include "BluetoothSerial.h"

class BluetoothComms {
public:
  void begin(const char* name);
  bool hasSolution();
  String getSolution();
private:
  BluetoothSerial bt_;
  String solution_;
};

void BluetoothComms::begin(const char* name) {
    bt_.begin(name);
}

bool BluetoothComms::isConnected() {
    return bt_.hasClient();
}

void BluetoothComms::sendImage(uint8_t *buf, size_t len) {
    bt_.print("IMG");
    bt_.write((uint8_t *)&len, sizeof(len));
    bt_.write(buf, len);
}

void BluetoothComms::sendDelimeter() {
    bt_.print("END");
}

