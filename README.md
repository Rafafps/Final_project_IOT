# AQUA_SENSE - IoT System for Water Resource Monitoring

## Overview

AQUA_SENSE is an IoT system designed to monitor water resources and provide early flood detection capabilities. The project addresses the growing need for automated water monitoring in urban and rural areas, where sudden water level changes can pose significant risks.

**Application Scenario**: Smart City / Environmental Monitoring  
**Focus**: Real-time flood detection and emergency response automation

## Problem Statement

Traditional water monitoring systems often rely on manual inspections or expensive hardware installations. AQUA_SENSE demonstrates how IoT technologies can provide cost-effective, automated monitoring with real-time alerting capabilities. The system simulates a network of sensors deployed in flood-prone areas, continuously monitoring water levels and rainfall patterns.

## System Architecture

### Architecture Pattern: Three-Tier Architecture with Event-Driven Communication

The system follows a **three-tier architecture** pattern, which provides clear separation of concerns and scalability:

**Tier 1 - Presentation/Application Layer:**
- Web dashboard (`dashboard/index.html`) for user interaction and visualization
- REST API (`api_server.py`) for programmatic access
- Responsible for: data presentation, user interface, external system integration

**Tier 2 - Business Logic/Processing Layer:**
- Data Manager service (rules engine, MQTT client, device registry)
- Responsible for: data processing, business rules evaluation, event handling, device management
- Acts as the central orchestrator between presentation and data layers

**Tier 3 - Data Layer:**
- SQLite database (`storage.py`) for persistent data storage
- IoT devices (sensors and actuators) as data sources and action executors
- Responsible for: data persistence, telemetry generation, command execution

### Event-Driven Communication

While the overall structure is three-tier, **communication between tiers uses an event-driven model**:
- IoT devices generate data asynchronously and continuously (event producers)
- MQTT broker acts as message hub (pub/sub pattern)
- Manager processes events reactively (event consumer)
- System reacts to events (high water levels) in real-time without polling
- This hybrid approach combines layered architecture benefits with event-driven responsiveness

### Component Responsibilities

**IoT Devices (Emulated)**:
- `water_sensor.py`: Measures water level in cm, publishes every 10s
- `rain_sensor.py`: Measures rainfall in mm, publishes every 10s  
- `emergency_light.py`: Actuator that receives ON/OFF commands
- `notification_hub.py`: Receives and displays alert notifications

**Data Collector & Manager**:
- `mqtt_client.py`: Subscribes to telemetry, processes incoming data
- `rules.py`: Evaluates business rules (thresholds), triggers alerts/commands
- `storage.py`: Persists telemetry and alerts in SQLite
- `device_registry.py`: Maintains device metadata and last-known state
- `api_server.py`: Exposes REST API for external access

**Applications**:
- `dashboard/index.html`: Web dashboard for real-time monitoring
- REST API endpoints for programmatic access

## Technical Decisions

### Why MQTT?
- **Lightweight**: Perfect for resource-constrained IoT devices
- **Pub/Sub model**: Natural fit for one-to-many communication (one sensor, multiple subscribers)
- **QoS levels**: Ensures message delivery reliability
- **Topic-based routing**: Flexible message routing without tight coupling

### Why FastAPI?
- **Performance**: High throughput for REST endpoints
- **Auto-documentation**: Built-in Swagger UI (`/docs`)
- **Type safety**: Pydantic models for request/response validation
- **Async support**: Can handle concurrent requests efficiently

### Why SQLite?
- **Simplicity**: No external database server needed
- **Sufficient for demo**: Handles moderate data volumes
- **Portable**: Database file can be easily backed up/moved
- **Note**: In production, would migrate to PostgreSQL or TimescaleDB for better scalability

## Features
- Real-time water level and rainfall monitoring
- Automated flood detection with configurable thresholds
- Emergency light activation on flood risk detection
- Alert notification system
- REST API for integration with external systems
- Web dashboard for visualization

## Data Flows

### Telemetry Flow (Device → Manager)
1. Sensors publish measurements to `telemetry/{device_type}/{device_id}` topics
2. Manager's MQTT client subscribes to `telemetry/+/+` pattern
3. Incoming telemetry is stored in SQLite database
4. Device registry is updated with latest state

### Command Flow (Manager → Device)
1. Rules engine evaluates telemetry against thresholds
2. When threshold exceeded, command published to `commands/{device_type}/{device_id}`
3. Actuator devices subscribe to their command topics
4. Device executes action (e.g., emergency light turns ON)

### Query Flow (App → Manager)
1. Dashboard/Apps make HTTP requests to REST API
2. API queries storage layer for telemetry/alerts
3. JSON response returned to client
4. Dashboard updates UI with latest data

### Closed Loop Example
```
Water Sensor (350cm) → Manager receives telemetry → 
Rule evaluates: water_level >= 350 → 
Command published to emergency_light → 
Light turns ON → Alert sent to notification_hub
```

## Project Structure
```
Final_project_IOT/
├── dashboard/                   # Tier 1: Presentation Layer
│   ├── index.html
│   └── start_dashboard.py
├── devices/                     # Tier 3: IoT Devices (emulated)
│   ├── rain_sensor.py
│   ├── water_sensor.py
│   ├── emergency_light.py
│   └── notification_hub.py
├── docker
├── docs
├── logs
├── manager/                     # Data Collector & Manager
│   ├── api_server.py
|   ├── aqua_sense.db   
|   ├── device_registry.py
|   ├── main.py        
│   ├── mqtt_client.py          
│   ├── rules.py                
│   ├── storage.py              
├── presentation
├── .gitignore
├── README.md
├── requirements.txt
└── README.md
```

## Quick Start

### Option 1: Docker Compose (Recommended)

The easiest way to run the entire system:

```bash
cd docker
docker-compose up -d
```

This starts:
- Mosquitto MQTT broker (port 1883)
- Manager service with REST API (port 7070)

Then start devices manually:
```bash
python devices/rain_sensor.py
python devices/water_sensor.py
python devices/emergency_light.py
python devices/notification_hub.py
```

### Option 2: Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MQTT broker:**
   ```bash
   mosquitto -p 1883 -v
   # Or use Docker: docker run -p 1883:1883 eclipse-mosquitto:2.0
   ```

3. **Start the Manager (REST API):**
   ```bash
   uvicorn manager.api_server:app --host 0.0.0.0 --port 7070
   ```

4. **Start IoT devices** (in separate terminals):
   ```bash
   python devices/rain_sensor.py
   python devices/water_sensor.py
   python devices/emergency_light.py
   python devices/notification_hub.py
   ```

5. **Access the system:**
   - REST API Swagger: http://localhost:7070/docs
   - Dashboard: Open `dashboard/index.html` in your browser

## Testing the System

### Verify Closed Loop Behavior

1. **Monitor MQTT messages:**
   ```bash
   mosquitto_sub -t "#" -v
   ```

2. **Trigger flood alert:**
   - Wait for water sensor to publish a value >= 350cm, OR
   - Manually send command via API:
   ```bash
   curl -X POST http://localhost:7070/commands \
     -H "Content-Type: application/json" \
     -d '{"topic": "commands/emergency_light/emergency-light-01", "payload": {"action": "ON", "reason": "test"}}'
   ```

3. **Check alerts:**
   ```bash
   curl http://localhost:7070/alerts
   ```

4. **View devices:**
   ```bash
   curl http://localhost:7070/devices
   ```

See [`docs/guides/COMPLETE_TEST_COMMANDS.md`](docs/guides/COMPLETE_TEST_COMMANDS.md) for comprehensive testing instructions.

## Configuration

### Device Configuration
Each device can be configured via `config.ini` files (optional). Default values work out of the box:
- MQTT broker: `localhost:1883`
- Publishing interval: 10 seconds
- Device IDs: `water-01`, `rain-01`, `emergency-light-01`, `notification-hub-01`

### Rule Thresholds
Configured in `manager/rules.py`:
- Water level threshold: 350cm (triggers flood alert)
- Rain threshold: 80mm (triggers heavy rain alert)

## Dependencies

- `paho-mqtt`: MQTT client library for Python
- `fastapi`: Modern web framework for REST API
- `uvicorn`: ASGI server for FastAPI

## Challenges & Solutions

### Challenge 1: Ensuring Message Delivery
**Problem**: IoT devices might miss commands if they're not subscribed when message is published.  
**Solution**: Used MQTT QoS level 1 for critical commands, ensuring at-least-once delivery.

### Challenge 2: Thread Safety
**Problem**: Multiple threads accessing shared state (device registry, storage).  
**Solution**: Implemented thread locks in `DeviceRegistry` and `Storage` classes.

### Challenge 3: Real-time Dashboard Updates
**Problem**: Dashboard needs to show latest data without manual refresh.  
**Solution**: Implemented auto-refresh every 5 seconds with JavaScript `setInterval`.

## Architecture Diagrams

See `docs/diagrams/` for:
- Class Diagram: Component relationships
- Data Flow Sequence Diagram: Senquece flows of commands related to the devices
- Decision Flow: Rule evaluation logic

## Author

**Rafaella Pinheiro**  
Project developed for the Distributed and IoT Software Architectures course.
Score of the project: 30/30

---

## License

This project is developed for academic purposes as part of the Distributed and IoT Software Architectures course.
