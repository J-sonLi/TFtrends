import sys
import requests
import json
import os
import urllib
import ssl
from collections import defaultdict
import time
import sqlite3
import asyncio
import aiohttp

# User-Agent can be found at https://www.whatismybrowser.com/detect/what-is-my-user-agent
# Get Riot development API key at https://developer.riotgames.com/

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": os.environ.get('RIOT_API')
}

# -----------------------------------------------------------------------------------------------------------------------

class TftPlayer:
    def __init__(self):
        self.name = None
        self.puuid = None
        self.matchlist = []
        self.champmap = defaultdict(int)


async def async_puuid():
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = []
        for player in playerList:
            task = asyncio.ensure_future(get_puuid(session, player))
            tasks.append(task)
        await asyncio.gather(*tasks)


# Get puuid from player name
async def get_puuid(session, player):
    try:
        encodedplayerName = urllib.parse.quote(player.name)
        summoner_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/'
        summoner_url += encodedplayerName
        async with session.get(summoner_url) as response:
            result_data = await response.json()
            player.puuid = result_data['puuid']
    except:
        print("API Key might be expired")
        sys.exit()


async def async_matchlist():
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = []
        for player in playerList:
            task = asyncio.ensure_future(get_matchList(session, player))
            tasks.append(task)
        await asyncio.gather(*tasks)


# Takes in puuid and returns match history list
async def get_matchList(session, player):
    match_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + player.puuid + '/ids?count=' + '10'
    async with session.get(match_url) as response:
        result_data = await response.json()
        player.matchlist = result_data


async def async_champsplayed():
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = []
        for player in playerList:
            task = asyncio.ensure_future(get_champsPLayed(session, player))
            tasks.append(task)
        await asyncio.gather(*tasks)


# Takes in matchid and returns champions played
#player_name, player_puuid, player_matchlist, player_champmap
async def get_champsPLayed(session, player):
    for player_match in player.matchlist:
        matchid_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/' + player_match
        async with session.get(matchid_url) as response:
            for attempt in range(2):
                try:
                    matchid_json = await response.json()
                    #print(matchid_json)
                    #await asyncio.sleep(1)
                    for j in range(8):
                        # Checks for correct PUUID and current set number (Set 5) and ranked queue
                        if matchid_json['info']['participants'][j]['puuid']== player.puuid and matchid_json['info']['tft_set_number'] == 5 and matchid_json['info']['queue_id'] == 1100:
                            for champions in matchid_json['info']['participants'][j]['units']:
                                    player.champmap[champions['character_id']] += 1
                            await asyncio.sleep(1)
                            break
                    break
                except KeyError:
                    print(matchid_json['status'])
                else:
                    print("An error has occured")
                    sys.exit()


# prints champmap
def sort_champMap(self):
    self.champmap = sorted(self.champmap.items(), key=lambda x: x[1])
    for i in self.champmap:
        print(i)
    #return self.champmap


def get_champdb():
    conn = sqlite3.connect('champmap.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE champions SET champ_count = 0")
        conn.commit()
        conn.close()
    except:
        c.execute("CREATE TABLE IF NOT EXISTS champions (champ_id text PRIMARY KEY, champ_cost integer, champ_count integer)")
        with open('champions.json', 'r') as content:
            championslist=json.load(content)
        for champ in championslist:
            #print(i['championId'],i['cost'])
            c.execute("INSERT INTO champions VALUES(?, ?, ?)", (champ['championId'], champ['cost'], 0,))
        conn.commit()
    conn.close()

def update_db(player):
    conn = sqlite3.connect('champmap.db')
    c = conn.cursor()
    for champ in player.champmap:
        c.execute("SELECT champ_count FROM champions WHERE champ_id = ?",(champ,))
        temp = c.fetchone()[0] + player.champmap[champ]
        c.execute("UPDATE champions SET champ_count = ? WHERE champ_id = ?",(temp,champ,))
    conn.commit()
    conn.close()


def main_program(playerList):
    # Must be in game for this link to work
    for attempt in range(2):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            live_url = urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/playerlist')
            live_response = json.loads(live_url.read())
            break
        except ConnectionRefusedError as e:
            print(e)
            print('Retrying connection...')
        except:
            with open('tempgame.json') as f:
                live_response = json.load(f)
                break
        else:
            print('You may not be in  a TFT game')

    for player, j in zip(playerList, range(8)):
        player.name = live_response[j]['summonerName']
    asyncio.run(async_puuid())
    asyncio.run(async_matchlist())
    asyncio.run(async_champsplayed())


# ----------------------------------------------------------------------------------------------------------------------
                                                    # MAIN
playerList = [TftPlayer() for i in range(8)]
main_program(playerList)

get_champdb()
start = time.time()
for player in playerList:
    print(player.name)
    sort_champMap(player)
    #update_db(player)



end = time.time()
print(end - start)