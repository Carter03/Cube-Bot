// BluetoothComms.h
#pragma once
#include <Arduino.h>
#include "BluetoothSerial.h"
#include <stdint.h>

class BluetoothComms {
public:
  void begin(const char *name);
  bool isConnected();
  void sendImage(uint8_t *buf, size_t len);
  void sendDelimiter();
  bool hasSolution();
  String getSolution();
private:
  BluetoothSerial bt_;
  String solution_;
};
