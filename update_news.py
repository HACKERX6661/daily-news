import feedparser
import os

FEEDS = [
    "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml",
    "https://rss.orf.at/news.xml"
]

def get_news():
    html = ""
    for url in FEEDS:
        feed = feedparser.parse(url)
        # Nimm die ersten 5 News pro Quelle
        for entry in feed.entries[:5]:
            description = entry.get('description', '')
            # Kürze die Beschreibung, falls sie zu lang ist
            if len(description) > 300:
                description = description[:300] + "..."
            
            html += f'''
            <div class="news-item">
                <div class="date">{entry.get('published', 'Aktuell')}</div>
                <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
                <p>{description}</p>
            </div>'''
    return html

# Datei einlesen
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    start_mark = ""
    end_mark = ""

    try:
        # Ersetze den Inhalt zwischen den Markierungen
        parts_start = content.split(start_mark)
        parts_end = content.split(end_mark)
        
        new_content = parts_start[0] + start_mark + get_news() + end_mark + parts_end[1]

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Update erfolgreich durchgeführt.")
    except IndexError:
        print("Fehler: Markierungen oder nicht gefunden!")
else:
    print("Fehler: index.html wurde nicht gefunden.")
