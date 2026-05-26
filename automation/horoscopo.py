import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_horoscope():
    print("Generating weekly behavior and horoscope report...")
    
    # We choose a general behavioral/astrological trend focus
    focuses = [
        "organização de rotina e priorização de tarefas profissionais",
        "gestão de tempo e redução de estresse nas comunicações de trabalho",
        "reflexão interna e equilíbrio entre vida pessoal e obrigações",
        "planejamento financeiro de curto prazo e controle de impulsos de consumo",
        "estímulo à criatividade e resolução pragmática de pendências antigas"
    ]
    
    selected_focus = random.choice(focuses)
    
    prompt = f"""
    Escreva um artigo de comportamento focado em recomendações de organização pessoal, bem-estar e planejamento semanal com base na transição astral do momento.
    O foco desta semana deve ser: {selected_focus}.
    
    Evite misticismo excessivo ou previsões de sorte/azar. Mantenha um tom de aconselhamento prático sobre comportamento, rotina saudável e produtividade para os leitores.
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (ex: 'Previsão comportamental sugere foco em [Tema] nesta semana')",
        "excerpt": "Um resumo em uma frase do artigo de comportamento (máximo 160 caracteres)",
        "content": "O texto completo dividido em pelo menos 3 parágrafos explicativos (sem subtítulos, apenas tags de parágrafo normais ou linhas vazias)",
        "tags": ["comportamento", "horóscopo", "produtividade", "rotina", "bem-estar"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'zen space' ou 'calendar planner')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False)
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['comportamento', 'bem-estar', 'planejamento'])
        image_query = data.get('keyword_imagem_ingles', 'calendar planner')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Comportamento",
            author="Canal Comportamento",
            tags=tags,
            image_query=image_query
        )
        print(f"Horoscope/Behavior report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate horoscope report: {e}")

if __name__ == "__main__":
    generate_horoscope()
