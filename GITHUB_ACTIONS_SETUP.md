# GitHub Actions Setup — Social Cann Agents

Este documento explica como configurar os GitHub Actions para rodar os agentes automaticamente na nuvem.

## Agentes Implementados

### 1. Cannabis Market Updates Agent
- **Frequência:** 1º e 15º de cada mês, às 6h UTC (3h BRT)
- **Função:** Encontra oportunidades de trabalho freelance em medical writing, UGC e conteúdo de saúde relacionado a cannabis
- **Entrega:** Telegram (4 mensagens estruturadas)
- **Workflow:** `.github/workflows/cannabis-market-updates.yml`

### 2. Mundo Cannabis Briefing Agent
- **Frequência:** Quarta e sexta-feira às 6h UTC (3h BRT)
- **Função:** Pesquisa e cura notícias sobre cannabis medicinal no Brasil e mundialmente
- **Entrega:** Telegram (3 mensagens estruturadas)
- **Workflow:** `.github/workflows/mundo-cannabis-briefing.yml`

---

## Como Configurar

### Passo 1: Adicionar GitHub Secrets

Os agentes precisam de 3 secrets configurados no repositório:

1. **ANTHROPIC_API_KEY** — Sua chave da API Anthropic
2. **TELEGRAM_BOT_TOKEN** — Token do Telegram bot (8888970813)
3. **TELEGRAM_CHAT_ID** — ID do chat Telegram (8334667802)

**Como adicionar:**

1. Vá para: `https://github.com/kahlouise88/social-cann-agents/settings/secrets/actions`
2. Clique em "New repository secret"
3. Adicione cada secret:
   - Name: `ANTHROPIC_API_KEY` → Value: [sua chave]
   - Name: `TELEGRAM_BOT_TOKEN` → Value: `8888970813`
   - Name: `TELEGRAM_CHAT_ID` → Value: `8334667802`

### Passo 2: Ativar GitHub Actions

1. Vá para: `https://github.com/kahlouise88/social-cann-agents/actions`
2. Clique em "Enable GitHub Actions" (se necessário)

### Passo 3: Testar os Workflows

Você pode rodar os agentes manualmente para testar:

1. Vá para: `https://github.com/kahlouise88/social-cann-agents/actions`
2. Selecione o workflow
3. Clique em "Run workflow" → "Run workflow"

---

## Como os Workflows Funcionam

### Estrutura

```yaml
on:
  schedule:
    - cron: '0 6 * * 1,15'  # Exemplo: 1º e 15º às 6h UTC
  workflow_dispatch:        # Permite rodar manualmente
```

### Passos Executados

1. ✅ Fazer checkout do código
2. ✅ Instalar Python 3.11
3. ✅ Instalar dependências (`pip install -r requirements.txt`)
4. ✅ Executar o script Python do agente
5. ✅ Script chama Claude API para gerar conteúdo
6. ✅ Script envia mensagens para Telegram

---

## Timezone — IMPORTANTE ⏰

Os workflows rodam em **UTC**. Você configurou `cron: '0 6 * * ...'` que significa **6h UTC**.

**Conversão para horários brasileiros:**
- 6h UTC = 3h BRT (horário de Brasília, em horário padrão)
- 6h UTC = 2h BRST (horário de Brasília, em horário de verão)

**Se você quer um horário diferente:**

Altere o valor do cron em `.github/workflows/*.yml`:

```yaml
# Exemplo: 9h UTC (6h BRT)
- cron: '0 9 * * 3,5'

# Exemplo: 11h UTC (8h BRT)
- cron: '0 11 * * 3,5'
```

---

## Monitorar Execução

### Ver logs dos workflows

1. Vá para: `https://github.com/kahlouise88/social-cann-agents/actions`
2. Clique no workflow que rodou
3. Clique no job
4. Veja o output em tempo real

### Verificar se as mensagens chegaram no Telegram

As mensagens devem aparecer no chat Telegram configurado (ID: 8334667802).

Se não chegarem:
1. Verificar os logs do GitHub Actions
2. Testar manualmente: `curl https://api.telegram.org/bot8888970813/sendMessage -d "chat_id=8334667802&text=test"`

---

## Variáveis de Ambiente

Os scripts usam 3 variáveis que o GitHub Actions injeta automaticamente:

```python
ANTHROPIC_API_KEY     # Sua chave da API Anthropic
TELEGRAM_BOT_TOKEN    # Token do bot Telegram
TELEGRAM_CHAT_ID      # ID do chat para enviar mensagens
```

---

## Troubleshooting

### "Secret not found"
- Certifique-se de adicionar as 3 secrets em Settings → Secrets
- Os nomes precisam estar **exatos** (case-sensitive)

### "ModuleNotFoundError: No module named 'anthropic'"
- O pip install está falhando
- Verifique se `requirements.txt` está correto
- Veja o log completo em Actions

### "Telegram message failed to send"
- Verifique se `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` estão corretos
- Teste manualmente o bot com um curl

### Workflow não executa no horário marcado
- GitHub Actions tem alguns minutos de atraso
- Schedules são run em "best effort" — nem sempre no minuto exato
- Se precisar de execução rigorosa, considere usar um serviço específico (AWS EventBridge, etc)

---

## Próximos Passos

1. ✅ Adicionar os 3 GitHub Secrets
2. ✅ Testar rodar um workflow manualmente
3. ✅ Verificar se mensagens chegam no Telegram
4. ✅ Ajustar timezone se necessário
5. ✅ Deixar rodando automaticamente

---

## Comandos Úteis (GitHub CLI)

Se você quer gerenciar via `gh` CLI:

```bash
# Ver todos os workflows
gh workflow list --repo kahlouise88/social-cann-agents

# Rodar um workflow específico
gh workflow run cannabis-market-updates.yml --repo kahlouise88/social-cann-agents

# Ver execuções recentes
gh run list --repo kahlouise88/social-cann-agents

# Ver logs de uma execução
gh run view <RUN_ID> --repo kahlouise88/social-cann-agents --log
```

---

*Documentação criada em 2025 | Social Cann Agents*
