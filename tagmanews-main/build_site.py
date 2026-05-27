import json
import re
import html

# Common typo cleanup dictionary for extracted WP strings
CLEANUPS = {
    "mantm": "mantém",
    "revelaes": "revelações",
    "revelao": "revelação",
    "lana": "lança",
    "oitavo lbum": "oitavo álbum",
    "importao": "importação",
    "alimentos  zerado": "alimentos é zerado",
    "revelaes": "revelações",
    "histria": "história",
    "emoo": "emoção",
    "resistncia": "resistência",
    "priso": "prisão",
    "polmica": "polêmica",
    "Histria de Amor": "História de Amor",
    "vsperas": "vésperas",
    "retorno  tv": "retorno à TV",
    "declaraes": "declarações",
    "corrupo": "corrupção",
    "ao": "aço",
    "alumnio": "alumínio",
    "importaes": "importações",
    "reunio": "reunião",
    "indstria": "indústria",
    "preos": "preços",
    "tera-feira": "terça-feira",
    "liderana": "liderança",
    "Cmara": "Câmara",
    "votao": "votação",
    "histrica": "histórica",
    "Ameaa": "Ameaça",
    "Rssia": "Rússia",
    "Ucrnia": "Ucrânia",
    "deportao": "deportação",
    "Justia": "Justiça",
    "inflao": "inflação",
    "candidatos s": "candidatos às",
    "presidncias": "presidências",
    "sbado": "sábado",
    "clssico": "clássico",
    "avanam s": "avançam às",
    "destruio": "destruição",
    "patinao": "patinação",
    "areo": "aéreo",
    "ntegra": "íntegra",
    "denncia": "denúncia",
    "critrios": "critérios",
    "cenrios": "cenários",
    "contnua": "contínua",
    "Conhea": "Conheça",
    "eleio": "eleição",
    "ocorre": "ocorre",
    "sbado": "sábado",
    "clssico": "clássico",
    "Atltico-MG": "Atlético-MG",
    "clssico": "clássico",
    "histrico": "histórico",
    "Mangueiro": "Mangueirão",
    "destruio": "destruição",
    "patinao": "patinação",
    "russos": "russos",
    "avanam": "avançam",
    "histria": "história",
    "emoo": "emoção",
    "resistncia": "resistência",
    "solto": "solto",
    "aps": "após",
    "priso": "prisão",
    "polmica": "polêmica",
    "Histria": "História",
    "vsperas": "vésperas",
    "cautela": "cautela",
    "aps": "após",
    "reunio": "reunião",
    "indstria": "indústria",
    "preos": "preços",
    "tera-feira": "terça-feira",
    "liderana": "liderança",
    "Cmara": "Câmara",
    "votao": "votação",
    "histrica": "histórica",
    "Norte-Coreanos": "Norte-Coreanos",
    "Ameaa": "Ameaça",
    "Rssia": "Rússia",
    "Ucrnia": "Ucrânia",
    "deportao": "deportação",
    "cerveja": "cerveja",
    "artesanal": "artesanal",
    "Justia": "Justiça",
    "TikTok": "TikTok",
    "inflao": "inflação",
    "candidatos": "candidatos",
    "presidncias": "presidências",
    "sbado": "sábado"
}

def clean_text(text):
    if not text:
        return ""
    for k, v in CLEANUPS.items():
        text = text.replace(k, v)
    # Remove any stray  characters
    text = text.replace("", "")
    return text

def build_site():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'posts.json')
    if not os.path.exists(json_path):
        json_path = r"C:\Users\leose\.gemini\antigravity\scratch\tnc_posts_extracted.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)
        
    print(f"Loaded {len(posts)} posts for site generation.")
    
    # 1. Clean all text content
    for p in posts:
        p['title'] = clean_text(p['title'])
        p['excerpt'] = clean_text(p['excerpt'])
        p['author'] = clean_text(p['author'])
        p['date'] = clean_text(p['date'])
        p['category'] = clean_text(p['category'])
        p['tags'] = [clean_text(t) for t in p['tags']]
        
        # Build category fallback from URL if blank
        if not p['category'] or p['category'] == 'Uncategorized':
            if 'politica' in p['url']:
                p['category'] = 'Política'
            elif 'economia' in p['url']:
                p['category'] = 'Economia'
            elif 'esportes' in p['url']:
                p['category'] = 'Esportes'
            elif 'internacional' in p['url']:
                p['category'] = 'Internacional'
            elif 'tv-e-celebridades' in p['url']:
                p['category'] = 'TV e Celebridades'
            elif 'musica' in p['url']:
                p['category'] = 'Música'
            elif 'ciencia' in p['url']:
                p['category'] = 'Ciência'
            elif 'comportamento' in p['url']:
                p['category'] = 'Comportamento'
            elif 'historia' in p['url']:
                p['category'] = 'História e Sociedade'
            else:
                p['category'] = 'Geral'
                
    # Normalize category names
    for p in posts:
        if p['category'] == 'Politica':
            p['category'] = 'Política'
        elif p['category'] == 'Ciencia':
            p['category'] = 'Ciência'
        elif p['category'] == 'Musica':
            p['category'] = 'Música'
        elif p['category'] == 'Historia E Sociedade':
            p['category'] = 'História e Sociedade'
        elif p['category'] == 'Tv E Celebridades':
            p['category'] = 'TV e Celebridades'
        elif p['category'] == 'Economia E Mercado':
            p['category'] = 'Economia'
            
    # Helper to resolve image paths with CDN fallback
    def get_img_attributes(post_img_path, default_unsplash):
        if not post_img_path:
            return f'src="{default_unsplash}" data-fallback="{default_unsplash}"'
            
        # If it's a web link already
        if post_img_path.startswith('http'):
            return f'src="{post_img_path}" data-fallback="{post_img_path}"'
            
        # It's a local path like "./Home - TN&C..._files/cropped-Design-sem-nome.png"
        # We build a Wayback Machine archive URL as fallback
        filename = post_img_path.split('/')[-1]
        # Clean url encoded spaces etc.
        filename_clean = filename.replace(' ', '%20')
        local_path = f"./Home - TN&C - Tendências, Notícias e Cultura - Informação relevante e atualizada_files/{filename}"
        
        # Wayback fallback URL
        # e.g., https://web.archive.org/web/20250805155622im_/https://tncbrasil.com.br/wp-content/uploads/2025/02/...
        # We can extract folder date from the original files if we want, or fall back to a reasonable upload folder:
        wayback_fallback = f"https://web.archive.org/web/20250805155622im_/https://tncbrasil.com.br/wp-content/uploads/2025/02/{filename_clean}"
        if '2025/01' in post_img_path:
            wayback_fallback = f"https://web.archive.org/web/20250805155622im_/https://tncbrasil.com.br/wp-content/uploads/2025/01/{filename_clean}"
            
        return f'src="{local_path}" data-fallback="{wayback_fallback}" onerror="this.onerror=null; this.src=this.dataset.fallback;"'

    # 2. Select Hero Post (Tag 'Capa')
    hero_candidates = [p for p in posts if any(t.lower() == 'capa' for t in p.get('tags', []))]
    hero = hero_candidates[0] if hero_candidates else (posts[0] if posts else None)
    
    # 3. Select Secondary Highlights (3 next to hero)
    # Exclude hero
    remaining = [p for p in posts if p['title'] != hero['title']]
    
    # 3. Select Secondary Highlights (Últimas Notícias - 3 posts)
    highlights = remaining[:3]
    remaining = remaining[3:]
            
    # Fill highlights to 3 if needed
    while len(highlights) < 3 and remaining:
        highlights.append(remaining.pop(0))
        
    # 4. Select Destaques Carousel/Row posts (Cultura & Tecnologia)
    destaques = []
    for p in remaining:
        if p['category'] in ['Cultura', 'Tecnologia'] and len(destaques) < 4:
            destaques.append(p)
    # Remove selected from remaining
    remaining = [p for p in remaining if p not in destaques]
            
    while len(destaques) < 4 and remaining:
        destaques.append(remaining.pop(0))
        
    # 5. Select Sidebar "Mais Lidas" (Tendências / Aleatórias para simular)
    mais_lidas = posts[4:10] if len(posts) > 10 else posts[:6]
            
    # 6. Select "Destaque da Semana" (Opinião / Geral)
    destaque_semana = posts[5] if len(posts) > 5 else hero

    # Pad sections to prevent IndexError on fresh starts
    while len(highlights) < 3: highlights.append(hero)
    while len(destaques) < 4: destaques.append(hero)
    while len(mais_lidas) < 6: mais_lidas.append(hero)
    # 7. Group articles by primary editorial sections
    # Sections: Política, Economia, Internacional, Esportes
    sections = {
        'Política': [],
        'Economia': [],
        'Internacional': [],
        'Esportes': []
    }
    
    # Populate editorial groups from remaining articles
    for p in posts:
        # Don't repeat hero or highlights in their own categories to make it clean
        if p['title'] == hero['title'] or any(h['title'] == p['title'] for h in highlights):
            continue
        cat = p['category']
        if cat in sections:
            sections[cat].append(p)
            
    # 8. Bottom Feed: Remaining articles (not in hero, highlights, destaques, or first items of category grids)
    # We want to display all 43 articles!
    used_titles = {hero['title'], destaque_semana['title']}
    for h in highlights: used_titles.add(h['title'])
    for d in destaques: used_titles.add(d['title'])
    
    # Category grids will show the first 3 articles of each category.
    # The rest will go into the bottom feed.
    bottom_feed = []
    for p in posts:
        if p['title'] in used_titles:
            continue
        # Check if it was featured in category grids (we will show up to 3 in each category grid)
        # If it falls outside the top 3 of its category, or its category isn't in sections, put in bottom feed
        cat = p['category']
        if cat in sections:
            cat_list = sections[cat]
            if p in cat_list[3:]:
                bottom_feed.append(p)
        else:
            bottom_feed.append(p)
            
    # Add any extra items from used lists to bottom feed if bottom feed is short
    # Let's verify we have a good list
    print(f"Hero: {hero['title']}")
    print(f"Highlights: {len(highlights)}")
    print(f"Destaques Row: {len(destaques)}")
    print(f"Destaque Semana: {destaque_semana['title']}")
    for s_name, s_posts in sections.items():
        print(f"Section {s_name}: {len(s_posts)} posts")
    print(f"Bottom Feed: {len(bottom_feed)} posts")

    # Define color accents for category chips
    category_colors = {
        'Política': 'bg-[#003311]',
        'Economia': 'bg-[#fcb900]',
        'Internacional': 'bg-[#0693e3]',
        'Esportes': 'bg-[#934b00]',
        'TV e Celebridades': 'bg-[#c36]',
        'Música': 'bg-[#c36]',
        'Ciência': 'bg-[#0693e3]',
        'Comportamento': 'bg-[#c36]',
        'História e Sociedade': 'bg-[#c36]',
        'Geral': 'bg-[#003311]'
    }

    # Generate HTML blocks
    
    # Highlights block
    highlights_html = ""
    highlight_pics = [
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop", # Moon/Sci
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=2070&auto=format&fit=crop", # Music
        "https://images.unsplash.com/photo-1526367790999-015078648c7e?q=80&w=2070&auto=format&fit=crop"  # Food/Econ
    ]
    for idx, h in enumerate(highlights):
        img_attr = get_img_attributes(h['image'], highlight_pics[idx])
        col_accent = category_colors.get(h['category'], 'bg-[#003311]')
        highlights_html += f"""
        <article class="flex flex-col border-b border-border-subtle md:border-b-0 pb-6 md:pb-0 group cursor-pointer">
            <div class="aspect-[16/10] overflow-hidden bg-gray-100 mb-4 relative">
                <img loading="lazy" alt="{h['title']}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {img_attr} />
            </div>
            <div class="flex items-center mb-2">
                <span class="inline-flex items-center border border-border-subtle bg-surface-container-low pl-0 pr-2 py-0.5 font-label-bold text-[9px] uppercase tracking-wider text-on-surface-variant">
                    <span class="w-1 h-3 {col_accent} mr-1.5"></span>
                    {h['category']}
                </span>
            </div>
            <h3 class="font-headline-sm text-[20px] md:text-[22px] leading-snug group-hover:underline text-primary">
                <a href="materia.html?id={h['id']}">{h['title']}</a>
            </h3>
        </article>
        """

    # Destaques Row
    destaques_html = ""
    for d in destaques:
        img_attr = get_img_attributes(d['image'], "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=2070&auto=format&fit=crop")
        col_accent = category_colors.get(d['category'], 'bg-[#003311]')
        destaques_html += f"""
        <article class="border border-border-subtle p-4 bg-white flex flex-col group cursor-pointer">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100 mb-4">
                <img loading="lazy" alt="{d['title']}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {img_attr} />
            </div>
            <div class="flex items-center mb-2">
                <span class="inline-flex items-center border border-border-subtle bg-surface-container-low pl-0 pr-2 py-0.5 font-label-bold text-[9px] uppercase tracking-wider text-on-surface-variant">
                    <span class="w-1 h-3 {col_accent} mr-1.5"></span>
                    {d['category']}
                </span>
            </div>
            <h4 class="font-headline-sm text-[16px] leading-snug group-hover:underline text-primary flex-1">
                <a href="materia.html?id={d['id']}">{d['title']}</a>
            </h4>
        </article>
        """

    # Mais Lidas Sidebar
    mais_lidas_html = ""
    for idx, m in enumerate(mais_lidas):
        num = f"0{idx+1}"
        mais_lidas_html += f"""
        <div class="flex gap-4 items-start group cursor-pointer border-b border-border-subtle pb-4 last:border-b-0">
            <span class="font-headline-md text-outline-variant text-[28px] leading-none font-extrabold">{num}</span>
            <h4 class="font-label-bold text-[13px] leading-tight group-hover:text-secondary text-primary font-bold">
                <a href="materia.html?id={m['id']}">{m['title']}</a>
            </h4>
        </div>
        """

    # Editorial Grid sections (Politics, Econ, Inter, Sports, Celebs)
    sections_html = ""
    # We lay them out in a 2-column container or sequentially. Let's do a modular grid of categories.
    section_pics = {
        'Política': 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=2070&auto=format&fit=crop',
        'Economia': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=2070&auto=format&fit=crop',
        'Internacional': 'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?q=80&w=2070&auto=format&fit=crop',
        'Esportes': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=2073&auto=format&fit=crop',
        'TV e Celebridades': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=2070&auto=format&fit=crop'
    }
    
    for s_name, s_posts in sections.items():
        if not s_posts:
            continue
            
        # Category header
        col_accent = category_colors.get(s_name, 'bg-[#003311]')
        
        # Spotlight (First post)
        spot = s_posts[0]
        spot_img = get_img_attributes(spot['image'], section_pics[s_name])
        
        # Remaining lists (Up to 4 more posts)
        list_html = ""
        for p in s_posts[1:4]:
            list_html += f"""
            <div class="py-3 border-b border-border-subtle last:border-b-0 group cursor-pointer">
                <h4 class="font-headline-sm text-[15px] leading-snug group-hover:underline text-primary">
                    <a href="materia.html?id={p['id']}">{p['title']}</a>
                </h4>
            </div>
            """
            
        sections_html += f"""
        <section class="border border-border-subtle p-6 bg-white flex flex-col justify-between">
            <div>
                <h2 class="font-label-bold text-[12px] uppercase tracking-widest text-primary border-b-2 border-primary pb-2 mb-6 flex items-center">
                    <span class="w-1.5 h-4 {col_accent} mr-2"></span>
                    {s_name}
                </h2>
                
                <article class="group cursor-pointer mb-6">
                    <div class="aspect-[16/10] overflow-hidden bg-gray-100 mb-4">
                        <img loading="lazy" alt="{spot['title']}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {spot_img} />
                    </div>
                    <h3 class="font-headline-sm text-[18px] md:text-[20px] leading-snug group-hover:underline text-primary mb-2">
                        <a href="materia.html?id={spot['id']}">{spot['title']}</a>
                    </h3>
                    <p class="font-body-sm text-[13px] text-on-surface-variant leading-relaxed line-clamp-3">
                        {spot['excerpt'] or "Confira a cobertura completa dos últimos acontecimentos na editoria de " + s_name + " do novo portal Tagma."}
                    </p>
                </article>
            </div>
            
            <div class="border-t border-border-subtle pt-3">
                {list_html}
            </div>
        </section>
        """

    # Bottom Feed
    bottom_feed_html = ""
    for idx, p in enumerate(bottom_feed):
        col_accent = category_colors.get(p['category'], 'bg-[#003311]')
        # Alternate between cards with smaller thumbnails and simple link blocks for premium variety
        if p['image'] or idx % 3 == 0:
            img_attr = get_img_attributes(p['image'], "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=2070&auto=format&fit=crop")
            bottom_feed_html += f"""
            <article class="flex flex-col sm:flex-row gap-6 p-4 border border-border-subtle bg-white group cursor-pointer">
                <div class="w-full sm:w-48 aspect-[16/10] sm:aspect-square shrink-0 overflow-hidden bg-gray-100">
                    <img loading="lazy" alt="{p['title']}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {img_attr} />
                </div>
                <div class="flex-1 flex flex-col justify-between py-1">
                    <div>
                        <div class="flex items-center mb-2">
                            <span class="inline-flex items-center border border-border-subtle bg-surface-container-low pl-0 pr-2 py-0.5 font-label-bold text-[9px] uppercase tracking-wider text-on-surface-variant">
                                <span class="w-1 h-3 {col_accent} mr-1.5"></span>
                                {p['category']}
                            </span>
                        </div>
                        <h3 class="font-headline-sm text-[18px] md:text-[20px] leading-snug group-hover:underline text-primary mb-2">
                            <a href="materia.html?id={p['id']}">{p['title']}</a>
                        </h3>
                        <p class="font-body-sm text-[13px] text-on-surface-variant leading-relaxed line-clamp-2">
                            {p['excerpt'] or "Acompanhe todos os detalhes desta cobertura jornalística no portal Tagma. Informação com ética e precisão."}
                        </p>
                    </div>
                    <div class="text-meta text-[11px] text-outline mt-4">
                        Por {p['author'] or 'Redação'} • {p['date'] or 'Últimas Horas'}
                    </div>
                </div>
            </article>
            """
        else:
            bottom_feed_html += f"""
            <article class="p-6 border border-border-subtle bg-white group cursor-pointer">
                <div class="flex items-center mb-2">
                    <span class="inline-flex items-center border border-border-subtle bg-surface-container-low pl-0 pr-2 py-0.5 font-label-bold text-[9px] uppercase tracking-wider text-on-surface-variant">
                        <span class="w-1 h-3 {col_accent} mr-1.5"></span>
                        {p['category']}
                    </span>
                </div>
                <h3 class="font-headline-sm text-[18px] md:text-[20px] leading-snug group-hover:underline text-primary mb-2">
                    <a href="materia.html?id={p['id']}">{p['title']}</a>
                </h3>
                <p class="font-body-sm text-[13px] text-on-surface-variant leading-relaxed line-clamp-2 mb-4">
                    {p['excerpt'] or "Análise aprofundada dos últimos eventos com a credibilidade jornalística e cobertura nacional e internacional do Tagma."}
                </p>
                <div class="text-meta text-[11px] text-outline">
                    Por {p['author'] or 'Redação'} • {p['date'] or 'Últimas Horas'}
                </div>
            </article>
            """

    # Assemble HTML Output
    full_html = f"""<!DOCTYPE html>
<html class="light" lang="pt-BR" dir="ltr">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Tagma - Tendências, Notícias e Cultura (antigo TN&C)</title>
    <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700;800&family=Literata:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:wght@400;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script id="tailwind-config">
      tailwind.config = {{
        darkMode: "class",
        theme: {{
          extend: {{
            colors: {{
              surface: "#fcf9f8",
              "on-surface": "#1c1b1b",
              "on-surface-variant": "#414940",
              outline: "#727970",
              "outline-variant": "#c1c9be",
              primary: "#001c06",
              "on-primary": "#ffffff",
              "primary-container": "#003311",
              secondary: "#934b00",
              "secondary-container": "#d8561c",
              error: "#ba1a1a",
              "surface-container-low": "#f6f3f2",
              "surface-off-white": "#fcfcfc",
              "border-subtle": "#e0e0e0",
              "editorial-green-deep": "#003311",
              "section-culture": "#c36",
              "section-tech": "#0693e3",
              "section-finance": "#fcb900"
            }},
            fontFamily: {{
              "headline-xl": ["'Hanken Grotesk'", "sans-serif"],
              "headline-lg": ["'Hanken Grotesk'", "sans-serif"],
              "headline-md": ["'Hanken Grotesk'", "sans-serif"],
              "headline-sm": ["'Hanken Grotesk'", "sans-serif"],
              "body-lg": ["Literata", "serif"],
              "body-md": ["Literata", "serif"],
              "body-sm": ["Literata", "serif"],
              "label-bold": ["'IBM Plex Sans'", "sans-serif"],
              meta: ["'IBM Plex Sans'", "sans-serif"]
            }}
          }}
        }}
      }}
    </script>
    <style>
        .material-symbols-outlined {{
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            display: inline-block;
            line-height: 1;
            text-transform: none;
            letter-spacing: normal;
            word-wrap: normal;
            white-space: nowrap;
            direction: ltr;
        }}
        body {{ background-color: #fcf9f8; -webkit-font-smoothing: antialiased; }}
        .container-custom {{ max-width: 1280px; margin-left: auto; margin-right: auto; }}
        @keyframes marquee {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
        .animate-marquee {{ animation: marquee 50s linear infinite; }}
        .line-clamp-2 {{
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;  
            overflow: hidden;
        }}
        .line-clamp-3 {{
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;  
            overflow: hidden;
        }}
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    
        *:focus-visible {{ outline: 2px solid #d8561c !important; outline-offset: 2px; }}
        @media (max-width: 480px) {{
            .font-headline-xl {{ font-size: 85% !important; }}
            .container-custom {{ padding-left: 16px !important; padding-right: 16px !important; }}
        }}
        .truncate-lines {{ display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        .skeleton {{ animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; background-color: #e0e0e0; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .5; }} }}
        
</style>
</head>
<body class="font-body-md text-on-surface">

<header class="bg-[#003311] text-white">
    <!-- Top Utility Bar (More Compact) -->
    <div class="container-custom px-4 lg:px-8 flex justify-between items-center text-meta font-meta py-1 border-b border-white/10">
        <div class="flex items-center space-x-4">
            <span class="hidden md:inline uppercase tracking-widest text-[9px] text-white/60">Hoje, 24 de Maio de 2026</span>
            <span class="md:hidden text-[9px] text-white/60">24 MAI 2026</span>
        </div>
        <div class="flex items-center space-x-4">
            <button class="hover:text-secondary-container transition-colors uppercase tracking-widest text-[9px] font-bold">Assine</button>
            <a href="admin.html" class="hover:text-secondary-container transition-colors uppercase tracking-widest text-[9px] font-bold">Entrar</a>
            
        <button onclick="openSearch()" class="flex items-center text-white/80 hover:text-white transition-colors p-1 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-secondary-container rounded" aria-label="Abrir busca">
            <span class="material-symbols-outlined text-[16px]" aria-hidden="true">search</span>
            <span class="hidden md:inline ml-1 text-[9px] font-label-bold uppercase tracking-widest opacity-60 font-bold border border-white/20 rounded px-1">Ctrl+K</span>
        </button>
        <button onclick="openDrawer()" class="md:hidden flex items-center text-white/80 hover:text-white transition-colors p-1 ml-2 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-secondary-container rounded" aria-label="Abrir menu">
            <span class="material-symbols-outlined text-[20px]" aria-hidden="true">menu</span>
        </button>
        
        </div>
    </div>
    
    <!-- Logo and Nav (More Compact & Elegant Serif Logo) -->
    <div class="container-custom px-4 lg:px-8 py-2 md:py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-2 md:gap-4">
        <div class="flex items-baseline space-x-3">
            <!-- Rebranded Premium Logo matching user image (lowercase serif font) -->
            <a class="block font-normal text-[28px] md:text-[32px] tracking-tight text-white lowercase leading-none" style="font-family: 'Literata', serif;" href="index.html">
                tagma
            </a>
            
        </div>
        <nav class="w-full md:w-auto overflow-x-auto no-scrollbar">
            <div class="flex items-center space-x-4 md:space-x-6 font-label-bold text-[10.5px] uppercase tracking-[0.12em] whitespace-nowrap py-1">
                <a class="hover:text-secondary-container transition-colors border-b border-transparent hover:border-secondary-container pb-0.5" href="categoria.html?c=politica">Política</a>
                <a class="hover:text-secondary-container transition-colors border-b border-transparent hover:border-secondary-container pb-0.5" href="categoria.html?c=economia">Economia</a>
                <a class="hover:text-secondary-container transition-colors border-b border-transparent hover:border-secondary-container pb-0.5" href="categoria.html?c=internacional">Internacional</a>
                <a class="hover:text-secondary-container transition-colors border-b border-transparent hover:border-secondary-container pb-0.5" href="categoria.html?c=esportes">Esportes</a>
                <a class="hover:text-secondary-container transition-colors border-b border-transparent hover:border-secondary-container pb-0.5" href="categoria.html?c=cultura">Cultura</a>
                <a class="hover:text-secondary-container transition-colors border-b border-transparent hover:border-secondary-container pb-0.5" href="categoria.html?c=tecnologia">Tecnologia</a>
            </div>
        </nav>
    </div>
</header>

<!-- Urgent Ticker (Plantão - More Compact) -->
<div class="border-b border-border-subtle bg-surface-container-low overflow-hidden">
    <div class="container-custom px-4 py-1 flex items-center">
        <span class="font-label-bold text-[9px] uppercase tracking-widest text-white bg-editorial-green-deep px-2 py-0.5 mr-4 shrink-0 font-bold">Plantão</span>
        <div class="animate-marquee whitespace-nowrap font-meta text-[11px] italic text-on-surface-variant">
            {hero['title']} &nbsp;&nbsp;&bull;&nbsp;&nbsp; {highlights[0]['title']} &nbsp;&nbsp;&bull;&nbsp;&nbsp; {highlights[1]['title']} &nbsp;&nbsp;&bull;&nbsp;&nbsp; {highlights[2]['title']} &nbsp;&nbsp;&bull;&nbsp;&nbsp; Acompanhe a transição do portal TN&C para o novo Tagma.
        </div>
    </div>
</div>

<main class="container-custom px-4 lg:px-8 py-8 md:py-12">
    <!-- Hero / Top Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 pb-12 border-b border-border-subtle">
        
        <!-- Left Side: Primary Headline (Hero) -->
        <div class="lg:col-span-8 flex flex-col justify-between">
            <article class="group cursor-pointer">
                <div class="flex justify-start mb-6">
                    <span class="inline-flex items-center border border-border-subtle bg-surface-container-low pl-0 pr-3 py-1 font-label-bold text-[10px] uppercase tracking-widest text-editorial-green-deep">
                        <span class="w-1.5 h-4 bg-editorial-green-deep mr-2"></span>
                        {hero['category']}
                    </span>
                </div>
                <h1 class="font-headline-xl text-left text-primary mb-8 font-extrabold text-[36px] md:text-[54px] lg:text-[60px] leading-[1.05] tracking-tight group-hover:underline">
                    <a href="materia.html?id={hero['id']}">{hero['title']}</a>
                </h1>
                
                <a href="materia.html?id={hero['id']}" class="block w-full aspect-[21/9] overflow-hidden bg-gray-100 mb-6">
                    <img loading="eager" alt="{hero['title']}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {get_img_attributes(hero['image'], "https://lh3.googleusercontent.com/aida-public/AB6AXuCN6PXdRVO_MXI055rQRS23Usy6yi8mCoNHa7Fwj-j2G4eIHdbbumA9SkcEQ-kBEOtruUjEYmQS5Y_DyI-ixZxtTVQryrYUi51yorp_fDTzh1rSETbrfyEuIHXMfoHo00ezCUFqafiJW6OjfT-YoR0dN1nm1T20H6ydS18GV8o_kb0c1q2-bcyPo1REMyrH8bpYgsaaOb3XT7ltB91mL0Ks2gn875uwSnRK6CV8czZlskno3ZfaHsDAZ8C3hIsD6jJJSP0p33O627E")} />
                </a>
                
                <div class="max-w-3xl mx-auto">
                    <p class="font-body-lg text-[18px] md:text-[20px] text-on-surface mb-6 leading-relaxed italic border-l-4 border-editorial-green-deep pl-6">
                        {hero['excerpt']}
                    </p>
                    <div class="flex items-center justify-between text-meta font-meta text-outline pt-4 border-t border-border-subtle">
                        <span>Por <strong>{hero['author'] or 'João Silva'}</strong>, Sucursal Brasília</span>
                        <span>{hero['date'] or 'Últimas horas'}</span>
                    </div>
                </div>
            </article>
        </div>
        
        <!-- Right Side: 3 Highlights Block -->
        <div class="lg:col-span-4 flex flex-col justify-between border-t lg:border-t-0 lg:border-l border-border-subtle pt-8 lg:pt-0 lg:pl-8">
            <h2 class="font-label-bold text-[12px] uppercase tracking-widest text-editorial-green-deep border-b border-editorial-green-deep pb-2 mb-6 font-bold">
                Em Destaque
            </h2>
            <div class="space-y-8 flex-1 flex flex-col justify-between">
                {highlights_html}
            </div>
        </div>
        
    </div>

    <!-- Destaques Row (Horizontal Grid) -->
    <div class="py-12 border-b border-border-subtle">
        <h2 class="font-label-bold text-[12px] uppercase tracking-widest text-primary border-b border-primary pb-2 mb-8">
            Cultura & Celebridades
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {destaques_html}
        </div>
    </div>

    <!-- Editorial Sections and Sidebar -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 py-12">
        
        <!-- Left Side: Editorial Grids -->
        <div id="editorias" class="lg:col-span-8 space-y-12">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                {sections_html}
            </div>
        </div>

        <!-- Right Side: Sidebar -->
        <aside class="lg:col-span-4 space-y-12 border-t lg:border-t-0 lg:border-l border-border-subtle pt-8 lg:pt-0 lg:pl-8">
            
            <!-- AdSense Slot (Fixed 300x250) -->
            <section class="bg-surface-container-low p-4 border border-border-subtle flex flex-col items-center justify-center min-h-[250px] text-center">
                <span class="font-meta text-[10px] uppercase tracking-widest text-outline mb-2">Publicidade</span>
                <div class="w-[300px] h-[250px] bg-white border border-border-subtle flex items-center justify-center">
                    <p class="text-xs text-outline italic">Espaço Otimizado AdSense (300x250)</p>
                </div>
                <span class="font-meta text-[9px] text-outline-variant mt-2">CLS Otimizado - Sem quebras de layout</span>
            </section>

            <!-- Destaque da Semana -->
            <section class="bg-surface-off-white p-6 border-t-4 border-editorial-green-deep border-x border-b border-border-subtle">
                <div class="mb-6 flex justify-between items-center border-b border-border-subtle pb-2">
                    <span class="font-label-bold text-[10px] text-editorial-green-deep uppercase tracking-widest font-bold">Opinião / Destaque</span>
                </div>
                <div class="space-y-4">
                    <h3 class="font-headline-sm text-[22px] leading-tight text-primary font-bold">
                        <a href="materia.html?id={destaque_semana['id']}" class="hover:underline">{destaque_semana['title']}</a>
                    </h3>
                    <p class="font-body-sm text-[13px] text-on-surface-variant leading-relaxed">
                        {destaque_semana['excerpt'] or "Análise comportamental mostra aumento significativo de divórcios na maturidade. Especialistas investigam as transformações sociais e emocionais nessa fase da vida."}
                    </p>
                    <a class="block text-center font-label-bold text-[10px] uppercase tracking-widest py-3 bg-editorial-green-deep text-white hover:bg-primary transition-colors mt-6 font-bold" href="materia.html?id={destaque_semana['id']}">Ler Artigo Completo</a>
                </div>
            </section>

            <!-- Mais Lidas -->
            <section class="pt-6 border-t border-primary">
                <h3 class="font-label-bold text-[12px] uppercase tracking-widest mb-6 flex items-center text-primary font-bold">
                    <span class="material-symbols-outlined mr-2 text-editorial-green-deep text-lg">trending_up</span> Mais Lidas
                </h3>
                <div class="space-y-6">
                    {mais_lidas_html}
                </div>
            </section>

        </aside>
    </div>

    <!-- Lomadee Offers Section (Rebranded BroadSheet Style) -->
    <section class="mt-12 border-t-4 border-double border-primary pt-12">
        <div class="flex items-center mb-8">
            <span class="material-symbols-outlined mr-2 text-editorial-green-deep">shopping_cart</span>
            <h2 class="font-label-bold text-[12px] uppercase tracking-[0.2em] text-primary font-bold">Tagma Shop • Ofertas imperdíveis</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-6 gap-6">
            <!-- Product 1 -->
            <div class="md:col-span-2 lg:col-span-3 border border-border-subtle p-6 flex flex-col md:flex-row gap-6 hover:bg-surface-container-low transition-colors group cursor-pointer bg-white">
                <div class="shrink-0 w-32 h-32 md:w-40 md:h-40 bg-white p-4 border border-border-subtle flex items-center justify-center">
                    <img loading="lazy" alt="Geladeira" class="w-full h-full object-contain mix-blend-multiply" src="./Home - TN&amp;C - Tendncias, Notcias e Cultura - Informao relevante e atualizada_files/geladeira-refrigerador-brastemp-554l-frost-free-french-door-bro85ak-092311191729.jpg" data-src="https://web.archive.org/web/20250805155622im_/https://gazin-marketplace.s3.amazonaws.com/midias/imagens/2023/11/geladeira-refrigerador-brastemp-554l-frost-free-french-door-bro85ak-092311191729.jpg" onerror="this.onerror=null; this.src=this.dataset.src;" />
                </div>
                <div class="flex-1 flex flex-col justify-center">
                    <span class="font-label-bold text-[9px] text-secondary uppercase tracking-widest mb-1">Cozinha Premium</span>
                    <h4 class="font-headline-sm text-[18px] mb-2 group-hover:underline">Geladeira French Door Brastemp 554L</h4>
                    <p class="text-primary font-bold text-xl mb-4">R$ 5.899,00</p>
                    <button class="w-full md:w-auto bg-primary text-white px-6 py-2 font-label-bold text-[9px] uppercase tracking-widest hover:bg-editorial-green-deep transition-colors font-bold">Comprar</button>
                </div>
            </div>
            <!-- Product 2 -->
            <div class="border border-border-subtle p-4 hover:bg-surface-container-low transition-colors bg-white flex flex-col justify-between">
                <div class="flex items-center justify-center p-2 bg-white aspect-square border border-border-subtle mb-4">
                    <img loading="lazy" alt="Fone" class="w-full h-full object-contain mix-blend-multiply" src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=200&auto=format&fit=crop" />
                </div>
                <div>
                    <h4 class="font-label-bold text-[11px] mb-1 line-clamp-2">Fone de Ouvido Wireless NC</h4>
                    <p class="font-bold text-primary text-[14px]">R$ 899,00</p>
                </div>
            </div>
            <!-- Product 3 -->
            <div class="border border-border-subtle p-4 hover:bg-surface-container-low transition-colors bg-white flex flex-col justify-between">
                <div class="flex items-center justify-center p-2 bg-white aspect-square border border-border-subtle mb-4">
                    <img loading="lazy" alt="Relógio" class="w-full h-full object-contain mix-blend-multiply" src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=200&auto=format&fit=crop" />
                </div>
                <div>
                    <h4 class="font-label-bold text-[11px] mb-1 line-clamp-2">Relógio Smartwatch Series V</h4>
                    <p class="font-bold text-primary text-[14px]">R$ 1.450,00</p>
                </div>
            </div>
            <!-- Product 4 (Desktop only) -->
            <div class="hidden lg:flex border border-border-subtle p-4 hover:bg-surface-container-low transition-colors bg-white flex-col justify-between">
                <div class="flex items-center justify-center p-2 bg-white aspect-square border border-border-subtle mb-4">
                    <img loading="lazy" alt="Tablet" class="w-full h-full object-contain mix-blend-multiply" src="https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?q=80&w=200&auto=format&fit=crop" />
                </div>
                <div>
                    <h4 class="font-label-bold text-[11px] mb-1 line-clamp-2">Tablet Ultra HD 10"</h4>
                    <p class="font-bold text-primary text-[14px]">R$ 2.199,00</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Bottom Feed: Latest News -->
    <div class="py-12 mt-12 border-t border-border-subtle">
        <h2 class="font-label-bold text-[12px] uppercase tracking-widest text-primary border-b border-primary pb-2 mb-8">
            Últimas Notícias
        </h2>
        <div id="latest-news-grid" class="grid grid-cols-1 md:grid-cols-2 gap-8">
            {bottom_feed_html}
        </div>
    </div>

</main>

<footer class="bg-primary text-white py-16 pb-24 md:pb-16">
    <div class="container-custom px-4 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12 border-b border-white/10 pb-12 mb-12">
            <div class="col-span-1 md:col-span-2">
                <div class="mb-4 font-normal text-[32px] tracking-tight text-white lowercase leading-none" style="font-family: 'Literata', serif;">
                    tagma
                </div>
                <p class="text-surface-container-low/70 text-sm max-w-sm font-body-sm leading-relaxed">
                    Informação com precisão, ética e independência. A evolução do antigo portal TN&C, reconstruído com infraestrutura escalável para levar o jornalismo de excelência a milhões de leitores.
                </p>
                <div class="flex space-x-6 mt-8">
                    <span class="material-symbols-outlined cursor-pointer hover:text-secondary-container transition-colors">facebook</span>
                    <span class="material-symbols-outlined cursor-pointer hover:text-secondary-container transition-colors">share</span>
                    <span class="material-symbols-outlined cursor-pointer hover:text-secondary-container transition-colors">podcasts</span>
                </div>
            </div>
            <div>
                <h5 class="font-label-bold uppercase tracking-widest mb-8 text-xs text-white font-bold">Editorias</h5>
                <ul class="space-y-4 text-surface-container-low/60 text-[12px] font-label-bold uppercase tracking-wider">
                    <li><a class="hover:text-white transition-colors" href="#politica">Política</a></li>
                    <li><a class="hover:text-white transition-colors" href="#economia">Economia</a></li>
                    <li><a class="hover:text-white transition-colors" href="#internacional">Internacional</a></li>
                    <li><a class="hover:text-white transition-colors" href="#esportes">Esportes</a></li>
                    <li><a class="hover:text-white transition-colors" href="#cultura">Cultura & Arte</a></li>
                </ul>
            </div>
            <div>
                <h5 class="font-label-bold uppercase tracking-widest mb-8 text-xs text-white font-bold">Institucional</h5>
                <ul class="space-y-4 text-surface-container-low/60 text-[12px] font-label-bold uppercase tracking-wider">
                    <li><a class="hover:text-white transition-colors" href="#">Quem Somos</a></li>
                    <li><a class="hover:text-white transition-colors" href="#">Expediente</a></li>
                    <li><a class="hover:text-white transition-colors" href="#">Anuncie</a></li>
                    <li><a class="hover:text-white transition-colors" href="#">Privacidade</a></li>
                </ul>
            </div>
        </div>
        <div class="text-center text-[10px] uppercase tracking-[0.3em] text-white/30">
            © 2026 TAGMA NOTÍCIAS. TODOS OS DIREITOS RESERVADOS.
        </div>
    </div>
</footer>

<!-- Bottom Navigation for Mobile -->
<nav class="md:hidden fixed bottom-0 left-0 w-full z-50 flex justify-around items-center h-16 bg-white border-t border-border-subtle shadow-2xl">
    <a class="flex flex-col items-center justify-center text-primary" href="#">
        <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">home</span>
        <span class="font-label-bold text-[9px] mt-1 uppercase tracking-tighter">Início</span>
    </a>
    <a class="flex flex-col items-center justify-center text-outline" href="#editorias">
        <span class="material-symbols-outlined">menu_book</span>
        <span class="font-label-bold text-[9px] mt-1 uppercase tracking-tighter">Sessões</span>
    </a>
    <a class="flex flex-col items-center justify-center text-outline" href="#">
        <span class="material-symbols-outlined">person</span>
        <span class="font-label-bold text-[9px] mt-1 uppercase tracking-tighter">Conta</span>
    </a>
</nav>

<script>
    // Header transition on scroll
    window.addEventListener('scroll', () => {{
        const header = document.querySelector('header');
        if (window.scrollY > 100) {{
            header.classList.add('shadow-xl');
        }} else {{
            header.classList.remove('shadow-xl');
        }}
    }});

    // Load custom posts from localStorage and prepend to the bottom grid
    const customPosts = JSON.parse(localStorage.getItem('tagma_custom_posts') || '[]');
    const newsGrid = document.getElementById('latest-news-grid');
    const categoryColors = {{
        'Política': 'bg-[#003311]',
        'Economia': 'bg-[#fcb900]',
        'Internacional': 'bg-[#0693e3]',
        'Esportes': 'bg-[#934b00]',
        'TV e Celebridades': 'bg-[#c36]',
        'Música': 'bg-[#c36]',
        'Ciência': 'bg-[#0693e3]',
        'Geral': 'bg-[#003311]'
    }};
    
    if (customPosts.length > 0 && newsGrid) {{
        customPosts.forEach((post) => {{
            const colAccent = categoryColors[post.category] || 'bg-[#003311]';
            const fallbackImg = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=600&auto=format&fit=crop";
            const imgTag = post.image ? `<img loading="lazy" alt="${{post.title}}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" src="${{post.image}}" onerror="this.onerror=null; this.src='${{fallbackImg}}';" />` : `<img loading="lazy" alt="${{post.title}}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" src="${{fallbackImg}}" />`;
            
            const card = document.createElement('article');
            card.className = "flex flex-col sm:flex-row gap-6 p-4 border border-border-subtle bg-yellow-50/20 hover:bg-yellow-50/40 transition-colors group cursor-pointer border-l-4 border-l-secondary";
            card.innerHTML = `
                <div class="w-full sm:w-48 aspect-[16/10] sm:aspect-square shrink-0 overflow-hidden bg-gray-100">
                    ${{imgTag}}
                </div>
                <div class="flex-1 flex flex-col justify-between py-1">
                    <div>
                        <div class="flex items-center mb-2">
                            <span class="inline-flex items-center border border-border-subtle bg-surface-container-low pl-0 pr-2 py-0.5 font-label-bold text-[9px] uppercase tracking-wider text-on-surface-variant">
                                <span class="w-1 h-3 ${{colAccent}} mr-1.5"></span>
                                ${{post.category}}
                            </span>
                        </div>
                        <h3 class="font-headline-sm text-[18px] md:text-[20px] leading-snug group-hover:underline text-primary mb-2">
                            <a href="materia.html?id=${{post.id}}">${{post.title}}</a>
                        </h3>
                        <p class="font-body-sm text-[13px] text-on-surface-variant leading-relaxed line-clamp-2">
                            ${{post.excerpt || 'Confira todos os detalhes desta matéria publicada por nosso correspondente local.'}}
                        </p>
                    </div>
                    <div class="text-meta text-[11px] text-outline mt-4">
                        Por <strong>${{post.author}}</strong> • ${{post.date}}
                    </div>
                </div>
            `;
            // Prepend to show first
            newsGrid.insertBefore(card, newsGrid.firstChild);
        }});
    }}
</script>

<!-- Search Modal -->
<dialog id="searchModal" class="backdrop:bg-black/80 p-0 rounded-xl shadow-2xl bg-surface border border-border-subtle w-11/12 max-w-2xl m-auto open:animate-in open:fade-in open:zoom-in-95">
    <div class="flex flex-col h-[60vh] md:h-[400px]">
        <div class="flex items-center px-4 py-3 border-b border-border-subtle">
            <span class="material-symbols-outlined text-outline mr-3" aria-hidden="true">search</span>
            <input type="text" id="searchInput" class="flex-1 bg-transparent border-none focus:ring-0 text-on-surface placeholder:text-outline-variant font-body-lg text-lg outline-none" placeholder="Buscar matérias..." aria-label="Buscar" role="search">
            <button id="closeSearchBtn" class="text-outline hover:text-error transition-colors p-2 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary-container">
                <span class="material-symbols-outlined" aria-hidden="true">close</span>
            </button>
        </div>
        <div id="searchResults" class="flex-1 overflow-y-auto p-4 space-y-4">
            <div class="text-center text-outline-variant py-8 font-meta text-sm italic">Comece a digitar para buscar...</div>
        </div>
    </div>
</dialog>

<!-- Mobile Hamburger Drawer -->
<div id="mobileDrawer" class="fixed inset-y-0 left-0 w-64 bg-surface shadow-2xl z-[100] transform -translate-x-full transition-transform duration-300 ease-in-out flex flex-col border-r border-border-subtle">
    <div class="p-4 border-b border-border-subtle flex justify-between items-center bg-primary text-white">
        <span class="font-normal text-[24px] tracking-tight lowercase leading-none" style="font-family: 'Literata', serif;">tagma</span>
        <button id="closeDrawerBtn" class="text-white/80 hover:text-white p-1 rounded focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary-container">
            <span class="material-symbols-outlined" aria-hidden="true">close</span>
        </button>
    </div>
    <nav class="flex flex-col p-4 space-y-4 font-label-bold text-[12px] uppercase tracking-widest text-on-surface">
        <a href="categoria.html?c=politica" class="py-2 border-b border-border-subtle hover:text-secondary-container focus:text-secondary-container">Política</a>
        <a href="categoria.html?c=economia" class="py-2 border-b border-border-subtle hover:text-secondary-container focus:text-secondary-container">Economia</a>
        <a href="categoria.html?c=internacional" class="py-2 border-b border-border-subtle hover:text-secondary-container focus:text-secondary-container">Internacional</a>
        <a href="categoria.html?c=esportes" class="py-2 border-b border-border-subtle hover:text-secondary-container focus:text-secondary-container">Esportes</a>
        <a href="categoria.html?c=cultura" class="py-2 border-b border-border-subtle hover:text-secondary-container focus:text-secondary-container">Cultura</a>
        <a href="categoria.html?c=tecnologia" class="py-2 hover:text-secondary-container focus:text-secondary-container">Tecnologia</a>
    </nav>
</div>
<div id="drawerOverlay" class="fixed inset-0 bg-black/60 z-[90] hidden transition-opacity opacity-0"></div>

<!-- Toast Container -->
<div id="toastContainer" class="fixed bottom-20 md:bottom-8 right-4 md:right-8 z-[110] flex flex-col space-y-2 pointer-events-none"></div>

<!-- Global UI Scripts -->
<script>
    // Toasts
    window.showToast = function(message) {{
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = 'bg-primary text-white px-6 py-3 rounded shadow-xl font-meta text-[13px] flex items-center transform transition-all duration-300 translate-y-full opacity-0 pointer-events-auto';
        toast.innerHTML = `<span class="material-symbols-outlined mr-2 text-[18px]" aria-hidden="true">info</span> ${{message}}`;
        container.appendChild(toast);
        
        requestAnimationFrame(() => {{
            toast.classList.remove('translate-y-full', 'opacity-0');
        }});
        
        setTimeout(() => {{
            toast.classList.add('opacity-0', 'translate-y-2');
            setTimeout(() => toast.remove(), 300);
        }}, 3000);
    }};

    // Attach toasts to dummy buttons
    document.querySelectorAll('button:not([id]), a[href="#"]').forEach(btn => {{
        if(btn.textContent.trim() === 'Assine' || btn.textContent.trim() === 'Comprar' || btn.href?.endsWith('#')) {{
            btn.addEventListener('click', (e) => {{
                e.preventDefault();
                window.showToast("Recurso indisponível no momento.");
            }});
        }}
    }});

    // Mobile Drawer
    const drawer = document.getElementById('mobileDrawer');
    const overlay = document.getElementById('drawerOverlay');
    
    window.openDrawer = function() {{
        drawer.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Prevent scroll
        setTimeout(() => overlay.classList.remove('opacity-0'), 10);
    }};
    
    window.closeDrawer = function() {{
        drawer.classList.add('-translate-x-full');
        overlay.classList.add('opacity-0');
        document.body.style.overflow = '';
        setTimeout(() => overlay.classList.add('hidden'), 300);
    }};

    document.getElementById('closeDrawerBtn')?.addEventListener('click', closeDrawer);
    overlay?.addEventListener('click', closeDrawer);

    // Search Logic
    const searchModal = document.getElementById('searchModal');
    const searchInput = document.getElementById('searchInput');
    const closeSearchBtn = document.getElementById('closeSearchBtn');
    
    window.openSearch = function() {{
        searchModal.showModal();
        searchInput.focus();
    }};

    closeSearchBtn?.addEventListener('click', () => searchModal.close());
    
    document.addEventListener('keydown', (e) => {{
        if (e.ctrlKey && e.key === 'k') {{
            e.preventDefault();
            window.openSearch();
        }}
    }});

    let allPosts = [];
    searchModal?.addEventListener('click', (e) => {{
        if(e.target === searchModal) searchModal.close();
    }});

    searchInput?.addEventListener('input', async (e) => {{
        const query = e.target.value.toLowerCase().trim();
        const resultsDiv = document.getElementById('searchResults');
        
        if (query.length < 2) {{
            resultsDiv.innerHTML = '<div class="text-center text-outline-variant py-8 font-meta text-sm italic">Comece a digitar para buscar...</div>';
            return;
        }}

        if (allPosts.length === 0) {{
            try {{
                const res = await fetch('posts.json');
                allPosts = await res.json();
            }} catch (err) {{
                console.error(err);
            }}
        }}

        const filtered = allPosts.filter(p => p.title.toLowerCase().includes(query) || (p.excerpt && p.excerpt.toLowerCase().includes(query)));
        
        if (filtered.length === 0) {{
            resultsDiv.innerHTML = '<div class="text-center text-outline-variant py-8 font-meta text-sm">Nenhum resultado encontrado.</div>';
            return;
        }}

        resultsDiv.innerHTML = filtered.map(p => `
            <a href="materia.html?id=${{p.id}}" class="flex gap-4 p-3 hover:bg-surface-container-low rounded-lg transition-colors group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary-container">
                <div class="w-20 h-20 shrink-0 bg-gray-100 rounded overflow-hidden">
                    <img src="${{p.image}}" class="w-full h-full object-cover" loading="lazy" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400';">
                </div>
                <div class="flex-1">
                    <span class="text-[9px] uppercase tracking-wider text-editorial-green-deep font-label-bold">${{p.category}}</span>
                    <h4 class="font-headline-sm text-sm font-bold text-primary group-hover:underline line-clamp-2">${{p.title}}</h4>
                </div>
            </a>
        `).join('');
    }});
</script>

</body>
</html>
"""

    with open(r"c:\Users\leose\Downloads\tagmanews-main\index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("Site index.html compiled successfully in root directory.")

if __name__ == '__main__':
    build_site()
