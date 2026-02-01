import requests
import os

# Diese Werte ziehen wir aus den GitHub Secrets (Sicherheit!)
API_TOKEN = os.getenv('PODIGEE_TOKEN')
PODCAST_ID = os.getenv('PODCAST_ID')

headers = {'Authorization': f'Bearer {API_TOKEN}'}
url = f'https://app.podigee.com/api/v1/podcasts/{PODCAST_ID}/episodes'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    episodes = response.json()
    os.makedirs('downloads', exist_ok=True)

    for ep in episodes:
        # Dateiname säubern
        title = "".join([c for c in ep['title'] if c.isalnum() or c in (' ', '_')]).strip()
        audio_url = ep.get('audio_files', [{}])[0].get('mp3_url')
        
        if audio_url:
            print(f"Lade: {title}")
            r = requests.get(audio_url)
            with open(f"downloads/{title}.mp3", 'wb') as f:
                f.write(r.content)
else:
    print(f"Fehler: {response.status_code}")
