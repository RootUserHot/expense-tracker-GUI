import sys
sys.path.append("../Lib/classes/")
from widget import *

mainLogic = takeData()
mainLayout = mainTab()

window = sg.Window('Expense Tracker v0.1').Layout(mainLayout.window).Finalize()

while True:
    event, values = window.Read()
    #router events
    if event is None or event == 'Exit':
        break
    if mainLogic.checkData(values['_AMOUNT_'], values['_Plus_'], values['_Loss_'], values['_CATEGORY_']) and event == 'Added':
        window.Element('_HISTORY_').Update(values=(mainLogic.viewHistory()))
    elif mainLogic.checkBalance(values['_BALANCE_']) and event == 'Change':
        strToSet = 'Monthly balance: {}, change: '.format(mainLogic.takeBalance()[0])
        window['_STRBALANCE_'].Update(strToSet)
    elif mainLogic.filterStat(values['_DATE1_'], values['_DATE2_']) and event == 'Filter':
        newStat = mainLayout.takeMainStat(mainLogic.filterStat(values['_DATE1_'], values['_DATE2_']))
        window['_ALLSTAT_'].Update(newStat)
        underStat = mainLayout.takeMainStat(mainLogic.filterStat(values['_DATE1_'], values['_DATE2_']), True)
        window['_US1_'].Update('Big +: {} ({})'.format(underStat[1], underStat[0]))
        window['_US2_'].Update('Big -: {} ({})'.format(underStat[3], underStat[2]))
        window['_US3_'].Update('BS: {} {}%'.format(underStat[5], underStat[4]))
    elif event == '_GRAPH_':
        mainLayout.takeMainStat(mainLogic.showGraph(values['_DATE1_'], values['_DATE2_']))
    else: sg.Popup('ERROR', 'Data entered incorrectly!')
window.Close()
