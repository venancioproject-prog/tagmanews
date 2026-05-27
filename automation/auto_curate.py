import random
import time
from rss_news import curate_and_publish, RSS_FEEDS

def main():
    print("--- Iniciando Auto-Curadoria (Drip-Feed) ---")
    categories = list(RSS_FEEDS.keys())
    
    # Escolhe apenas 1 categoria aleatória para não sobrecarregar a API do Groq
    chosen_cat = random.choice(categories)
    
    print(f"\nCategoria sorteada para este ciclo: {chosen_cat}")
    curate_and_publish(chosen_cat, count=1)
    
if __name__ == "__main__":
    main()
