#---------------------------------------------------------------------------------------
import xlrd
import re
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

from pylab import mpl
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes

def process_raw_data(file_name):
    file=open(file_name,'r',encoding='utf-8')
    raw_data_list=file.read().splitlines()
    file.close()
    processed_data=[[],[],[],[]]
    for days in raw_data_list:
        list=days.split(' ',-1)
        list=[elem for elem in list if (re.match(r'＋',elem) == None)
              and (re.match(r"\+", elem) == None) and (elem != '')]
        processed_data[0].append(list[0])
        processed_data[1].append(int(list[1]))
        processed_data[2].append(float(list[2]) if len(list) > 2 else None)
        processed_data[3].append(int(list[3]) if len(list) > 3 else None)

    return processed_data

def read_wx_bd_data(file_name):
    wx_bd_data=[[],[],[],[]]
    file=xlrd.open_workbook(file_name)
    st=file.sheets()[0]
    nrows=st.nrows
    for i in range(1,nrows):
        row_data=st.row_values(i)
        row_data[0]=xlrd.xldate.xldate_as_datetime(row_data[0],0).strftime('%m-%d')
        wx_bd_data[0].append(row_data[0])
        for j in range(1,4):
            wx_bd_data[j].append(int(row_data[j]))
    return wx_bd_data

def remove_non(list,length):
    for i in range(length):
        list.pop(0)
    while list[0]==None:
        list.pop(0)
    return list

def plot_inc_delta(x,arr,x_label,y_label0,y_label1,title):
    arr=remove_non(arr,0)
    x=remove_non(x,len(x)-len(arr))

    pre_list,post_list=list(arr),list(arr) #for vectorization
    pre_list.pop(-1)
    post_list.pop(0)
    delta=list(map(lambda post, pre: post - pre, post_list, pre_list))
    delta.insert(0,0)

    mpl.rcParams['font.sans-serif'] = ['simHei']
    fig=plt.figure()
    yax1=fig.add_subplot(111)
    yax1.set_title(title,size=13)
    yax2=yax1.twinx()
    yax1.plot(x,arr,color='green',label=y_label0)
    yax2.plot(x,delta,color="orange",label=y_label1,linestyle='--')
    yax1.legend(loc=2)
    yax2.legend(loc=1)
    yax1.set_ylabel(y_label0, color='green')
    yax2.set_ylabel(y_label1,color='orange')
    yax1.tick_params(axis='y',colors='green')
    yax2.tick_params(axis='y',colors='orange')
    plt.show()
    return 0

def plot_bd(x,arr1,arr2,x_label,y_label0,y_label1,title):

    mpl.rcParams['font.sans-serif'] = ['simHei']
    fig=plt.figure()
    yax1=fig.add_subplot(111)
    yax1.set_title(title,size=13)
    yax2=yax1.twinx()
    yax1.plot(x,arr1,color='green',label=y_label0)
    yax2.plot(x,arr2,color="orange",label=y_label1,linestyle='--')
    plt.xticks(rotation=45)
    for xtick in yax1.get_xticklabels():
        xtick.set_rotation(50)
    yax1.set_ylabel(y_label0, color='green')
    yax2.set_ylabel(y_label1,color='orange')
    yax1.tick_params(axis='y',colors='green')
    yax2.tick_params(axis='y',colors='orange')
    yax1.legend(loc=2)
    yax2.legend(loc=1)
    plt.show()
    return 0
def plot_wx(x,arr1,y_label0,title):
    mpl.rcParams['font.sans-serif'] = ['simHei']
    fig=plt.figure()
    yax1=fig.add_subplot(111)
    yax1.set_title(title,size=13)

    yax1.plot(x,arr1,color='green',label=y_label0)
    for xtick in yax1.get_xticklabels():
        xtick.set_rotation(50)
    yax1.set_ylabel(y_label0, color='green')
    yax1.tick_params(axis='y',colors='green')
    yax1.legend(loc=2)
    plt.show()
    return 0
'''
def plot_wx_bd_data(dates, list0, list1, list2, x_label,
                    ylabel0, ylabel1, ylabel2, title):
    mpl.rcParams['font.sans-serif'] = ['simHei']

    fig=plt.figure(1)

    ax1=HostAxes(fig,[0.1, 0.1, 0.8, 0.8])
    ax2=ParasiteAxes(ax1, sharex=ax1)
    ax3=ParasiteAxes(ax1, sharex=ax1)
    ax1.parasites.append(ax2)
    ax1.parasites.append(ax3)

    ax1.axis['right'].set_visible(False)
    ax2.axis['right'].set_visible(True)
    ax2.axis['right'].major_ticklabels.set_visible(True)
    ax2.axis['right'].label.set_visible(True)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(ylabel0,color='b')
    ax1.set_title(title)
    ax2.set_ylabel(ylabel1)
    ax3.set_ylabel(ylabel2)

    axisline3 = ax3.get_grid_helper().new_fixed_axis
    ax3.axis['right1'] = axisline3(loc='right', axes=ax3, offset=(70, 0))

    fig.add_axes(ax1)

    a1,=ax1.plot(dates,list0,label=ylabel0,color='b')
    a2,=ax2.plot(list1,label=ylabel1,color='orange',linestyle=':')
    a3,=ax3.plot(list2,label=ylabel2,color='green',linestyle='--')

    ax2.axis['right'].label.set_color('orange')
    ax2.axis['right'].major_ticks.set_color('orange')
    ax2.axis['right'].line.set_color('orange')
    ax3.axis['right1'].label.set_color('green')
    ax3.axis['right1'].major_ticks.set_color('green')
    ax3.axis['right1'].line.set_color('green')

    ax1.legend()
    plt.show()
    return 0
'''
#
def main(super_topic_file,wx_bd_file):
    data=process_raw_data(super_topic_file)
    plot_inc_delta(data[0],data[1],'日期','粉丝量','增量','超话粉丝增长情况')
    plot_inc_delta(data[0],data[2],'日期','讨论数(万)','增量(万)','超话讨论数增长情况')
    plot_inc_delta(data[0],data[3],'日期','帖子数','增量','超话帖子增长情况')
    bd_data=read_wx_bd_data(wx_bd_file)
    plot_bd(bd_data[0],bd_data[1],bd_data[2],'日期','百度搜索 index','百度媒体 index','百度指数变化(关键词：黄霄云 + 黄霄雲)')
    plot_wx(bd_data[0],bd_data[3],'微信 index','微信index变化(关键词：黄霄云 + 黄霄雲)')
    #plot_wx_bd_data(data[0],data[1],data[2],data[3],'日期','百度搜索 index','百度媒体 index','微信 index','百度及微信指数变化(关键词：黄霄云 + 黄霄雲)')

if __name__ == '__main__':
    main('RawData.txt','wx_bd_index.xlsx')

