import feedparser
import os

def run():
    feeds = ["https://rss.orf.at/news.xml", "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"]
    news_html = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                news_html += f'<div class="news-item"><div style="font-size:0.7rem;color:#9ca3af;">{e.get("published", "Aktuell")}</div>'
                news_html += f'<h3><a href="{e.link}" target="_blank">{e.title}</a></h3>'
                news_html += f'<p>{e.get("description", "")[:200]}...</p></div>'
        except Exception as err:
            print(f"Fehler bei Feed {url}: {err}")
            continue

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        start, end = "", ""
        if start in content and end in content:
            new_content = content.split(start)[0] + start + news_html + end + content.split(end)[1]
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Erfolgreich aktualisiert!")
        else:
            print("Markierungen oder nicht gefunden!")

if __name__ == "__main__":
    run()
