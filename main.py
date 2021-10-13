import requests
import configparser
import discum
import os

config = configparser.ConfigParser()

cwd = os.path.dirname(__file__)
configFile = os.path.join(cwd, 'config.ini')
config.read(configFile)

response = requests.get("https://www.miningpoolsprofits.com/api/stats")

data = response.json()

data.sort(key = lambda json: json['profit_56d_total'], reverse=True)
conversion = 1000000000000000000
rank = 1
header = """```
|   eth pool   | ▼ 56d  |   28d  |  21d   |   14d  |   7d   |   3d   |   1d   |
+--------------+--------+--------+--------+--------+--------+--------+--------+
"""
body = ""

footer = """+--------------+--------+--------+--------+--------+--------+--------+--------+
Data from miningpoolprofits.com for 100MH/s and 0% stales/invalids```"""

for pool in (x for x in data if x['active'] == 1):
    poolNameRank = '{:{align}{width}}'.format(str(rank) + '. ' + pool['code'], align='<', width='12')
    body += "| {:.12} | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |".format(poolNameRank, pool['profit_56d_total']/conversion, pool['profit_28d_total']/conversion, pool['profit_21d_total']/conversion, pool['profit_14d_total']/conversion, pool['profit_7d_total']/conversion, pool['profit_3d_total']/conversion, pool['profit_1d_total']/conversion) + '\n'
    rank +=1

message = header + body + footer

bot = discum.Client(token=config['Discord']['token'])
bot.sendMessage(config['Discord']['channel_id'], message)