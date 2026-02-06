import feedparser
import os

FEEDS = [
    "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml",
    "https://rss.orf.at/news.xml"
]

def get_news_html():
    html = ""
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                date = entry.get('published', 'Aktuell')
                title = entry.get('title', 'Kein Titel')
                link = entry.get('link', '#')
                desc = entry.get('description', '')[:250] + "..."
                html += f'''
                <div class="news-item">
                    <div class="date">{date}</div>
                    <h3><a href="{link}" target="_blank">{title}</a></h3>
                    <p>{desc}</p>
                </div>'''
        except Exception as e:
            print(f"Fehler beim Laden von {url}: {e}")
    return html

def update_index():
    if not os.path.exists("index.html"):
        print("index.html nicht gefunden!")
        return

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    start_mark = ""
    end_mark = ""

    if start_mark in content and end_mark in content:
        # Alles vor der Start-Markierung + Markierung
        head = content.split(start_mark)[0] + start_mark
        # Alles nach der End-Markierung + Markierung
        tail = end_mark + content.split(end_mark)[1]
        
        full_content = head + get_news_html() + tail
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_content)
        print("News erfolgreich eingefügt!")
    else:
        print("Markierungen im HTML fehlen!")

if __name__ == "__main__":
    update_index()
