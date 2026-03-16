from flask import Flask
import requests
from datetime import datetime

app = Flask(__name__)

def get_air_day(anime):
    """Extract the day of the week an anime airs."""
    if 'broadcast' in anime and anime['broadcast']:
        broadcast = anime['broadcast']
        if 'day' in broadcast and broadcast['day']:
            return broadcast['day']

    if 'aired' in anime and anime['aired']:
        aired = anime['aired']
        if 'from' in aired and aired['from']:
            try:
                from_date = aired['from']
                dt = datetime.fromisoformat(from_date.replace('Z', '+00:00'))
                return dt.strftime('%A')
            except:
                pass

    return "Unknown"

@app.route('/')
def home():
    # Fetch anime data
    url = "https://api.jikan.moe/v4/seasons/now"
    response = requests.get(url)

    if response.status_code != 200:
        return "Failed to fetch anime data"

    data = response.json()
    anime_list = data['data']
    print(f"Total anime found: {len(anime_list)}")


# Group by day
    anime_by_day = {}
    for anime in anime_list:
        day = get_air_day(anime)
        title = anime['title']

        if day not in anime_by_day:
            anime_by_day[day] = []
        anime_by_day[day].append(title)

    # Build HTML
    html = "<h1>📅 Anime Release Calendar</h1>"
    html += "<p>Current Season</p>"

    # Order days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Unknown']
    print("Days with anime:", {day: len(titles) for day, titles in anime_by_day.items()})

    for day in day_order:
        # Get count (0 if day not in dictionary)
        count = len(anime_by_day.get(day, []))
        html += f"<h2>{day} ({count} anime)</h2>"

        if count > 0:
            html += "<ul>"
            for title in anime_by_day[day]:
                html += f"<li>{title}</li>"
            html += "</ul>"
        else:
            html += "<p>✨ No anime airing this day</p>"

    return html

if __name__ == '__main__':
    app.run(debug=True)