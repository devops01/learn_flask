# coding:utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from matplotlib.finance import candlestick
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY


def pandas_candlestick_ohlc(stock_data, otherseries=None):
    # 设置绘图参数，主要是坐标轴
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    dayFormatter = DateFormatter('%d')

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if stock_data.index[-1] - stock_data.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.grid(True)

    # 创建K线图
    stock_array = np.array(stock_data.reset_index()[['date', 'open', 'high', 'low', 'close']])
    stock_array[:, 0] = date2num(stock_array[:, 0])
    candlestick(ax, stock_array, colorup="red", colordown="green", width=0.4)

    # 可同时绘制其他折线图
    if otherseries is not None:
        for each in otherseries:
            plt.plot(stock_data[each], label=each)
        plt.legend()

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

if __name__ == '__main__':
    # 读取数据
    stock = pd.read_csv('sh600011.csv', parse_dates=[0], index_col=0)
    # stock = stock[::-1]  # 逆序排列
    # stock.head()
    # stock['close'].plot(grid=True)
    # plt.show()
    pandas_candlestick_ohlc(stock)