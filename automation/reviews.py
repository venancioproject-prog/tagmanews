import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

# Placeholder list of product categories and example items (normally fetched via Amazon API)
PRODUCTS = [
    {"title": "Echo Dot (5ª geração)", "category": "Eletrônicos", "price": "R$ 299", "benefit": "Assistente de voz Alexa integrado"},
    {"title": "Kindle Paperwhite", "category": "Leitura", "price": "R$ 449", "benefit": "Tela antirreflexo e bateria de semanas"},
    {"title": "Cafeteira Nespresso Vertuo", "category": "Café", "price": "R$ 399", "benefit": "Cápsulas compatíveis com várias intensidades"},
    {"title": "Fitbit Charge 6", "category": "Fitness", "price": "R$ 399", "benefit": "Monitoramento avançado de saúde e sono"},
    {"title": "Headset Logitech G733", "category": "Games", "price": "R$ 599", "benefit": "Áudio sem fio com som surround"}
]

def generate_product_review():
    print("Generating product review for affiliate link...")
    product = random.choice(PRODUCTS)
    data_str = json.dumps(product, ensure_ascii=False)

    prompt = f"""
    Escreva uma análise curta, objetiva e jornalística sobre o produto abaixo, destacando suas características técnicas, preço e benefícios práticos para o consumidor.
    Dados do produto (JSON):
    {data_str}
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura:
    {{
        "title": "Título da matéria "{{product['title']}}" (objetivo e informativo)",
        "excerpt": "Resumo curto (máx 160 caracteres) sobre o produto e utilidade",
        "content": "Texto jornalístico dividido em ao menos 3 parágrafos que descrevem especificações, preço, e aplicação prática",
        "tags": ["review", "produto", "consumidor", "tecnologia", "afiliado"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'product review' ou 'gadget')"
    }}
    """
    try:
        response_text = call_groq_api(prompt, dense=False)
        data = json.loads(response_text)
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['review', 'produto'])
        image_query = data.get('keyword_imagem_ingles', 'product review')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Geral",
            author="Redação Afiliados",
            tags=tags,
            image_query=image_query
        )
        print(f"Product review published! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate product review: {e}")

if __name__ == "__main__":
    generate_product_review()
