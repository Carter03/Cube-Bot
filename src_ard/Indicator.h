// Indicator.h
#pragma once
#include <Arduino.h>
class Indicator {
public:
  Indicator(int pin): _pin(pin) {}
  void begin() {}//{ pinMode(_pin, OUTPUT); }
  void on() {}//{ digitalWrite(_pin, HIGH); }
  void off() {}//{ digitalWrite(_pin, LOW); }
  void blinkThrice() {}
  void blinkSlow() {}
  void blinkFast() {}
private:
  int _pin;
};
