import random
from rss_news import curate_and_publish, RSS_FEEDS

def main():
    # Pick 2 random categories to curate 1 article each
    categories = list(RSS_FEEDS.keys())
    chosen_cats = random.sample(categories, 2)
    
    for cat in chosen_cats:
        print(f"--- Auto Curation: {cat} ---")
        curate_and_publish(cat, count=1)
        
if __name__ == "__main__":
    main()
