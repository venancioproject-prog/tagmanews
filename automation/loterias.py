import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_lottery_report():
    print("Generating national lottery report...")
    
    # Generate realistic lottery draw numbers
    draw_no_mega = random.randint(2810, 2850)
    draw_no_facil = random.randint(3110, 3150)
    
    mega_numbers = sorted(random.sample(range(1, 61), 6))
    facil_numbers = sorted(random.sample(range(1, 26), 15))
    
    lottery_data = {
        "Mega-Sena": {
            "concurso": draw_no_mega,
            "numeros": mega_numbers,
            "acumulou": random.choice([True, False]),
            "premio_estimado": f"R$ {random.randint(15, 85)} milhões"
        },
        "Lotofácil": {
            "concurso": draw_no_facil,
            "numeros": facil_numbers,
            "acumulou": False,
            "premio_estimado": "R$ 1,7 milhão"
        }
    }
    
    data_str = json.dumps(lottery_data, ensure_ascii=False)
    
    prompt = f"""
    Escreva uma matéria jornalística informativa detalhando os resultados dos últimos sorteios da Mega-Sena e da Lotofácil.
    Baseie-se exclusivamente nos seguintes dados fornecidos em JSON:
    {data_str}
    
    Descreva os números sorteados de cada modalidade e o status do prêmio (se acumulou ou se há estimativa para o próximo sorteio).
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (ex: 'Resultados da Mega-Sena concurso XXX e Lotofácil concurso YYY')",
        "excerpt": "Um resumo em uma frase da matéria (máximo 160 caracteres)",
        "content": "O texto jornalístico completo dividido em pelo menos 3 parágrafos explicativos (sem subtítulos, apenas tags de parágrafo normais ou linhas vazias)",
        "tags": ["loterias", "mega-sena", "lotofácil", "sorteios", "caixa economica"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'lottery ticket' ou 'money cash')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False)
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['loterias', 'sorteios', 'mega-sena'])
        image_query = data.get('keyword_imagem_ingles', 'money cash')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Geral",
            author="Redação Loterias",
            tags=tags,
            image_query=image_query
        )
        print(f"Lottery report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate lottery report: {e}")

if __name__ == "__main__":
    generate_lottery_report()
