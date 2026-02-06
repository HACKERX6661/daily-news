import feedparser

# Liste der Quellen (RSS-Feeds)
FEEDS = ["https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"]

def fetch_news():
    html_output = ""
    for url in FEEDS:
        feed = feedparser.parse(url)
        # Nimmt die aktuellsten 15 Meldungen
        for entry in feed.entries[:15]:
            description = entry.description if 'description' in entry else ""
            published = entry.published if 'published' in entry else "Unbekannt"
            
            html_output += f'''
            <div class="news-item">
                <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
                <p>{description}</p>
                <div class="date">Stand: {published}</div>
            </div>
            '''
    return html_output

# HTML-Datei lesen
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# News-Bereich im HTML finden und ersetzen
start_marker = '<div id="news-container">'
end_marker = '</div>'
parts = content.split(start_marker)
top_part = parts[0] + start_marker
bottom_part = end_marker + parts[1].split(end_marker)[-1]

# Datei mit neuen Inhalten überschreiben
with open("index.html", "w", encoding="utf-8") as f:
    f.write(top_part + fetch_news() + bottom_part)
