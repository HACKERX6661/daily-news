import feedparser
import os

def get_news_content():
    feeds = ["https://rss.orf.at/news.xml", "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"]
    html = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                d = e.get('published', 'Aktuell')
                t = e.get('title', 'News')
                l = e.get('link', '#')
                s = e.get('description', '')[:250] + "..."
                html += f'<div class="news-item"><div class="date">{d}</div>'
                html += f'<h3><a href="{l}" target="_blank">{t}</a></h3>'
                html += f'<p>{s}</p></div>'
        except: continue
    return html

file_path = "index.html"
start_m, end_m = "", ""

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if start_m in content and end_m in content:
        parts = content.split(start_m)
        head = parts[0] + start_m
        tail = end_m + parts[1].split(end_m)[1]
        new_content = head + get_news_content() + tail
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("News erfolgreich in HTML geschrieben.")
    else:
        print("Markierungen fehlen im HTML!")
