import glob
import re

files = glob.glob('automation/*.py')
new_phrase = '"content": "Um artigo jornalístico profissional, extenso e aprofundado (mínimo de 500 palavras), formatado obrigatoriamente em Markdown autêntico (usando hashtags ## para subtítulos reais, listas com -, e texto em negrito com **). O texto DEVE conter manchete atrativa no H1, lide jornalístico, análise de contexto profundo, desdobramentos, impacto na sociedade ou mercado, e citações (entre aspas) simuladas de especialistas ou entidades para dar credibilidade e peso à matéria. Escreva com excelência como um repórter premiado de um grande portal de credibilidade (como G1, Reuters ou Estadão)."'

for f in files:
    if f.endswith('publish.py'): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to replace "content": "..."
    content = re.sub(r'"content":\s*".*?"', new_phrase, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print('Regex updated', f)
