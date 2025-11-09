// MotorController.h
#pragma once
#include <Arduino.h>

class MotorController {
    inline static const int NUM_SCAN_POSITIONS = 10;
public:
  void begin();
  void rotateToScanPosition(int pos_idx);
  void returnToStart();
  void loadSolution(const String& moves);
  void executeSolution();
private:
  void stepMotor(int motor, int steps, bool dir);
};
