import acct
import json
import math
import requests
import robin_stocks as r
from pprint import pprint

login = r.login(acct.username, acct.password)

def getPositions():
    return r.build_holdings()

def getUserProfile():
    return r.build_user_profile()

def getPrice(symbol):
    return float(r.stocks.get_latest_price(symbol)[0])

def deriveTargetPosition(equity, longs):
    return (float(equity) * 0.95) / len(longs)

def deriveBuysAndSells(positions, longs, shorts, targetPositionValue, sectorsToETFs):
    buys = {}
    sells = {}
    for sector in shorts:  # build sell orders for positions with negative QCI
        symbol = sectorsToETFs[sector]
        if symbol in positions:
            shs = positions[symbol]['quantity']
            print('Sell ' + symbol + ' because QCI is negative')
            sells[symbol] = shs
    for sector in longs:   # build buy/sell orders for positions with positive QCIs
        symbol = sectorsToETFs[sector]
        if symbol in positions:
            info = positions[symbol]
            equity = float(info['equity'])
            price = float(info['price'])
            if equity > targetPositionValue:
                diff = round(equity - targetPositionValue, 2)
                shs = math.ceil(diff / price)
                print('Too much ' + symbol + ': sell off at least $' + str(diff) + ' (' + str(shs) + ' shares)')
                sells[symbol] = shs
            elif equity < targetPositionValue:
                diff = round(targetPositionValue - equity, 2)
                if diff > price:
                    shs = math.floor(diff / price)
                    print('Not enough ' + symbol + ': buy up to $' + str(diff) + ' (' + str(shs) + ' shares)')
                    buys[symbol] = shs
        else:
            price = float(r.stocks.get_latest_price(symbol)[0])
            shs = math.floor(targetPositionValue / price)
            print('Open position in ' + symbol + ': buy up to $' + str(round(targetPositionValue, 2)) + ' (' + str(shs) + ' shares)')
            buys[symbol] = shs
    return buys, sells

def processSells(sells):
    for symbol, shs in sells.items():
        order = r.orders.order_sell_market(symbol, shs, extendedHours='false')

def processBuys(buys):
    for symbol, shs in buys.items():
        order = r.order_buy_market(symbol, shs)

def checkIfSellsOpen():
    orders = r.orders.get_all_open_orders()
    if orders[0] == None:
        print('Sell orders finished!')
        return False
    else:
        for order in orders:
            info = r.orders.get_order_info(order['id'])
            if info['state'] != 'filled':
                print('Sell orders still open!')
                return True
        return False

def analyzeQCIs(sectorsToETFs, qics, codeToSectorName):
    longs = []
    shorts = []
    for sector in sectorsToETFs:
        if sector in qics:
            if float(qics[sector]['QCI_' + sector.upper()]) >= 0.0:
                print('Long ', codeToSectorName[sector])
                longs.append(sector)
            else:
                print('Short', codeToSectorName[sector])
                shorts.append(sector)
    return longs, shorts

def rhApiCall(url):
    return json.loads(requests.get(url).text)