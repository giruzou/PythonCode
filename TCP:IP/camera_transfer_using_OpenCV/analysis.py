# -*- coding:utf-8 -*-
#!/usr/bin/python

import numpy as np 
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

client_init_time=0

def analysis_client():
    print 'analysis client'
    start=[]
    getend=[]
    shwend=[]
    f=open("res.txt",'r')
    lines=f.readlines()
    xs=[]
    for lin in lines:
        word=lin.split()
        if "start" in lin:
            start.append(float(word[1]))
        if "getend" in lin:
            getend.append(float(word[1]))
        if "shw_end" in lin:
            shwend.append(float(word[1]))
    f.close()
    print"getend-start"
    print np.average([getend[i]-start[i] for i in range(len(start))])*1000,"ms"
    print"showend-getend"
    print np.average([shwend[i]-getend[i] for i in range(len(getend))])*1000,"ms"
    for i,s in enumerate(start):
        plt.annotate(str(i),
             xy=(s, 0.5), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    for i,s in enumerate(getend):
        plt.annotate(str(i),
             xy=(s, 1), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    for i,s in enumerate(shwend):
        plt.annotate(str(i),
             xy=(s, 1.5), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    global client_init_time
    #client_init_time=start[1]+(getend[1]-start[1])/2.0
    client_init_time=start[0]+(getend[0]-start[0])/2.0
    client_init_time=0
    plt.plot(start,[0.5 for s in start],"o")
    plt.plot(getend,[1 for s in getend],"o")
    plt.plot(shwend,[1.5 for s in shwend],"o")

    return start,getend,shwend

def analysis_server():
    print "server analysis"
    start=[]
    capend=[]
    proend=[]
    f=open("ser_res.txt",'r')
    lines=f.readlines()
    for lin in lines:
        word=lin.split()
        if "start" in lin:
            start.append(float(word[1])+client_init_time)
        if "capend" in lin:
            capend.append(float(word[1])+client_init_time)
        if "proend" in lin:
            proend.append(float(word[1])+client_init_time)
    f.close()
    start=np.array(start)
    capend=np.array(capend)
    proend=np.array(proend)
    #ori_start_1=start[1]-client_init_time
    #start-=ori_start_1
    #capend-=ori_start_1
    #proend-=ori_start_1
    print"capend-start"
    print np.average([capend[i]-start[i] for i in range(len(start))])*1000,"ms"
    print"proc-capsend"
    print np.average([proend[i]-capend[i] for i in range(len(capend))])*1000,"ms"

    for i,s in enumerate(start):
        plt.annotate(str(i),
             xy=(s, 2), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    for i,s in enumerate(capend):
        plt.annotate(str(i),
             xy=(s, 2.5), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    for i,s in enumerate(proend):
        plt.annotate(str(i),
             xy=(s, 3), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    plt.plot(start,[2 for s in start],"o")
    plt.plot(capend,[2.5 for s in capend],"o")
    plt.plot(proend,[3 for s in proend],"o")

    return start,capend, proend

def main():
    #adjust graph
    majorLocator=MultipleLocator(1)
    majorFormatter=FormatStrFormatter("%f")
    minorLocator=MultipleLocator(0.1)
    fig,ax=plt.subplots()

    c_start,getend,shwend=analysis_client()
    s_start,capend,proend=analysis_server()

    leflim=0
    riglim=2
    plt.xlim(leflim,riglim)
    plt.ylim(0,3.5)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)


    plt.show()

if __name__ == '__main__':
    main()