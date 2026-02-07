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
    
    # Falls die Datei existiert, versuchen wir sie zu aktualisieren
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Sicherer Check: Sind beide Markierungen da und NICHT leer?
        if start_mark in content and end_mark in content:
            try:
                before = content.split(start_mark)[0]
                after = content.split(end_mark)[1]
                final_html = before + start_mark + news_content + end_mark + after
            except Exception:
                # Falls split() doch zickt, Notfall-Layout nutzen
                final_html = f"<html><body>{news_content}</body></html>"
        else:
            # Falls Markierungen fehlen, hängen wir es einfach an
            final_html = content + "\n" + news_content
    else:
        # Falls gar keine index.html da ist, erstellen wir eine rudimentäre
        final_html = f"<!DOCTYPE html><html><body>{news_content}</body></html>"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    run()
