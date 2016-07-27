import numpy as np
from matplotlib import pyplot as plt

delta=0.1

def get_integral_curve(f,init_xy,end_x):
    """solve ode 'dy/dx=f(x,y)'
    """
    (x,y)=init_xy
    xs,ys=[x],[y]
    for i in np.arange(init_xy[0],end_x,delta):
        y+=delta*f((x,y))
        x+=delta
        xs.append(x)
        ys.append(y)
    return xs,ys

def main():
    """solve logistic equation dy/dx=y(1-y)
    """
    #set initial values of x and y
    init_xy=(0,0.5)
    end_x=4

    fig,ax=plt.subplots()

    #show integral curve of logistic equation 
    xs,ys=get_integral_curve(lambda (x,y):y*(1-y),init_xy,end_x)
    ax.plot(xs,ys,"o",color='blue')

    #show exact solution
    sigmoid_xs=np.arange(-5,5,delta)
    sigmoid_ys=1/(1+np.exp(-sigmoid_xs))
    ax.plot(sigmoid_xs,sigmoid_ys,"-",color='red')
    
    ax.set_xlim([-5,5])
    ax.set_ylim([-0.5,1.5])
    plt.show()

if __name__=='__main__':
    main()