import Annual_return_calculation as main
import yfinance as yf
import scipy as sp
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd

#================| Investment Variables |=================

monthly_invest = 1
gap_sample = np.linspace(-7, 7, 1000)


#=====================| Strategies |=======================

def always_the_same(gap, price, index, cash):
    new_index = index +  price*monthly_invest
    new_cash = cash
    return new_index, new_cash

def optimize_strategy(gap, price, index, cash):
    if gap >= 0:
        if gap >=1:
            gap = 1

        new_index = index + (1-gap)*price*monthly_invest
        new_cash = cash + gap*monthly_invest
    else:
        if gap <= -1:
            gap = -1

        if cash>= abs(gap)*monthly_invest:
            new_index = index + (1-gap)*price*monthly_invest
            new_cash = cash + gap*monthly_invest
        else:
            new_index = index + (cash + monthly_invest)*price
            new_cash = 0
    print(gap)
    return new_index, new_cash

def opti(gap, price, index, cash):
    if gap>= 1:
        new_index = index + (1/gap)*price*monthly_invest
        new_cash = cash + ((gap-1)/gap)*monthly_invest
    elif gap<=-1:
        if monthly_invest*abs(gap)<=cash:
            new_index = index + price*monthly_invest*(1+abs(gap))
            new_cash = cash - abs(gap)*monthly_invest
        else:
            new_index = index + price*(cash+monthly_invest)
            new_cash = 0
    else:
        new_index = index + price*monthly_invest
        new_cash = cash
    return new_index, new_cash

def strat(gap, price, index, cash):
    if gap>=7:
        new_index = index
        new_cash = cash + monthly_invest
    elif gap<=-1:
        new_index = index + price*(monthly_invest + cash)
        new_cash = 0
    else:
        new_index = index + price*monthly_invest
        new_cash = cash
    return new_index, new_cash

#================| Generalized Strategy |==================

def evaluate(strategy, gap):
    i=1
    while (gap_sample[i]<=gap):
        i+=1

    slope = (strategy[i]-strategy[i-1])/(gap_sample[i]-gap_sample[i-1])
    return slope*(gap-gap_sample[i-1])+strategy[i-1]

def investment(strategy, gap, price, index, cash):
    to_invest = evaluate(strategy, gap)

    if to_invest-monthly_invest >= cash:
        to_invest = cash + monthly_invest
        to_stock = 0

    elif to_invest-monthly_invest <= 0:
        to_stock = monthly_invest - to_invest
    
    new_index = index + price*to_invest
    new_cash = cash + to_stock
    return new_index, new_cash

#=====================| Back test |========================

def get_first_working_day(year, month, data):
    day = main.datetime.date(year, month, 1)
    while(not(str(day)) in data.index):
        day = day + main.datetime.timedelta(days =1)
    return day


def back_test(strategy, data):
    today = main.datetime.date.today()
    regular_return = main.get_cagr(data)
    cash = 0
    index = 0
    cash_list= np.array([])
    total_list = np.array([])

    for y in range(1957, today.year):
        for m in range(1, 13):
            current = get_first_working_day(y, m, data)
            index, cash = strategy(main.get_annual_return(data, current, regular_return), data.loc[str(current), "Close"], index, cash)
            total_list = np.append(total_list, data.loc[str(current), "Close"]*index + cash)
            cash_list =np.append(cash_list, cash)

    total = data.loc[str(current), "Close"]*index + cash
    print(index, cash, total)
    return index, cash, total, total_list, cash_list

#=====================| Entry Point |========================


_, _, t1, total_l1, c_l1 = back_test(strat, main.data_spx)
_, _, t2, total_l2, c_l2 = back_test(always_the_same, main.data_spx)
print(t1-t2, (t1-t2)/t2)


fig, ax = plt.subplots(1, 1)
ax.plot(total_l1, color = main.green)
ax.plot(total_l2, color = main.red)
ax.plot(total_l1-total_l2)
plt.show()

fig, ax = plt.subplots(1, 1)
ax.plot(c_l1, color = main.green)
ax.plot(c_l2, color = main.red)
plt.show()