import re
import html
import json

def parse_articles():
    path = r"C:\Users\leose\Downloads\Home - TN&C - Tendências, Notícias e Cultura - Informação relevante e atualizada.html"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <article ...> ... </article> blocks
    # We use re.DOTALL and a non-greedy match to find articles.
    article_blocks = re.findall(r'<article\b[^>]*>.*?</article>', content, re.DOTALL)
    print(f"Found {len(article_blocks)} total article blocks in HTML.")
    
    posts = []
    seen_titles = set()
    
    for block in article_blocks:
        # Check if it is an elementor-post or has elementor-post class
        if 'elementor-post' not in block:
            continue
            
        # 1. Extract class attributes from the article tag to find categories and tags
        article_tag_match = re.match(r'<article\b([^>]*)>', block, re.DOTALL)
        category = ""
        post_id = ""
        tags = []
        if article_tag_match:
            tag_attrs = article_tag_match.group(1)
            # Find category-xxx
            cat_matches = re.findall(r'\bcategory-([a-zA-Z0-9_-]+)\b', tag_attrs)
            if cat_matches:
                category = cat_matches[0].replace('-', ' ').title()
            
            # Find tags
            tag_matches = re.findall(r'\btag-([a-zA-Z0-9_-]+)\b', tag_attrs)
            tags = [t.replace('-', ' ').title() for t in tag_matches]
            
            # Find post id
            id_match = re.search(r'\bpost-(\d+)\b', tag_attrs)
            if id_match:
                post_id = id_match.group(1)
                
        # 2. Extract Title and URL
        # Look for <hX class="elementor-post__title"> <a href="URL">TITLE</a> </hX>
        title = ""
        url = ""
        title_match = re.search(r'class="elementor-post__title"[^>]*>\s*<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
        if not title_match:
            # Fallback title search
            title_match = re.search(r'<a\b[^>]*href="([^"]+)"[^>]*class="elementor-post__title"[^>]*>(.*?)</a>', block, re.DOTALL)
        if not title_match:
            # Fallback 2
            title_match = re.search(r'<h\d\b[^>]*class="elementor-post__title"[^>]*>.*?<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
            
        if title_match:
            url = title_match.group(1)
            title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
            title = html.unescape(title)
            title = re.sub(r'\s+', ' ', title)
            
        # Clean URL
        url = re.sub(r'^https://web\.archive\.org/web/\d+/', '', url)
        
        # 3. Extract Image
        image = ""
        img_match = re.search(r'<img\b[^>]*>', block, re.DOTALL)
        if img_match:
            img_tag = img_match.group(0)
            src_match = re.search(r'\bsrc="([^"]+)"', img_tag)
            data_src_match = re.search(r'\bdata-src="([^"]+)"', img_tag)
            img_src = ""
            if data_src_match:
                img_src = data_src_match.group(1)
            elif src_match:
                img_src = src_match.group(1)
                
            if img_src:
                img_src = re.sub(r'^https://web\.archive\.org/web/\d+(im_)?/', '', img_src)
                if not any(x in img_src.lower() for x in ['transparent', 'spacer', 'avatar', 'gravatar', 'logo']):
                    image = img_src
                    
        # 4. Extract Excerpt
        excerpt = ""
        excerpt_match = re.search(r'class="elementor-post__excerpt"[^>]*>(.*?)</div>', block, re.DOTALL)
        if excerpt_match:
            excerpt = re.sub(r'<[^>]+>', '', excerpt_match.group(1)).strip()
            excerpt = html.unescape(excerpt)
            excerpt = re.sub(r'\s+', ' ', excerpt)
            
        # 5. Extract Meta (Author, Date)
        author = ""
        date = ""
        author_match = re.search(r'class="elementor-post-author"[^>]*>(.*?)</span>', block, re.DOTALL)
        if author_match:
            author = re.sub(r'<[^>]+>', '', author_match.group(1)).strip()
            author = html.unescape(author)
        date_match = re.search(r'class="elementor-post-date"[^>]*>(.*?)</span>', block, re.DOTALL)
        if date_match:
            date = re.sub(r'<[^>]+>', '', date_match.group(1)).strip()
            date = html.unescape(date)
            
        # Ignore empty titles
        if not title or len(title) < 10:
            continue
            
        # Deduplicate
        title_key = title.lower()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        
        posts.append({
            'id': post_id,
            'title': title,
            'url': url,
            'image': image,
            'category': category,
            'tags': tags,
            'excerpt': excerpt,
            'author': author,
            'date': date
        })
        
    print(f"Extracted {len(posts)} unique elementor posts.")
    for idx, p in enumerate(posts):
        print(f"[{idx+1}] Category: {p['category']} | Title: {p['title']} | Image: {p['image']}")
        
    with open(r"C:\Users\leose\.gemini\antigravity\scratch\tnc_posts_extracted.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    parse_articles()
