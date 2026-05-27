import sys
import time
from rss_news import curate_and_publish, RSS_FEEDS

def main():
    print("--- Inciando Boot/Auto-Curation Geral ---")
    categories = list(RSS_FEEDS.keys())
    
    for cat in categories:
        print(f"\n--- Gerando matéria para o eixo: {cat} ---")
        curate_and_publish(cat, count=1)
        
        # Pausa de segurança de 15 segundos para evitar bloqueio 429 da API do Groq
        print("Pausa de 15 segundos antes da próxima editoria...")
        time.sleep(15)
        
if __name__ == "__main__":
    main()
