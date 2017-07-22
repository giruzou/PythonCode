from matplotlib import pyplot as plt 
import numpy as np
from scipy import stats
def main():
    sample1=2*[0]+4*[1]+12*[2]+24*[3]+24*[4]+10*[5]
    sample2=6*[0]+14*[1]+18*[2]+18*[3]+14*[4]+6*[5]
    sample3=2*[5]+4*[4]+12*[3]+24*[2]+24*[1]+10*[0]

    fig=plt.figure(figsize=(12,6))

    ax1=fig.add_subplot(131)
    ax2=fig.add_subplot(132)
    ax3=fig.add_subplot(133)
    
    for i in [1,2,3]:
        eval("ax{0}.set_title(\
                'skew=%f'%stats.skew(sample{0}))".format(i))
        eval("ax{0}.hist(sample{0})".format(i))
    
    plt.show()

if __name__ == '__main__':
    main()