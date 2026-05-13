# 🤖 AGENTE PROSPECTOR INTELIGENTE - SETUP COMPLETO
## Cannabis Medicinal | Automation 360°

---

## 📋 RESUMO EXECUTIVO

Você vai ter um **sistema automático em 3 peças** que roda sozinho:

1. **Data Enrichment** (Hunter.io) → Valida/encontra e-mails
2. **Automação de Mensagens** (N8N + APIs) → Envia LinkedIn/E-mail/WhatsApp em sequência
3. **CRM & Tracking** (Pipedrive) → Rastreia jornada, qualifica leads, prepara você para venda

**Resultado**: Você só intervém quando há resposta qualificada. O resto é automático.

---

## 🔧 STACK RECOMENDADO

| Peça | Ferramenta | Custo | Por quê |
|------|-----------|-------|--------|
| **Data Enrichment** | Hunter.io | Grátis (50/mês) ou $49/mês | Validar e-mails, encontrar dados |
| **Automação** | N8N (self-hosted) | Grátis | Conecta tudo, sem limite |
| **WhatsApp** | Twilio API | ~$0.01/msg | Envio automatizado |
| **CRM** | Pipedrive | $15/mês | Leve, visual, fácil |
| **Armazenamento** | Google Sheets | Grátis | Database simples dos contatos |

**Custo total**: ~$15/mês (depois que setup)

---

## 📊 ARQUITETURA DO AGENTE

```
┌─────────────────────────────────────┐
│ ENTRADA: Google Sheets              │
│ (50-100 contatos + segmentação)     │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ HUNTER.IO (via N8N)                 │
│ Validar e-mail + Enriquecer dados   │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ N8N WORKFLOW (Automação Central)    │
│                                     │
│ DIA 1: Conectar LinkedIn            │
│ DIA 3: Enviar E-mail                │
│ DIA 6: Enviar WhatsApp (se resposta)│
│ SEMPRE: Logs para Pipedrive         │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ PIPEDRIVE (CRM)                     │
│ Cada contato = 1 deal               │
│ Status: Prospect → Qualificado →    │
│ Reunião → Proposta → Contrato       │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ VOCÊ (Qualificação 1:1)             │
│ Conversa profunda + Demonstração    │
│ + Apresentação da Sessão Estratégica│
└─────────────────────────────────────┘
```

---

## 🚀 FASE 1: SETUP (Dia 1-2, ~3-4 horas)

### PASSO 1: Preparar Base de Dados (Google Sheets)

**Criar aba no Google Sheets com estas colunas:**

```
| Nome | Especialidade | E-mail | WhatsApp | LinkedIn URL | Tier | Status | Data Contato | Resposta |
|------|--------------|--------|----------|-------------|------|--------|--------------|----------|
```

**Tier definido assim:**
- **Tier 1**: Tem Instagram + LinkedIn com posts últimas 2 semanas = Prospectar HOJE
- **Tier 2**: Tem presença mas inativa = Prospectar depois
- **Tier 3**: Sem presença = último

**Ação sua**: Copiar seus 50-100 contatos + classificar tier (2 horas max)

---

### PASSO 2: Validar E-mails com Hunter.io

1. **Criar conta** em hunter.io (grátis)
2. **Upload** da lista do Google Sheets
3. **Deixar rodar** → Valida e-mails, encontra faltantes
4. **Copiar resultado** de volta para o Google Sheets

**Tempo**: 45 minutos

---

### PASSO 3: Montar N8N (Automação)

N8N é uma ferramenta que conecta sistemas. Você vai:

1. **Instalar N8N** (docker ou cloud)
   - Opção fácil: Usar N8N Cloud (pago, $10/mês)
   - Opção gratuita: Self-hosted via Docker (grátis, mas setup técnico)

2. **Criar 3 Workflows automáticos:**

   **WORKFLOW 1: LinkedIn Connector (Dia 1)**
   - Trigger: Novo contato com Tier 1 no Sheets
   - Action: Conectar LinkedIn (via API ou manual com aviso)
   - Log: Registrar em Pipedrive

   **WORKFLOW 2: E-mail Automático (Dia 3)**
   - Trigger: LinkedIn conectado + 2 dias passaram
   - Action: Enviar e-mail educativo (via Gmail API)
   - Personalizar: Nome, especialidade, pain point
   - Log: Registrar tentativa em Pipedrive

   **WORKFLOW 3: WhatsApp Follow-up (Dia 6)**
   - Trigger: Nenhuma resposta ao e-mail
   - Action: Enviar WhatsApp (via Twilio)
   - Log: Registrar em Pipedrive

---

### PASSO 4: Configurar Pipedrive (CRM)

1. **Criar conta** em pipedrive.com
2. **Customizar Pipeline:**
   - Stage 1: Prospect (contato feito)
   - Stage 2: Qualificado (respondeu)
   - Stage 3: Reunião Agendada
   - Stage 4: Proposta Enviada
   - Stage 5: Contrato Fechado

3. **Integrar com N8N:**
   - Cada resposta do contato → Pipedrive atualiza automaticamente
   - Você vê em tempo real quem respondeu

---

## 💬 FASE 2: PERSONALIZAÇÃO DAS MENSAGENS (Dia 3, ~2 horas)

### Template 1: E-mail (Dia 3)

**ASSUNTO** (varia por Tier):
- Tier 1: "Prescritor que cresce não faz assim 👀"
- Tier 2: "As melhores estratégias de cannabis em 2026"
- Tier 3: "Achei seu perfil e precisamos conversar"

**CORPO** (template com variáveis):

```
Oi [Nome],

Achei seu LinkedIn e vi que você trabalha com [especialidade].

[PARÁGRAFO 1 - PERSONALIZADO por especialidade]
Se você trabalha com [RheumaSI/Derm/Neuro], sabe que cannabis medicinal
é o futuro. Mas 80% dos prescritores NÃO conseguem explicar isso
de forma científica (sem parecer ativista).

[PARÁGRAFO 2 - TOCA NO PAIN POINT]
O resultado? Poucos pacientes chegam. Poucos recomendam.
Faturamento fica estagnado.

[PARÁGRAFO 3 - VOCÊ COMO SOLUÇÃO]
Sou Katharine, profissional de saúde + estrategista digital.
Ajudo prescritores a estruturar presença profissional e crescer.

[PARÁGRAFO 4 - CALL-TO-ACTION]
Montei um briefing de 5 páginas: "3 Tendências que Diferenciam
Prescritores que Crescem". É a realidade que está acontecendo agora.

Quer que eu envie?

Abs,
Katharine Rodrigues
[WhatsApp]
[LinkedIn]
```

---

### Template 2: WhatsApp (Dia 6, se sem resposta)

```
Oi [Nome], tudo bem? 👋

Vi que você não viu meu e-mail (ou tá lotado mesmo).

Mas achei que você gostaria de saber como os melhores prescritores
estão crescendo em 2026.

Marquei uns 30min na agenda. Você teria terça ou quarta?

Abçs 🙌
```

---

## 📈 FASE 3: AUTOMAÇÃO + MONITORAMENTO (Rodando)

### O que roda automático:

✅ **Dia 1**: Conectar com 5 contatos Tier 1 no LinkedIn
✅ **Dia 3**: Enviar e-mail educativo
✅ **Dia 6**: Enviar WhatsApp (se sem resposta)
✅ **Todo dia**: Log de atividade em Pipedrive

### O que você faz:

📌 **Diariamente (15 min):**
- Abrir Pipedrive
- Ver quem respondeu
- Agendar conversas 1:1

📌 **2-3x por semana (1-2h):**
- Conversa 1:1 com qualificados
- Demonstrar expertise
- Propor sessão estratégica

---

## 🎯 MÉTRICAS QUE VOCÊ ACOMPANHA

| Métrica | Meta em 30 dias | Meta em 90 dias |
|---------|-----------------|-----------------|
| Contatos prospectados | 50 | 150 |
| Taxa de resposta | 5-10% | 5-10% |
| Conversas agendadas | 3-5 | 12-15 |
| Propostas enviadas | 2 | 5-6 |
| Contratos fechados | 1 | 3 |
| Receita gerada | R$ 4.000 | R$ 12.000 |

---

## ⚠️ PONTOS LEGAIS & CONFORMIDADE

### LGPD (Lei Geral de Proteção de Dados)

✅ **O que você PODE fazer:**
- Usar dados públicos (LinkedIn, CFM)
- Enviar e-mail educativo (não é spam se é relevante)
- Rastrear abertura de e-mail

❌ **O que você NÃO PODE fazer:**
- Vender lista de contatos
- Enviar WhatsApp sem prévia autorização (use após e-mail responder)
- Compartilhar dados sem consentimento

**Solução**: Você quer dados de dados "consentidos" (que responderam).

### Marketing Médico

⚠️ **Cuidado**: Não é como marketing consumer. Médicos têm regras.
- Conteúdo educativo é OK
- Venda agressiva é ruim
- Você está no caminho certo: educação → qualificação → venda

---

## 🛠️ IMPLEMENTAÇÃO PRÁTICA

### Se você é técnica:

**Opção 1**: Self-hosted (gratuita, mas setup)
- Docker + N8N + Google Sheets + Pipedrive
- Tempo setup: 4-6 horas

**Opção 2**: N8N Cloud (paga, mas rápida)
- N8N Cloud + Google Sheets + Pipedrive
- Tempo setup: 2-3 horas

### Se você não é técnica:

**Opção**: Contratar um dev para setup
- Budget: R$ 800-1.500 (one-time)
- Tempo dele: 4-6 horas
- Depois você gerencia via interface simples

---

## 📅 CRONOGRAMA DE IMPLEMENTAÇÃO

| Semana | O quê | Quem | Tempo |
|--------|-------|------|--------|
| **1** | Setup Google Sheets + Hunter.io + N8N | Você | 4-5h |
| **1** | Setup Pipedrive + integrações | Dev (se contratar) | 3-4h |
| **2** | Criar templates mensagens | Você | 2h |
| **2** | Começar prospecting Tier 1 (manual + auto) | Você + Agente | 2h/semana |
| **3-4** | Qualificação + conversas 1:1 | Você | 5-10h/semana |

---

## 🎁 O QUE VOCÊ GANHA

✨ **Agente que faz 80% do trabalho:**
- Valida dados
- Envia mensagens personalizadas em sequência
- Rastreia respostas
- Te avisa quando há qualificado para você agir

✨ **Você foca em 20% do trabalho:**
- Qualificação profunda (conversa 1:1)
- Demonstração de expertise
- Fechamento de contratos

✨ **Resultado esperado em 90 dias:**
- 3 contratos de R$ 4.000+ = R$ 12.000/mês
- Modelo pronto para escalar
- Sistema que roda sozinho

---

## ❓ PRÓXIMAS QUESTÕES

1. Você prefere **self-hosted gratuito** ou **N8N Cloud paga**?
2. Você conhece técnico que possa fazer setup, ou eu recomendo alguém?
3. Quer que eu customize os templates AGORA com sua voz?

**Respond aqui e vamos rodar!**
