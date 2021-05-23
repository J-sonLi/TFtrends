import requests
import json
import os
import urllib
import ssl
from collections import defaultdict
import time

# User-Agent can be found at https://www.whatismybrowser.com/detect/what-is-my-user-agent
# Get Riot development API key at https://developer.riotgames.com/

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": os.environ.get('RIOT_API')
}

# # -----------------------------------------------------------------------------------------------------------------------

class TftPlayer:
    def __init__(self):
        self.name = None
        self.puuid = None
        self.matchlist = []
        self.champmap = defaultdict(int)

# Get player names using ingame-api


# Get puuid from player name
def get_puuid(self):
    # GET puuid of summoner
    encodedplayerName = urllib.parse.quote(self.name)
    summoner_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/'
    summoner_url += encodedplayerName
    summoner_response = requests.get(url=summoner_url, headers=header)
    summoner_json = summoner_response.json()
    return summoner_json['puuid']


# Takes in puuid and returns match history list
def get_matchList(self):
    match_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + self.puuid + '/ids?count=5'
    match_response = requests.get(url=match_url, headers=header)
    match_json = match_response.json()
    return match_json


# Takes in matchid and returns champions played
#player_name, player_puuid, player_matchlist, player_champmap
def get_champsPLayed(self):
    for player_match in self.matchlist:

        matchid_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/' + player_match
        matchid_response = requests.get(url=matchid_url, headers=header)
        matchid_json = matchid_response.json()
        #print(player_match)
        #if len(matchid_json['info']['participants'])== 8:
        for j in range(8):
    #         # Checks for correct PUUID and correct set number
            if matchid_json['info']['participants'][j]['puuid']==self.puuid and matchid_json['info']['tft_set_number'] == 5:
                for champions in matchid_json['info']['participants'][j]['units']:
                        self.champmap[champions['character_id']] += 1
                break
    return self.champmap


# ----------------------------------------------------------------------------------------------------------------------
                                                    # MAIN
#Must be in game for this link to work
ssl._create_default_https_context = ssl._create_unverified_context
live_url = urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/playerlist')
live_response = json.loads(live_url.read())

# with open('tempgame.json') as f:
#     live_response=json.load(f)
#     #print(live_response)
playerList = [TftPlayer() for i in range(8)]
for player, j in zip(playerList, range(8)):
    # print(i)
    player.name = live_response[j]['summonerName']
    player.puuid = get_puuid(player)
    player.matchlist = get_matchList(player)
    player.champmap = get_champsPLayed(player)
    #
    #
    print(player.name)
    player.champmap = sorted(player.champmap.items(), key=lambda x:x[1])
    for a in player.champmap:
        print(a)








