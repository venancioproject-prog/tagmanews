import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_tech_report():
    print("Generating tech and AI report...")
    
    topics = [
        {"topic": "Adoção de modelos de inteligência artificial de código aberto em servidores locais", "context": "Crescimento da implementação de LLMs locais por corporações que visam garantir privacidade de dados e conformidade regulatória."},
        {"topic": "Competição tecnológica na manufatura de chips de silício para processamento de IA", "context": "Análise da demanda industrial por novos aceleradores gráficos da NVIDIA (arquitetura Blackwell) e concorrência direta de novos designs da AMD e Intel."},
        {"topic": "Regulamentação e diretrizes de conformidade para o uso de inteligência artificial", "context": "Atualizações sobre a implementação do AI Act na União Europeia e discussões legislativas no Congresso dos Estados Unidos sobre responsabilidade de dados corporativos."},
        {"topic": "Integração de agentes autônomos de IA em sistemas operacionais móveis", "context": "Desenvolvimento de novos recursos de processamento local (on-device) de linguagem natural no Android e iOS, reduzindo dependência de servidores na nuvem."},
        {"topic": "Avanços experimentais em hardware e correção de erros na computação quântica", "context": "Publicação de novas pesquisas focadas em qubits físicos supercondutores voltados a mitigar a taxa de erros lógicos em algoritmos complexos."}
    ]
    
    selected_topic = random.choice(topics)
    data_str = json.dumps(selected_topic, ensure_ascii=False)
    
    prompt = f"""
    Escreva um artigo de divulgação científica e tecnológica sobre o seguinte tópico em evidência:
    {data_str}
    
    Descreva a importância do tema, o contexto da indústria ou pesquisa e as implicações práticas de forma técnica, imparcial e puramente factual.
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (ex: '[Tema] altera dinâmica de mercado de tecnologia')",
        "excerpt": "Um resumo em uma frase da matéria (máximo 160 caracteres)",
        "content": "O texto jornalístico completo dividido em pelo menos 3 parágrafos explicativos (sem subtítulos, apenas tags de parágrafo normais ou linhas vazias)",
        "tags": ["tecnologia", "inteligência artificial", "inovação", "ciência", "corporativo"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'artificial intelligence' ou 'microchip hardware')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False) # use lightweight model for tech report
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['tecnologia', 'inteligência artificial', 'inovação'])
        image_query = data.get('keyword_imagem_ingles', 'artificial intelligence')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="Ciência",
            author="Redação Tecnologia",
            tags=tags,
            image_query=image_query
        )
        print(f"Tech report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate tech report: {e}")

if __name__ == "__main__":
    generate_tech_report()
