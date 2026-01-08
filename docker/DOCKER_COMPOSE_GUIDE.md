# 🐳 Docker Compose Guide - AQUA_SENSE

## 📋 What Docker Compose Does

The `docker-compose.yml` creates and manages two services:

1. **Mosquitto MQTT Broker** - MQTT message broker
2. **Manager** - REST API + Data Collector

## 🚀 How to Use

### Option 1: Start only Broker + Manager (Recommended)

```bash
cd docker
docker-compose up -d
```

This will:
- ✅ Start MQTT broker on port 1883
- ✅ Start Manager on port 7070
- ✅ Create Docker network for service communication

### Option 2: View logs in real-time

```bash
docker-compose up
```

### Option 3: Stop services

```bash
docker-compose down
```

## 📡 Run IoT Devices

IoT devices should be executed **locally** (outside Docker):

```bash
# Terminal 1 - Rain Sensor
python3 devices/rain_sensor.py

# Terminal 2 - Water Sensor
python3 devices/water_sensor.py

# Terminal 3 - Emergency Light
python3 devices/emergency_light.py

# Terminal 4 - Notification Hub
python3 devices/notification_hub.py
```

**Why?** Devices need visible logs and user interaction during demo.

## ✅ Verify It's Working

### 1. Check running services:
```bash
docker-compose ps
```

### 2. View Manager logs:
```bash
docker-compose logs manager
```

### 3. View Broker logs:
```bash
docker-compose logs mosquitto
```

### 4. Access API:
```bash
# Swagger UI
http://localhost:7070/docs

# Health check
curl http://localhost:7070/health
```

## 🔧 Configuration

### Environment Variables (Manager)

You can edit `docker-compose.yml` to add variables:

```yaml
environment:
  - MQTT_BROKER=mosquitto
  - MQTT_PORT=1883
  - WATER_THRESHOLD=350
  - RAIN_THRESHOLD=80
```

### Ports

- **1883** - MQTT Broker (MQTT default)
- **9001** - MQTT WebSocket (optional)
- **7070** - REST API Manager

## 🐛 Troubleshooting

### Problem: Port 1883 already in use
```bash
# Check what's using the port
sudo lsof -i :1883

# Or change port in docker-compose.yml:
ports:
  - "1884:1883"  # Use 1884 externally
```

### Problem: Manager doesn't connect to broker
```bash
# Check if they're on the same network
docker network inspect final_project_iot_aqua_sense_net

# Check logs
docker-compose logs manager
```

### Problem: Mosquitto permissions
```bash
# Fix permissions
sudo chown -R 1883:1883 mosquitto/data mosquitto/log
```

## 📝 Important Notes

1. **IoT Devices:** Should run locally for visible logs
2. **Persistence:** Mosquitto data is saved in `mosquitto/data/`
3. **Logs:** Manager logs are saved in `logs/`
4. **Network:** Services communicate via Docker network `aqua_sense_net`

## 🎯 Complete Flow

```bash
# 1. Start infrastructure (Broker + Manager)
cd docker
docker-compose up -d

# 2. Wait a few seconds for initialization
sleep 5

# 3. Run devices locally
cd ..
python3 devices/rain_sensor.py &
python3 devices/water_sensor.py &
python3 devices/emergency_light.py &
python3 devices/notification_hub.py &

# 4. Access API
curl http://localhost:7070/devices
```

## 🔄 Update after code changes

```bash
# Rebuild and restart
cd docker
docker-compose down
docker-compose build --no-cache manager
docker-compose up -d
```

---

**Tip:** Use `docker-compose` for development and production, but run devices locally during demo for better visibility!
