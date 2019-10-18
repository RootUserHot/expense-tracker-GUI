'''
accountTab class UI tab Accounting
statisticTab class UI tab Statistics
settingTab class UI tab Settings
mainTab class UI tab with all tabs
'''
import PySimpleGUI as sg

from logic import *

class accountTab(takeData):

    def __init__(self):
        super().__init__()

    def accountLayout(self):
        #self.rerq = [123, 321, 999]
        #self.rer = self.checkData(self.rerq)
        self.Layout = [[
                    sg.Text('Amount:', size=(6, 1)),
                    sg.InputText(key='_AMOUNT_', size=(12, 1)),
                    sg.Radio('Profit', "group1", default=True, size=(4, 1), key='_Plus_'),
                    sg.Radio('Expenses', "group1", default=False, size=(8, 1), key='_Loss_'),
                    sg.Combo((self.takeCategory()), key='_CATEGORY_', size=(12, 1), readonly=True),
                    sg.Button('Added')],
                    [
                        sg.Listbox(values=(self.viewHistory()), size=(70, 14), key='_HISTORY_', background_color='Light Gray')]
                    ]
        return self.Layout

class statisticTab(statistic):

    def __init__(self):
        super().__init__()

    def statisticLayout(self):
        self.Layout = [[
            sg.Multiline(self.takeMainStat(), size=(70, 13), key='_ALLSTAT_', background_color='Light Gray', disabled=True),],
            [
                sg.Text('Big +: use filter', key='_US1_', size=(21, 1)), sg.Text('Big -: use filter', key='_US2_', size=(21, 1)), sg.Text('BS: use filter', key='_US3_', size=(15, 1))
            ],
            [
                sg.Text('From:', size=(4, 1)), sg.InputText(default_text=datetime.date.today(), key='_DATE1_', size=(12, 1)), sg.Text('to:', size=(2, 1)), sg.InputText(default_text=datetime.date.today(), key='_DATE2_', size=(12, 1)), sg.Button('Filter'), sg.Button('Graph', key='_GRAPH_')
            ]
        ]
        return self.Layout

class settingTab:

    def __init__(self):
        super().__init__()

    def settingLayout(self):
        self.Layout = [[
            sg.Text('Monthly balance: {}, change: '.format(self.takeBalance()[0]), size=(26, 1), key='_STRBALANCE_'),
            sg.InputText(key='_BALANCE_', size=(13, 1)),
            sg.Button('Change')
        ]]
        return self.Layout

class mainTab(accountTab, statisticTab, settingTab):

    def __init__(self):
        super().__init__()
        self.window = self.mainLayout()

    def mainLayout(self):
        self.Layout = [
            [
                sg.TabGroup(
                [[
                    sg.Tab('Accounting', self.accountLayout()), sg.Tab('Statistics', self.statisticLayout()), sg.Tab('Settings', self.settingLayout())
                ]])
            ]
        ]
        return self.Layout

    def updAccountTab(self):
        return window.Element('_HISTORY_').Update(values=('123', '321'))