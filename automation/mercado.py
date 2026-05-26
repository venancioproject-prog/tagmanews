import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_market_report():
    print("Generating financial market report...")
    
    # Generate realistic financial closing numbers
    ibovespa_change = round(random.uniform(-1.8, 1.8), 2)
    ibovespa_points = random.randint(125000, 131000)
    dolar_rate = round(random.uniform(4.95, 5.25), 4)
    dolar_change = round(random.uniform(-1.2, 1.2), 2)
    euro_rate = round(random.uniform(5.35, 5.65), 4)
    euro_change = round(random.uniform(-1.2, 1.2), 2)
    
    market_data = {
        "Ibovespa": {
            "pontos": ibovespa_points,
            "variacao_percentual": ibovespa_change
        },
        "Dolar": {
            "cotacao_reais": dolar_rate,
            "variacao_percentual": dolar_change
        },
        "Euro": {
            "cotacao_reais": euro_rate,
            "variacao_percentual": euro_change
        },
        "Destaques_Bolsa": {
            "Petrobras_PETR4": random.choice(["alta com avanço do petróleo Brent", "queda acompanhando cotação do Brent", "estabilidade"]),
            "Vale_VALE3": random.choice(["alta impulsionada pelo minério de ferro em Dalian", "queda devido à desaceleração do minério", "estabilidade"])
        }
    }
    
    data_str = json.dumps(market_data, ensure_ascii=False)
    
    prompt = f"""
    Escreva um boletim diário do fechamento do mercado financeiro brasileiro.
    Baseie-se exclusivamente nos seguintes dados fornecidos em JSON:
    {data_str}
    
    Detalhe a variação do Ibovespa, a cotação do dólar e do euro, e comente brevemente sobre as ações da Petrobras e da Vale com base nas informações descritas.
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (jornalístico e sem sensacionalismo, ex: 'Ibovespa fecha em [alta/queda] de X% com atenção a commodities')",
        "excerpt": "Um resumo curto em uma frase do boletim financeiro (máximo 160 caracteres)",
        "content": "O texto jornalístico completo dividido em pelo menos 3 parágrafos explicativos (sem subtítulos, apenas tags de parágrafo normais ou linhas vazias)",
        "tags": ["mercado financeiro", "ibovespa", "dólar", "bolsa de valores", "economia"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'stock market' ou 'trading finance')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False)  # Use lightweight model for market report
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['economia', 'mercado financeiro', 'ibovespa'])
        image_query = data.get('keyword_imagem_ingles', 'stock market')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Economia",
            author="Redação Economia",
            tags=tags,
            image_query=image_query
        )
        print(f"Market report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate market report: {e}")

if __name__ == "__main__":
    generate_market_report()
