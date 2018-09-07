import pandas as pd 
import os 
import csv
from utils.heros import heroList

class Hero(object):
    def __init__(self):
        self.heroData = []
        try:
            self.loadHeroData()
        except Exception as e:
            print 'Loading Error', e

    def loadHeroData(self):
        rootPath = os.path.abspath('..')
        path = rootPath + '\\src\\utils\\heroData.csv'
        with open(path, 'rb') as stream:
            reader = csv.reader(stream)
            for line in reader:
                line = [float(item) for item in line]
                self.heroData.append(line)

    def teamStats(self, radiantIdx, direIdx):
        radiantSynergy = sum(self.heroData[i][j] for i in radiantIdx for j in radiantIdx[i:])
        radiantCounterpick = sum(self.heroData[i][j] for i in radiantIdx for j in direIdx)

        direSynergy = sum(self.heroData[i][j] for i in direIdx for j in direIdx[i:])
        direCounterpick = sum(self.heroData[i][j] for i in direIdx for j in radiantIdx)

        radiantNumAdvOver = sum(1 for i in radiantIdx for j in direIdx if self.heroData[i][j] >= 0)
        direNumAdvOver = sum(1 for i in direIdx for j in radiantIdx if self.heroData[i][j] >= 0)

        return radiantSynergy, radiantCounterpick, radiantNumAdvOver, direSynergy, direCounterpick, direNumAdvOver, 

    def isInputValid(self, radiant, dire):
        if not (radiant and dire):
            return False
        if len(radiant) != len(dire):
            return False
        if not (len(radiant) == 5 and  len(dire) == 5):
            return False
        if not all(item in heroList for item in radiant + dire):
            return False
        
        return True

    def calcAdvantagePercentages(self, radiant, dire):
        if not self.isInputValid(radiant, dire):
            raise Exception('Wrong')

        radiantIdx = [heroList.index(name) for name in radiant]
        direIdx = [heroList.index(name) for name in dire]
        
        radiantSynergy, radiantCounterpick, radiantNumAdvOver, direSynergy, direCounterpick, direNumAdvOver = self.teamStats(radiantIdx, direIdx)

        radiantSynergyDiff = radiantSynergy - direSynergy
        radiantCounterDiff = radiantCounterpick - direCounterpick

        direSynergyDiff = -1 * radiantSynergyDiff
        direCounterDiff = -1 * radiantCounterDiff

        return (radiantSynergy, radiantCounterpick, 
                radiantSynergyDiff, radiantCounterDiff,
                radiantNumAdvOver,
                direSynergy, direCounterpick, 
                direSynergyDiff, direCounterDiff,
                direNumAdvOver)

if __name__ == '__main__':
    dire = ['Abaddon',
        'Alchemist',
        'Ancient Apparition',
        'Anti-Mage',
        'Arc Warden',]
    radiant = ['Warlock',
        'Weaver',
        'Windranger',
        'Winter Wyvern',
        'Witch Doctor']

    hero = Hero()
    print hero.calcAdvantagePercentages(dire, radiant)