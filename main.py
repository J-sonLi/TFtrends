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
def get_playerNames():
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        live_url = urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/playerlist')
        live_response = json.loads(live_url.read())
        #print(live_response)
        for i in range(len(live_response)):
            playerName = live_response[i]['summonerName']
            playerPUUID = get_puuid(playerName)
            # # print(playerPUUID)
            playerList[playerName] = playerPUUID
            # # print(playerName,' -> ', playerPUUID)

    except:
        print('You are not in game')
        return


# Get puuid from player name
def get_puuid(playerName):
    # GET puuid of summoner
    encodedplayerName = urllib.parse.quote(playerName)
    summoner_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    summoner_url += encodedplayerName
    #print(summoner_url)
    summoner_response = requests.get(url=summoner_url, headers=header)
    summoner_json = summoner_response.json()
    #print(summoner_json['puuid'])
    return summoner_json['puuid']


# Takes in puuid and returns match history list
def get_matchList(puuid):
    match_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?count=10'
    match_response = requests.get(url=match_url, headers=header)
    match_json = match_response.json()
    return match_json


# Takes in matchid and returns champions played
def get_champsPLayed(player, puuid, match_list, champMap):
    for match_string in match_list:
        matchid_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/' + match_string
        matchid_response = requests.get(url=matchid_url, headers=header)
        matchid_json = matchid_response.json()
        if len(matchid_json['info']['participants'])== 8:
        # Count each champion once
            champSet = set()
            for i in range(8):
                # Checks for correct PUUID and correct set number
                if(matchid_json['info']['participants'][i]['puuid']==puuid and matchid_json['info']['tft_set_number'] == 5):
                    for champions in matchid_json['info']['participants'][i]['units']:
                        champSet.add(champions['character_id'])
                    champsPlayed[player] = champSet
                    for i in champSet:
                        champMap[i]+=1

# -----------------------------------------------------------------------------------------------------------------------


# dictionary that takes in <PLAYERNAME: PUUID>
playerList = {}

# dictionary that takes in <PLAYERNAME : matchlist>
matchList = defaultdict(list)

get_playerNames()
# dictionary that stores <Champion name : count>
champMap = defaultdict(int)

champsPlayed = defaultdict(int)

# populate matchList for each player in game
# player = player's name
# playerList[player] = player's puuid
for player in playerList:
    #matchList[player] = list of 'n' matches for player
    matchList[player] = get_matchList(playerList[player])
    get_champsPLayed(player, playerList[player],matchList[player], champMap)

# Sorts champMap in ascending order
temp = sorted(champMap.items(), key=lambda x:x[1])
for i in temp:
    print(i)


