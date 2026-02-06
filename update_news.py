import feedparser

FEEDS = [
    "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml",
    "https://rss.orf.at/news.xml"
]

def get_news():
    html = ""
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            html += f'''
            <div class="news-item">
                <div class="date">{entry.get('published', 'Aktuell')}</div>
                <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
                <p>{entry.get('description', '')[:300]}...</p>
            </div>'''
    return html

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Sucht die Markierungen und tauscht den Inhalt dazwischen aus
start_mark = ""
end_mark = ""

new_content = content.split(start_mark)[0] + start_mark + get_news() + end_mark + content.split(end_mark)[1]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
