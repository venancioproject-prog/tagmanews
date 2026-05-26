import json
import random
from datetime import datetime
from publish import call_groq_api, publish_article

def generate_ibge_report():
    print("Generating IBGE/Socioeconomic data report...")
    
    topics = [
        {
            "indicator": "Censo Demográfico 2022: Envelhecimento da População", 
            "data": "A idade mediana da população brasileira subiu de 29 anos em 2010 para 35 anos em 2022, indicando um aumento da proporção de idosos e desaceleração do crescimento populacional."
        },
        {
            "indicator": "PNAD Contínua: Mercado de Trabalho e Desocupação", 
            "data": "A taxa de desocupação no país registrou recuo para 7,5% no trimestre de análise, com rendimento médio real estimado em R$ 3.118 por trabalhador ativo."
        },
        {
            "indicator": "IPCA: Índice Nacional de Preços ao Consumidor Ampliado", 
            "data": "A inflação oficial medida pelo IPCA registrou alta acumulada de 4,3% nos últimos 12 meses, com os grupos de transportes e alimentação fora do lar representando as maiores pressões de custos."
        },
        {
            "indicator": "Pesquisa Industrial Mensal (PIM): Bens de Capital", 
            "data": "A produção industrial nacional apresentou alta pontual de 0,3%, impulsionada principalmente pelo setor de bens de capital e pela fabricação de máquinas e equipamentos eletrônicos."
        },
        {
            "indicator": "Censo Demográfico 2022: Crescimento de Cidades Médias", 
            "data": "Municípios de médio porte, que possuem entre 100 mil e 500 mil habitantes, apresentaram o maior ritmo relativo de crescimento demográfico e migração interna no país."
        }
    ]
    
    selected_topic = random.choice(topics)
    data_str = json.dumps(selected_topic, ensure_ascii=False)
    
    prompt = f"""
    Escreva um artigo de jornalismo de dados e análise socioeconomicodemográfica.
    Baseie-se no seguinte tópico e dados estatísticos fornecidos em JSON:
    {data_str}
    
    Explique o significado dos dados apresentados, a tendência histórica e as consequências para as políticas públicas e planejamento econômico de forma analítica, fria, clara e puramente factual.
    
    REGRAS DE REDAÇÃO (OBRIGATÓRIAS):
    - NÃO use adjetivos como: crucial, fundamental, espetacular, impressionante, chocante, incrível.
    - NÃO use conclusões prontas ou clichês de IA (ex: 'em suma', 'portanto', 'em resumo', 'concluindo', 'seja como for').
    - NÃO use palavras de transição comuns de IA (ex: 'mergulhe', 'jornada', 'desvendar', 'explorar', 'rico').
    - Apresente apenas fatos objetivos e dados concretos.
    
    Você deve retornar estritamente um objeto JSON com a seguinte estrutura de chaves (sem formatação markdown de código, apenas o JSON cru):
    {{
        "title": "Título da matéria (ex: '[Tema] reflete mudanças na estrutura econômica do país')",
        "excerpt": "Um resumo em uma frase dos dados analisados (máximo 160 caracteres)",
        "content": "Um artigo jornalístico profissional, extenso e aprofundado (mínimo de 500 palavras), formatado obrigatoriamente em Markdown autêntico (usando hashtags ## para subtítulos reais, listas com -, e texto em negrito com **). O texto DEVE conter manchete atrativa no H1, lide jornalístico, análise de contexto profundo, desdobramentos, impacto na sociedade ou mercado, e citações (entre aspas) simuladas de especialistas ou entidades para dar credibilidade e peso à matéria. Escreva com excelência como um repórter premiado de um grande portal de credibilidade (como G1, Reuters ou Estadão).",
        "tags": ["sociedade", "ibge", "censo", "economia", "dados demograficos"],
        "keyword_imagem_ingles": "query em inglês curta de 2 palavras para buscar foto no Pexels (ex: 'brazil city' ou 'demographic census')"
    }}
    """
    
    try:
        response_text = call_groq_api(prompt, dense=False) # use lightweight model (dense model was decommissioned)
        data = json.loads(response_text)
        
        title = data['title']
        excerpt = data['excerpt']
        content = data['content']
        tags = data.get('tags', ['sociedade', 'ibge', 'dados demograficos'])
        image_query = data.get('keyword_imagem_ingles', 'brazil city')
        
        post_id = publish_article(
            title=title,
            excerpt=excerpt,
            content=content,
            category="História e Sociedade",
            author="Redação Sociedade",
            tags=tags,
            image_query=image_query
        )
        print(f"IBGE report published successfully! ID: {post_id}")
    except Exception as e:
        print(f"Failed to generate IBGE report: {e}")

if __name__ == "__main__":
    generate_ibge_report()
