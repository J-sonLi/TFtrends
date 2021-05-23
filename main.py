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
#
#
# # Get player names using ingame-api
# def get_playerNames():
#     try:
#         ssl._create_default_https_context = ssl._create_unverified_context
#         live_url = urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/playerlist')
#         live_response = json.loads(live_url.read())
#         #print(live_response)
#         for i in range(len(live_response)):
#             playerName = live_response[i]['summonerName']
#             playerPUUID = get_puuid(playerName)
#             # # print(playerPUUID)
#             playerList[playerName] = playerPUUID
#             # # print(playerName,' -> ', playerPUUID)
#
#     except:
#         print('You are not in game')
#         return
#
#
# # Get puuid from player name
# def get_puuid(playerName):
#     # GET puuid of summoner
#     encodedplayerName = urllib.parse.quote(playerName)
#     summoner_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
#     summoner_url += encodedplayerName
#     #print(summoner_url)
#     summoner_response = requests.get(url=summoner_url, headers=header)
#     summoner_json = summoner_response.json()
#     #print(summoner_json['puuid'])
#     return summoner_json['puuid']
#
#
# # Takes in puuid and returns match history list
# def get_matchList(puuid):
#     match_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?count=10'
#     match_response = requests.get(url=match_url, headers=header)
#     match_json = match_response.json()
#     return match_json

# # -----------------------------------------------------------------------------------------------------------------------


class TftPlayer:
    def __init__(self):
        self.name = None
        self.puuid = None
        self.matchlist = []
        self.champmap = defaultdict(int)

# Get player names using ingame-api


# Get puuid from player name
def get_puuid(player_name):
    # GET puuid of summoner
    encodedplayerName = urllib.parse.quote(player_name)
    summoner_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/'
    summoner_url += encodedplayerName
    summoner_response = requests.get(url=summoner_url, headers=header)
    summoner_json = summoner_response.json()
    return summoner_json['puuid']


# Takes in puuid and returns match history list
def get_matchList(player_puuid):
    match_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + player_puuid + '/ids?count=5'
    match_response = requests.get(url=match_url, headers=header)
    match_json = match_response.json()
    return match_json

#
# # Takes in matchid and returns champions played
def get_champsPLayed(player_name, player_puuid, player_matchlist, player_champmap):
    for player_match in player_matchlist:

        matchid_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/' + player_match
        matchid_response = requests.get(url=matchid_url, headers=header)
        matchid_json = matchid_response.json()
        #print(player_match)
        #if len(matchid_json['info']['participants'])== 8:
        for j in range(8):
    #         # Checks for correct PUUID and correct set number
            if matchid_json['info']['participants'][j]['puuid']==player_puuid and matchid_json['info']['tft_set_number'] == 5:
                for champions in matchid_json['info']['participants'][j]['units']:
                        player_champmap[champions['character_id']] += 1
                break
    return player_champmap



# ----------------------------------------------------------------------------------------------------------------------------------------------
# ssl._create_default_https_context = ssl._create_unverified_context
# live_url = urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/playerlist')
# live_response = json.loads(live_url.read())

with open('tempgame.json') as f:
    live_response=json.load(f)
    #print(live_response)
playerList = [TftPlayer() for i in range(8)]
for i, j in zip(playerList, range(8)):
    # print(i)
    i.name = live_response[j]['summonerName']
    i.puuid = get_puuid(i.name)
    i.matchlist = get_matchList(i.puuid)
    i.champmap = get_champsPLayed(i.name, i.puuid, i.matchlist, i.champmap)
    print(i.name, i.champmap)




