import requests
import os
from dotenv import find_dotenv, load_dotenv
import json
import random
import accessories
import lyricsgenius as lg

load_dotenv(find_dotenv())
BASE_URL = "https://accounts.spotify.com/api/token"
BASE_GENIUS_TOKEN = "https://api.genius.com/oauth/authorize"

# Encoding and getting authorizaition
def getAuthToken():

    ID = os.getenv("ID")
    clientS = os.getenv("API_KEY")

    headers = {}
    data = {}
    headers["Authorization"] = f"Basic {accessories.convertID(ID, clientS)}"
    data["grant_type"] = "client_credentials"

    response = requests.post(BASE_URL, headers=headers, data=data)
    response_json = response.json()
    token = response_json["access_token"]

    return token


# Getting the random artist, the list of songs, and formatting them
def getSongs(token, artists_list):

    BASE_BROWSE = f"https://api.spotify.com/v1/artists/{accessories.getRandArtist(artists_list)}/top-tracks"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    params = {"market": "US"}

    response2 = requests.get(BASE_BROWSE, headers=headers, params=params)
    response2_json = response2.json()

    dataList = []
    try:
        for i in range(len(response2_json["tracks"])):
            dataList.append(
                {
                    "Song": response2_json["tracks"][i]["name"],
                    "Artist": "By " + response2_json["tracks"][i]["artists"][0]["name"],
                    "Image": response2_json["tracks"][i]["album"]["images"][0]["url"],
                    "Pop": response2_json["tracks"][i]["popularity"],
                    "Album": response2_json["tracks"][i]["album"]["name"],
                    "Rel": response2_json["tracks"][i]["album"]["release_date"],
                    "Preview": response2_json["tracks"][i]["preview_url"],
                }
            )
    except:
        dataList.append(
            {
                "Song": "Unavailable",
                "Artist": "Error",
                "Image": "/static/Error_Message.png",
                "Preview": "Unavailable",
            }
        )

    trackIndex = random.randrange(len(dataList))
    print(dataList[trackIndex])

    return dataList[trackIndex]


# Genius Authorization
def getGeniusAuth(songTitle, name):
    G_TOKEN = os.getenv("GENIUS_TOKEN")

    ly = ""

    try:
        genius = lg.Genius(G_TOKEN)
        song = genius.search_song(songTitle, name)

        # Check if lyrics exist or not
        if type(song.lyrics) == None:
            ly = "No lyrics available for this song"
        else:
            ly = song.lyrics
            print(song.lyrics + "\n")
    except:
        ly = "No lyrics available for this song"

    return ly
