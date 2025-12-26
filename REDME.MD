# AQUA_SENSE - IoT System for Water Resource Monitoring

## Description
AQUA_SENSE is a distributed IoT-based system for monitoring and managing water resources, focusing on flood detection and emergency alerts. The system simulates sensors and actuators connected via MQTT and exposes a REST API for integration with external systems.

## Features
- Emulation of rain and water level sensors
- Emulation of actuators: emergency light and notification hub
- MQTT communication for telemetry and commands
- REST API (FastAPI) for querying data, devices, rules, and alerts
- Simple storage (memory or SQLite) for data and alert history
- Configurable rules for triggering alerts and commands

## Project Structure
```
Final_project_IOT/
├── Dockerfile
├── requirements.txt
├── REDME.MD
├── devices/
│   ├── rain_sensor.py
│   ├── water_sensor.py
│   ├── emergency_light.py
│   └── notification_hub.py
└── manager/
    ├── main.py
    ├── mqtt_client.py
    ├── rules.py
    ├── storage.py
    └── device_registry.py
```

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Final_project_IOT
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or use Docker:
   ```bash
   docker build -t aqua_sense .
   docker run -p 7070:7070 aqua_sense
   ```

## Usage
- Run sensors and actuators in separate terminals:
  ```bash
  python devices/rain_sensor.py
  python devices/water_sensor.py
  python devices/emergency_light.py
  python devices/notification_hub.py
  ```
- Start the REST API:
  ```bash
  python manager/main.py
  ```
- Access the Swagger documentation at: `http://localhost:7070/docs`

## Dependencies
- paho-mqtt
- flask
- numpy
- pandas

## Notes
- The system uses MQTT topics for communication between sensors, actuators, and the manager.
- Business rules and alerts are configurable in the `manager/rules.py` module.
- Storage is simple and can be expanded to more robust databases.

## Author
Rafaella Pinheiro

---
Project developed for the Distributed and IoT Architectures course.
