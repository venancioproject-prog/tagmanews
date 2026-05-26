import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

# Simple placeholder list of SaaS products with brief descriptors
SAAS_PRODUCTS = [
    {"name": "Notion", "category": "Produtividade", "price": "Planos a partir de US$ 4/mês", "benefit": "Organização tudo‑em‑um com documentos, bases de dados e blocos"},
    {"name": "Canva Pro", "category": "Design", "price": "US$ 12,99/mês", "benefit": "Acesso a milhões de templates, imagens premium e exportação avançada"},
    {"name": "Zapier", "category": "Automação", "price": "Planos a partir de US$ 20/mês", "benefit": "Conexão de apps via workflows sem código"},
    {"name": "Slack Enterprise Grid", "category": "Comunicação", "price": "Preços personalizados", "benefit": "Plataforma de mensagens centralizada para grandes organizações"},
    {"name": "Webflow", "category": "Web Design", "price": "Planos a partir de US$ 16/mês", "benefit": "Construtor visual com CMS e hosting integrado"}
]

def generate_saas_affiliate():
    print("Generating SaaS affiliate article...")
    product = random.choice(SAAS_PRODUCTS)
    data_str = json.dumps(product, ensure_ascii=False)

    prompt = f"""
    Escreva uma matéria curta, objetiva e jornalística que apresente o SaaS abaixo, descrevendo seu propósito, principais recursos, modelo de preço e benefícios práticos para o usuário ou empresa.
    Dados do produto (JSON):
    {data_str}
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria "{{product['name']}}" (informativo e direto)",
        "excerpt": "Resumo curto (máx 160 caracteres) sobre a proposta e valor do SaaS",
        "content": "Texto jornalístico dividido em ao menos 3 parágrafos que detalham funcionalidades, uso prático e preço",
        "tags": ["saas", "software", "affiliate", "technology", "review"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'software interface' ou 'cloud service')"
    }}
    """
    try:
        response_text = call_groq_api(prompt, dense=False)
        data = json.loads(response_text)
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['saas', 'software'])
        image_query = data.get('keyword_imagem_ingles', 'software interface')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Geral",
            author="Redação Afiliados",
            tags=tags,
            image_query=image_query
        )
        print(f"SaaS affiliate article published! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate SaaS affiliate article: {e}")

if __name__ == "__main__":
    generate_saas_affiliate()
