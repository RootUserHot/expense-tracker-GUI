import sqlite3

class db:

    def __init__(self):
        self.nameBD = '../Lib/base/data.db'

    def connectDB(self):
        self.conn = sqlite3.connect(self.nameBD)
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def query(self, query, varAggr = False):
        if varAggr:
            return self.cur.execute(query, varAggr)
        else:
            return self.cur.execute(query)

    def creatRecord(self, listAttr):
        self.connectDB()
        self.result = self.query('INSERT INTO `records` VALUES (NULL, ?, ?, ?, ?)', listAttr)
        self.conn.commit()
        self.disconnect()
        return True

    def selectRecord(self, columnRecord = False, agrRecord = False):
        self.connectDB()
        if columnRecord != '*' and agrRecord != '*':
            self.result = self.query('SELECT * FROM `records` WHERE {} = ? ORDER BY `id` DESC'.format(columnRecord), (agrRecord,))
            self.data = self.result.fetchall()
            self.disconnect()
            return self.data
        self.result = self.query('SELECT * FROM `records` ORDER BY `id` ASC')
        self.data = self.result.fetchall()
        self.disconnect()
        return self.data

    def test(self, timeq):
        self.connectDB()
        self.result = self.query('SELECT *  FROM `records` WHERE datetime({})'.format(timeq))
        self.data = self.result.fetchall()
        self.disconnect()
        return self.data

    def deleteRecord(self, columnRecord, agrRecord):
        self.connectDB()
        self.result = self.query('DELETE FROM `records` WHERE {} = ?'.format(columnRecord), (agrRecord,))
        self.conn.commit()
        self.disconnect()

    def updateRecord(self, columnRecord, columnRecordValue, columnRecordWho, columnRecordValueWho):
        self.connectDB()
        self.result = self.query('UPDATE `records` SET {} = ? WHERE {} = ?'.format(columnRecord, columnRecordWho), (columnRecordValue, columnRecordValueWho,))
        self.conn.commit()
        self.disconnect()