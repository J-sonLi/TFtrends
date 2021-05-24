import sqlite3
import json
#from main import playerList


conn = sqlite3.connect('champmap.db')
c = conn.cursor()


try:
    c.execute("SELECT * FROM champions")
    print(c.fetchall())
except:
    c.execute("CREATE TABLE IF NOT EXISTS champions (champ_id text, champ_cost integer)")
    with open('champions.json', 'r') as content:
        championslist=json.load(content)
    for i in championslist:
        #print(i['championId'],i['cost'])
        c.execute("INSERT INTO champions VALUES(?, ?)", (i['championId'], i['cost'],))
    conn.commit()
    c.execute("SELECT * FROM champions")
    print(c.fetchall())
#
#
#
#

conn.close()