import feedparser
import os
import urllib.request
import json

def get_weather():
    # Wetterdaten für Graz (Latitude: 47.0667, Longitude: 15.45)
    url = "https://api.open-meteo.com/v1/forecast?latitude=47.0667&longitude=15.45&current=temperature_2m,apparent_temperature,weather_code&timezone=Europe%2FBerlin"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            current = data['current']
            temp = round(current['temperature_2m'])
            feels_like = round(current['apparent_temperature'])
            code = current['weather_code']
            
            # Wetter-Code zu Emoji & Text zuordnen
            w_map = {
                0: ("☀️", "Klarer Himmel"),
                1: ("🌤️", "Hauptsächlich klar"), 2: ("⛅", "Teils bewölkt"), 3: ("☁️", "Bedeckt"),
                45: ("🌫️", "Nebelig"), 48: ("🌫️", "Raureifnebel"),
                51: ("🌧️", "Leichter Niesel"), 53: ("🌧️", "Mäßiger Niesel"), 55: ("🌧️", "Starker Niesel"),
                61: ("🌧️", "Leichter Regen"), 63: ("🌧️", "Regen"), 65: ("🌧️", "Starker Regen"),
                71: ("❄️", "Leichter Schneefall"), 73: ("❄️", "Schneefall"), 75: ("❄️", "Starker Schneefall"),
                95: ("⛈️", "Gewitter")
            }
            icon, desc = w_map.get(code, ("🌡️", "Wetter"))
            return f"{icon} {temp}°C (Gefühlt: {feels_like}°C) - {desc}"
    except:
        return "☀️ Wetterdaten aktuell nicht verfügbar"

def run():
    weather_info = get_weather()
    feeds = [
        "https://rss.orf.at/steiermark.xml",
        "https://rss.orf.at/news.xml",
        "https://www.tagesschau.de/infosilla/headlines/index~rss2.xml"
    ]
    news_html = ""
    
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:12]: 
                date = e.get('published', 'Aktuell')
                title = e.get('title', 'News')
                link = e.get('link', '#')
                summary = e.get('description', '')[:180] + "..."
                news_html += f'''
                <div class="news-item">
                    <div class="date">{date}</div>
                    <h3><a href="{link}" target="_blank">{title}</a></h3>
                    <p>{summary}</p>
                </div>'''
        except: continue

    full_html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graz News Hub 📰</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📰</text></svg>">
    <style>
        :root {{ 
            --bg: #0b0f19; --card: #161d2f; --accent: #00f2ff; --text: #f3f4f6; --muted: #9ca3af;
        }}
        body {{ 
            font-family: 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); 
            margin: 0; padding: 20px; line-height: 1.6;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        header {{ margin-bottom: 30px; text-align: center; }}
        h1 {{ color: var(--accent); text-transform: uppercase; letter-spacing: 4px; font-size: 2.5rem; margin: 0; }}
        
        .weather-bar {{
            background: linear-gradient(90deg, #1e293b, #334155);
            padding: 15px; border-radius: 12px; margin-bottom: 30px;
            font-size: 1.1rem; font-weight: bold; border: 1px solid var(--accent);
            box-shadow: 0 4px 15px rgba(0, 242, 255, 0.1);
        }}

        #news-container {{ 
            display: grid; grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); gap: 25px; 
        }}
        .news-item {{ 
            background: var(--card); border-radius: 15px; padding: 25px; border: 1px solid #2d3748; 
            transition: 0.3s; display: flex; flex-direction: column;
        }}
        .news-item:hover {{ transform: translateY(-5px); border-color: var(--accent); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }}
        .date {{ font-size: 0.75rem; color: var(--accent); margin-bottom: 10px; font-weight: bold; }}
        .news-item h3 {{ margin: 0 0 12px 0; font-size: 1.3rem; }}
        .news-item h3 a {{ color: var(--text); text-decoration: none; }}
        .news-item p {{ color: var(--muted); font-size: 0.95rem; margin: 0; }}
        
        .footer {{ margin-top: 60px; padding: 30px; border-top: 1px solid #2d3748; font-size: 0.85rem; color: var(--muted); text-align: center; }}

        @media (max-width: 600px) {{
            #news-container {{ grid-template-columns: 1fr; }}
            h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>GRAZ DAILY NEWS</h1>
            <p style="color: var(--muted);">Dein Fenster zur Steiermark & der Welt</p>
        </header>

        <div class="weather-bar">
            Graz aktuell: {weather_info}
        </div>
        
        <div id="news-container">
            {news_html}
        </div>
        
        <div class="footer">
            &copy; 2026 Graz News Hub | 📰 v4.0 | Automatisch aktualisiert
        </div>
    </div>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("Update mit Wetter erfolgreich!")

if __name__ == "__main__":
    run()
