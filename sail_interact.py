#!/usr/bin/env python

from matplotlib.widgets import Cursor,CheckButtons
import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(121, axisbg='#FFFFCC',polar=True)
ax2 = fig.add_subplot(122, axisbg='#FFFFCC')

# get formulas from the sailing module
import sailing as s

ax.plot(s.xx,s.yy,'b',-s.xx,s.yy,'b',s.xx,np.abs(np.cos(s.xx))*s.yy,"g",-s.xx,s.abs(np.cos(s.xx))*s.yy,"g")
ax.plot(s.xx,np.ones_like(s.xx),'r',-s.xx,np.ones_like(s.xx),'r')
ax.plot(s.xx[s.yy>0],s.AAW(s.xx,s.yy),'k')
ax2.set_xlim(-4, 4)
ax2.set_ylim(-4, 4)
ax2.set_aspect('equal')

def draw_arrow(x,y):
    ax2.cla()
#    v=s.Funv_gamma(x)
    v=y
    s.values[s.gamma]=x
    s.values[s.v]=v

    if(float(v)>0):
        s.values[s.gamma]=x
        s.values[s.v]=v
        if lab_frame_toggle: 
            angle=-x
        else:
            angle=0.0
        if not force_toggle: 
            vec1=(s.ROT(angle)*s.u.subs(s.values)).evalf()
            vec2=(v*s.ROT(angle)*s.ev).subs(s.values).evalf()
            vec3=vec1+vec2
            s.u.normalized().subs(s.values)
            ax2.arrow(0,0,float(vec1[0]),float(vec1[1]),alpha=0.5,width=.2,head_width=.51,head_length=.7,facecolor='g')
            ax2.arrow(0,0,float(vec2[0]),float(vec2[1]),alpha=0.5,width=.2,head_width=.51,head_length=.7,facecolor='b')
            ax2.arrow(0,0,float(vec3[0]),float(vec3[1]),alpha=0.5,width=.2,head_width=.51,head_length=.5,facecolor='c')
        else:
            scale=0.1
            FL=scale*s.Cz.subs(s.values)*v*v*(s.ROT(angle)*s.up.subs(s.values)).evalf().normalized()
            FD=scale*s.Cx.subs(s.values)*v*v*(s.ROT(angle)*s.u.subs(s.values)).evalf().normalized()
            F2=scale*s.CHx.subs(s.values)*v*v*(s.ROT(angle)*s.ev.subs(s.values)).evalf()
     
            F=FL+FD
            maximum=.3*F.norm()
            F=F/maximum
            FD=FD/maximum
            FL=FL/maximum
            
            ax2.arrow(0,0,float(FL[0]),float(FL[1]),alpha=0.5,width=.2,head_width=.51,head_length=.5,facecolor='k')
            ax2.arrow(0,0,float(FD[0]),float(FD[1]),alpha=0.5,width=.2,head_width=.51,head_length=.5,facecolor='k')
            ax2.arrow(0,0,float(F[0]),float(F[1]),alpha=0.5,width=.2,head_width=.51,head_length=.5,facecolor='r')

        s.values.pop(s.gamma)
        s.values.pop(s.v)


def my_selector(event):
    draw_arrow(event.xdata ,event.ydata)
    plt.draw()

def click(label):
    global lab_frame_toggle
    global force_toggle
    if label == "vehicle frame":
        lab_frame_toggle = not lab_frame_toggle
    else:
        force_toggle=  not force_toggle


lab_frame_toggle=False
force_toggle=False
rax = plt.axes([0.03, 0.1, 0.2, 0.15])
check = CheckButtons(rax, ('vehicle frame','show force'), (False,False))
check.on_clicked(click)
# set useblit = True on gtkagg for enhanced performance
cursor = Cursor(ax, useblit=True)
cursor.horizOn=False
cursor.vertOn=False
plt.ion()
plt.connect('button_press_event', my_selector)
#plt.connect('motion_notify_event', my_selector)
plt.show()
