#!/usr/bin/env python3
"""
Cannabis Market Updates Agent
Finds freelance opportunities in medical writing, UGC, health/wellness content
related to cannabis in UK/USA/Canada/Europe
Delivers to Telegram on the 1st and 15th of each month
"""

import os
import sys
import requests
from datetime import datetime
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()

# Get credentials from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
    sys.exit(1)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_message(text: str, parse_mode: str = "HTML") -> bool:
    """Send a message to Telegram chat"""
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": parse_mode,
            },
            timeout=10,
        )
        if response.status_code == 200:
            print(f"✓ Message sent to Telegram")
            return True
        else:
            print(f"✗ Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error sending Telegram message: {e}")
        return False


def generate_market_updates() -> str:
    """Generate market updates using Claude"""
    prompt = """Você é um especialista em oportunidades de trabalho freelance para profissionais de saúde especializados em cannabis medicinal.

Sua missão: identificar e curar as 5 melhores oportunidades de trabalho freelance/projeto desta semana em:
- Medical writing (artigos, whitepapers, estudos de caso)
- UGC (conteúdo gerado por usuário) em cannabis medicinal
- Conteúdo de saúde e bem-estar relacionado a cannabis
- Consultoria para marcas de cannabis em mercados regulados

CONTEXTO:
- Perfil-alvo: Katharine Louise — enfermeira, especialista em cannabis medicinal, experiência internacional (Brasil, Europa), auditora ISO, contextos regulados e críticos
- Regiões: UK, USA, Canadá, Europa
- Plataformas: Upwork, Fiverr, LinkedIn, Toptal, Dribbble, Behance, Medium Publications, newsletters especializadas

FORMATO DE RESPOSTA (estruturado para cada oportunidade):

**[Número]. [Título da Oportunidade]**
- Plataforma: [onde está postada]
- Tipo: [medical writing / UGC / consultoria / conteúdo]
- Regiões: [UK / USA / Canada / Europa]
- Budget/Rate: [se informado]
- Por que é relevante para Katharine: [2-3 linhas conectando ao perfil dela]
- Link/Como aplicar: [instruções diretas]

---

CRITÉRIOS DE SELEÇÃO (priorizar):
1. Alinhamento com o perfil de Katharine (saúde + contexto regulado + autoridade)
2. Budget competitivo (acima da média para a área)
3. Oportunidades de longo prazo/recorrentes
4. Potencial para portfólio e case de sucesso
5. Envolvimento com educação de mercado (não apenas venda)

BUSCAR ATIVAMENTE EM:
- Upwork: buscar por "cannabis medicinal", "medical writing", "health content"
- LinkedIn: procurar por "Health Writer", "Cannabis Content", "Regulatory Compliance" (especialmente com marcas consolidadas)
- Newsletters especializadas (MJBizDaily, Cannabis Business Times, etc)
- Comunidades de profissionais de saúde (Reddit r/MedicalWriters, etc)

RESULTADO ESPERADO:
Uma lista de 5 oportunidades concretas, verificadas, com links diretos e análise de fit com o perfil da Katharine.
Se não encontrar 5 oportunidades qualificadas, liste as melhores que encontrar com honestidade.

Comece a busca agora e relate as oportunidades encontradas."""

    try:
        message = client.messages.create(
            model="claude-opus-4-1",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except Exception as e:
        print(f"✗ Error calling Claude API: {e}")
        return None


def format_for_telegram(content: str) -> list:
    """Format the content into 4 sequential Telegram messages"""
    # Split content into logical sections
    # Message 1: Header + intro
    # Message 2-3: Opportunities
    # Message 4: Footer

    lines = content.split("\n")
    messages = []

    current_message = ""
    message_count = 0
    max_length = 4096  # Telegram message limit

    for line in lines:
        if len(current_message) + len(line) + 1 > max_length and current_message:
            messages.append(current_message.strip())
            current_message = ""
            message_count += 1
            if message_count >= 4:  # Max 4 messages
                break

        current_message += line + "\n"

    if current_message and message_count < 4:
        messages.append(current_message.strip())

    # Ensure we have at least a message to send
    if not messages:
        messages = [content]

    return messages


def main():
    """Main function"""
    print(f"[{datetime.now().isoformat()}] Starting Cannabis Market Updates Agent...")

    # Generate market updates
    print("Generating market updates from Claude...")
    updates = generate_market_updates()

    if not updates:
        print("✗ Failed to generate market updates")
        send_telegram_message(
            "❌ <b>Cannabis Market Updates Agent Error</b>\n\n"
            "Failed to generate market updates. Please check the logs.",
            parse_mode="HTML",
        )
        sys.exit(1)

    # Format for Telegram (split into messages)
    print("Formatting content for Telegram...")
    telegram_messages = format_for_telegram(updates)

    # Add header and footer
    header = (
        f"🌿 <b>Cannabis Market Updates — {datetime.now().strftime('%d/%m/%Y')}</b>\n\n"
        "Oportunidades freelance desta semana em medical writing, UGC e saúde.\n"
    )

    footer = (
        "\n---\n"
        "📱 <b>Próxima execução:</b> 1º ou 15º do próximo mês\n"
        "✉️ Perguntas? Responde esse bot."
    )

    # Send header first
    send_telegram_message(header, parse_mode="HTML")

    # Send main content messages
    for i, msg in enumerate(telegram_messages, 1):
        send_telegram_message(msg, parse_mode="HTML")
        print(f"Sent message {i}/{len(telegram_messages)}")

    # Send footer
    send_telegram_message(footer, parse_mode="HTML")

    print(f"[{datetime.now().isoformat()}] Cannabis Market Updates Agent completed successfully ✓")


if __name__ == "__main__":
    main()
