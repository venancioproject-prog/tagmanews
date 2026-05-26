import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_games_report():
    print("Generating games review report...")
    
    games_list = [
        {"title": "Hades II", "genre": "Roguelike de Ação", "platform": "PC (Steam)", "developer": "Supergiant Games", "aspect": "sistema de combate refinado e progressão narrativa"},
        {"title": "Elden Ring: Shadow of the Erdtree", "genre": "RPG de Ação", "platform": "PC, PlayStation 5, Xbox Series X/S", "developer": "FromSoftware", "aspect": "expansão do mapa e novos chefes desafiadores"},
        {"title": "Senua's Saga: Hellblade II", "genre": "Aventura/Ação Cinematográfica", "platform": "PC, Xbox Series X/S (Disponível no Xbox Game Pass)", "developer": "Ninja Theory", "aspect": "fidelidade gráfica avançada e design de áudio imersivo"},
        {"title": "Helldivers 2", "genre": "Tiro Tático Cooperativo", "platform": "PC, PlayStation 5", "developer": "Arrowhead Game Studios", "aspect": "sistema de física caótico e dinâmica de jogo cooperativo contínuo"},
        {"title": "Baldur's Gate 3", "genre": "RPG de Turnos", "platform": "PC, PlayStation 5, Xbox Series X/S", "developer": "Larian Studios", "aspect": "profundidade de escolhas narrativas e adaptação do sistema D&D 5ª edição"}
    ]
    
    selected_game = random.choice(games_list)
    data_str = json.dumps(selected_game, ensure_ascii=False)
    
    prompt = f"""
    Escreva uma análise técnica jornalística sobre um jogo eletrônico em evidência no mercado.
    Baseie-se nos seguintes dados do jogo fornecidos em JSON:
    {data_str}
    
    Aborde os aspectos técnicos do jogo, mecânicas de gameplay, plataformas disponíveis e recepção de público/crítica de forma neutra e objetiva.
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (ex: 'Análise técnica de [Título do Jogo] avalia desempenho e mecânicas no [Plataforma]')",
        "excerpt": "Um resumo em uma frase da análise do jogo (máximo 160 caracteres)",
        "content": "O texto jornalístico completo dividido em pelo menos 3 parágrafos explicativos (sem subtítulos, apenas tags de parágrafo normais ou linhas vazias)",
        "tags": ["games", "jogos eletrônicos", "steam", "review", "tecnologia"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'video game' ou 'gaming controller')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False)
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['games', 'jogos eletrônicos', 'review'])
        image_query = data.get('keyword_imagem_ingles', 'video game')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="TV e Celebridades", # Or Geral. Since TV e Celebridades/Cultura covers games, we put it here or Geral
            author="Redação Games",
            tags=tags,
            image_query=image_query
        )
        print(f"Games report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate games report: {e}")

if __name__ == "__main__":
    generate_games_report()
