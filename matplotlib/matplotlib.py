#coding
import numpy as np 
from matplotlib import pyplot as plt
#
xs=np.arrange(-3,3,0.01)
y_sin=np.sin(x)
y_cos=np.cos(x)
# figure object
fig=plt.figure(1)
print("type(fig): {}".format(type(fig)))

ax1=fig.add_subplot(2,1,1)
ax2=fig.add_subplot(2,1,2)
print("type(ax1): {}".format(type(ax1)))

ax1.plot(x,y_sin)
ax2.plot(x,y_cos)

ax1.set_ylim(-1.3,1.3)
ax2.set_ylim(-1.3,1.3)

ax1.set_title("$\sin x$")
ax2.set_title("$\cos x$")

ax1.set_xlabel("x")
ax2.set_xlabel("x")

fig.tight_layout()
