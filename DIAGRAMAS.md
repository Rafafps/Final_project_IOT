# 📊 Diagramas Necessários para o Projeto AQUA_SENSE

Baseado nos requisitos do curso, você precisa criar os seguintes diagramas para a **Fase 2** e **apresentação (Fase 3)**:

---

## ✅ Diagramas Obrigatórios

### 1. **Diagrama de Arquitetura de Componentes** (Component Diagram)
**O que mostra:** Componentes do sistema e suas responsabilidades

**Deve incluir:**
- Dispositivos IoT (sensors e actuators)
- Data Collector & Manager
- Storage/Database
- MQTT Broker
- REST API
- Apps/Observers
- Relações entre componentes

**Por que é importante:** Mostra a estrutura geral do sistema e separação de responsabilidades.

---

### 2. **Diagrama de Deployment** (Deployment Diagram)
**O que mostra:** Como os componentes são distribuídos em máquinas/containers

**Deve incluir:**
- Onde cada dispositivo roda (emulação local)
- Onde o Manager roda (servidor/container)
- Onde o MQTT Broker roda
- Como Apps/Observers acessam o sistema
- Rede e comunicação entre componentes

**Por que é importante:** Demonstra a arquitetura distribuída e como os componentes se comunicam fisicamente.

---

### 3. **Diagrama de Sequência** (Sequence Diagram) - **CLOSED LOOP**
**O que mostra:** Fluxo de interação entre componentes em um cenário específico

**Deve incluir pelo menos:**
- **Cenário 1:** Telemetria do sensor → Manager → Storage → Regras → Comando para atuador
- **Cenário 2:** App/Observer consultando dados via REST API
- **Cenário 3:** Configuração de regras via API

**Por que é importante:** Demonstra o **closed loop** obrigatório e o fluxo de dados end-to-end.

---

## 📋 Diagramas Recomendados (Plus)

### 4. **Diagrama de Fluxo de Dados** (Data Flow Diagram)
**O que mostra:** Como os dados fluem pelo sistema

**Deve incluir:**
- Telemetria (Device → Manager)
- Comandos (Manager → Device)
- Queries (App → Manager)
- Configuração (App → Manager)

**Por que é importante:** Complementa o diagrama de sequência mostrando todos os fluxos de dados.

---

### 5. **Diagrama de Tópicos MQTT** (MQTT Topic Structure)
**O que mostra:** Estrutura hierárquica dos tópicos MQTT

**Deve incluir:**
- `telemetry/rain/rain-01`
- `telemetry/water/water-01`
- `telemetry/emergency_light/emergency-light-01`
- `commands/emergency_light/+`
- `alerts/notification`

**Por que é importante:** Documenta o protocolo de comunicação MQTT usado.

---

### 6. **Diagrama de Estados** (State Diagram) - Opcional
**O que mostra:** Estados dos dispositivos e transições

**Deve incluir:**
- Estados do Emergency Light (ON/OFF)
- Estados dos sensores (ativo/inativo)
- Transições baseadas em eventos

**Por que é importante:** Mostra o comportamento dinâmico do sistema.

---

## 🎨 Ferramentas Recomendadas

### Opção 1: **Mermaid** (Recomendado - pode ir no README)
- ✅ Gratuito
- ✅ Integrado ao GitHub/Markdown
- ✅ Código versionável
- ✅ Fácil de atualizar

### Opção 2: **Draw.IO** (diagrams.net)
- ✅ Gratuito
- ✅ Interface visual
- ✅ Exporta para PNG/SVG
- ✅ Boa para apresentações

### Opção 3: **PlantUML**
- ✅ Código versionável
- ✅ Integração com Markdown
- ✅ Boa para diagramas técnicos

---

## 📝 Onde Incluir os Diagramas

1. **README.md** - Diagramas principais (Mermaid)
2. **Slides da Apresentação** - Versões exportadas (PNG/SVG)
3. **Documentação do Projeto** - Arquivo separado `docs/architecture.md` (opcional)

---

## 🎯 Checklist para Apresentação

- [ ] Diagrama de Componentes criado
- [ ] Diagrama de Deployment criado
- [ ] Diagrama de Sequência (closed loop) criado
- [ ] Diagramas incluídos nas slides (5-10 slides recomendado)
- [ ] Diagramas explicados durante a apresentação
- [ ] Diagramas refletem a implementação real

---

## 💡 Dica Importante

Os diagramas devem **refletir a implementação real**. Se você mostrar um diagrama na apresentação, o código deve seguir exatamente o que está desenhado. O professor pode perguntar sobre discrepâncias!

---

## 📚 Próximos Passos

1. Criar os diagramas usando Mermaid ou Draw.IO
2. Incluir no README.md (se usar Mermaid)
3. Exportar para slides (PNG/SVG)
4. Praticar a explicação de cada diagrama

