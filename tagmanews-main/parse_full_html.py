import re
import html
import json
from html.parser import HTMLParser

class TNCParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = []
        self.current_tag = None
        self.in_heading = False
        self.in_excerpt = False
        self.in_category = False
        self.current_article = None
        self.heading_level = None
        
        # Temp fields
        self.temp_text = []
        self.temp_excerpt = []
        self.temp_category = []
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        # In Elementor, posts are typically in containers with classes like "elementor-post"
        # Or let's detect when we enter a heading (h1, h2, h3, h4) that contains a link
        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.in_heading = True
            self.heading_level = tag
            self.temp_text = []
            # Start a new article search
            self.current_article = {
                'title': '',
                'tag': tag,
                'url': '',
                'image': '',
                'category': '',
                'excerpt': ''
            }
            
        elif self.in_heading and tag == 'a' and self.current_article:
            if 'href' in attrs_dict:
                self.current_article['url'] = attrs_dict['href']
                
        # Detect images inside containers
        elif tag == 'img' and self.current_article:
            # If we find an image and don't have one yet, assign it
            # Elementor uses src, data-src, srcset
            img_src = attrs_dict.get('src') or attrs_dict.get('data-src')
            if img_src and not self.current_article['image']:
                # Ignore small spacer or loading images
                if not any(x in img_src.lower() for x in ['spacer', 'shim', 'avatar', 'logo']):
                    self.current_article['image'] = img_src
                    
        # Detect category links (usually has /editoria/ in href)
        elif tag == 'a' and 'href' in attrs_dict and '/editoria/' in attrs_dict['href']:
            self.in_category = True
            self.temp_category = []
            
        # Detect paragraph tags for excerpts
        elif tag == 'p' and self.current_article:
            self.in_excerpt = True
            self.temp_excerpt = []

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.in_heading = False
            if self.current_article:
                title_text = "".join(self.temp_text).strip()
                title_text = re.sub(r'\s+', ' ', title_text)
                self.current_article['title'] = html.unescape(title_text)
                
                # Deduplicate and validate
                if len(self.current_article['title']) > 10:
                    # Look at what category we captured around it or within it
                    # Let's add it to articles
                    self.articles.append(self.current_article)
                self.current_article = None
                
        elif tag == 'a' and self.in_category:
            self.in_category = False
            cat_text = "".join(self.temp_category).strip()
            # If we are currently building an article, assign category to it
            # Otherwise, assign it to the last added article if it doesn't have one yet
            cat_text = html.unescape(cat_text)
            if self.current_article:
                self.current_article['category'] = cat_text
            elif self.articles:
                # Assign to last article if it was just added and has no category
                if not self.articles[-1]['category']:
                    self.articles[-1]['category'] = cat_text
                    
        elif tag == 'p' and self.in_excerpt:
            self.in_excerpt = False
            exc_text = "".join(self.temp_excerpt).strip()
            exc_text = re.sub(r'\s+', ' ', exc_text)
            exc_text = html.unescape(exc_text)
            if self.current_article:
                self.current_article['excerpt'] = exc_text
            elif self.articles:
                if not self.articles[-1]['excerpt']:
                    self.articles[-1]['excerpt'] = exc_text

    def handle_data(self, data):
        if self.in_heading:
            self.temp_text.append(data)
        if self.in_category:
            self.temp_category.append(data)
        if self.in_excerpt:
            self.temp_excerpt.append(data)

def parse_html():
    path = r"C:\Users\leose\Downloads\Home - TN&C - Tendências, Notícias e Cultura - Informação relevante e atualizada.html"
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = TNCParser()
    parser.feed(html_content)
    
    # Process and filter articles
    unique_articles = []
    seen_titles = set()
    
    # Ignore list for generic titles
    ignore_titles = {
        "Mais lidas", "Destaque da semana", "Internacional", "Polícia", "Cultura", 
        "Esportes", "Tendências", "Notícias", "Tecnologia", "TV e Celebridades", 
        "Gastronomia", "Negócios", "Saúde", "Sustentabilidade", "Viagens", "Ir para o conteúdo",
        "Home", "Ir para o contedo", "TN&C Insights", "Arquitetura e Design", "Carros e Mobilidade"
    }
    
    for art in parser.articles:
        title = art['title'].strip()
        if not title or len(title) < 10 or title in ignore_titles:
            continue
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())
        
        # Try to find an image in the HTML near this article if not found
        # (This is a fallback; since our parser is simple, we might miss some images)
        unique_articles.append(art)
        
    # Let's output all unique articles
    print(f"Extracted {len(unique_articles)} unique articles.")
    for idx, item in enumerate(unique_articles[:20]):
        print(f"\n[{idx+1}] Category: {item['category']}")
        print(f"    Title: {item['title']}")
        print(f"    URL: {item['url']}")
        print(f"    Image: {item['image']}")
        print(f"    Excerpt: {item['excerpt']}")
        
    # Write to file
    with open(r"C:\Users\leose\.gemini\antigravity\scratch\tnc_articles.json", "w", encoding="utf-8") as f:
        json.dump(unique_articles, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    parse_html()
