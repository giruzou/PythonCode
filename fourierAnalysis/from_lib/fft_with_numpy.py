#coding:utf-8

import numpy as np 
from scipy import fftpack 
from matplotlib import pyplot as plt 

def main():
    num_samples=1000
    plot_interval=0.01
    xs=np.arange(0,num_samples*plot_interval,plot_interval)
    f1,f2=3,4
    ys=np.sin(2*np.pi*f1*xs)+np.sin(2*np.pi*f2*xs)

    fourier_value=np.fft.fft(ys)
    frq=np.fft.fftfreq(num_samples,d=plot_interval)
    amplitude_spectrum=np.abs(fourier_value)
    print(len(frq),len(amplitude_spectrum))

    plt.plot(frq,amplitude_spectrum,'-')
    plt.xlim([0,5])
    plt.show()




if __name__ == '__main__':
    main()