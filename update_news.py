import feedparser
import os

def get_news():
    feeds = ["https://rss.orf.at/news.xml", "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"]
    html = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                date = e.get('published', 'Aktuell')
                title = e.get('title', 'News')
                link = e.get('link', '#')
                summary = e.get('description', '')[:200] + "..."
                html += f'<div class="news-item"><div style="font-size:0.7rem;color:#9ca3af;">{date}</div>'
                html += f'<h3><a href="{link}" target="_blank">{title}</a></h3>'
                html += f'<p>{summary}</p></div>'
        except: continue
    return html

def run():
    start_mark = ""
    end_mark = ""
    news_content = get_news()
    file_path = "index.html"
    
    if not os.path.exists(file_path): return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Sicherer Split
    if start_mark in content and end_mark in content:
        parts_start = content.split(start_mark)
        parts_end = parts_start[1].split(end_mark)
        
        final_html = parts_start[0] + start_mark + news_content + end_mark + parts_end[1]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print("Update erfolgreich durchgeführt.")
    else:
        print("Fehler: Markierungen im HTML nicht gefunden. Nichts geändert.")

if __name__ == "__main__":
    run()
