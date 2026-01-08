# 🏗️ Diagramas de Arquitetura - AQUA_SENSE

Este documento contém os diagramas de arquitetura do projeto AQUA_SENSE em formato Mermaid.

---

## 1. Diagrama de Componentes (Component Diagram)

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
        CUSTOM[Custom Apps]
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
    CUSTOM --> API
    
    style RS fill:#e1f5ff
    style WS fill:#e1f5ff
    style EL fill:#fff4e1
    style NH fill:#fff4e1
    style MQTT fill:#ffe1f5
    style MQTT_CLIENT fill:#e1ffe1
    style RULES fill:#ffe1e1
    style STORAGE fill:#f0e1ff
    style API fill:#e1ffe1
```

---

## 2. Diagrama de Deployment (Deployment Diagram)

```mermaid
graph TB
    subgraph "Local Machine / Development Environment"
        subgraph "Terminal 1"
            BROKER[MQTT Broker<br/>mosquitto<br/>Port: 1883]
        end
        
        subgraph "Terminal 2"
            MANAGER[Manager Service<br/>uvicorn<br/>Port: 7070]
        end
        
        subgraph "Terminal 3-6"
            DEVICES[IoT Devices<br/>Python Scripts<br/>rain_sensor.py<br/>water_sensor.py<br/>emergency_light.py<br/>notification_hub.py]
        end
        
        subgraph "Browser"
            SWAGGER[Swagger UI<br/>http://localhost:7070/docs]
        end
        
        subgraph "File System"
            DB[(SQLite Database<br/>aqua_sense.db)]
            LOGS[Log Files<br/>logs/*.log]
        end
    end
    
    DEVICES -.->|MQTT Pub/Sub| BROKER
    MANAGER -.->|MQTT Subscribe| BROKER
    MANAGER -.->|MQTT Publish| BROKER
    MANAGER -->|Read/Write| DB
    DEVICES -->|Write| LOGS
    MANAGER -->|Write| LOGS
    SWAGGER -.->|HTTP REST| MANAGER
    
    style BROKER fill:#ffe1f5
    style MANAGER fill:#e1ffe1
    style DEVICES fill:#e1f5ff
    style DB fill:#f0e1ff
    style SWAGGER fill:#fff4e1
```

---

## 3. Diagrama de Sequência - Closed Loop (Sequence Diagram)

### 3.1 Fluxo: Telemetria → Regra → Comando (Water Level Alert)

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

### 3.2 Fluxo: App Consultando Dados via REST API

```mermaid
sequenceDiagram
    participant APP as App/Observer
    participant API as REST API<br/>(FastAPI)
    participant ST as Storage
    participant REG as Device Registry
    
    APP->>API: GET /devices
    API->>REG: list_devices()
    REG-->>API: List of devices
    API-->>APP: JSON response
    
    APP->>API: GET /telemetry?deviceId=water-01
    API->>ST: get_telemetry(deviceId, limit)
    ST-->>API: Telemetry data
    API-->>APP: JSON response
    
    APP->>API: GET /alerts
    API->>ST: get_alerts(limit)
    ST-->>API: Alert history
    API-->>APP: JSON response
```

### 3.3 Fluxo: Configuração Manual de Comando

```mermaid
sequenceDiagram
    participant APP as App/Observer
    participant API as REST API
    participant MC as MQTT Client
    participant MQTT as MQTT Broker
    participant EL as Emergency Light
    
    APP->>API: POST /commands<br/>{topic: "commands/emergency_light/...",<br/>payload: {action: "ON"}}
    API->>MC: publish_command(topic, payload)
    MC->>MQTT: Publish command
    MQTT->>EL: Command message
    EL->>EL: Execute action
    EL-->>APP: (via telemetry update)
```

---

## 4. Diagrama de Fluxo de Dados (Data Flow Diagram)

```mermaid
flowchart LR
    subgraph "Data Sources"
        S1[Rain Sensor]
        S2[Water Sensor]
        S3[Emergency Light]
    end
    
    subgraph "Data Collector"
        MQTT_BRIDGE[MQTT Bridge]
        STORAGE[(Storage)]
        REGISTRY[Registry]
    end
    
    subgraph "Processing"
        RULES[Rules Engine]
    end
    
    subgraph "Data Consumers"
        ACT1[Emergency Light]
        ACT2[Notification Hub]
        API[REST API]
    end
    
    subgraph "External"
        APPS[Apps/Observers]
    end
    
    S1 -->|Telemetry| MQTT_BRIDGE
    S2 -->|Telemetry| MQTT_BRIDGE
    S3 -->|Status| MQTT_BRIDGE
    
    MQTT_BRIDGE --> STORAGE
    MQTT_BRIDGE --> REGISTRY
    MQTT_BRIDGE --> RULES
    
    RULES -->|Commands| ACT1
    RULES -->|Alerts| ACT2
    
    STORAGE --> API
    REGISTRY --> API
    API --> APPS
    
    style S1 fill:#e1f5ff
    style S2 fill:#e1f5ff
    style S3 fill:#fff4e1
    style ACT1 fill:#fff4e1
    style ACT2 fill:#fff4e1
    style RULES fill:#ffe1e1
    style STORAGE fill:#f0e1ff
```

---

## 5. Estrutura de Tópicos MQTT

```mermaid
graph TD
    ROOT[MQTT Topics]
    
    ROOT --> TELEMETRY[telemetry/]
    ROOT --> COMMANDS[commands/]
    ROOT --> ALERTS[alerts/]
    
    TELEMETRY --> T_RAIN[rain/rain-01]
    TELEMETRY --> T_WATER[water/water-01]
    TELEMETRY --> T_LIGHT[emergency_light/emergency-light-01]
    
    COMMANDS --> C_LIGHT[emergency_light/+]
    
    ALERTS --> A_NOTIF[notification]
    
    style ROOT fill:#ffe1f5
    style TELEMETRY fill:#e1f5ff
    style COMMANDS fill:#fff4e1
    style ALERTS fill:#ffe1e1
```

---

## 📝 Notas sobre os Diagramas

### Component Diagram
- Mostra a separação de responsabilidades
- Indica protocolos de comunicação (MQTT, HTTP REST)
- Diferencia sensores (azul) de atuadores (amarelo)

### Deployment Diagram
- Mostra que tudo roda localmente (desenvolvimento)
- Indica portas e protocolos
- Mostra persistência (arquivos)

### Sequence Diagrams
- **Obrigatório:** Mostra o closed loop funcionando
- Demonstra interação temporal entre componentes
- Facilita explicação durante apresentação

### Data Flow Diagram
- Complementa o sequence diagram
- Mostra todos os fluxos de dados
- Útil para entender o sistema completo

### MQTT Topics Structure
- Documenta o protocolo de comunicação
- Facilita debugging e testes
- Importante para explicar escolhas de design

---

## 🎨 Como Usar

1. **No README.md:** Copie os diagramas Mermaid diretamente (GitHub renderiza automaticamente)
2. **Nas Slides:** Exporte como PNG usando:
   - [Mermaid Live Editor](https://mermaid.live)
   - [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
   - Screenshot do GitHub
3. **Na Apresentação:** Explique cada diagrama e como ele reflete a implementação

---

## ✅ Checklist

- [x] Diagrama de Componentes criado
- [x] Diagrama de Deployment criado
- [x] Diagrama de Sequência (closed loop) criado
- [x] Diagrama de Fluxo de Dados criado
- [x] Estrutura de Tópicos MQTT documentada
- [ ] Diagramas incluídos no README.md
- [ ] Diagramas exportados para slides
- [ ] Praticar explicação de cada diagrama

