# ⚡ Quick Start - Quick Commands

## 🎯 Executive Summary

Run these commands in **7 different terminals** (or use `tmux`/`screen` for multiple sessions):

---

## 📝 Commands by Terminal

### Terminal 1 - MQTT Broker:
```bash
mosquitto -p 1883 -v
```

### Terminal 2 - Manager (API):
```bash
cd /home/rafaella/Final_project_IOT
uvicorn manager.api_server:app --host 0.0.0.0 --port 7070
```

### Terminal 3 - Rain Sensor:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/rain_sensor.py
```

### Terminal 4 - Water Sensor:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/water_sensor.py
```

### Terminal 5 - Emergency Light:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/emergency_light.py
```

### Terminal 6 - Notification Hub:
```bash
cd /home/rafaella/Final_project_IOT
python3 devices/notification_hub.py
```

### Terminal 7 - Testing (optional):
```bash
# View devices
curl http://localhost:7070/devices

# View telemetry
curl http://localhost:7070/telemetry

# View alerts
curl http://localhost:7070/alerts

# Access Swagger UI
# Open in browser: http://localhost:7070/docs
```

---

## ✅ Quick Verification

1. ✅ Broker running? → Terminal 1 should show Mosquitto logs
2. ✅ Manager connected? → Terminal 2 should show "Connected to MQTT broker"
3. ✅ Devices publishing? → Terminals 3-6 should show publication logs
4. ✅ API working? → Access http://localhost:7070/docs in browser

---

## 🔄 Startup Order

1. **First:** MQTT Broker (Terminal 1)
2. **Second:** Manager (Terminal 2) - wait for connection
3. **Then:** Devices (Terminals 3-6) - order doesn't matter

---

## 🛑 Stop Everything

Press `Ctrl+C` in each terminal in reverse order (6 → 5 → 4 → 3 → 2 → 1)

---

For more details, see `COMMANDS.md` (in this directory)
