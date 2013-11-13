from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
# get formulas from sailing.py
import sailing  as s

fig = plt.figure(figsize=(3,3))
ax = plt.subplot(111,polar=True)
ax.set_position([0.1,0.3, 0.9,0.62])
def update(val):
    s.values[s.CHx]=slider1.val
    s.values[s.CHx2]=slider2.val
    s.values[s.Cz]=slider3.val
    ax.cla()
    draw_force()
    plt.draw()


def draw_force():

    s.force_simp=s.lambdify((s.gamma,s.v),(s.force1-s.force2).subs(s.values))
    s.force=s.lambdify((s.gamma,s.v),(s.force1- s.force2 - s.CHx*s.v**2-s.CHx2).subs(s.values))
    X = np.linspace(0, 3.14, 20)
    Y = np.linspace(0, 6, 20)
    
    Z=np.array([[s.force(g,h) for g in X] for h in Y])
    X, Y = np.meshgrid(X, Y)
    maximum=Z.max()
    
    surf = ax.contourf(X, Y, Z, np.linspace(0, maximum, 20), rstride=1, cstride=1, cmap=cm.jet,linewidth=0, antialiased=False)

    surf = ax.contourf(-X, Y, Z, np.linspace(0, maximum, 20), rstride=1, cstride=1, cmap=cm.jet,linewidth=0, antialiased=False)
    ax.set_ylim(0,6);
#    fig.colorbar(surf, shrink=0.5, aspect=5)


axcolor = 'lightgoldenrodyellow'
ax1 = plt.axes([0.15, 0.1, 0.7, 0.03], axisbg=axcolor)
ax2 = plt.axes([0.15, 0.15, 0.7, 0.03], axisbg=axcolor)
ax3 = plt.axes([0.15, 0.2, 0.7, 0.03], axisbg=axcolor)
slider1 = Slider(ax1, 'CHx', 0.0, 1.50, valinit=0.3)
slider2 = Slider(ax2, 'CHx2', 0.0, 10, valinit=0.0)
slider3 = Slider(ax3, 'Cz', 0.0, 10, valinit=4.0)
slider1.on_changed(update)
slider2.on_changed(update)
slider3.on_changed(update)


s.values={s.Cz:5.5,s.Cx:1,s.CHx:slider1.val,s.CHx2:slider2.val,s.v_w:1.0}
draw_force()
plt.show()

