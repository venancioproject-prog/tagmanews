import re

def process_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Extract base.html
    main_start = html.find('<main class="container-custom px-4 lg:px-8 py-8 md:py-12">')
    main_end = html.find('</main>')
    
    if main_start == -1 or main_end == -1:
        print("Could not find main tags")
        return

    main_start_tag_end = main_start + len('<main class="container-custom px-4 lg:px-8 py-8 md:py-12">')
    
    base_html = html[:main_start_tag_end] + '\n{% block content %}\n{% endblock %}\n' + html[main_end:]
    
    with open('base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)

    # 2. Extract index.html
    main_content = html[main_start_tag_end:main_end]
    
    # 3. Replace the repeating blocks
    # Looking at the original HTML, the "Ciência & Tecnologia" section is:
    # <section class="space-y-8">
    # <h2 class="...">Ciência &amp; Tecnologia</h2>
    # <div class="...">...</div>
    # <div class="...">...</div>
    # </section>
    
    # We will replace the inner contents of these sections.
    # The sections to target are inside a div: <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12 pt-8 border-t border-outline-variant">
    
    replacement_loop = """
{% for post in collections.posts %}
<div class="group cursor-pointer border-b border-outline-variant pb-6">
<a href="{{ post.url }}">
<span class="font-label-bold text-[9px] text-outline uppercase tracking-wider">{{ post.category }}</span>
<h3 class="font-headline-sm text-[20px] mt-1 group-hover:underline">{{ post.title }}</h3>
</a>
</div>
{% endfor %}"""

    # We will just replace the entire <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12 pt-8 border-t border-outline-variant"> ... </div>
    # with a single section containing the loop. Or keep the columns?
    # "Substitua a estrutura repetitiva em HTML pela sintaxe de loop do Stitch"
    # The prompt says: "localize as seções onde as notícias secundárias estão fixas (como os blocos de "Ciência & Tecnologia" ou "Cultura & Economia"). Substitua a estrutura repetitiva em HTML pela sintaxe de loop"
    
    # Let's replace the first section's articles with the loop, and remove the second section completely to avoid having two identical loops side by side, or replace both.
    # Let's replace both sections' content with the loop.
    
    # Section 1 (Ciência & Tecnologia)
    pattern1 = re.compile(r'(<h2[^>]*>Ciência &amp; Tecnologia</h2>).*?(</section>)', re.DOTALL)
    main_content = pattern1.sub(r'\1' + replacement_loop + r'\n\2', main_content)

    # Section 2 (Cultura & Economia)
    pattern2 = re.compile(r'(<h2[^>]*>Cultura &amp; Economia</h2>).*?(</section>)', re.DOTALL)
    main_content = pattern2.sub(r'\1' + replacement_loop + r'\n\2', main_content)

    index_html = '{% extends "base.html" %}\n\n{% block content %}\n' + main_content + '\n{% endblock %}\n'
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    print("Processed successfully.")

if __name__ == '__main__':
    process_html()
