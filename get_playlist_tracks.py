import requests, json, os
from base64 import b64encode

# Create your app
# https://developer.spotify.com/documentation/general/guides/authorization/app-settings/
client_id = "xxxxxxxxxx"
client_secret = "xxxxxxxxxx"

# Output name
filename = "playlist_track_list.txt"

# Playlist test
playlist_id = "5CrFrAj6h7SYVOAwKESxA7"
# User lostmap
user_id = "hn84m2848h6li44z4u2gjog5q"

def get_token(client_id, client_secret):
    headers =  {'Authorization': 'Basic ' + b64encode((client_id + ':' + client_secret).encode()).decode() }
    payload = {'grant_type': 'client_credentials'}
    api = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=payload)
    return json.loads(api.text)

def get_me(token):
    headers =  {'Authorization': 'Bearer ' + token }
    api = requests.get(f"https://api.spotify.com/v1/me", headers=headers)
    return json.loads(api.text)

def get_user_playlists(token, user_id, limit=50, offset=0):
    headers =  {'Authorization': 'Bearer ' + token }
    api = requests.get(f"https://api.spotify.com/v1/users/{user_id}/playlists", headers=headers, params={
        'offset': offset,
        'count': limit,
    })
    return json.loads(api.text)

def get_playlist_tracks(token, playlist_id, limit=50, offset=0):
    headers =  {'Authorization': 'Bearer ' + token }
    api = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, params={
        'offset': offset,
        'count': limit,
    })
    return json.loads(api.text)

def get_playlist_track_list_to_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass
    offset = 0
    limit = 100
    token = get_token(client_id, client_secret)
    items = get_playlist_tracks(token['access_token'], playlist_id, limit=limit, offset=offset)
    total_track_count = items['total']
    count = 1
    while offset <= total_track_count:
        if offset != 0:
            items = get_playlist_tracks(token['access_token'], playlist_id, limit=limit, offset=offset)
        for item in items['items']:
            artists = []
            for artist in item['track']['artists']:
               artists.append(artist['name'])
            with open(filename, 'a') as f:
                out = "track №" + str(count) + " " + str(item['track']['name']) + "| album: " + str(item['track']['album']['name']) + "| artists" + ', '.join(artists) + "\n"
                f.write(out)
            count += 1
        offset += limit

def main():
    get_playlist_track_list_to_file(filename)
    #token = get_token(client_id, client_secret)
    #print(token)
    #out = get_user_playlists(token['access_token'], user_id)
    #out = get_me(token['access_token'])
    #print(out['items'][0]['owner'])
    #with open('data.json', 'w', encoding='utf-8') as f:
    #   json.dump(out, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
