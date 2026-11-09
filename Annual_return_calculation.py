
import yfinance as yf
import scipy as sp
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd

#=========================| Plt |=========================

plt.style.use('dark_background')
grey = (0.5, 0.5, 0.5)
white = (0.8, 0.8, 0.8)
red = (0.9, 0, 0)
light_red =(1, 0.38, 0)
green = (0.071, 0.502, 0)
light_green = (0.106, 0.761, 0)

#====================| Get Data |=====================

#S&P 500
spx = yf.Ticker("^SPX")
data_spx = spx.history(period="80y")
spx_return = 0.083

#NASDAQ 100
ndq = yf.Ticker("^NDX")
data_ndq = ndq.history(period="60y")
ndq_return = 0.16

#====================| Regular Annual Return |=====================

def get_arithmetical_mean_annual_return(data, nb_days):

    current = datetime.date.today() - datetime.timedelta(days =1)
    annual_return = np.array([])

    for i in range(0, nb_days):
        if ((current.day != 29 or current.month != 2) and (str(current) in data.index)):
            date_last_year = current.replace(year = current.year -1)
            while (not(str(date_last_year) in data.index)):
                date_last_year = date_last_year - datetime.timedelta(days=1)

            annual_return = np.append(annual_return, (data.loc[str(current), "Close"]-data.loc[str(date_last_year), "Close"])/data.loc[str(date_last_year), "Close"])
        current = current - datetime.timedelta(days=1)

    return np.mean(annual_return)

def get_cagr(data):

    today = datetime.date.today() - datetime.timedelta(days = 1)
    while(not(str(today) in data.index)):
        today = today - datetime.timedelta(days = 1)
    first_day = datetime.date(year = 1957, day= 4, month = 3)

    delta_t = (today-first_day).total_seconds()/(365.25*24*3600)
    return np.exp(1/delta_t*np.log(data.loc[str(today), "Close"]/data.loc[str(first_day), "Close"])) -1


#====================| Annual Return Calculation |=====================

def get_annual_return(data, date, regular_return):

    #get the same day of the passed year
    date_last_year = date
    if (date.day == 29 and date.month == 2):
        date_last_year = date_last_year.replace(day = 28)
    date_last_year = date_last_year.replace(year = date.year -1)
    while (not(str(date_last_year) in data.index)):
        date_last_year = date_last_year - datetime.timedelta(days=1)

    current_return = (data.loc[str(date), "Close"]-data.loc[str(date_last_year), "Close"])/data.loc[str(date_last_year), "Close"]
    return (current_return - regular_return)/regular_return



def print_annual_return(data_list, index_list, return_list, nb_days):

    current = datetime.date.today() - datetime.timedelta(days =1)
    annual_return = np.array([])
    time = np.array([])

    fig, ax_l = plt.subplots(1,len(data_list))

    for id in range(0, len(data_list)):
        for i in range(0, nb_days):
            if (str(current) in data_list[id].index):
                annual_return = np.append(annual_return, get_annual_return(data_list[id], current, return_list[id]))
                time = np.append(time, current)
            current = current - datetime.timedelta(days=1)

        mean = np.zeros(len(annual_return))
        ten_percent = 0.1*np.ones(len(annual_return))
        twnety_percent = 0.2*np.ones(len(annual_return))
        negative_ten_percent = -0.1*np.ones(len(annual_return))
        negative_twenty_percent = -0.2*np.ones(len(annual_return))
        
        ax_l[id].plot(time, annual_return, color= grey)
        ax_l[id].plot(time, mean, color = white)
        ax_l[id].plot(time, ten_percent, color = light_green)
        ax_l[id].plot(time, twnety_percent, color = light_green)
        ax_l[id].plot(time, negative_ten_percent, color = red)
        ax_l[id].plot(time, negative_twenty_percent, color = red)
        ax_l[id].set_title(index_list[id])
    plt.show()
    print(np.mean(annual_return))


#====================| Entry Point |=====================



