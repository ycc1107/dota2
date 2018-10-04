import os
import requests
import json
import time
from auth import KEY

matchIdQuery = '''SELECT matches.match_id
               FROM matches 
               WHERE matches.start_time >= extract(epoch from timestamp '2017-01-01T20:28:32.040Z')'''

matchQuery = 'https://api.opendota.com/api/matches/{}?{}'

ROOT_PATH = os.path.abspath('..')

def getMatchIds(force=False):
    filePath = ROOT_PATH + '\\src\\data\\matchId.txt'
    if os.path.exists(filePath) and not force:
        with open(filePath, 'rb') as stream:
            matchIds = [line for line in stream]
    else:
        req= requests.get('https://api.opendota.com/api/explorer?sql={}'.format(matchIdQuery))
        txt= req.text
        rawData = json.loads(txt)
        matchIds = set(row['match_id'] for row in rawData['rows'])
        
        with open(filePath, 'wb') as stream:
            for line in matchIds:
                stream.write(str(line) + '\n')

    print 'get all matchs'        
    return matchIds

def getMatchData(matchIds):
    res = []
    idx = 0
    matchCount = len(matchIds)
    while idx < matchCount:
        matchId = matchIds[idx]
        query = matchQuery.format(matchId, KEY)
        req = requests.get(query)
        
        while '{"error":"rate limit exceeded"}' in req.text:
            print 'Error sleep 1 sec'
            
            time.sleep(10)
            if res:
                with open(ROOT_PATH + '\\src\\data\\rawData.txt', 'a+') as stream:
                    for line in res:
                        try:
                            line = line.encode('ascii',errors='ignore')
                            stream.write(line + '\n')
                        except Exception as e:
                            print e        
                res = []
            req = requests.get(query)

        res.append(req.text)
        req.connection.close()
        print 'get match {}'.format(idx)
        idx += 1
            
        
        
def run():
    matchIds = getMatchIds()
    getMatchData(matchIds)
if __name__ == '__main__':
    run()