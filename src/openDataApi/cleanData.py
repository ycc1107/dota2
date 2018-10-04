import json
import os
import math

UNCERTAIN_ACTIONS = ['purchase_time', 'kills_log']
MIN_ACTIONS = ['dn_t', 'gold_t', 'lh_t', 'xp_t',]
ROOT_PATH = os.path.abspath('..')


class MatchObject(object):
    def __init__(self, matchData):
        self.matchData = matchData
        self.res = {}
    
    def getFuncAndSide(self, info):
        if 'barracks_status' in info:
            funcName = 'barracks_status'

        if 'tower_status' in info:
            funcName = 'tower_status'  

        if 'radiant'in info:
            side = 'radiant'
        elif 'dire' in info:
            side = 'dire'
        else:
            side = ''

        return funcName, side

    def getPlay(self, code):
        code = '{:08b}'.format(int(code))
        side = 'dire' if code[0] == 1 else 'radiant'
        palyerNumber = str(int(code[-3:],2))

    def objectives(self, info, side):
        for event in info:
            if 'slot' in event:
                code = event['slot']
                palyerNumber, side = self.getPlay(code)

        return palyerNumber, side

    def tower_states(self, code, side):
        names = ['ancientBottom',
        'ancientTop',
        'bottomTier3',
        'bottomTier2',
        'bottomTier1',
        'middleTier3',
        'middleTier2',
        'middleTier1',
        'topTier3',
        'topTier2',
        'topTier1',]

        code = '{:011b}'.format(int(code))
        names = ['{}_{}'.format(name, side) for name in names]
        
        for name, val in zip(names, code[1:]):
            self.res[name] = val

    def barracks_status(self, code, side):
        names =['bottomRanged ',
        'bottomMelee',
        'middleRanged',
        'middleMelee',
        'topRanged',
        'topMelee',]

        names = ['{}_{}'.format(name, side) for name in names] 
        code = '{:08b}'.format(int(code))

        for name, val in zip(names, code[2:]):
            self.res[name] = val


class NonDataException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

def flatData(matchData):
    if 'radiant_win' not in matchData:
         raise NonDataException('Missing Win')
    matchResult = int(matchData['radiant_win'])
    featureValue = {}
    duration = matchData['duration']
    calcFunc = lambda numA, numB: math.log((1.0 * j + 1) / (i + 1)) * 100
    for idx, playerInfo in enumerate(matchData['players']):
        side =  'radiant' if playerInfo['isRadiant'] else 'dire'
        #heroId= playerInfo['hero_id']

        for key in MIN_ACTIONS:
            name = '{}_{}_{}'.format(side, idx, key)
            value = playerInfo[key]
            if not value:
                raise NonDataException(key)
                
            featureValue[name] = [calcFunc(i, j) for i,j in zip(value, value[1:])]


        for key in UNCERTAIN_ACTIONS:
            value = [0] * (duration // 60)
            name = '{}_{}_{}'.format(side, idx, key)
            itemDatas = playerInfo[key]
            if not isinstance(itemDatas, list):
                itemDatas = [itemDatas]

            for itemData in itemDatas:
                for k, v in itemData.iteritems():
                    if v > duration:
                        continue
                    #findItemValue(k)
                    seekIdx = (v//60) - 1
                    if seekIdx > len(value):
                        continue
                    try:
                        value[seekIdx] = 1
                    except:
                        print 'error'

            featureValue[name] = value
    return matchResult, featureValue

def saveData(rawData, path, isLabel=False):
    with open(path, 'a+') as stream:
        for line in rawData:
            try:
                if isLabel:
                    stream.write(str(line[0]) + '\n')
                else:
                    for k, v in line[1].iteritems():
                        stream.write( str(k) + ',' + ','.join(map(str, v)) + '\n')
                    stream.write('\n')
            except Exception as e:
                print e
               

def run():
    res = []
    with open(ROOT_PATH + '\\src\\data\\rawData.txt', 'rb') as stream:
        for idx, line in enumerate(stream):
            try:
                value = flatData(json.loads(line))
                res.append(value)
            except NonDataException as e:
                print 'Error ', idx, e

    labelPath = ROOT_PATH + '\\src\\data\\tsDataY.txt'
    featurePath = ROOT_PATH + '\\src\\data\\tsDataX.txt'
    saveData(res, labelPath, True)
    saveData(res, featurePath, False)

if __name__ == '__main__':
    run()