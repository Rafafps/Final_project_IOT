# 🚀 Step-by-Step Guide - AQUA_SENSE

This guide shows the exact commands to run the AQUA_SENSE project.

## 📋 Prerequisites

Make sure you have installed:
- Python 3.9+
- Mosquitto MQTT Broker (or Docker to run the broker)

---

## 🔧 STEP 1: Install Dependencies

```bash
cd /home/rafaella/Final_project_IOT
pip install -r requirements.txt
```

**OR** if using a virtual environment:

```bash
cd /home/rafaella/Final_project_IOT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 STEP 2: Start MQTT Broker (Mosquitto)

**Option A - If Mosquitto is already installed:**

```bash
mosquitto -p 1883 -v
```

**Option B - Using Docker (if Mosquitto is not installed):**

```bash
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto:2.0
```

**Option C - If you already have a broker running elsewhere, skip this step.**

Keep this terminal open! The broker needs to be running.

---

## 🖥️ STEP 3: Start the Manager (REST API + MQTT Bridge)

Open a **NEW TERMINAL** and run:

```bash
cd /home/rafaella/Final_project_IOT
python3 -m manager.api_server
```

**OR** using uvicorn directly:

```bash
cd /home/rafaella/Final_project_IOT
uvicorn manager.api_server:app --host 0.0.0.0 --port 7070
```

You should see messages like:
- `Manager MQTT bridge started`
- `Connected to MQTT broker`
- `Subscribed to telemetry topic pattern telemetry/+/+`
- `Uvicorn running on http://0.0.0.0:7070`

**Keep this terminal open!**

---

## 📡 STEP 4: Start IoT Devices

Open **4 SEPARATE TERMINALS** (one for each device):

### Terminal 4 - Rain Sensor:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/rain_sensor.py
```

### Terminal 5 - Water Sensor:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/water_sensor.py
```

### Terminal 6 - Emergency Light:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/emergency_light.py
```

### Terminal 7 - Notification Hub:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/notification_hub.py
```

**Keep all terminals open!**

---

## ✅ STEP 5: Verify Everything is Working

### 5.1 - Access REST API (Swagger UI)

Open your browser and access:

```
http://localhost:7070/docs
```

You will see the Swagger interface with all available endpoints.

### 5.2 - Test Endpoints via Terminal (curl)

**List devices:**
```bash
curl http://localhost:7070/devices
```

**View telemetry:**
```bash
curl http://localhost:7070/telemetry
```

**View telemetry from a specific device:**
```bash
curl http://localhost:7070/telemetry?deviceId=water-01
```

**View alerts:**
```bash
curl http://localhost:7070/alerts
```

**Health check:**
```bash
curl http://localhost:7070/health
```

### 5.3 - Observe the Closed Loop Working

1. **Observe device terminals** - they should be publishing data periodically
2. **Observe Manager terminal** - you should see telemetry received messages
3. **When water_sensor publishes a value >= 350 cm**, you should see:
   - In **Emergency Light** terminal: command received message
   - In **Manager** terminal: command published to emergency light
4. **When rain_sensor publishes a value >= 80 mm**, you should see:
   - In **Notification Hub** terminal: alert received
   - In **Manager** terminal: alert published

---

## 🧪 STEP 6: Send Manual Command via API

You can send commands manually using the API:

```bash
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "commands/emergency_light/emergency-light-01",
    "payload": {
      "action": "ON",
      "reason": "manual_test"
    }
  }'
```

You should see the message in the Emergency Light terminal!

---

## 🛑 To Stop Everything

In each terminal, press `Ctrl+C` to stop services in reverse order:

1. Stop devices (terminals 4-7)
2. Stop Manager (terminal 3)
3. Stop MQTT Broker (terminal 2)

---

## 📊 MQTT Topic Structure

The system uses the following topics:

- **Telemetry (Device → Manager):**
  - `telemetry/rain/rain-01`
  - `telemetry/water/water-01`
  - `telemetry/emergency_light/emergency-light-01`

- **Commands (Manager → Device):**
  - `commands/emergency_light/+` (to turn emergency light on/off)
  - `alerts/notification` (to send alerts to notification hub)

---

## 🐛 Troubleshooting

### Problem: "Connection refused" in Manager
- **Solution:** Check if MQTT broker is running (STEP 2)

### Problem: Devices don't appear in API
- **Solution:** Wait a few seconds after starting devices. They register automatically when publishing telemetry.

### Problem: Port 7070 already in use
- **Solution:** Stop the previous process or change the port:
  ```bash
  uvicorn manager.api_server:app --host 0.0.0.0 --port 8080
  ```

### Problem: Module import errors
- **Solution:** Make sure you're in the project root directory and all dependencies are installed.

---

## 📝 Important Notes

- Devices publish data every **10 seconds** by default
- Water threshold is **350 cm** (configurable in `manager/rules.py`)
- Rain threshold is **80 mm** (configurable in `manager/rules.py`)
- Data is stored in SQLite at `manager/aqua_sense.db`
- Logs are saved in the `logs/` folder

---

## 🎯 Next Steps

After verifying everything works:

1. Explore the Swagger API at `http://localhost:7070/docs`
2. Test different threshold values in rules
3. Add new devices or rules as needed
4. Prepare presentation with slides and demo!

