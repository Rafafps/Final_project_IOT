# 📋 Guia Completo de Testes - AQUA_SENSE

Este documento contém **TODOS** os comandos necessários para testar completamente o sistema AQUA_SENSE.

---

## 🚀 PARTE 1: COMANDOS DE INICIALIZAÇÃO

### 1.1 Instalar Dependências

```bash
# Instalação padrão
cd /home/rafaella/Final_project_IOT
pip install -r requirements.txt

# OU com ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.2 Iniciar MQTT Broker (Mosquitto)

```bash
# Opção A: Mosquitto instalado diretamente
mosquitto -p 1883 -v

# Opção B: Via Docker
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto:2.0

# Opção C: Docker Compose (recomendado)
cd /home/rafaella/Final_project_IOT/docker
docker-compose up -d

# Verificar se está rodando
mosquitto_sub -t "#" -v
```

### 1.3 Iniciar o Manager (API REST + MQTT Bridge)

```bash
# Método 1: Via módulo Python
cd /home/rafaella/Final_project_IOT
python3 -m manager.api_server

# Método 2: Via uvicorn direto
cd /home/rafaella/Final_project_IOT
uvicorn manager.api_server:app --host 0.0.0.0 --port 7070

# Método 3: Com reload para desenvolvimento
uvicorn manager.api_server:app --host 0.0.0.0 --port 7070 --reload

# Método 4: Com logs detalhados
cd /home/rafaella/Final_project_IOT
python3 -m manager.api_server 2>&1 | tee logs/manager.log
```

### 1.4 Iniciar os Dispositivos IoT

```bash
# Terminal 1: Sensor de Chuva
cd /home/rafaella/Final_project_IOT
python3 devices/rain_sensor.py

# Terminal 2: Sensor de Água
cd /home/rafaella/Final_project_IOT
python3 devices/water_sensor.py

# Terminal 3: Luz de Emergência
cd /home/rafaella/Final_project_IOT
python3 devices/emergency_light.py

# Terminal 4: Hub de Notificações
cd /home/rafaella/Final_project_IOT
python3 devices/notification_hub.py
```

### 1.5 Iniciar Dashboard

```bash
# Método 1: Abrir diretamente no navegador
# Basta abrir o arquivo: dashboard/index.html

# Método 2: Servidor HTTP (se necessário)
cd /home/rafaella/Final_project_IOT
python3 -m http.server 8080
# Acessar: http://localhost:8080/dashboard/index.html
```

---

## ✅ PARTE 2: TESTES DA API REST

### 2.1 Health Check

```bash
# Verificar se a API está online
curl http://localhost:7070/health

# Saída esperada: {"status":"ok"}
```

### 2.2 Testar Endpoints de Dispositivos

```bash
# Listar todos os dispositivos registrados
curl http://localhost:7070/devices

# Listar dispositivos com formatação JSON bonito
curl -s http://localhost:7070/devices | python3 -m json.tool

# Registrar um novo dispositivo (POST)
curl -X POST http://localhost:7070/devices \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "test-sensor-01",
    "deviceType": "test_sensor",
    "capabilities": ["telemetry"]
  }'

# Verificar dispositivo específico
curl http://localhost:7070/devices | grep "water-01"
```

### 2.3 Testar Endpoints de Telemetria

```bash
# Listar toda a telemetria
curl http://localhost:7070/telemetry

# Telemetria com limite de registros
curl "http://localhost:7070/telemetry?limit=10"

# Telemetria de dispositivo específico
curl "http://localhost:7070/telemetry?deviceId=water-01"

# Telemetria de dispositivo com limite
curl "http://localhost:7070/telemetry?deviceId=water-01&limit=5"

# Telemetria formatada
curl -s http://localhost:7070/telemetry | python3 -m json.tool
```

### 2.4 Testar Endpoints de Alertas

```bash
# Listar todos os alertas
curl http://localhost:7070/alerts

# Alertas com limite
curl "http://localhost:7070/alerts?limit=10"

# Alertas formatados
curl -s http://localhost:7070/alerts | python3 -m json.tool
```

### 2.5 Testar Envio de Comandos

```bash
# Ligar luz de emergência manualmente
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "commands/emergency_light/emergency-light-01",
    "payload": {
      "action": "ON",
      "reason": "manual_test"
    }
  }'

# Desligar luz de emergência
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "commands/emergency_light/emergency-light-01",
    "payload": {
      "action": "OFF",
      "reason": "manual_test"
    }
  }'

# Testar comando inválido (sem topic)
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{"payload": {"action": "ON"}}'

# Deve retornar erro 422 ou 400
```

---

## 🔧 PARTE 3: TESTES MQTT

### 3.1 Assinar Todos os Tópicos (Monitoramento)

```bash
# Assinar toda a telemetria
mosquitto_sub -t "telemetry/+" -v

# Assinar telemetria específica de água
mosquitto_sub -t "telemetry/water/#" -v

# Assinar telemetria específica de chuva
mosquitto_sub -t "telemetry/rain/#" -v

# Assinar comandos para luz de emergência
mosquitto_sub -t "commands/emergency_light/#" -v

# Assinar alertas
mosquitto_sub -t "alerts/#" -v

# Assinar todos os tópicos (debugging)
mosquitto_sub -t "#" -v
```

### 3.2 Publicar Mensagens MQTT (Testes Manuais)

```bash
# Publicar telemetria de sensor de água (VALOR ALTO = ACIONA EMERGÊNCIA)
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}'

# Publicar telemetria de sensor de água (VALOR NORMAL)
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 200,
  "timestamp": "2024-01-15T10:30:00Z"
}'

# Publicar telemetria de sensor de chuva (VALOR ALTO = ACIONA ALERTA)
mosquitto_pub -t "telemetry/rain/rain-01" -m '{
  "deviceId": "rain-01",
  "deviceType": "rain_sensor",
  "rain_mm": 90,
  "timestamp": "2024-01-15T10:30:00Z"
}'

# Publicar telemetria de sensor de chuva (VALOR NORMAL)
mosquitto_pub -t "telemetry/rain/rain-01" -m '{
  "deviceId": "rain-01",
  "deviceType": "rain_sensor",
  "rain_mm": 30,
  "timestamp": "2024-01-15T10:30:00Z"
}'
```

### 3.3 Testar Comando Direto via MQTT

```bash
# Ligar luz de emergência via MQTT
mosquitto_pub -t "commands/emergency_light/emergency-light-01" -m '{
  "action": "ON",
  "reason": "mqtt_test"
}'

# Desligar luz de emergência via MQTT
mosquitto_pub -t "commands/emergency_light/emergency-light-01" -m '{
  "action": "OFF",
  "reason": "mqtt_test"
}'
```

---

## 🧪 PARTE 4: SCRIPTS DE TESTE AUTOMATIZADOS

### 4.1 Script de Teste Completo do Sistema

Crie o arquivo `test_system.sh`:

```bash
#!/bin/bash
# test_system.sh - Script de teste completo do AQUA_SENSE

echo "========================================="
echo "🧪 TESTE COMPLETO DO SISTEMA AQUA_SENSE"
echo "========================================="

echo ""
echo "1️⃣ Testando Health Check..."
curl -s http://localhost:7070/health
echo ""

echo ""
echo "2️⃣ Listando dispositivos..."
curl -s http://localhost:7070/devices
echo ""

echo ""
echo "3️⃣ Enviando telemetria de água (NORMAL - 200cm)..."
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 200,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 2

echo ""
echo "4️⃣ Enviando telemetria de água (ALERTA - 400cm)..."
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 400,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 2

echo ""
echo "5️⃣ Enviando telemetria de chuva (NORMAL - 30mm)..."
mosquitto_pub -t "telemetry/rain/rain-01" -m '{
  "deviceId": "rain-01",
  "deviceType": "rain_sensor",
  "rain_mm": 30,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 2

echo ""
echo "6️⃣ Enviando telemetria de chuva (ALERTA - 90mm)..."
mosquitto_pub -t "telemetry/rain/rain-01" -m '{
  "deviceId": "rain-01",
  "deviceType": "rain_sensor",
  "rain_mm": 90,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 2

echo ""
echo "7️⃣ Verificando alertas gerados..."
curl -s "http://localhost:7070/alerts?limit=10"
echo ""

echo ""
echo "8️⃣ Verificando telemetria..."
curl -s "http://localhost:7070/telemetry?limit=10"
echo ""

echo ""
echo "9️⃣ Enviando comando manual para luz de emergência..."
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "commands/emergency_light/emergency-light-01",
    "payload": {"action": "ON", "reason": "test_completo"}
  }'
echo ""

echo ""
echo "🔟 Desligando luz de emergência..."
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "commands/emergency_light/emergency-light-01",
    "payload": {"action": "OFF", "reason": "test_completo"}
  }'
echo ""

echo ""
echo "========================================="
echo "✅ TESTE COMPLETO FINALIZADO!"
echo "========================================="
```

Para executar:
```bash
chmod +x test_system.sh
./test_system.sh
```

### 4.2 Script de Teste de Carga

Crie o arquivo `test_load.sh`:

```bash
#!/bin/bash
# test_load.sh - Teste de carga do sistema

echo "🧪 Enviando 100 mensagens de telemetria..."

for i in {1..100}; do
  WATER_LEVEL=$((200 + RANDOM % 300))
  
  mosquitto_pub -t "telemetry/water/water-01" -m "{
    \"deviceId\": \"water-01\",
    \"deviceType\": \"water_sensor\",
    \"water_level_cm\": $WATER_LEVEL,
    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }"
  
  echo "Mensagem $i enviada (nível de água: ${WATER_LEVEL}cm)"
  sleep 0.5
done

echo "✅ Teste de carga concluído!"
echo "Verificando telemetria armazenada..."
curl -s "http://localhost:7070/telemetry?limit=100"
```

### 4.3 Script de Teste de Limiares

Crie o arquivo `test_thresholds.sh`:

```bash
#!/bin/bash
# test_thresholds.sh - Testar diferentes limiares

echo "🧪 Teste de Limiares do Sistema"
echo "Limiar de água: 350cm | Limiar de chuva: 80mm"
echo ""

# Teste 1: Água no limiar exato
echo "1️⃣ Testando água no limiar (350cm)..."
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 350,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 3

# Teste 2: Água abaixo do limiar
echo "2️⃣ Testando água abaixo do limiar (349cm)..."
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 349,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 3

# Teste 3: Chuva no limiar exato
echo "3️⃣ Testando chuva no limiar (80mm)..."
mosquitto_pub -t "telemetry/rain/rain-01" -m '{
  "deviceId": "rain-01",
  "deviceType": "rain_sensor",
  "rain_mm": 80,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 3

# Teste 4: Chuva abaixo do limiar
echo "4️⃣ Testando chuva abaixo do limiar (79mm)..."
mosquitto_pub -t "telemetry/rain/rain-01" -m '{
  "deviceId": "rain-01",
  "deviceType": "rain_sensor",
  "rain_mm": 79,
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'
sleep 3

echo ""
echo "✅ Teste de limiares concluído!"
echo "Verifique os alertas gerados:"
curl -s http://localhost:7070/alerts
```

---

## 🔍 PARTE 5: VERIFICAÇÃO DE LOGS

### 5.1 Ver Logs do Manager

```bash
# Ver logs em tempo real
tail -f logs/manager.log

# Ver todas as entradas de log
cat logs/manager.log

# Buscar por erros
grep -i error logs/manager.log

# Buscar por comandos publicados
grep -i "command" logs/manager.log

# Buscar por alertas
grep -i "alert" logs/manager.log
```

### 5.2 Verificar Logs dos Dispositivos

```bash
# Rain Sensor
tail -f logs/rain_sensor.log

# Water Sensor
tail -f logs/water_sensor.log

# Emergency Light
tail -f f/emergency_light.log

# Notification Hub
tail -f logs/notification_hub.log
```

### 5.3 Verificar Logs do MQTT Broker

```bash
# Se usando Docker
docker logs mosquitto

# Verificar últimos 100 logs
docker logs --tail 100 mosquitto
```

---

## 🗄️ PARTE 6: VERIFICAÇÃO DO BANCO DE DADOS

### 6.1 Verificar Dados no SQLite

```bash
# Acessar banco de dados
cd /home/rafaella/Final_project_IOT/manager
sqlite3 aqua_sense.db

# Dentro do sqlite3:
.tables
.schema telemetry
.schema alerts
SELECT * FROM telemetry LIMIT 10;
SELECT * FROM alerts LIMIT 10;
.exit
```

### 6.2 Verificar via Script Python

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('manager/aqua_sense.db')
cursor = conn.cursor()

print('=== TABELAS ===')
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
print([r[0] for r in cursor.fetchall()])

print('\n=== TELEMETRIA (últimos 5) ===')
cursor.execute('SELECT * FROM telemetry ORDER BY id DESC LIMIT 5')
for row in cursor.fetchall():
    print(row)

print('\n=== ALERTAS (últimos 5) ===')
cursor.execute('SELECT * FROM alerts ORDER BY id DESC LIMIT 5')
for row in cursor.fetchall():
    print(row)

conn.close()
"
```

---

## 🐛 PARTE 7: TESTES DE ERRO E EDGE CASES

### 7.1 Testar API com Dados Inválidos

```bash
# Testar registro de dispositivo sem deviceId
curl -X POST http://localhost:7070/devices \
  -H "Content-Type: application/json" \
  -d '{"deviceType": "test"}'

# Testar comando sem topic
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{"payload": {"action": "ON"}}'

# Testar topic vazio
curl -X POST http://localhost:7070/commands \
  -H "Content-Type: application/json" \
  -d '{"topic": "", "payload": {"action": "ON"}}'
```

### 7.2 Testar MQTT com Payload Inválido

```bash
# Publicar JSON inválido
mosquitto_pub -t "telemetry/water/water-01" -m "invalid json"

# Publicar JSON com campos faltando
mosquitto_pub -t "telemetry/water/water-01" -m '{"water_level_cm": 100}'

# Publicar com timestamp inválido
mosquitto_pub -t "telemetry/water/water-01" -m '{
  "deviceId": "water-01",
  "deviceType": "water_sensor",
  "water_level_cm": 400,
  "timestamp": "data-invalida"
}'
```

### 7.3 Testar Limites de Dados

```bash
# Testar limite muito alto
curl "http://localhost:7070/telemetry?limit=99999"

# Testar limite zero
curl "http://localhost:7070/telemetry?limit=0"

# Testar limite negativo
curl "http://localhost:7070/telemetry?limit=-1"
```

---

## 🐳 PARTE 8: TESTES COM DOCKER

### 8.1 Build e Run com Docker

```bash
# Build da imagem
cd /home/rafaella/Final_project_IOT/docker
docker build -t aqua_sense .

# Run do container
docker run -p 7070:7070 --network=host aqua_sense

# Com variáveis de ambiente
docker run -p 7070:7070 \
  -e MQTT_BROKER=localhost \
  -e MQTT_PORT=1883 \
  --network=host \
  aqua_sense
```

### 8.2 Docker Compose

```bash
# Iniciar todos os serviços
cd /home/rafaella/Final_project_IOT/docker
docker-compose up -d

# Ver status dos serviços
docker-compose ps

# Ver logs de todos os serviços
docker-compose logs -f

# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

### 8.3 Testar após Deploy Docker

```bash
# Verificar containers ativos
docker ps

# Acessar API
curl http://localhost:7070/health

# Verificar logs do Manager
docker logs aquasense-manager-1

# Verificar logs do Mosquitto
docker logs aquasense-mosquitto-1
```

---

## 📊 PARTE 9: TESTES DO DASHBOARD

### 9.1 Verificar Interface Web

```bash
# Abrir dashboard no navegador
# URL: http://localhost:8080/dashboard/index.html

# OU se usando servidor HTTP
# URL: http://localhost:8080/dashboard/
```

### 9.2 Testar Endpoints do Dashboard

```bash
# Health check
curl http://localhost:7070/health

# Lista dispositivos (formato esperado pelo dashboard)
curl http://localhost:7070/devices

# Telemetria (formato esperado pelo dashboard)
curl http://localhost:7070/telemetry

# Alertas (formato esperado pelo dashboard)
curl http://localhost:7070/alerts
```

---

## 🎯 PARTE 10: CHECKLIST DE TESTES COMPLETO

| Teste | Status | Comando |
|-------|--------|---------|
| Health Check | ⬜ | `curl http://localhost:7070/health` |
| Listar Devices | ⬜ | `curl http://localhost:7070/devices` |
| Registrar Device | ⬜ | `curl -X POST .../devices` |
| Listar Telemetria | ⬜ | `curl http://localhost:7070/telemetry` |
| Telemetria por Device | ⬜ | `curl ...?deviceId=water-01` |
| Listar Alertas | ⬜ | `curl http://localhost:7070/alerts` |
| Enviar Comando ON | ⬜ | `curl -X POST ...commands` |
| Enviar Comando OFF | ⬜ | `curl -X POST ...commands` |
| MQTT Telemetria Água (Alto) | ⬜ | `mosquitto_pub ... 400cm` |
| MQTT Telemetria Água (Baixo) | ⬜ | `mosquitto_pub ... 200cm` |
| MQTT Telemetria Chuva (Alto) | ⬜ | `mosquitto_pub ... 90mm` |
| MQTT Telemetria Chuva (Baixo) | ⬜ | `mosquitto_pub ... 30mm` |
| Verificar Alerta Gerado | ⬜ | `curl http://localhost:7070/alerts` |
| Verificar Logs | ⬜ | `tail -f logs/manager.log` |
| Dashboard Funcionando | ⬜ | Abrir `dashboard/index.html` |
| Banco de Dados OK | ⬜ | `sqlite3 ...aqua_sense.db` |
| Erro 400/422 | ⬜ | `curl -X POST dados-invalidos` |

---

## 🛑 PARTE 11: COMANDOS DE PARADA

```bash
# Parar todos os dispositivos (Ctrl+C em cada terminal)

# Parar Manager (Ctrl+C)

# Parar Mosquitto (Ctrl+C)

# Se usando Docker
docker-compose down

# Matar processos em porta 7070
lsof -ti:7070 | xargs kill -9

# Matar processos em porta 1883
lsof -ti:1883 | xargs kill -9
```

---

## 📝 ANOTAÇÕES

- **Limiar de Água:** 350cm (configurável em `manager/rules.py`)
- **Limiar de Chuva:** 80mm (configurável em `manager/rules.py`)
- **Frequência de Publicação:** 10 segundos (padrão dos dispositivos)
- **Banco de Dados:** `manager/aqua_sense.db`
- **Logs:** `logs/` directory
- **Porta API:** 7070
- **Porta MQTT:** 1883
- **Dashboard:** `dashboard/index.html`

---

**✅ Este guia cobre TODOS os testes possíveis do sistema AQUA_SENSE!**

