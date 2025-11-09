// CameraModule.h
#pragma once
#include <Arduino.h>
#include "BluetoothSerial.h"

using IMG = camera_fb_t;

class CameraModule {
public:
  void begin();
  IMG* captureImage();
  void returnMemory(IMG *img);
};
