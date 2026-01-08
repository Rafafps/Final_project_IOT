# ⚡ Quick Start - Comandos Rápidos

## 🎯 Resumo Executivo

Execute estes comandos em **7 terminais diferentes** (ou use `tmux`/`screen` para múltiplas sessões):

---

## 📝 Comandos por Terminal

### Terminal 1 - Broker MQTT:
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

### Terminal 7 - Testes (opcional):
```bash
# Ver dispositivos
curl http://localhost:7070/devices

# Ver telemetria
curl http://localhost:7070/telemetry

# Ver alertas
curl http://localhost:7070/alerts

# Acessar Swagger UI
# Abra no navegador: http://localhost:7070/docs
```

---

## ✅ Verificação Rápida

1. ✅ Broker rodando? → Terminal 1 deve mostrar logs do Mosquitto
2. ✅ Manager conectado? → Terminal 2 deve mostrar "Connected to MQTT broker"
3. ✅ Dispositivos publicando? → Terminais 3-6 devem mostrar logs de publicação
4. ✅ API funcionando? → Acesse http://localhost:7070/docs no navegador

---

## 🔄 Ordem de Inicialização

1. **Primeiro:** Broker MQTT (Terminal 1)
2. **Segundo:** Manager (Terminal 2) - aguarde conectar
3. **Depois:** Dispositivos (Terminais 3-6) - ordem não importa

---

## 🛑 Parar Tudo

Pressione `Ctrl+C` em cada terminal na ordem inversa (6 → 5 → 4 → 3 → 2 → 1)

---

Para mais detalhes, veja `COMANDOS.md`

