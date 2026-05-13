#!/usr/bin/env python3
"""
Mundo Cannabis Briefing Agent
Curates cannabis medicinal news from Brazil and worldwide
Generates newsletter content for Instagram/newsletter/YouTube
Delivers to Telegram every Wednesday and Friday
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


def generate_briefing() -> str:
    """Generate briefing using Claude"""
    prompt = """Você é o redator da newsletter semanal "Mundo Cannabis" — curadoria de cannabis medicinal para médicos prescritores no Brasil, escrita por Katharine Louise.

Seu trabalho esta semana: pesquisar as notícias mais recentes sobre cannabis medicinal no Brasil e mundialmente, e montar um briefing estruturado pronto para a newsletter.

REGRAS DE SELEÇÃO DE HISTÓRIAS:
1. Escolha as 5-7 notícias mais relevantes para médicos prescritores brasileiros
2. Priorize: regulação Brasil > evidência científica nova > mercado e tendências > contexto global
3. Descarte: notícias muito internacionais sem impacto direto no Brasil, repetições de semanas anteriores, boatos não verificados

REGRAS DE PESQUISA:
- Use seu conhecimento até a data de corte (setembro 2024)
- Se não souber de notícias muito recentes, seja honesto sobre isso
- Priorize fontes confiáveis: Agência Brasil, CNPL, Anvisa, Lancet, Nature, NEJM, ScienceDaily

ESTRUTURA OBRIGATÓRIA DO BRIEFING:

---
**DATA:** [data de hoje]

**NOTÍCIAS PRINCIPAIS:**

**[Número]. [Título da Notícia]**
- Relevância: [Alta / Média / Baixa]
- Fonte: [nome e link se possível]
- O que é: [1 parágrafo resumo]
- Por que importa para médicos prescritores: [2-3 linhas]

---

DEPOIS DO BRIEFING, INCLUA:

**ANÁLISE SEMANAL:**
- Movimento regulatório Brasil (se houver)
- Descoberta científica destaque
- Oportunidade de posicionamento para médicos

**PRÓXIMOS PASSOS SUGERIDOS:**
- Qual tópico merecia um post no Instagram
- Qual merecia aprofundamento em newsletter
- Qual é o ângulo estratégico

---

RESULTADO ESPERADO:
Um briefing de 5-7 notícias estruturadas, verificadas, prontas para transformar em conteúdo semanal para Instagram, newsletter e YouTube.

Comece a pesquisa agora."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except Exception as e:
        print(f"✗ Error calling Claude API: {e}")
        return None


def format_for_telegram(content: str) -> list:
    """Format the content into 3 sequential Telegram messages"""
    # Split content into logical sections
    # Message 1: Header + top stories
    # Message 2: Middle stories
    # Message 3: Analysis + recommendations

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
            if message_count >= 3:  # Max 3 messages
                break

        current_message += line + "\n"

    if current_message and message_count < 3:
        messages.append(current_message.strip())

    # Ensure we have at least a message to send
    if not messages:
        messages = [content]

    return messages


def main():
    """Main function"""
    print(f"[{datetime.now().isoformat()}] Starting Mundo Cannabis Briefing Agent...")

    # Generate briefing
    print("Generating briefing from Claude...")
    briefing = generate_briefing()

    if not briefing:
        print("✗ Failed to generate briefing")
        send_telegram_message(
            "❌ <b>Mundo Cannabis Briefing Error</b>\n\n"
            "Failed to generate briefing. Please check the logs.",
            parse_mode="HTML",
        )
        sys.exit(1)

    # Format for Telegram (split into messages)
    print("Formatting content for Telegram...")
    telegram_messages = format_for_telegram(briefing)

    # Add header
    day_name = datetime.now().strftime("%A")
    date_str = datetime.now().strftime("%d/%m/%Y")
    header = (
        f"📰 <b>Mundo Cannabis Briefing — {date_str}</b>\n\n"
        "Notícias da semana em cannabis medicinal para médicos prescritores.\n"
        "Tom: analítico · estratégico · sóbrio · baseado em evidência.\n\n"
    )

    # Send header first
    send_telegram_message(header, parse_mode="HTML")

    # Send main content messages
    for i, msg in enumerate(telegram_messages, 1):
        send_telegram_message(msg, parse_mode="HTML")
        print(f"Sent message {i}/{len(telegram_messages)}")

    # Send footer
    footer = (
        "\n---\n"
        "📱 <b>Próxima execução:</b> Quarta e sexta-feira às 6h\n"
        "✉️ Tem uma questão sobre cannabis medicinal? Responde esse bot.\n"
        "#CannabisMedicinal #MédicoPrescritor #CannabisNoBrasil"
    )
    send_telegram_message(footer, parse_mode="HTML")

    print(f"[{datetime.now().isoformat()}] Mundo Cannabis Briefing Agent completed successfully ✓")


if __name__ == "__main__":
    main()
