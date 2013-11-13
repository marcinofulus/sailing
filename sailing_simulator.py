from __future__ import division
from visual import *
from math import sqrt
import numpy as np

print """
Modded Bruce Sherwood script 02_Newton.py
"""

h = w = 800
scene.width = w
scene.height = h
scene.x = scene.y = 0
scene.background = color.white
wide = 1.
scene.fov = 1.0
scene.range = wide
scene.userzoom = 1
#scene.userspin = 0v
scene.forward=vector(-0.0150208226310425, 0.90546222687271, -0.424160972502411)
ball = sphere(pos=(0,0,0), radius=wide/30, color=(0,0.7,0))
ball.mass = 0.2
ball.p = vector(0,0,0)
mpos = vector(0,0,0)
grid = frame()
trail = curve(frame=grid, color=ball.color)
gridd = 0.5*wide
gridr = 12*wide+gridd
gridcolor = (0.7,0.7,0.7)
for x in arange(-gridr,gridr+gridd/2,gridd):
    curve(frame=grid, pos=[(x,-gridr,0),(x,gridr,-0.1)], color=gridcolor)
for y in arange(-gridr,gridr+gridd/2,gridd):
    curve(frame=grid, pos=[(-gridr,y,0),(gridr,y,-0.1)], color=gridcolor)
dt = 0.02
Foffset = vector(0,0,-ball.radius)
Fvec = arrow(pos=ball.pos+Foffset, axis=(0,0,0), shaftwidth=wide/30., color=color.red)
pvec = arrow(pos=ball.pos, axis=(0,0,0), shaftwidth=wide/30., color=(.22,.33,.64))
pvec_VMG = arrow(pos=ball.pos, axis=(0,0,0), shaftwidth=wide/30., color=(.22,1,.64))
vaxis=cylinder(pos=ball.pos,axis=(0,0,.5),radius=0.01)
pvec_APPARENT_WIND = arrow(pos=ball.pos, axis=(0,0,0), shaftwidth=wide/30., color=(.52,1,.4))

Fmouse = 1. # F mouse scale factor

#ship=convex(pos=ball.pos)

Fview = 12. # F view scale factor
pview = 12 # p view scale factor
drag = 0
F = vector(0,0,0)
count = 0

# import sailing formulas
import sailing as s
s.values={s.Cz:5.5,s.Cx:1,s.CHx:0.4,s.CHx2:0.0,s.v_w:0.1}
force=s.lambdify((s.gamma,s.v),(s.force1- s.force2 ).subs(s.values))
u=s.lambdify( (s.gamma,s.v),s.u.subs(s.values))
def force_robust(x,v):
    x1=np.abs(np.fmod(x,2*np.pi))
    if x1>=0 and x1 <np.pi:
        f=force(x1,v)
    else:
        f=force(2*np.pi-x1,v)
    return (np.sign(f)+1)/2. * f
gamma=1.
CHx=1.
while 1:
    rate(100)
    if scene.mouse.events: # check for mouse events
        m = scene.mouse.getevent() # get the mouse info
        if m.drag == 'left' or m.press == 'left':
            drag = 1
        elif m.drop == 'left':
            drag = 0
    if drag:
        F = Fmouse*(scene.mouse.pos-scene.center)
        gamma =  arctan2(F[1],F[0])
        F[2]=0
#    Fvec.axis = Fview*F

    v=ball.p/ball.mass
    vmod=sqrt(v[0]*v[0]+v[1]*v[1])

    fv=force_robust(gamma,vmod)
    F[0],F[1] = fv*cos(gamma),fv*sin(gamma)
    if vmod>0.001:
        friction=1.0
    else:
        friction=0.0
    vmod =  vmod + (fv - CHx*friction*vmod**2)*dt/ball.mass 
    print "V=", vmod, fv,-CHx*friction*vmod**2
    ball.p[0],ball.p[1] = ball.mass*vmod*cos(gamma),ball.mass*vmod*sin(gamma) 
    #ball.p + F*dt
    ball.pos = ball.pos + (ball.p/ball.mass)*dt

    scene.center = ball.pos # follow the ball, keeping it in the center
    trail.append(pos=ball.pos)
    if abs(ball.pos.x) >= gridr:
        ball.p.x = -ball.p.x
    if abs(ball.pos.y) >= gridr:
        ball.p.y = -ball.p.y
    Fvec.pos = ball.pos
    Fvec.pos[2]=0.05
    Fvec.axis = Fview*F
    pvec.pos = ball.pos
    pvec.axis = pview*ball.p
    pvec_VMG.pos = ball.pos
    pvec_VMG.pos[2]=0.1
    pvec_VMG.axis = pview*ball.p
    pvec_VMG.axis[1] = 0
    vaxis.pos=ball.pos
    pvec_APPARENT_WIND.pos = ball.pos
    pvec_APPARENT_WIND.pos[2]=0.1

    pvec_APPARENT_WIND.axis=vector(    u(gamma,vmod)[0,0],u(gamma,vmod)[1,0],0)


    
