UESFUL_KEYS = ['barracks_status_dire',
 'radiant_win',
 'barracks_status_radiant',
 'first_blood_time',
 'chat',
 'dire_score',
 'duration',
 'lobby_type',
 'tower_status_dire',
 'objectives',
 'radiant_score',
 'human_players',
 'tower_status_radiant',
 'radiant_xp_adv',
 'radiant_gold_adv',
 'players']

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

    def flatData(self):
        for info in UESFUL_KEYS:
            funcName, side = self.getFuncAndSide(info)
            value = self.matchData.get(info)
            getattr(self, funcName)(value, side)

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
