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

def fetch_rss_items(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    items = []
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
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
        
        # Build strict EEAT Prompt
        prompt = f"""
Atue como um jornalista experiente e curador de conteúdo sênior de um portal de notícias de alta credibilidade (ex: G1, Reuters, Estadão).
Sua tarefa é analisar a notícia bruta abaixo e escrever uma reportagem original, completa e aprofundada. O Google valoriza conteúdo EEAT (Experiência, Especialidade, Autoridade, Confiança). Não faça um resumo raso ou clichê.

FATO BRUTO:
Título Original: {original_title}
Descrição Original/Resumo: {item['description']}
Fonte: {item['link']}

INSTRUÇÕES DE REDAÇÃO (CRÍTICO PARA ADSENSE):
1. **Análise Crítica:** Identifique os pontos factuais mais importantes. Ignore opiniões ou ruídos.
2. **Reescrita Original:** NUNCA copie frases inteiras do original. Escreva com suas próprias palavras. Adicione contexto, explique o impacto desse fato para a sociedade/mercado e faça perguntas retóricas para engajar o leitor. Inclua citações simuladas/parafraseadas verossímeis de especialistas para dar peso à matéria.
3. **Tom e Voz:** Informativo, profissional, isento e cativante. Evite adjetivos emocionais e chavões de IA (como "Em suma", "Explore essa jornada").
4. **Formato Exigido:** O artigo DEVE ter mais de 500 palavras e usar marcações Markdown autênticas: H1 para título, H2/H3 para subtítulos, negritos (**) em termos chave, e listas se apropriado.
5. **Estrutura do Texto:**
   - Manchete atrativa
   - Lide (Introdução direta)
   - Desenvolvimento aprofundado com subtítulos (O que aconteceu, Impacto, Contexto Histórico)
   - Conclusão / Desdobramentos futuros
   - **Fontes e Referências:** Obrigatório adicionar no final: "Fonte: [Nome do Veículo Original]({item['link']})"

Você deve retornar ESTRITAMENTE um objeto JSON válido (sem tags markdown na borda do JSON). Siga esta estrutura exata:
{{
    "title": "Novo título magnético e jornalístico (sem sensacionalismo)",
    "excerpt": "Linha fina / subtítulo em uma frase impactante (máx 160 caracteres)",
    "content": "O texto completo da reportagem formatado rigorosamente em Markdown autêntico (mínimo de 500 palavras, com H2, H3, negritos e seção de fontes no final).",
    "tags": ["array", "de", "strings", "contendo", "de 3 a 5 palavras-chave", "limpas", "curtas", "em minúsculas", "e muito precisas"],
    "keyword_imagem_ingles": "query em inglês curta (2 palavras) para o Pexels que defina bem o contexto visual da matéria"
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
