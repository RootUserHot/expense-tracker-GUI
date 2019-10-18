from base import *
import datetime, time
import pandas as pd
from matplotlib import pylab as plt
from PIL import Image

class takeInfoTxt:

    def __init__(self):
        super().__init__()
        self.takeCategory()

    def takeInfoTxt(self, nameFile):
        self.newListTxt = list()
        self.file = open('../Lib/base/{}.txt'.format(nameFile))
        for line in self.file:
            self.newListTxt.append(line)
        return self.newListTxt

    def takeCategory(self):
        return self.takeInfoTxt('articles')

    def takeBalance(self):
        return self.takeInfoTxt('balance')

class takeHistoty:

    def __init__(self):
        super().__init__()

    def viewHistory(self):
        self.newListHistory = list()
        for key in self.selectRecord():
            self.newListHistory.append("{} | {} | {} | {}".format(self.getTime(key[1]), key[3], self.whichRecord(key[2]), key[4]))
        return self.newListHistory

    def getTime(self, timeS):
        return time.ctime(timeS)

    def whichRecord(self, status):
        if int(status) == 1: return 'Profit'
        else: return 'Expenses'


class statistic():

    def __init__(self):
        super().__init__()

    def takeMainStat(self, records = False, underStat = False):
        if records:
            self.result = records
        else:
            self.result = self.selectRecord()
        self.category, self.allInfo, self.profit, self.expen = [], [], [], []
        for key in self.result:
            if key[4] in self.category:
                continue
            self.category.append(key[4])
        for key in self.category:
            self.categoryN = self.selectRecord('category', key)
            self.p, self.e = 0, 0
            for key2 in self.categoryN:
                if int(key2[2]) == 1:
                    try:
                        self.p = self.p + int(key2[3])
                    except:
                        self.p = self.p + float(key2[3])
                if int(key2[2]) == 0:
                    try:
                        self.e = self.e + int(key2[3])
                    except:
                        self.e = self.e + float(key2[3])
            self.profit.append(self.p)
            self.expen.append(self.e)

        self.subCategory = list()
        for key in self.category:
            self.subCategory.append(key.replace('\n', ':').capitalize())

        if underStat: #uder stat on tab statistic
            if records: #record befor filter
                self.listProf = list()
                self.listExpen = list()
                for key in records:
                    if int(key[2]) == 1:
                        try:
                            self.listProf.append(int(key[3]))
                        except:
                            self.listProf.append(float(key[3]))
                    if int(key[2]) == 0:
                        try:
                            self.listExpen.append(int(key[3]))
                        except:
                            self.listExpen.append(float(key[3]))
                self.differences = (float(str(self.takeBalance()[0])) / float(str(sum(self.listExpen))) - 1) * 100  # differences expenses and month balance in %
                self.recordP = self.selectRecord('count', max(self.listProf))[0]
                self.recordE = self.selectRecord('count', max(self.listExpen))[0]
                self.listUnderStat = [self.recordP[4].replace('\n', ''), self.recordP[3],
                                      self.recordE[4].replace('\n', ''), self.recordE[3], round(self.differences),
                                      round(float(str(self.takeBalance()[0])) - float(str(sum(self.listExpen))))]
                return self.listUnderStat

        self.dataTable = {'Category': self.subCategory, 'Profit': self.profit, 'Expenses': self.expen}
        self.df = pd.DataFrame(data=self.dataTable)
        self.df = self.df.append({'Category': 'Total', 'Profit': sum(self.profit), 'Expenses': sum(self.expen)}, ignore_index=True)
        return self.df

class filterMainStat(statistic):

    def __init__(self):
        super().__init__()

    def filterStat(self, fromS, toS, reverse = False):
        try:
            self.fromSplit = fromS.split('-')
            self.toSplit = toS.split('-')
            self.dateFrom = self.makeSeconds(int(self.fromSplit[0]), int(self.fromSplit[1]), int(self.fromSplit[2]))
            self.dateTo = (self.makeSeconds(int(self.toSplit[0]), int(self.toSplit[1]), int(self.toSplit[2])) + 86400)
            if reverse:
                self.resultDate = self.selectRecord('*', '*')
            else:
                self.resultDate = self.selectRecord()
            self.dataListFilter = list()
            for key in self.resultDate:
                if key[1] >= self.dateFrom and key[1] <= self.dateTo:  # choose the gap
                    self.dataListFilter.append(key)
            return self.dataListFilter
        except:
            return False

    # date convert to seconds for take in base
    def makeSeconds(self, year, month, day):
        self.dateS = datetime.datetime(year, month, day, 0, 0)
        return round(time.mktime(self.dateS.timetuple()))

class makeGraph:

    def __init__(self):
        super().__init__()

    def showGraph(self, fromS, toS):
        try:
            self.listProfGraph = list()
            self.listExpenGraph = list()
            self.recordF = self.filterStat(fromS, toS, True)
            for key in self.recordF:
                if int(key[2]) == 1:
                    try:
                        self.listProfGraph.append(int(key[3]))
                    except:
                        self.listProfGraph.append(float(key[3]))
                if int(key[2]) == 0:
                    try:
                        self.listExpenGraph.append(int(key[3]))
                    except:
                        self.listExpenGraph.append(float(key[3]))
            plt.plot(range(0, len(self.listProfGraph), 1), self.listProfGraph, label='Profit')
            plt.plot(range(0, len(self.listExpenGraph), 1), self.listExpenGraph, label='Expense')
            plt.xlabel('Time')
            plt.ylabel('Amount')
            plt.title("Difference in income and expenses")
            plt.legend()
            plt.savefig("../Include/img/graph.jpg")
            plt.clf()
            self.img = Image.open('../Include/img/graph.jpg')
            return self.img.show()
        except:
            return False

class takeData(db, takeInfoTxt, takeHistoty, filterMainStat, makeGraph):

    def __init__(self):
        super().__init__() #start __init__ in parent

    def checkBalance(self, amount): #rewrite file balance.txt
        try:
            if int(amount):
                with open('../Lib/base/balance.txt', 'w') as f:
                    f.write(amount)
                    f.close()
                return True
        except:
            return False

    def checkData(self, *args):
        self.newListData = list()
        self.newListData.append(round(time.time()))
        try:
            if args[1]:
                self.newListData.append(1)
            else:
                self.newListData.append(0)
            if args[3].find('*') > -1: #check category on sym *
                return False
            if args[0].find('.') == -1: #if is integer, without dot
                if args[0].isnumeric():
                    self.newListData.append(args[0])
                    self.newListData.append(args[3])
                    return self.insertData(self.newListData)
            else:
                self.dot = args[0].find(".") #position dot in num
                self.amount = int(args[0][:self.dot]) #principal amount
                self.cent = int(args[0][(self.dot + 1):]) #cent amount
                if self.cent < 100:
                    self.numWidthDot = "{}{}{}".format(self.amount, '.', self.cent)
                    self.newListData.append(self.numWidthDot)
                    self.newListData.append(args[3])
                    return self.insertData(self.newListData)
        except:
            return False

    def insertData(self, listData):
        return self.creatRecord(listData)
