# Health Monitoring and Alert System

## Table of Contents
- [Introduction](#introduction)
- [Technical Overview](#technical-overview)
  - [Components](#components)
  - [Communication](#communication)
  - [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
  - [MicroPython and Thonny](#micropython-and-thonny)
  - [Blynk Dashboard Setup](#blynk-dashboard-setup)
  - [Project Deployment](#project-deployment)
- [Usage](#usage)

## Introduction
The Health Monitoring and Alert System is an IoT solution designed for continuous vital signs monitoring and real-time alerts in healthcare settings. It incorporates sensors like the MAX30100 and load cell to measure parameters such as heart rate, blood oxygen saturation (SpO2), weight (for IV bag monitoring), and utilizes a display, buzzer, and button for user interaction. Despite the critical need, dedicated IV bag monitoring solutions are lacking, posing risks to patient safety.

## Technical Overview

### Components:
- **Microcontroller:** ESP32/ESP8266 for processing and connectivity, programmed using MicroPython.
- **Sensors:** MAX30100 (Heart Rate and SpO2), Load Cell (Weight).
- **Display:** SH1106 for data visualization.
- **Alerting:** Buzzer for real-time alerts.
- **Interaction:** Button for user input.

### Communication:
- Utilizes Blynk 2.0 for web and app interfaces.
- Sensor data processed and transmitted to Blynk cloud.
- Real-time alerts triggered based on thresholds.

### Architecture:
- Modular design for easy integration and scalability.
- Sensor data collected, processed, and transmitted seamlessly.
- Scalable to accommodate multiple sensor nodes and users.

## Setup Instructions

### MicroPython and Thonny:
1. Install MicroPython firmware on ESP32/ESP8266 microcontroller.
2. Use Thonny IDE for MicroPython code development and deployment.

### Blynk Dashboard Setup:
1. Sign up or log in to the Blynk 2.0 platform.
2. Create a new project and obtain the authentication token.
3. Configure widgets in the Blynk app or web interface for data visualization and alert settings.

### Project Deployment:

1. **Cloning the Repository:**
   - Clone the repository to your local machine:
     ```
     git clone https://github.com/HacksterAman/IoT-Enabled-Health-Monitoring-and-Alert-System.git
     ```

2. **WiFi Credentials and Blynk Authentication Token:**
   - Open the "main.py" file in your preferred code editor.
   - Replace the placeholders with your WiFi credentials and Blynk authentication token.
   - Save the changes to the "main.py" file.

3. **Upload Code to Microcontroller:**
   - Use Thonny IDE to open and upload the MicroPython code to the ESP32/ESP8266 microcontroller.

## Usage
- Ensure proper deployment and connectivity of sensor nodes within the network.
- Access the Blynk web or app interface to monitor real-time data and customize alert thresholds.
- Respond promptly to notifications received through the Blynk app, and take appropriate action as necessary.
