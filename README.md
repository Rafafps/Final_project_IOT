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

## Architecture

### Component Diagram

```mermaid
graph TB
    subgraph "IoT Devices Layer"
        RS[Rain Sensor<br/>rain-01]
        WS[Water Sensor<br/>water-01]
        EL[Emergency Light<br/>emergency-light-01]
        NH[Notification Hub<br/>notification-hub-01]
    end
    
    subgraph "Communication Layer"
        MQTT[MQTT Broker<br/>Mosquitto :1883]
    end
    
    subgraph "Data Collector & Manager"
        MQTT_CLIENT[MQTT Client<br/>Subscriber]
        RULES[Rules Engine<br/>Threshold Logic]
        STORAGE[Storage<br/>SQLite]
        REGISTRY[Device Registry<br/>Metadata]
        API[REST API<br/>FastAPI :7070]
    end
    
    subgraph "Apps & Observers"
        SWAGGER[Swagger UI<br/>/docs]
        CLI[cURL/CLI]
    end
    
    RS -->|telemetry/rain/rain-01| MQTT
    WS -->|telemetry/water/water-01| MQTT
    EL -->|telemetry/emergency_light/+| MQTT
    
    MQTT -->|Subscribe telemetry/+/+| MQTT_CLIENT
    MQTT_CLIENT --> STORAGE
    MQTT_CLIENT --> REGISTRY
    MQTT_CLIENT --> RULES
    
    RULES -->|commands/emergency_light/+| MQTT
    RULES -->|alerts/notification| MQTT
    
    MQTT -->|commands/emergency_light/+| EL
    MQTT -->|alerts/notification| NH
    
    API --> STORAGE
    API --> REGISTRY
    API --> MQTT_CLIENT
    
    SWAGGER --> API
    CLI --> API
```

### Sequence Diagram - Closed Loop

```mermaid
sequenceDiagram
    participant WS as Water Sensor
    participant MQTT as MQTT Broker
    participant MC as MQTT Client
    participant ST as Storage
    participant RE as Rules Engine
    participant EL as Emergency Light
    
    Note over WS,EL: Closed Loop: Water Level Threshold
    
    WS->>MQTT: Publish telemetry<br/>topic: telemetry/water/water-01<br/>payload: {water_level_cm: 380}
    
    MQTT->>MC: Message received
    MC->>ST: save_telemetry(device_id, payload)
    MC->>RE: evaluate(payload)
    
    alt water_level >= 350 cm
        RE->>ST: save_alert(FLOOD_RISK)
        RE->>MQTT: Publish command<br/>topic: commands/emergency_light/water-01<br/>payload: {action: "ON", reason: "flood_risk"}
        MQTT->>EL: Command received
        EL->>EL: Execute action: ON
        Note over EL: Emergency Light Activated!
    end
```

> **Note:** For complete architecture diagrams, see [`docs/architecture_diagrams.md`](docs/architecture_diagrams.md)

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
├── manager/
│   ├── api_server.py   # FastAPI app (uvicorn entrypoint)
│   ├── main.py         # Backward-compatible entrypoint
│   ├── mqtt_client.py  # MQTT bridge + rules engine hook
│   ├── rules.py        # Threshold-based rules
│   ├── storage.py      # SQLite persistence
│   └── device_registry.py
└── mosquitto/ (config and state if using local broker)
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

## Usage (local)
- Start a MQTT broker (e.g. mosquitto on localhost:1883).
- Run sensors and actuators in separate terminals (they have safe defaults):
  ```bash
  python devices/rain_sensor.py
  python devices/water_sensor.py
  python devices/emergency_light.py
  python devices/notification_hub.py
  ```
- Start the REST API:
  ```bash
  uvicorn manager.api_server:app --host 0.0.0.0 --port 7070
  ```
- Access Swagger docs: `http://localhost:7070/docs`

## Docker (API only)
```
docker build -t aqua_sense .
docker run -p 7070:7070 --network=host aqua_sense
```
Ensure a MQTT broker is reachable at the configured host (default `localhost:1883`).

## Dependencies
- paho-mqtt
- fastapi + uvicorn

## Notes
- The system uses MQTT topics for communication between sensors, actuators, and the manager.
- Business rules and alerts are configurable in the `manager/rules.py` module.
- Storage is simple and can be expanded to more robust databases.
- Closed loop: water level above threshold triggers command to `commands/emergency_light/<deviceId>` and alert published to notification hub (`alerts/#`).

## Author
Rafaella Pinheiro

---
Project developed for the Distributed and IoT Architectures course.
