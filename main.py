import requests
import json
import os
import urllib
import ssl
from collections import defaultdict


# User-Agent can be found at https://www.whatismybrowser.com/detect/what-is-my-user-agent
# Get Riot development API key at https://developer.riotgames.com/

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": os.environ.get('RIOT_API')
}

# Get player names using ingame-api
def get_playerName():
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        live_url = urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/playerlist')
        live_response = json.loads(live_url.read())
        for i in range(len(live_response)):
            playerName = live_response[i]['summonerName']
            playerPUUID = get_puuid(playerName)
            playerList[playerName] = playerPUUID
            # print(playerName,' -> ', playerPUUID)
    except:
        print('You are not in game')
        return


# Get puuid from player name
def get_puuid(playerName):
    # GET puuid of summoner
    encodedplayerName = urllib.parse.quote(playerName)
    summoner_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    summoner_url += encodedplayerName
    summoner_response = requests.get(url=summoner_url, headers=header)
    summoner_json = summoner_response.json()
    return summoner_json['puuid']


# Takes in puuid and returns match history list
def get_matchList(puuid):
    match_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?count=2'
    match_response = requests.get(url=match_url, headers=header)
    match_json = match_response.json()
    return match_json
# -----------------------------------------------------------------------------------------------------------------------


# dictionary that takes in <PLAYERNAME : PUUID>
playerList = {}

# dictionary that takes in <PLAYERNAME : matchlist>
matchList = defaultdict(list)

get_playerName()
# populate matchList for each player in game
for player in playerList:
    matchList[player] = get_matchList(playerList[player])
    print(player, ' -> ', matchList[player])
