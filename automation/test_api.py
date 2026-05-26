import os
import json
from publish import call_groq_api, fetch_pexels_image

def test_pexels():
    print("--- TESTING PEXELS API ---")
    query = "financial stock market"
    image_url = fetch_pexels_image(query, "Economia")
    if image_url and image_url.startswith("http"):
        print(f"SUCCESS: Pexels API returned image URL: {image_url}")
        return True
    else:
        print("FAILED: Pexels API test failed.")
        return False

def test_groq():
    print("\n--- TESTING GROQ API (Llama 3 8B) ---")
    prompt = (
        "Gere um JSON com os seguintes campos sobre o clima de hoje em São Paulo:\n"
        "1. title: O título da notícia\n"
        "2. excerpt: Resumo curto da notícia\n"
        "3. content: O texto jornalístico completo da matéria (1 parágrafo com fatos objetivos)\n"
        "4. keyword: palavra chave em inglês de 2 palavras para buscar imagem\n"
        "Lembrete: Responda APENAS com o JSON cru, sem caracteres extras."
    )
    try:
        response_text = call_groq_api(prompt, dense=False)
        print("Raw Groq Response:")
        print(response_text)
        
        # Verify JSON parsing
        data = json.loads(response_text)
        if all(k in data for k in ['title', 'excerpt', 'content', 'keyword']):
            print("SUCCESS: Groq API returned valid JSON with all required fields!")
            print(f"Title: {data['title']}")
            print(f"Keyword: {data['keyword']}")
            return True
        else:
            print("FAILED: Groq API JSON missing keys.")
            return False
    except Exception as e:
        print(f"FAILED: Groq API call raised error: {e}")
        return False

if __name__ == "__main__":
    pexels_success = test_pexels()
    groq_success = test_groq()
    
    print("\n--- TEST SUMMARY ---")
    print(f"Pexels API: {'WORKING' if pexels_success else 'FAILED'}")
    print(f"Groq API: {'WORKING' if groq_success else 'FAILED'}")
