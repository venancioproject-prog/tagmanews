import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_weather_report():
    print("Generating national weather report...")
    
    # Mock data with realistic temperature ranges for main Brazilian capitals
    capitals_data = {
        "São Paulo": {"temp": random.randint(16, 24), "condition": random.choice(["nublado com garoa", "sol entre nuvens", "chuvas isoladas"])},
        "Rio de Janeiro": {"temp": random.randint(22, 29), "condition": random.choice(["ensolarado", "sol com algumas nuvens", "pancadas de chuva à tarde"])},
        "Brasília": {"temp": random.randint(18, 26), "condition": random.choice(["tempo firme e seco", "poucas nuvens", "céu aberto"])},
        "Salvador": {"temp": random.randint(24, 30), "condition": random.choice(["chuvas rápidas", "sol com aumento de nuvens", "ensolarado"])},
        "Porto Alegre": {"temp": random.randint(12, 19), "condition": random.choice(["frio com névoa úmida", "céu nublado", "chuva contínua"])},
        "Manaus": {"temp": random.randint(26, 33), "condition": random.choice(["abafado com pancadas de chuva", "trovoadas isoladas", "calor e umidade alta"])}
    }
    
    # Format the data into a prompt
    data_str = json.dumps(capitals_data, ensure_ascii=False)
    
    prompt = f"""
    Gere uma matéria jornalística informativa e objetiva sobre a previsão do tempo para as capitais brasileiras hoje.
    Baseie-se exclusivamente nos seguintes dados reais fornecidos em JSON:
    {data_str}
    
    O seu texto DEVE descrever as condições climáticas nessas capitais sem floreios ou termos informais.
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (jornalístico, informativo e sem sensacionalismo)",
        "excerpt": "Um resumo em uma ou duas frases para servir de linha de apoio (máximo 160 caracteres)",
        "content": "O texto jornalístico completo dividido em pelo menos 3 parágrafos explicativos (sem subtítulos, apenas tags de parágrafo normais ou linhas vazias)",
        "tags": ["clima", "previsão do tempo", "capitais", "meteorologia"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'brazil weather' ou 'cloudy sky')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False)
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['clima', 'previsão do tempo', 'capitais'])
        image_query = data.get('keyword_imagem_ingles', 'cloudy sky')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Internacional", # Colocamos na editoria Internacional ou Geral (o site usa: Política, Economia, Internacional, Esportes, Cultura, Tecnologia)
            author="Redação Clima",
            tags=tags,
            image_query=image_query
        )
        print(f"Weather report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate weather report: {e}")

if __name__ == "__main__":
    generate_weather_report()
