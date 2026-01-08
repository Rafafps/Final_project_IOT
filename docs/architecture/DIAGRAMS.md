# 📊 Required Diagrams for AQUA_SENSE Project

Based on course requirements, you need to create the following diagrams for **Phase 2** and **presentation (Phase 3)**:

---

## ✅ Mandatory Diagrams

### 1. **Component Architecture Diagram** (Component Diagram)
**What it shows:** System components and their responsibilities

**Must include:**
- IoT Devices (sensors and actuators)
- Data Collector & Manager
- Storage/Database
- MQTT Broker
- REST API
- Apps/Observers
- Relationships between components

**Why it's important:** Shows the overall system structure and separation of responsibilities.

---

### 2. **Deployment Diagram** (Deployment Diagram)
**What it shows:** How components are distributed across machines/containers

**Must include:**
- Where each device runs (local emulation)
- Where the Manager runs (server/container)
- Where the MQTT Broker runs
- How Apps/Observers access the system
- Network and communication between components

**Why it's important:** Demonstrates the distributed architecture and how components communicate physically.

---

### 3. **Sequence Diagram** (Sequence Diagram) - **CLOSED LOOP**
**What it shows:** Interaction flow between components in a specific scenario

**Must include at least:**
- **Scenario 1:** Sensor telemetry → Manager → Storage → Rules → Command to actuator
- **Scenario 2:** App/Observer querying data via REST API
- **Scenario 3:** Rule configuration via API

**Why it's important:** Demonstrates the mandatory **closed loop** and end-to-end data flow.

---

## 📋 Recommended Diagrams (Plus)

### 4. **Data Flow Diagram** (Data Flow Diagram)
**What it shows:** How data flows through the system

**Must include:**
- Telemetry (Device → Manager)
- Commands (Manager → Device)
- Queries (App → Manager)
- Configuration (App → Manager)

**Why it's important:** Complements the sequence diagram showing all data flows.

---

### 5. **MQTT Topic Diagram** (MQTT Topic Structure)
**What it shows:** Hierarchical structure of MQTT topics

**Must include:**
- `telemetry/rain/rain-01`
- `telemetry/water/water-01`
- `telemetry/emergency_light/emergency-light-01`
- `commands/emergency_light/+`
- `alerts/notification`

**Why it's important:** Documents the MQTT communication protocol used.

---

### 6. **State Diagram** (State Diagram) - Optional
**What it shows:** Device states and transitions

**Must include:**
- Emergency Light states (ON/OFF)
- Sensor states (active/inactive)
- Event-based transitions

**Why it's important:** Shows the dynamic behavior of the system.

---

## 🎨 Recommended Tools

### Option 1: **Mermaid** (Recommended - can go in README)
- ✅ Free
- ✅ Integrated with GitHub/Markdown
- ✅ Versionable code
- ✅ Easy to update

### Option 2: **Draw.IO** (diagrams.net)
- ✅ Free
- ✅ Visual interface
- ✅ Exports to PNG/SVG
- ✅ Good for presentations

### Option 3: **PlantUML**
- ✅ Versionable code
- ✅ Markdown integration
- ✅ Good for technical diagrams

---

## 📝 Where to Include Diagrams

1. **README.md** - Main diagrams (Mermaid)
2. **Presentation Slides** - Exported versions (PNG/SVG)
3. **Project Documentation** - Separate file `docs/architecture/architecture_diagrams.md` (optional)

---

## 🎯 Checklist for Presentation

- [ ] Component Diagram created
- [ ] Deployment Diagram created
- [ ] Sequence Diagram (closed loop) created
- [ ] Diagrams included in slides (5-10 slides recommended)
- [ ] Diagrams explained during presentation
- [ ] Diagrams reflect actual implementation

---

## 💡 Important Tip

Diagrams must **reflect the actual implementation**. If you show a diagram in the presentation, the code must follow exactly what is drawn. The teacher may ask about discrepancies!

---

## 📚 Next Steps

1. Create diagrams using Mermaid or Draw.IO
2. Include in README.md (if using Mermaid)
3. Export for slides (PNG/SVG)
4. Practice explaining each diagram

