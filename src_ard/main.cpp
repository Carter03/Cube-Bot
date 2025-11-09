#include "CameraModule.h"
#include "MotorController.h"
#include "BluetoothComms.h"
#include "Indicator.h"
#include "Button.h"

enum SystemState {
  DISCONNECTED,
  IDLE,
  SCANNING,
  WAITING_FOR_SOLUTION,
  READY_TO_SOLVE,
  SOLVING,
  EXIT
};

SystemState state = DISCONNECTED;

CameraModule camera;
MotorController motors;
BluetoothComms comms;
Indicator led(2); // e.g., GPIO2
Button button(4); // e.g., GPIO4

void setup() {
  Serial.begin(115200);
  led.begin();
  camera.begin();
  comms.begin("CUBE-BOT-ESP32");
//   motors.begin();
  button.begin();

  led.on();
  Serial.println("Cube Solver Ready.");
}

void loop() {
  switch (state) {
    case DISCONNECTED:
        if (comms.isConnected()) {
            Serial.println("COMMS CONNECTED. GOING TO IDLE");
            led.blinkThrice();
            state = IDLE;
        }
        break;

    case IDLE:
      if (button.pressed()) {
        Serial.println("BUTTON PRESSED. GOING TO SCANNING");
        led.blinkSlow();
        state = SCANNING;
      }
      break;

    case SCANNING:
      for (int i {}; i < motors.NUM_SCAN_POSITIONS; ++i) {
        Serial.println("CAPTURING.");
        // motors.rotateToScanPosition(i);
        IMG *frame = camera.captureImage();
        comms.sendImage(frame->buf, frame->len);
        camera.returnMemory(frame);
      }
      motors.returnToStart();
      comms.sendDelimiter();
      state = WAITING_FOR_SOLUTION;
      led.blinkFast();
      Serial.println("DELIMITER SENT. GOING TO WAITING.");
      break;

    case WAITING_FOR_SOLUTION:
      if (comms.hasSolution()) {
        Serial.println("RECEIVED SOLUTION. GOING TO READY");
        // motors.loadSolution(comms.getSolution());
        Serial.println(comms.getSolution());
        led.on();
        state = READY_TO_SOLVE;
      }
      break;

    case READY_TO_SOLVE:
      if (button.pressed()) {
        Serial.println("BUTTON PRESSED. GOING TO SOLVING");
        state = SOLVING;
        led.blinkFast();
      }
      break;

    case SOLVING:
      Serial.println("EXECUTING SOLN. RETURNING TO IDLE.");
    //   motors.executeSolution();
      led.on();
      state = EXIT;
      break;
    case default:
      return;
  }

  delay(10);
}
