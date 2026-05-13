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


def fetch_recent_news() -> list:
    """Fetch this week's news about cannabis medicinal from PRINCIPAIS countries + Europe"""
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        print("⚠ NEWSAPI_KEY not set — usando conhecimento base do Claude")
        return []

    try:
        from datetime import datetime, timedelta

        # Get news from last 14 days (wider range for international coverage)
        today = datetime.utcnow()
        two_weeks_ago = today - timedelta(days=14)
        from_date = two_weeks_ago.strftime("%Y-%m-%d")

        base_url = "https://newsapi.org/v2/everything"

        # PRINCIPAIS countries + rest of Europe
        # Priority order: Brasil, UK, Spain, Netherlands, Germany, then rest of Europe
        queries = [
            # BRASIL (Portuguese)
            ("cannabis medicinal regulação Brasil", "pt"),
            ("cannabis medicinal pesquisa Brasil", "pt"),
            ("cannabis medicinal mercado Brasil", "pt"),

            # UK (English)
            ("medical cannabis UK regulation", "en"),
            ("cannabis medicinal research UK", "en"),

            # ESPAÑA (Spanish)
            ("cannabis medicinal regulación España", "es"),
            ("cannabis medicinal investigación España", "es"),

            # NETHERLANDS (English/Dutch focus)
            ("medical cannabis Netherlands", "en"),
            ("cannabis regulation Netherlands", "en"),

            # DEUTSCHLAND (English/German focus)
            ("medical cannabis Germany regulation", "en"),
            ("cannabis medicinal Deutschland", "de"),

            # EUROPA GERAL (English)
            ("medical cannabis Europe 2026", "en"),
            ("cannabis medicinal European regulation", "en"),
            ("cannabis research Europe 2026", "en"),
        ]

        all_articles = []
        article_count = 0

        for query, language in queries:
            params = {
                "q": query,
                "from": from_date,
                "sortBy": "publishedAt",
                "pageSize": 15,
                "language": language,
                "apiKey": api_key
            }

            try:
                response = requests.get(base_url, params=params, timeout=10)
                if response.status_code == 200:
                    articles = response.json().get("articles", [])
                    all_articles.extend(articles)
                    article_count += len(articles)
                    print(f"✓ {len(articles)} articles: '{query}' ({language})")
                else:
                    print(f"⚠ Error '{query}': {response.status_code}")
            except Exception as e:
                print(f"⚠ Failed '{query}': {e}")

        # Remove duplicates by URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            url = article.get("url")
            if url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)

        # Sort by date (newest first)
        unique_articles.sort(
            key=lambda x: x.get("publishedAt", ""),
            reverse=True
        )

        print(f"✓ Total: {len(unique_articles)} unique articles from Brasil, UK, Spain, Netherlands, Germany + Europe")
        return unique_articles[:30]  # Top 30

    except Exception as e:
        print(f"✗ Error fetching news: {e}")
        return []


def generate_briefing() -> str:
    """Generate briefing using Claude"""
    # Fetch recent news
    recent_news = fetch_recent_news()

    news_context = ""
    if recent_news:
        news_context = "\n\nNOTÍCIAS RECENTES PARA ANÁLISE:\n"
        for i, article in enumerate(recent_news[:10], 1):
            news_context += f"\n{i}. {article.get('title', 'Sem título')}\n"
            news_context += f"   Fonte: {article.get('source', {}).get('name', 'Unknown')}\n"
            news_context += f"   Data: {article.get('publishedAt', 'Unknown')}\n"
            if article.get('description'):
                news_context += f"   Resumo: {article['description'][:200]}...\n"

    prompt = f"""Você é REPÓRTER INTERNACIONAL da newsletter "Mundo Cannabis" — cobertura de cannabis medicinal para médicos prescritores globais, escrita por Katharine Louise.

COBERTURA GEOGRÁFICA (PRIORIDADE):
🇧🇷 BRASIL (prioridade 1)
🇬🇧 UK (prioridade 1)
🇪🇸 ESPANHA (prioridade 1)
🇳🇱 HOLANDA (prioridade 1)
🇩🇪 ALEMANHA (prioridade 1)
🇪🇺 Resto da Europa (prioridade 2)

SUA MISSÃO ESTA SEMANA:
Analisar as notícias DOS ÚLTIMOS 14 DIAS fornecidas abaixo e montar um BRIEFING JORNALÍSTICO INTERNACIONAL — não é análise especulativa, é cobertura de fatos reais que aconteceram no mundo.

REGRAS DE SELEÇÃO (Prioridade absoluta):
1. Escolha as 5-8 histórias MAIS RELEVANTES (priorizando países principais)
2. PRIORIZE:
   - Regulação cannabis medicinal (Brasil, UK, Espanha, Holanda, Alemanha)
   - Evidência científica nova (pesquisa, estudos clínicos)
   - Mercado e tendências internacionais
   - Oportunidades de posicionamento global para médicos
3. DESCARTE:
   - Sensacionalismo ou "lifestyle cannabis"
   - Conteúdo não-medicinal
   - Notícias duplicadas
   - Notícias sem data ou muito antigas

TOM JORNALÍSTICO PROFISSIONAL:
- Analítico, assertivo, baseado em fatos verificados
- Contexto internacional: por que isso importa para médicos em diferentes países?
- Estrutura: fato → contexto → implicação prática
- Oportunidade: identifique oportunidades de posicionamento ou movimento de mercado

CRITÉRIO ABSOLUTO:
Você é uma repórter cobrindo cannabis medicinal GLOBALMENTE. Cada história deve responder: "Por que um médico que atua nessa área precisa saber disso?"

NOTÍCIAS DOS ÚLTIMOS 14 DIAS (Brasil, UK, Espanha, Holanda, Alemanha + Europa):
{news_context}

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
            model="claude-opus-4-1",
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
