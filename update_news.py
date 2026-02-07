import feedparser
import os

def run():
    feeds = ["https://rss.orf.at/news.xml", "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"]
    news_html = ""
    
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                news_html += f'''
                <div class="news-item">
                    <div style="font-size:0.7rem; color:#9ca3af;">{e.get('published', 'Aktuell')}</div>
                    <h3><a href="{e.link}" target="_blank">{e.title}</a></h3>
                    <p>{e.get('description', '')[:200]}...</p>
                </div>'''
        except: continue

    file_path = "index.html"
    if not os.path.exists(file_path):
        print("Datei index.html nicht gefunden!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_mark = ""
    end_mark = ""

    if start_mark in content and end_mark in content:
        # Hier lag der Fehler: Wir trennen jetzt sauberer
        before = content.split(start_mark)[0]
        after = content.split(end_mark)[1]
        new_content = before + start_mark + news_html + end_mark + after
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Update erfolgreich!")
    else:
        print("FEHLER: Markierungen oder fehlen in der index.html!")

if __name__ == "__main__":
    run()
