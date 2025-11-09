// Button.h
#pragma once
#include <Arduino.h>
// class Button {
// public:
//   Button(int pin): _pin(pin) {}
//   void begin() { pinMode(_pin, INPUT_PULLUP); }
//   bool pressed() {
//     static bool last = HIGH;
//     bool now = digitalRead(_pin);
//     if (last == HIGH && now == LOW) {
//       delay(30);
//       last = now;
//       return true;
//     }
//     last = now;
//     return false;
//   }
// private:
//   int _pin;
// };

class Button {
    unsigned long stime;
public:
    Button(int pin) { stime = millis(); }
    void begin() {}
    bool pressed() { return millis() - stime > 5000}
    
}
