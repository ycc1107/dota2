import json
import os
import math
from utils.heroid import heroes
from dotaPicker.getData import Hero

UNCERTAIN_ACTIONS = ['purchase_time', 'kills_log']
MIN_ACTIONS = ['dn_t', 'gold_t', 'lh_t', 'xp_t',]
ROOT_PATH = os.path.abspath('..')

class NonDataException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

def genHeroNameMapping():
    return {item['id']:item['localized_name'] for item in heroes if item['localized_name']}
        
def flatData(matchData, mapping, calc, itemMapping):
    if 'radiant_win' not in matchData:
         raise NonDataException('Missing Win')
    matchResult = int(matchData['radiant_win'])
    featureValue = {}
    heroNames = {}
    duration = matchData['duration']
   
    for idx, playerInfo in enumerate(matchData['players']):
        side =  'radiant' if playerInfo['isRadiant'] else 'dire'
        if side not in heroNames:
            heroNames[side] = []
        heroNames[side].append(mapping[int(playerInfo['hero_id'])])

        for key in MIN_ACTIONS:
            name = '{}_{}_{}'.format(side, idx, key)
            value = playerInfo[key]
            if not value:
                raise NonDataException(key)
                
            featureValue[name] = value #[calcFunc(i, j) for i,j in zip(value, value[1:])]


        for key in UNCERTAIN_ACTIONS:
            flag = False
            value = [0] * (duration // 60)
            value1 = [0] * (duration // 60)
            name = '{}_{}_{}'.format(side, idx, key)
            kdaName = '{}_{}_{}_{}'.format(side, idx, key, 'kda')
            assistName = '{}_{}_{}_{}'.format(side, idx, key, 'assist')
            itemDatas = playerInfo[key]
            if not isinstance(itemDatas, list):
                itemDatas = [itemDatas]

            for itemData in itemDatas:
                for k, v in itemData.iteritems():
                    if v > duration:
                        continue
                    seekIdx = (v//60) - 1
                    if seekIdx > len(value):
                        continue
                    try:
                        if k != 'time':
                            k = ''.join(k.split('_')).capitalize()
                            flag = True
                            if k in itemMapping:
                                itemV = itemMapping[k]
                            else:
                                itemV = itemMapping['Default']

                            value[seekIdx] += float(itemV[0])
                            value1[seekIdx] += float(itemV[-1])
                        else:
                            value[seekIdx] += 1
                    except Exception as e:
                        print 'error', e
                        print value
            if flag:
                featureValue[kdaName] = value
                featureValue[assistName] = value1
            else:
                featureValue[name] = value

    for name, item in calc.calcAdvantagePercentages(heroNames['dire'], heroNames['radiant']).iteritems():
        featureValue[name] = [item] * (duration // 60)

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
               
def loadItemValue():
    import datetime
    today = datetime.date.today()
    res = {}
    kda, assis = 0,0 
    with open(ROOT_PATH + '\\src\\data\\itemValue{}_{}.csv'.format(today.month, today.year), 'rb') as stream:
        for line in stream:
            line = line.split(',')
            res[line[0]] = line[1:]
            kda += float(line[1])
            assis += float(line[-1])
    res['Default'] = [kda/len(res), assis/len(res)]
    return res

def run():
    res = []
    mapping = genHeroNameMapping()
    itemMapping = loadItemValue()
    calc = Hero() 
    with open(ROOT_PATH + '\\src\\data\\rawData.txt', 'rb') as stream:
        for idx, line in enumerate(stream):
            try:
                value = flatData(json.loads(line), mapping, calc, itemMapping)
                res.append(value)
            except NonDataException as e:
                print 'Error ', idx, e

    labelPath = ROOT_PATH + '\\src\\data\\tsDataY.txt'
    featurePath = ROOT_PATH + '\\src\\data\\tsDataX.txt'
    saveData(res, labelPath, True)
    saveData(res, featurePath, False)

if __name__ == '__main__':
    run()
