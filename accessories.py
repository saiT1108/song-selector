import json
import random
import base64
import getData
import requests

# artists = [
#     "13ab1LgQZ3tQOhkDRRYB8Y",
#     "5INjqkS1o8h1imAzPqGZBb",
#     "1nIUhcKHnK6iyumRyoV68C",
#     "3hOdow4ZPmrby7Q1wfPLEy",
#     "3q1NKu1dVzFcBfxFos4kE3",
#     "1Xyo4u8uXC1ZmMpatF05PJ",
#     "2DxvKWtxPfttWviSORrEqc",
#     "2YZyLoL8N0Wb9xBt1NhZWg",
#     "6eJa3zG1QZLRB3xgRuyxbm",
#     "3MZsBdqDrRTJihTHQrO6Dq",
#     "2h93pZq0e7k5yf4dywlkpM",
# ]

# Picks a random artist from the list above
def getRandArtist(artistsParam):
    artistIndex = random.randrange(len(artistsParam))
    return artistsParam[artistIndex]


# Converts Spotify ID to base64, then decodes and returns the final converted value
def convertID(ID, key):
    code = f"{ID}:{key}"
    codeBytes = code.encode("ascii")
    base64code = base64.b64encode(codeBytes)
    baseM = base64code.decode("ascii")
    return baseM


def check_valid_id(artistID):
    token = getData.getAuthToken()
    BASE_BROWSE = f"https://api.spotify.com/v1/artists/{artistID}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(BASE_BROWSE, headers=headers)
    response_json = response.json()
    print(type(response_json))
    if "error" not in response_json:
        print(response_json["name"])
        list = [True, response_json["name"]]
        return list
    else:
        list = [False, "Artist does not exist"]
        return list
