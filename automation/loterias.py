import os
import json
import ssl
import time
import urllib.request
from datetime import datetime
from publish import call_groq_api, publish_article

def test_caixa_api(lottery):
    url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/{lottery}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    })
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            data = json.loads(response.read())
            return data
    except Exception as e:
        print(f"Error fetching {lottery}: {e}")
        return None

def generate_lottery_report():
    print("Iniciando varredura das Loterias Oficiais da Caixa...")
    
    lotteries = [
        ('megasena', 'Mega-Sena'),
        ('lotofacil', 'Lotofácil'),
        ('quina', 'Quina'),
        ('lotomania', 'Lotomania')
    ]
    
    # Load advanced guidelines
    guidelines_path = os.path.join(os.path.dirname(__file__), 'prompt_guidelines.txt')
    advanced_guidelines = ""
    if os.path.exists(guidelines_path):
        with open(guidelines_path, 'r', encoding='utf-8') as gf:
            advanced_guidelines = gf.read()

    for code, name in lotteries:
        print(f"\nColetando dados: {name}")
        data = test_caixa_api(code)
        
        if not data:
            print(f"Falha ao obter dados de {name}. Pulando...")
            continue
            
        concurso = data.get('numero')
        data_sorteio = data.get('dataApuracao')
        dezenas = ", ".join(data.get('listaDezenas', []))
        acumulou = "SIM (Acumulou)" if data.get('acumulado') else "NÃO (Houve ganhadores)"
        premio_estimado = data.get('valorEstimadoProximoConcurso', 0)
        
        prompt = f"""
{advanced_guidelines}

Atue como um jornalista investigativo e financeiro de alta credibilidade.
Sua tarefa é escrever uma reportagem original e aprofundada informando o resultado do último sorteio oficial da loteria '{name}'. O texto NÃO PODE USAR TRAVESSÕES.

DADOS BRUTOS OFICIAIS (CAIXA ECONÔMICA FEDERAL):
Loteria: {name}
Concurso: {concurso}
Data do Sorteio: {data_sorteio}
Dezenas Sorteadas: {dezenas}
Acumulou? {acumulou}
Prêmio Estimado para o Próximo Concurso: R$ {premio_estimado:,.2f}

INSTRUÇÕES DE REDAÇÃO (CRÍTICO PARA ADSENSE E EEAT):
1. Informe os números exatos e se a loteria acumulou. Explique rapidamente como funciona essa loteria e a probabilidade matemática.
2. Adicione contexto socioeconômico sobre o que esse valor representa na vida dos brasileiros ou inclua uma citação simulada verossímil de um economista sobre educação financeira ou destinação de prêmios.
3. Não faça uma lista enumerada simples com os números. Incorpore os dados organicamente no texto.
4. O artigo DEVE ter mais de 500 palavras e usar marcações Markdown autênticas (H1, H2, negritos). 
5. Cumpra a promessa de entregar uma dica de planejamento no final.

Você deve retornar ESTRITAMENTE um objeto JSON válido (sem tags markdown na borda do JSON). Siga esta estrutura exata:
{{
    "title": "Novo título magnético e jornalístico (sem sensacionalismo, incluindo o nome {name})",
    "excerpt": "Linha fina / subtítulo impactante com os números centrais",
    "content": "O texto completo da reportagem formatado rigorosamente em Markdown autêntico (mínimo 500 palavras, H2, H3, sem usar travessões).",
    "tags": ["{name.lower()}", "sorteio", "loterias da caixa", "resultado"],
    "keyword_imagem_ingles": "lottery ticket money"
}}
"""
        
        try:
            response_text = call_groq_api(prompt, dense=False)
            output_data = json.loads(response_text)
            
            post_id = publish_article(
                title=output_data['title'],
                excerpt=output_data['excerpt'],
                content=output_data['content'],
                category="Economia", # Loteria moves to Economia for better indexing
                author="Redação Tagma",
                tags=output_data.get('tags', ['loterias']),
                image_query=output_data.get('keyword_imagem_ingles', 'money lottery')
            )
            print(f"Sucesso! Matéria da {name} publicada: {post_id}")
            time.sleep(20) # Pausa segura entre loterias para o Groq
        except Exception as e:
            print(f"Falha ao gerar matéria da {name}: {e}")

if __name__ == "__main__":
    generate_lottery_report()
