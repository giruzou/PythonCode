import numpy as np 
from matplotlib import pyplot as plt

class PointsBrowser():
    def __init__(self,fig,ax,xs,ys,plotted):
        self.lastind=0
        self.selected, =ax.plot([xs[0]],[ys[0]],'o', ms=12,alpha=0.4,
                            color='red', visible=False)
        self.moved, =ax.plot([xs[0]],[ys[0]],'o', ms=12,alpha=0.4,
                            color='green', visible=False)
        self.movedxy=None
        self.fig=fig
        self.ax=ax
        self.xs=xs
        self.ys=ys
        self.plotted=plotted

        self.pressed_loc=None

    def onpick(self,event):
        if event.artist!=self.plotted:
            return True

        N=len(event.ind)
        print(event.ind)
        print(N)
        if not N:
            return True

        x=event.mouseevent.xdata
        y=event.mouseevent.ydata

        distances=np.hypot(x-self.xs[event.ind],y-self.ys[event.ind])
        indmin=distances.argmin()
        dataind=event.ind[indmin]

        self.pressed_loc = x,y

        self.lastind=dataind
        self.plot_last_ind_point()


    def on_key_pressed(self,event):
        if self.lastind is None:
            return

        if event.key in ['n', 'right','up']:
            inc=1
        elif event.key in ['p','left','down']:
            inc=-1
        else:
            inc=0
            
        print(event.key)
        self.lastind+=inc
        self.lastind=self.lastind % len(self.xs)
        self.plot_last_ind_point()

    def plot_last_ind_point(self):
        if self.lastind is None:
            return 

        dataind=self.lastind
        self.selected.set_visible(True)
        self.selected.set_data(self.xs[dataind],self.ys[dataind])
        self.fig.canvas.draw()

    def on_motion(self,event):

        if self.pressed_loc is None:
            return
        if event.inaxes != self.ax:
            return

        xpress,ypress=self.pressed_loc        
        print(event,xpress,ypress)

        dx=event.xdata-xpress
        dy=event.ydata-ypress

        xnew,ynew=dx+self.xs[self.lastind],dy+self.ys[self.lastind]
        print(xnew,ynew)
        self.moved.set_visible(True)
        self.moved.set_data([xnew],[ynew])
        self.fig.canvas.draw()
        self.movedxy=(xnew,ynew)

    def on_release(self,event):

        if self.movedxy is None:
            return True

        self.pressed_loc=None
        self.moved.set_visible(False)
        self.moved.set_data([self.movedxy[0]],self.movedxy[1])

        self.xs[self.lastind]=self.movedxy[0]
        self.ys[self.lastind]=self.movedxy[1]

        self.plotted.set_data(self.xs,self.ys)
        self.fig.canvas.draw()
        self.plot_last_ind_point()
        self.movedxy=None



def main():
    X=np.random.rand(7,200)
    xs=np.mean(X,axis=1)
    ys=np.std(X,axis=1)

    fig, ax=plt.subplots()
    plotted, =ax.plot(xs,ys,'o',picker=5)

    browser=PointsBrowser(fig,ax,xs,ys,plotted)

    fig.canvas.mpl_connect('pick_event',browser.onpick)
    fig.canvas.mpl_connect('key_press_event',browser.on_key_pressed)
    fig.canvas.mpl_connect('motion_notify_event',browser.on_motion)
    fig.canvas.mpl_connect('button_release_event',browser.on_release)

    plt.show()

if __name__ == '__main__':
    main()