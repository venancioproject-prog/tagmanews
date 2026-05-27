import os
import sys
import json
import random
import urllib.request
import xml.etree.ElementTree as ET
import time
from publish import call_groq_api, publish_article

# Define our RSS sources mapped to our portal categories
RSS_FEEDS = {
    "Política": [
        "https://news.google.com/rss/search?q=Política+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml"
    ],
    "Economia": [
        "https://news.google.com/rss/search?q=Economia+Negócios+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "https://agenciabrasil.ebc.com.br/rss/economia/feed.xml"
    ],
    "Internacional": [
        "https://news.google.com/rss/search?q=Notícias+Internacionais&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "https://agenciabrasil.ebc.com.br/rss/internacional/feed.xml"
    ],
    "Esportes": [
        "https://news.google.com/rss/search?q=Esportes+Futebol+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "https://agenciabrasil.ebc.com.br/rss/esportes/feed.xml"
    ],
    "Cultura": [
        "https://news.google.com/rss/search?q=Cultura+Entretenimento+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    ],
    "Tecnologia": [
        "https://news.google.com/rss/search?q=Tecnologia+Inovação&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    ]
}

def get_existing_titles():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    posts_path = os.path.join(base_dir, 'posts.json')
    if os.path.exists(posts_path):
        with open(posts_path, 'r', encoding='utf-8') as f:
            try:
                posts = json.load(f)
                return [p.get('title', '').lower() for p in posts]
            except:
                return []
    return []

import requests

def fetch_rss_items(url):
    items = []
    try:
        response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        xml_data = response.content
        root = ET.fromstring(xml_data)
        channel = root.find('channel')
        if channel is not None:
            for item in channel.findall('item'):
                title = item.find('title')
                desc = item.find('description')
                link = item.find('link')
                if title is not None and desc is not None:
                    items.append({
                        'title': title.text,
                        'description': desc.text,
                        'link': link.text if link is not None else ""
                    })
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return items

def curate_and_publish(category, count=1):
    print(f"Starting curation for category: {category}")
    feeds = RSS_FEEDS.get(category, [])
    if not feeds:
        print("Invalid category.")
        return
    
    existing_titles = get_existing_titles()
    feed_url = random.choice(feeds)
    print(f"Fetching RSS: {feed_url}")
    
    items = fetch_rss_items(feed_url)
    
    published = 0
    for item in items:
        if published >= count:
            break
            
        original_title = item['title'].strip()
        # Basic uniqueness check
        if any(t in original_title.lower() for t in existing_titles) or any(original_title.lower() in t for t in existing_titles):
            continue
            
        print(f"Curating article: {original_title}")
        
        # Load advanced guidelines
        guidelines_path = os.path.join(os.path.dirname(__file__), 'prompt_guidelines.txt')
        advanced_guidelines = ""
        if os.path.exists(guidelines_path):
            with open(guidelines_path, 'r', encoding='utf-8') as gf:
                advanced_guidelines = gf.read()

        # Build strict EEAT Prompt
        prompt = f"""
{advanced_guidelines}

Atue como um jornalista experiente e curador de conteúdo sênior de um portal de notícias de alta credibilidade (ex: G1, Reuters, Estadão).
Sua tarefa é analisar a notícia bruta abaixo e escrever uma reportagem original, completa e aprofundada, APLICANDO RIGOROSAMENTE todas as regras de estilo e táticas avançadas (anti-detecção e tom cético) listadas acima.

FATO BRUTO:
Título Original: {original_title}
Descrição Original/Resumo: {item['description']}
Fonte: {item['link']}

INSTRUÇÕES DE REDAÇÃO ESTRUTURAL (CRÍTICO PARA ADSENSE):
1. **Análise Crítica e Contexto:** Identifique os fatos concretos. Explique o impacto do fato. Adicione perguntas retóricas para engajar.
2. **Sem Travessões:** Siga a regra de estilo estrita de JAMAIS usar travessões.
3. **Tom Orgânico e Cético:** Aplique o tom irônico e direto exigido nas regras. Evite enrolação.
4. **Formato Exigido:** O artigo DEVE ter entre 250 e 400 palavras. Jamais repita os mesmos parágrafos ou encha linguiça. Use marcações Markdown autênticas (H2/H3 para subtítulos, negritos em termos chave).
5. **Estrutura do Texto:**
   - Lide (Introdução direta)
   - Desenvolvimento objetivo com blocos variados
   - Conclusão / Provocação em aberto (NÃO RECAPITULE)
   - **Fontes e Referências:** Obrigatório adicionar no final: "Fonte: [Nome do Veículo Original]({item['link']})"

Você deve retornar ESTRITAMENTE um objeto JSON válido (sem tags markdown na borda do JSON). Siga esta estrutura exata:
{{
    "title": "Novo título magnético e jornalístico (sem sensacionalismo)",
    "excerpt": "Linha fina / subtítulo impactante (máx 160 caracteres)",
    "content": "O texto completo da reportagem em Markdown (seja conciso e coeso, H2, sem travessões, NUNCA REPITA PARÁGRAFOS).",
    "tags": ["array", "de", "strings", "contendo", "de 3 a 5 palavras-chave", "curtas"],
    "keyword_imagem_ingles": "query em inglês curta e CONCEITUAL (2 palavras) para ilustrar a matéria no Pexels (evite termos genéricos como news, jornalism)"
}}
"""
        try:
            response_text = call_groq_api(prompt, dense=False)
            data = json.loads(response_text)
            
            # Publish
            post_id = publish_article(
                title=data['title'],
                excerpt=data['excerpt'],
                content=data['content'],
                category=category,
                author="Redação Especial",
                tags=data.get('tags', [category.lower(), 'notícias', 'atualidades']),
                image_query=data.get('keyword_imagem_ingles', 'news press')
            )
            print(f"SUCCESS: Article published! ID: {post_id}")
            published += 1
            existing_titles.append(data['title'].lower())
            
            # Small delay if multiple to avoid rate limits
            if published < count:
                print("Waiting 15 seconds before next...")
                time.sleep(15)
                
        except Exception as e:
            print(f"FAILED to curate {original_title}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cat = sys.argv[1]
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        curate_and_publish(cat, count)
    else:
        print("Usage: python rss_news.py <Category> [count]")
