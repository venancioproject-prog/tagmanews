import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error
import subprocess
from datetime import datetime

# Load environment variables manually from .env
def load_env():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    env_path = os.path.join(base_dir, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()

load_env()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

# Category fallback images
CATEGORY_FALLBACK_IMAGES = {
    'Política': 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=1200&auto=format&fit=crop',
    'Economia': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=1200&auto=format&fit=crop',
    'Internacional': 'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?q=80&w=1200&auto=format&fit=crop',
    'Esportes': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=1200&auto=format&fit=crop',
    'TV e Celebridades': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=1200&auto=format&fit=crop',
    'Música': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1200&auto=format&fit=crop',
    'Ciência': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop',
    'Geral': 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop'
}

# 1. Fetch image from Pexels API
def fetch_pexels_image(query, category="Geral"):
    if not PEXELS_API_KEY:
        print("Warning: PEXELS_API_KEY not found. Using fallback image.")
        return CATEGORY_FALLBACK_IMAGES.get(category, CATEGORY_FALLBACK_IMAGES['Geral'])
        
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.pexels.com/v1/search?query={encoded_query}&per_page=1"
        req = urllib.request.Request(url)
        req.add_header('Authorization', PEXELS_API_KEY)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('photos') and len(data['photos']) > 0:
                img_url = data['photos'][0]['src']['landscape']
                print(f"Pexels Image Found for '{query}': {img_url}")
                return img_url
    except Exception as e:
        print(f"Error fetching Pexels image for '{query}': {e}")
        
    print(f"Using category fallback image for {category}.")
    return CATEGORY_FALLBACK_IMAGES.get(category, CATEGORY_FALLBACK_IMAGES['Geral'])

# 2. Call Groq API completions
def call_groq_api(prompt, dense=False):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
        
    model = "llama-3.3-70b-versatile" if dense else "llama-3.1-8b-instant"
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um jornalista sênior de um portal de notícias de alta reputação.\n"
                    "Escreva com total imparcialidade técnica e tom jornalístico sério.\n"
                    "TRAVAS DE REDAÇÃO CRÍTICAS:\n"
                    "- NUNCA use adjetivos qualificadores (ex: fantástico, impressionante, crucial, fundamental).\n"
                    "- NUNCA termine com conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').\n"
                    "- NUNCA use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').\n"
                    "- Apresente apenas fatos objetivos e dados concretos.\n"
                    "- Retorne estritamente um JSON estruturado. Não use markdown codeblocks no JSON em si."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_content = res_data['choices'][0]['message']['content']
            return text_content
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error calling Groq API: {e.code} {e.reason}")
        print(f"Response Body: {error_body}")
        raise e
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        raise e

# 3. Clean strings for slugs
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

# 4. Generate sitemaps and RSS feed
def generate_sitemaps_and_rss(posts):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    site_url = "https://venancioproject-prog.github.io/tagma-portal" # Replace with actual dynamic url if available
    
    # 4.1. Generate sitemap.xml
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_xml += f'  <url>\n    <loc>{site_url}/index.html</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    
    for p in posts:
        sitemap_xml += f'  <url>\n    <loc>{site_url}/materia.html?id={p["id"]}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    
    # 4.2. Generate news-sitemap.xml (Google News standard: last 2 days of news only)
    news_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n'
    # Sort posts to put newest first (mock date sort)
    for p in posts[:15]:  # Google News sitemap lists last posts
        news_xml += f'  <url>\n    <loc>{site_url}/materia.html?id={p["id"]}</loc>\n'
        news_xml += '    <news:news>\n'
        news_xml += '      <news:publication>\n        <news:name>Tagma Notícias</news:name>\n        <news:language>pt</news:language>\n      </news:publication>\n'
        # Convert date to standard ISO 8601 if possible, fallback to now
        news_xml += f'      <news:publication_date>{datetime.now().strftime("%Y-%m-%d")}</news:publication_date>\n'
        news_xml += f'      <news:title><![CDATA[{p["title"]}]]></news:title>\n'
        news_xml += '    </news:news>\n  </url>\n'
    news_xml += '</urlset>'
    
    # 4.3. Generate rss.xml
    rss_xml = '<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n<channel>\n'
    rss_xml += '  <title>Tagma Notícias</title>\n'
    rss_xml += f'  <link>{site_url}</link>\n'
    rss_xml += '  <description>Informação com precisão, ética e independência.</description>\n'
    rss_xml += '  <language>pt-br</language>\n'
    
    for p in posts[:20]:
        rss_xml += '  <item>\n'
        rss_xml += f'    <title><![CDATA[{p["title"]}]]></title>\n'
        rss_xml += f'    <link>{site_url}/materia.html?id={p["id"]}</link>\n'
        rss_xml += f'    <description><![CDATA[{p["excerpt"]}]]></description>\n'
        rss_xml += f'    <category>{p["category"]}</category>\n'
        rss_xml += '  </item>\n'
    rss_xml += '</channel>\n</rss>'

    # Save to root and deploy folder
    for folder in [base_dir, os.path.join(base_dir, 'Tagma-V1-GitHubReady')]:
        if os.path.exists(folder):
            with open(os.path.join(folder, 'sitemap.xml'), 'w', encoding='utf-8') as f:
                f.write(sitemap_xml)
            with open(os.path.join(folder, 'news-sitemap.xml'), 'w', encoding='utf-8') as f:
                f.write(news_xml)
            with open(os.path.join(folder, 'rss.xml'), 'w', encoding='utf-8') as f:
                f.write(rss_xml)
                
    print("Sitemaps and RSS feed generated successfully in root and deploy folders.")

# 5. Core publish function
def publish_article(title, excerpt, content, category, author, tags, image_query):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    posts_json_path = os.path.join(base_dir, 'posts.json')
    deploy_posts_json_path = os.path.join(base_dir, 'Tagma-V1-GitHubReady', 'posts.json')
    
    # 5.1. Fetch high quality Pexels Image
    image_url = fetch_pexels_image(image_query, category)
    
    # 5.2. Create unique ID and slug
    post_id = "auto-" + str(int(datetime.now().timestamp()))
    slug = slugify(title)
    
    post_date = datetime.now().strftime("%d de %B de %Y").lower()
    # Translate month name to Portuguese standard
    months_pt = {
        'january': 'janeiro', 'february': 'fevereiro', 'march': 'março', 'april': 'abril',
        'may': 'maio', 'june': 'junho', 'july': 'julho', 'august': 'agosto',
        'september': 'setembro', 'october': 'outubro', 'november': 'novembro', 'december': 'dezembro'
    }
    for eng, pt in months_pt.items():
        post_date = post_date.replace(eng, pt)
        
    post_date = post_date.capitalize()
    
    # 5.3. Save Markdown Article
    materias_dir = os.path.join(base_dir, 'materias')
    os.makedirs(materias_dir, exist_ok=True)
    
    md_content = f"""---
id: "{post_id}"
title: "{title}"
excerpt: "{excerpt}"
category: "{category}"
image: "{image_url}"
author: "{author}"
date: "{post_date}"
tags: {json.dumps(tags)}
---

{content}
"""
    
    md_filepath = os.path.join(materias_dir, f"{slug}.md")
    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Markdown post written to {md_filepath}")

    # 5.4. Load and append to posts.json
    posts = []
    if os.path.exists(posts_json_path):
        with open(posts_json_path, 'r', encoding='utf-8') as f:
            posts = json.load(f)
            
    # Remove post with same title if running tests to avoid duplicates
    posts = [p for p in posts if p['title'] != title]
    
    # Prepend new post
    new_post_entry = {
        "id": post_id,
        "title": title,
        "url": f"materia.html?id={post_id}",
        "image": image_url,
        "category": category,
        "tags": tags,
        "excerpt": excerpt,
        "content": content,
        "author": author,
        "date": post_date
    }
    
    posts.insert(0, new_post_entry)
    
    # Save back to both locations
    for path in [posts_json_path, deploy_posts_json_path]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
            
    print(f"Updated posts.json. Added post: {title}")
    
    # 5.5. Rebuild sitemaps & RSS
    generate_sitemaps_and_rss(posts)
    
    # 5.6. Recompile site index.html
    build_script = os.path.join(base_dir, 'tagmanews-main', 'build_site.py')
    if os.path.exists(build_script):
        print("Recompiling site homepage...")
        subprocess.run(['python', build_script], cwd=os.path.dirname(build_script), check=True)
        
        # Copy newly compiled index.html to deploy folder
        compiled_index = os.path.join(base_dir, 'index.html')
        deploy_index = os.path.join(base_dir, 'Tagma-V1-GitHubReady', 'index.html')
        if os.path.exists(compiled_index):
            with open(compiled_index, 'r', encoding='utf-8') as src:
                with open(deploy_index, 'w', encoding='utf-8') as dest:
                    dest.write(src.read())
            print("Copied compiled index.html to deploy directory.")
            
    return post_id
