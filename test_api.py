import requests

print("Asking the API for current anime...\n")

url = "https://api.jikan.moe/v4/seasons/now"
response = requests.get(url)

if response.status_code == 200:
    print("SUCCESS! Got data from API\n")

    data = response.json()
    anime_list = data['data']

    print(f"Found {len(anime_list)} anime in the current season\n")
    print("Here are the first 5:")
    print("-" * 50)

    for anime in anime_list[:5]:
        title = anime['title']
        print(f"📺 {title}")
else:
    print("Failed to get data. Status code:", response.status_code)