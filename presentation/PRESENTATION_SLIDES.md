# 🎤 Presentation Slides - AQUA_SENSE

**Project:** AQUA_SENSE - IoT System for Water Resource Monitoring  
**Course:** Distributed and Internet of Things Software Architectures  
**Participant:** Rafaella Pinheiro  
**Date:** [Fill in]

---

## Slide 1: Title and Introduction

# AQUA_SENSE
## IoT System for Water Resource Monitoring

**Project developed for:**  
Distributed and Internet of Things Software Architectures

**Participant:**  
Rafaella Pinheiro

---

## Slide 2: Application Scenario

# Scenario: Flood Monitoring

**Problem:**
- Water resource monitoring in urban areas
- Early detection of flood risks
- Automatic alerts for public safety

**AQUA_SENSE Solution:**
- Distributed IoT system for real-time monitoring
- Rain and water level sensors
- Actuators for alerts and emergency signaling
- Automatic analysis with configurable rules

---

## Slide 3: IoT Devices

# Emulated Devices

## Sensors (Telemetry)
- **Rain Sensor** (`rain-01`)
  - Measures precipitation in mm
  - Publishes every 10 seconds
  
- **Water Sensor** (`water-01`)
  - Measures water level in cm
  - Publishes every 10 seconds

## Actuators (Commands)
- **Emergency Light** (`emergency-light-01`)
  - Receives commands to turn on/off
  - Emergency signaling
  
- **Notification Hub** (`notification-hub-01`)
  - Receives system alerts
  - Simulates sending notifications (SMS/Email/App)

---

## Slide 4: System Architecture

# Component Architecture

```
┌─────────────┐     ┌─────────────┐
│ Rain Sensor │     │Water Sensor │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └─────────┬─────────┘
                 │ MQTT
         ┌───────▼───────┐
         │ MQTT Broker  │
         └───────┬───────┘
                 │
    ┌────────────┼────────────┐
    │                          │
┌───▼──────────┐      ┌───────▼──────┐
│   Manager    │      │  Emergency   │
│              │      │    Light     │
│ - MQTT Client│      └──────────────┘
│ - Rules      │
│ - Storage    │      ┌──────────────┐
│ - REST API   │      │Notification  │
└───┬──────────┘      │    Hub       │
    │                  └──────────────┘
    │ REST API
┌───▼──────────┐
│ Swagger UI   │
│ Apps/CLI     │
└──────────────┘
```

**Architectural Pattern:** Event-Driven Architecture with Message Broker

---

## Slide 5: Closed Loop (Main Flow)

# Closed Loop: Telemetry → Rule → Command

## Example: High Water Level Detection

```
1. Water Sensor detects level >= 350 cm
   ↓
2. Publishes telemetry via MQTT
   ↓
3. Manager receives and stores
   ↓
4. Rules Engine evaluates threshold
   ↓
5. Generates automatic command
   ↓
6. Publishes command to Emergency Light
   ↓
7. Emergency Light executes action (ON)
```

**Result:** System reacts automatically without human intervention

---

## Slide 6: Protocols and Technologies

# Technical Choices

## Communication Protocols

**MQTT (Message Queuing Telemetry Transport)**
- Pub/Sub for telemetry and commands
- QoS 1 for delivery guarantee
- Hierarchical topics: `telemetry/+/+`, `commands/+`

**REST API (HTTP)**
- FastAPI framework
- Automatic Swagger UI
- Endpoints: `/devices`, `/telemetry`, `/alerts`, `/commands`

## Technologies

- **Python 3.9+** - Main language
- **FastAPI** - REST API framework
- **SQLite** - Data persistence
- **Mosquitto** - MQTT Broker
- **Docker** - Containerization

---

## Slide 7: Data Structure

# Data Format (JSON)

## Telemetry
```json
{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "timestamp": "2024-01-08T10:30:00Z",
  "water_level_cm": 380
}
```

## Commands
```json
{
  "action": "ON",
  "reason": "flood_risk"
}
```

## MQTT Topics
- `telemetry/rain/rain-01`
- `telemetry/water/water-01`
- `commands/emergency_light/+`
- `alerts/notification`

---

## Slide 8: Business Rules

# Rules Engine

## Implemented Rules

**Rule 1: Flood Risk**
- **Condition:** `water_level_cm >= 350`
- **Action:** Turn on Emergency Light
- **Topic:** `commands/emergency_light/{deviceId}`

**Rule 2: Heavy Rain**
- **Condition:** `rain_mm >= 80`
- **Action:** Send alert to Notification Hub
- **Topic:** `alerts/notification`

**Characteristics:**
- Automatic real-time evaluation
- Alert persistence in history
- Configurable thresholds in code

---

## Slide 9: Demonstration

# System Demo

## Test Scenario

1. **Start components:**
   - MQTT Broker (Mosquitto)
   - Manager (REST API)
   - IoT Devices

2. **Observe telemetry:**
   - Access Swagger UI: `http://localhost:7070/docs`
   - Query `/telemetry` and `/devices`

3. **Trigger rule:**
   - Water Sensor publishes value >= 350 cm
   - Emergency Light receives command automatically

4. **Verify history:**
   - Query `/alerts` to see generated alerts

**Result:** System working end-to-end with closed loop

---

## Slide 10: Conclusions

# Conclusions and Results

## Achieved Objectives ✅

- ✅ Functional distributed IoT system
- ✅ 4 emulated devices (2 sensors + 2 actuators)
- ✅ Complete Data Collector & Manager
- ✅ Closed loop implemented
- ✅ REST API for Apps/Observers
- ✅ Complete documentation

## Learnings

- Event-Driven Architecture with MQTT
- Integration of distributed components
- Design of automated business rules
- Northbound API for external integration

## Next Steps (Optional)

- Dynamic rule configuration via API
- Web dashboard for visualization
- Integration with real physical systems

---

## Slide 11: Questions

# Questions?

**Contact:**  
Rafaella Pinheiro  
rafaella.pinheiro@ufv.br

**Repository:**  
[GitHub URL]

**Documentation:**  
README.md with complete execution instructions

---

## 📝 Presentation Notes

### Estimated Time: 10-15 minutes

1. **Slide 1-2** (2 min): Introduction and context
2. **Slide 3-4** (3 min): Devices and architecture
3. **Slide 5** (2 min): **HIGHLIGHT the Closed Loop** (mandatory!)
4. **Slide 6-7** (2 min): Protocols and data
5. **Slide 8** (2 min): Business rules
6. **Slide 9** (3 min): **LIVE DEMO** (essential!)
7. **Slide 10-11** (1 min): Conclusions and questions

### Important Tips:

- **Practice the demo** before presentation
- **Have screenshots** ready in case demo fails
- **Explain the closed loop** clearly (it's mandatory!)
- **Show the code** if asked about implementation
- **Use the diagrams** created to explain architecture

### Pre-Presentation Checklist:

- [ ] Slides created and reviewed
- [ ] Demo tested and working
- [ ] Screenshots prepared (backup)
- [ ] Diagrams exported to PNG
- [ ] Code reviewed and commented
- [ ] README updated
- [ ] Presentation practice completed
