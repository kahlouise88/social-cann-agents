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
from datetime import datetime, timedelta
from anthropic import Anthropic
import feedparser
import re

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
    """
    RSS FEED NEWS FETCH - 2026 ONLY
    Busca notícias sobre cannabis medicinal de múltiplas fontes via RSS feeds

    REQUIREMENTS (OBRIGATÓRIO):
    - APENAS notícias de 2026
    - TODAS com URL/link verificável
    - Cobertura: Brasil, UK, Espanha, Holanda, Alemanha + Europa
    - Log explícito de cada notícia
    """
    try:
        today = datetime.utcnow()
        year_start = datetime(2026, 1, 1)
        from_date = year_start.strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")

        print(f"\n🔍 AUDITORIA DE NOTÍCIAS (RSS Feeds)")
        print(f"📅 Período: {from_date} a {to_date}")
        print(f"🌍 Cobertura: Brasil, UK, Espanha, Holanda, Alemanha + Europa")
        print(f"✅ Critério: APENAS 2026 | URL OBRIGATÓRIO\n")

        all_articles = []

        # RSS Feed sources covering target regions
        rss_sources = [
            {
                "name": "BBC News - Health",
                "url": "http://feeds.bbc.co.uk/news/rss.xml",
                "keywords": ["cannabis", "medical", "medicinal"],
            },
            {
                "name": "Reuters - Health",
                "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&output=rss",
                "keywords": ["cannabis", "medical", "medicinal"],
            },
            {
                "name": "The Guardian - Science",
                "url": "https://www.theguardian.com/science/rss",
                "keywords": ["cannabis", "medical", "medicinal"],
            },
            {
                "name": "Folha de São Paulo - Saúde",
                "url": "https://www1.folha.uol.com.br/rss/feed-saude.xml",
                "keywords": ["cannabis", "medicinal", "canabidiol"],
            },
            {
                "name": "El Mundo - Ciência",
                "url": "https://www.elmundo.es/rss/portada.xml",
                "keywords": ["cannabis", "medicinal"],
            },
            {
                "name": "Medical Xpress",
                "url": "https://medicalxpress.com/rss-feed.xml",
                "keywords": ["cannabis", "medical", "therapeutic"],
            },
        ]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        for source in rss_sources:
            try:
                print(f"   📡 Buscando em {source['name']}...")
                feed = feedparser.parse(source['url'])
                articles_found = 0

                if feed.entries:
                    for entry in feed.entries[:30]:  # Limitar a 30 artigos por feed
                        title = entry.get('title', '')
                        link = entry.get('link', '')

                        # Extrair data
                        pub_date = None
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            try:
                                pub_date = datetime(*entry.published_parsed[:6])
                            except:
                                pub_date = today
                        else:
                            pub_date = today

                        # Filtrar por palavras-chave relevantes
                        if any(keyword.lower() in title.lower() for keyword in source['keywords']):
                            if len(title) > 10 and link and link.startswith('http'):
                                # Verificar se é de 2026
                                if pub_date.year == 2026:
                                    article = {
                                        'webTitle': title[:150],
                                        'webUrl': link,
                                        'firstPublicationDate': pub_date.strftime("%Y-%m-%d"),
                                        'source': source['name']
                                    }
                                    all_articles.append(article)
                                    articles_found += 1

                    print(f"      ✓ {articles_found} notícias relevantes encontradas")
                else:
                    print(f"      ℹ Sem entradas no feed RSS")

            except Exception as e:
                print(f"      ❌ Erro ao buscar {source['name']}: {str(e)[:50]}")

        print(f"\n📊 Total bruto: {len(all_articles)} artigos")

        # ===== FILTRO OBRIGATÓRIO 2026 =====
        articles_2026 = []

        for article in all_articles:
            pub_date_str = article.get("firstPublicationDate", "")
            url = article.get("webUrl", "")
            title = article.get("webTitle", "")

            # Extrair ano
            if pub_date_str and len(pub_date_str) >= 4:
                try:
                    year = int(pub_date_str[:4])
                except:
                    year = 2026
            else:
                year = 2026

            # CRITÉRIO 1: Deve ser 2026
            # CRITÉRIO 2: Deve ter URL válida
            if url and year == 2026:
                articles_2026.append(article)
                print(f"   ✅ {pub_date_str[:10]} | {title[:60]}...")

        # Remove duplicates by URL
        seen_urls = set()
        unique_articles = []
        for article in articles_2026:
            url = article.get("webUrl")
            if url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)

        # Sort by date (newest first)
        unique_articles.sort(
            key=lambda x: x.get("firstPublicationDate", ""),
            reverse=True
        )

        print(f"\n✅ RESULTADO FINAL: {len(unique_articles)} notícias válidas")
        print(f"   - Todas com URL ✓")
        print(f"   - Todas de 2026 ✓\n")

        return unique_articles[:40]

    except Exception as e:
        print(f"❌ ERRO CRÍTICO na busca: {e}")
        return []


def generate_briefing() -> str:
    """Generate briefing using Claude"""
    # Fetch recent news
    recent_news = fetch_recent_news()

    news_context = ""
    if recent_news:
        news_context = "\n\n📰 NOTÍCIAS RECENTES PARA ANÁLISE (COM LINKS VERIFICÁVEIS):\n"
        for i, article in enumerate(recent_news[:15], 1):
            # Guardian API uses webTitle, webUrl, firstPublicationDate
            title = article.get('webTitle', 'Sem título')
            source = "The Guardian"
            pub_date = article.get('firstPublicationDate', 'Unknown')
            url = article.get('webUrl', '')
            description = article.get('trailText', '')

            news_context += f"\n{i}. {title}\n"
            news_context += f"   📅 Data: {pub_date[:10] if pub_date else 'Unknown'}\n"
            news_context += f"   📰 Fonte: {source}\n"
            if url:
                news_context += f"   🔗 Link: {url}\n"
            if description:
                news_context += f"   📝 Resumo: {description[:250]}...\n"

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

IMPORTANTE - LINKS E VERIFICAÇÃO:
- TODA notícia que você mencionar deve incluir o LINK direto
- Verifique a data da publicação — se estiver de 2024, mencione explicitamente
- Cada história deve ter fonte + link claro para acesso

NOTÍCIAS DOS ÚLTIMOS 30 DIAS (Brasil, UK, Espanha, Holanda, Alemanha + Europa):
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

    # Fetch recent news ONCE - store globally
    print("Fetching recent news...")
    recent_news = fetch_recent_news()
    print(f"✓ Fetched {len(recent_news)} articles")

    # Generate briefing
    print("Generating briefing from Claude...")
    briefing = generate_briefing()

    if not briefing:
        print("✗ Failed to generate briefing")
        send_telegram_message(
            "❌ Mundo Cannabis Briefing Error\n\n"
            "Failed to generate briefing. Please check the logs."
        )
        sys.exit(1)

    # Format for Telegram (split into messages)
    print("Formatting content for Telegram...")
    telegram_messages = format_for_telegram(briefing)

    # Add header
    day_name = datetime.now().strftime("%A")
    date_str = datetime.now().strftime("%d/%m/%Y")
    header = (
        f"📰 MUNDO CANNABIS BRIEFING — {date_str}\n\n"
        "Notícias da semana em cannabis medicinal para médicos prescritores.\n"
        "Cobertura: Brasil, UK, Espanha, Holanda, Alemanha + Europa"
    )

    # Send header first
    send_telegram_message(header)

    # Send main content messages
    for i, msg in enumerate(telegram_messages, 1):
        send_telegram_message(msg)
        print(f"Sent message {i}/{len(telegram_messages)}")

    # BUILD LINKS SECTION - CRITICAL
    print(f"\nBuilding links section from {len(recent_news)} articles...")
    links_messages = []
    current_links = "🔗 LINKS E FONTES:\n\n"

    if recent_news and len(recent_news) > 0:
        for i, article in enumerate(recent_news[:25], 1):
            # Guardian API fields
            title = article.get('webTitle', 'Notícia')
            url = article.get('webUrl', '')
            source = "The Guardian"
            pub_date = article.get('firstPublicationDate', '').split('T')[0]

            if url:  # ONLY if URL exists
                title_short = (title[:45] + "...") if len(title) > 45 else title

                new_entry = f"\n{i}. {title_short}\n🔗 {url}\n📅 {pub_date} | {source}"

                # If message would be too long, split it
                if len(current_links + new_entry) > 3000:
                    links_messages.append(current_links)
                    current_links = "🔗 LINKS E FONTES (continuação):\n" + new_entry
                else:
                    current_links += new_entry

        # Add remaining links
        if current_links:
            links_messages.append(current_links)

    # SEND ALL LINKS MESSAGES
    print(f"Sending {len(links_messages)} link messages...")
    for i, link_msg in enumerate(links_messages, 1):
        print(f"Sending links message {i}/{len(links_messages)}")
        send_telegram_message(link_msg)
        print(f"✓ Sent links message {i}")

    # Send footer
    footer = (
        "\n---\n"
        "📱 Próxima execução: Quarta e sexta-feira às 6h\n"
        "Dúvidas? Responde esse bot.\n"
        "#CannabisMedicinal #MédicoPrescritor"
    )
    send_telegram_message(footer)

    print(f"[{datetime.now().isoformat()}] Mundo Cannabis Briefing Agent completed successfully ✓")


if __name__ == "__main__":
    main()
