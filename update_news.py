import feedparser
import os

def run():
    feeds = ["https://rss.orf.at/news.xml", "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"]
    news_html = ""
    
    # News abrufen
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                date = e.get('published', 'Aktuell')
                title = e.get('title', 'News')
                link = e.get('link', '#')
                summary = e.get('description', '')[:200] + "..."
                news_html += f'''
                <div class="news-item">
                    <div style="font-size:0.7rem; color:#9ca3af;">{date}</div>
                    <h3><a href="{link}" target="_blank">{title}</a></h3>
                    <p>{summary}</p>
                </div>'''
        except: continue

    # Die komplette HTML-Seite als String definieren
    full_html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graz News Hub 📰</title>
    <style>
        :root {{ --bg: #05070a; --card: #111827; --accent: #00f2ff; --text: #e5e7eb; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; text-align: center; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: var(--accent); text-transform: uppercase; letter-spacing: 2px; }}
        .news-item {{ background: var(--card); border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #1f2937; text-align: left; }}
        .news-item h3 a {{ color: var(--accent); text-decoration: none; font-weight: bold; }}
        .footer {{ margin-top: 50px; padding: 20px; border-top: 1px solid #1f2937; font-size: 0.8rem; color: #4b5563; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>GRAZ DAILY NEWS</h1>
        <p>Update täglich um 06:00 Uhr</p>
        <hr style="border: 1px solid var(--accent); margin: 20px 0;">
        <div id="news-container">
            {news_html}
        </div>
        <div class="footer">Automatisiertes System für Graz</div>
    </div>
</body>
</html>'''

    # Datei einfach komplett überschreiben
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("Seite komplett neu generiert!")

if __name__ == "__main__":
    run()
