# 📁 AQUA_SENSE Project Structure

Organized project structure for easy navigation and maintenance.

```
Final_project_IOT/
│
├── 📄 README.md                    # Main project documentation
├── 📄 STRUCTURE.md                 # This file (project structure)
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                   # Files ignored by Git
│
├── 📁 devices/                     # Emulated IoT Devices
│   ├── rain_sensor.py             # Rain sensor
│   ├── water_sensor.py            # Water level sensor
│   ├── emergency_light.py         # Actuator: emergency light
│   └── notification_hub.py        # Actuator: notification hub
│
├── 📁 manager/                     # Data Collector & Manager
│   ├── api_server.py              # REST API (FastAPI)
│   ├── main.py                    # Compatibility entry point
│   ├── mqtt_client.py             # MQTT client (bridge)
│   ├── rules.py                   # Rules engine
│   ├── storage.py                 # SQLite persistence
│   └── device_registry.py         # Device registry
│
├── 📁 docs/                        # 📚 Technical Documentation
│   ├── README.md                  # Documentation index
│   │
│   ├── 📁 guides/                 # Practical Guides
│   │   ├── COMMANDS.md           # Complete step-by-step guide
│   │   ├── QUICK_START.md         # Quick command summary
│   │   └── PROJECT_CHECKLIST.md   # Requirements checklist
│   │
│   └── 📁 architecture/            # Architecture and Diagrams
│       ├── DIAGRAMS.md           # Guide about diagrams
│       ├── DIAGRAMS_SUMMARY.md    # Diagrams summary
│       └── architecture_diagrams.md # Mermaid diagrams (5 diagrams)
│
├── 📁 presentation/                # 🎤 Presentation Materials
│   ├── PRESENTATION_SLIDES.md     # Complete slide content
│   └── SLIDES_GUIDE.md            # Guide to create slides
│
├── 📁 docker/                      # 🐳 Docker and Containerization
│   ├── docker-compose.yml         # Compose for Broker + Manager
│   ├── Dockerfile                 # Manager Docker image
│   └── DOCKER_COMPOSE_GUIDE.md    # Docker Compose usage guide
│
├── 📁 config/                      # ⚙️ Configuration Files
│   └── (device configurations - optional)
│
├── 📁 data/                        # 💾 Persistent Data
│   └── aqua_sense.db              # SQLite database (generated)
│
├── 📁 logs/                        # 📝 System Logs
│   └── *.log                       # Device and manager logs
│
└── 📁 mosquitto/                   # 🌐 MQTT Broker (Mosquitto)
    ├── config/                     # Broker configuration
    ├── data/                       # Broker data
    └── log/                        # Broker logs
```

## 🎯 Where to Find What

### 🚀 To Start Using
- **Quick start:** `docs/guides/QUICK_START.md`
- **Complete guide:** `docs/guides/COMMANDS.md`
- **Main documentation:** `README.md`

### 📊 Diagrams and Architecture
- **All diagrams:** `docs/architecture/architecture_diagrams.md`
- **Diagrams guide:** `docs/architecture/DIAGRAMS.md`

### 🎤 Presentation
- **Slide content:** `presentation/PRESENTATION_SLIDES.md`
- **How to create slides:** `presentation/SLIDES_GUIDE.md`

### 🐳 Docker
- **Docker Compose:** `docker/docker-compose.yml`
- **Docker guide:** `docker/DOCKER_COMPOSE_GUIDE.md`

### 💻 Source Code
- **Devices:** `devices/`
- **Manager:** `manager/`

## 📝 Notes

- `.db`, `.log` files are automatically generated and should not be versioned
- Optional configurations can be added in `config/`
- Technical documentation is all in `docs/`
- Presentation materials are in `presentation/`
