# 🚀 Guia Passo a Passo - AQUA_SENSE

Este guia mostra os comandos exatos para executar o projeto AQUA_SENSE.

## 📋 Pré-requisitos

Certifique-se de ter instalado:
- Python 3.9+
- Mosquitto MQTT Broker (ou Docker para rodar o broker)

---

## 🔧 PASSO 1: Instalar Dependências

```bash
cd /home/rafaella/Final_project_IOT
pip install -r requirements.txt
```

**OU** se usar ambiente virtual:

```bash
cd /home/rafaella/Final_project_IOT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 PASSO 2: Iniciar o Broker MQTT (Mosquitto)

**Opção A - Se o Mosquitto já está instalado:**

```bash
mosquitto -p 1883 -v
```

**Opção B - Usando Docker (se não tiver Mosquitto instalado):**

```bash
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto:2.0
```

**Opção C - Se já tem um broker rodando em outro lugar, pule este passo.**

Deixe este terminal aberto! O broker precisa estar rodando.

---

## 🖥️ PASSO 3: Iniciar o Manager (API REST + MQTT Bridge)

Abra um **NOVO TERMINAL** e execute:

```bash
cd /home/rafaella/Final_project_IOT
python3 -m manager.api_server
```

**OU** usando uvicorn diretamente:

```bash
cd /home/rafaella/Final_project_IOT
uvicorn manager.api_server:app --host 0.0.0.0 --port 7070
```

Você deve ver mensagens como:
- `Manager MQTT bridge started`
- `Connected to MQTT broker`
- `Subscribed to telemetry topic pattern telemetry/+/+`
- `Uvicorn running on http://0.0.0.0:7070`

**Deixe este terminal aberto!**

---

## 📡 PASSO 4: Iniciar os Dispositivos IoT

Abra **4 TERMINAIS SEPARADOS** (um para cada dispositivo):

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

**Deixe todos os terminais abertos!**

---

## ✅ PASSO 5: Verificar se Está Funcionando

### 5.1 - Acessar a API REST (Swagger UI)

Abra seu navegador e acesse:

```
http://localhost:7070/docs
```

Você verá a interface Swagger com todos os endpoints disponíveis.

### 5.2 - Testar Endpoints via Terminal (curl)

**Listar dispositivos:**
```bash
curl http://localhost:7070/devices
```

**Ver telemetria:**
```bash
curl http://localhost:7070/telemetry
```

**Ver telemetria de um dispositivo específico:**
```bash
curl http://localhost:7070/telemetry?deviceId=water-01
```

**Ver alertas:**
```bash
curl http://localhost:7070/alerts
```

**Health check:**
```bash
curl http://localhost:7070/health
```

### 5.3 - Observar o Closed Loop Funcionando

1. **Observe os terminais dos dispositivos** - eles devem estar publicando dados periodicamente
2. **Observe o terminal do Manager** - você deve ver mensagens de telemetria recebida
3. **Quando o water_sensor publicar um valor >= 350 cm**, você deve ver:
   - No terminal do **Emergency Light**: mensagem de comando recebido
   - No terminal do **Manager**: comando publicado para o emergency light
4. **Quando o rain_sensor publicar um valor >= 80 mm**, você deve ver:
   - No terminal do **Notification Hub**: alerta recebido
   - No terminal do **Manager**: alerta publicado

---

## 🧪 PASSO 6: Enviar Comando Manual via API

Você pode enviar comandos manualmente usando a API:

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

Você deve ver a mensagem no terminal do Emergency Light!

---

## 🛑 Para Parar Tudo

Em cada terminal, pressione `Ctrl+C` para parar os serviços na ordem inversa:

1. Pare os dispositivos (terminais 4-7)
2. Pare o Manager (terminal 3)
3. Pare o Broker MQTT (terminal 2)

---

## 📊 Estrutura de Tópicos MQTT

O sistema usa os seguintes tópicos:

- **Telemetria (Device → Manager):**
  - `telemetry/rain/rain-01`
  - `telemetry/water/water-01`
  - `telemetry/emergency_light/emergency-light-01`

- **Comandos (Manager → Device):**
  - `commands/emergency_light/+` (para ligar/desligar luz de emergência)
  - `alerts/notification` (para enviar alertas ao notification hub)

---

## 🐛 Troubleshooting

### Problema: "Connection refused" no Manager
- **Solução:** Verifique se o broker MQTT está rodando (PASSO 2)

### Problema: Dispositivos não aparecem na API
- **Solução:** Aguarde alguns segundos após iniciar os dispositivos. Eles se registram automaticamente quando publicam telemetria.

### Problema: Porta 7070 já em uso
- **Solução:** Pare o processo anterior ou mude a porta:
  ```bash
  uvicorn manager.api_server:app --host 0.0.0.0 --port 8080
  ```

### Problema: Erro de importação de módulos
- **Solução:** Certifique-se de estar no diretório raiz do projeto e que todas as dependências foram instaladas.

---

## 📝 Notas Importantes

- Os dispositivos publicam dados a cada **10 segundos** por padrão
- O threshold de água é **350 cm** (configurável em `manager/rules.py`)
- O threshold de chuva é **80 mm** (configurável em `manager/rules.py`)
- Os dados são armazenados em SQLite em `manager/aqua_sense.db`
- Logs são salvos na pasta `logs/`

---

## 🎯 Próximos Passos

Após verificar que tudo funciona:

1. Explore a API Swagger em `http://localhost:7070/docs`
2. Teste diferentes valores de threshold nas regras
3. Adicione novos dispositivos ou regras conforme necessário
4. Prepare a apresentação com slides e demo!

