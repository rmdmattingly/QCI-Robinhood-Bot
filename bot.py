import func
import Quikfo
from time import sleep
sectorsToETFs = {'fi':'VFH', 'it':'VGT', 'hc':'VHT', 'cs':'VDC', 'sp500':'SPY'}
codeToSectorName = {'fi':'Financials', 'it':'Info Tech', 'hc':'Health Care', 'cs':'Consumer Staples', 'sp500':'SP500'}

## Get QCIs and derive longs, shorts (only dealing with longs for now)
print('QCI Recommendations:')
qics = Quikfo.getQCIs()
longs, shorts = func.analyzeQCIs(sectorsToETFs, qics, codeToSectorName)
print('~~~~~\nTODO:')
# Get info on active positions ... [symbol] => {'quantity', 'price'}
positions = func.getPositions()
# Get info on profile such as cash and total equity
profile = func.getUserProfile()
equity = profile['equity']          # cash + investment value
targetPositionValue = func.deriveTargetPosition(equity, longs)
# Get buy & sell orders
buys, sells = func.deriveBuysAndSells(positions, longs, shorts, targetPositionValue, sectorsToETFs)
# Process sell orders
print('~~~~~\nSells')
func.processSells(sells)
# Verify sell orders complete
print('~~~~~\nWaiting for Sell Orders to Complete')
sellsOpen = True
while sellsOpen:
    sellsOpen = func.checkIfSellsOpen()
    sleep(10)
# Process buy orders
print('~~~~~\nBuys')
func.processBuys(buys)
print('Execution complete')