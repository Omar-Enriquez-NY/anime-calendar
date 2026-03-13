import requests
import json
from datetime import datetime

def get_air_day(anime):
    """Extract the day of the week an anime airs."""
    # Method 1: Check broadcast field
    if 'broadcast' in anime and anime['broadcast']:
        broadcast = anime['broadcast']
        if 'day' in broadcast and broadcast['day']:
            return broadcast['day']

    # Method 2: Parse from aired.from date
    if 'aired' in anime and anime['aired']:
        aired = anime['aired']
        if 'from' in aired and aired['from']:
            try:
                from_date = aired['from']  # e.g., "2024-04-06T00:00:00+00:00"
                # Parse the ISO format date
                dt = datetime.fromisoformat(from_date.replace('Z', '+00:00'))
                return dt.strftime('%A')  # Returns full day name: Monday, Tuesday, etc.
            except:
                pass

    return "Unknown"

print("Asking the API for current anime...\n")

url = "https://api.jikan.moe/v4/seasons/now"
response = requests.get(url)

if response.status_code == 200:
    print("SUCCESS! Got data from API\n")

    data = response.json()
    anime_list = data['data']

    # Save full data to a file for exploration
    with open('anime_data_full.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved full data to anime_data_full.json")

    print(f"Found {len(anime_list)} anime in the current season\n")
    print("Here are the first 5:")
    print("-" * 50)

    for anime in anime_list[:10]:
        title = anime['title']
        day = get_air_day(anime)
        print(f"📺 {title} — Airs on: {day}")

        # Group anime by air day
    anime_by_day = {}

    for anime in anime_list:
        day = get_air_day(anime)
        title = anime['title']

        if day not in anime_by_day:
            anime_by_day[day] = []
        anime_by_day[day].append(title)

    # Print the grouped results
    print("\n" + "="*50)
    print("ANIME BY AIR DAY")
    print("="*50)

    for day, titles in anime_by_day.items():
        print(f"\n{day} ({len(titles)} anime)")
        for title in titles[:5]:  # Show first 5 per day to keep output clean
            print(f"  • {title}")
else:
    print("Failed to get data. Status code:", response.status_code)