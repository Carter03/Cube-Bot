
# Cube-Bot

![Project Status](https://img.shields.io/badge/Status-Work%20In%20Progress-yellow)

This repository contains the code, design files, and documentation for a 3D-printed, automated Rubik's Cube solving robot.

The goal is to build a machine that takes a scrambled 3x3 Rubik's Cube and solves it quickly. The core logic is split between an ESP32-CAM for hardware control and image capture and a PC or remote server for image processing and algorithm solving.

---

## Core Components

* **Microcontroller:** ESP32-CAM
* **Actuators:** 5x Stepper Motors
* **Frame:** Custom 3D-Printed Parts
* **Computer Vision:** Onboard camera of the ESP32-CAM
* **Communication:** Bluetooth for data transfer between the ESP32 and a PC
* **Solving Brain:** A PC-side application (Python, C++)

---

## How It Works

The solving process follows a clear, step-by-step workflow:

1.  **Scanning Phase:** The robot holds the cube, and the ESP32-CAM captures images of faces from each side. The robot performs specific turns to reveal all six sides to the top-mounted camera without moving the camera itself.
2.  **Data Transmission:** The captured image data is sent to a paired PC over a Bluetooth connection.
3.  **State Detection:** A PC application processes the images to recognize the color and position of each sticker, building a digital data structure of the cube's current state.¹
4.  **Solution Calculation:** Using an algorithm (e.g., Kociemba's two-phase, or perhaps something custom), the PC application calculates a reasonable series moves to solve the cube.
5.  **Command Transmission:** The calculated move sequence is transmitted back to the ESP32-CAM via Bluetooth.
6.  **Execution Phase:** The ESP32 interprets the commands and precisely controls the five stepper motors to execute the turns, solving the Rubik's Cube.

¹The most popular human solving method (and the one I use) is called CFOP. It generally takes ~60 turns to solve the cube, taking advanced speedcubers <10 s. However, a solution always exists that takes 20 turns or fewer. Both schemes may be implemented in this project. 

---

## Current Status & To-Do

This project has just begun. The immediate focus is on developing the foundational components.

### To-Do List:
* [ ] Finalize the 3D models for the frame and motor mounts.
* [ ] Establish a stable Bluetooth communication link between the ESP32 and PC.
* [ ] Develop the initial ESP32 firmware for capturing and relaying images.
* [ ] Create the basic PC- or server-side script for receiving data.
* [ ] Write and test the stepper motor control logic.
