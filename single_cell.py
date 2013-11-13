from sympy import *
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

Cx=Symbol('Cx',real=True)
CHx=Symbol('CHx',real=True)
CHx2=Symbol('CHx2',real=True) # constant drag
Cz=Symbol('Cz',real=True)
v=Symbol('v',real=True)
u=Symbol('u',real=True)
v_w=Symbol('v_w',real=True)
gamma=Symbol('gamma',real=True)
vx=Symbol('vx',real=True)
vy=Symbol('vy',real=True)

u=-Matrix([v*cos(gamma)+v_w,v*sin(gamma)])
ev=Matrix([cos(gamma),sin(gamma)])
up=Matrix([-v*sin(gamma),v*cos(gamma)+v_w])
force1=trigsimp( (up.normalized().dot(ev))*u.norm()**2*Cz )
force2=trigsimp(-u.normalized().dot(ev)*u.norm()**2*Cx)

xx=np.linspace(0,np.pi-0.001,50)
values={Cz:5.5,Cx:1,CHx:0.5,v_w:1.0}
force=lambdify((gamma,v),(force1-force2 - CHx*v**2).subs(values))
force_simp=lambdify((gamma,v),(force1-force2).subs(values))

fig = plt.figure(figsize=(3,3))
ax = plt.subplot(111,polar=True)
X = np.linspace(0, 3.14, 50)
Y = np.linspace(0, 3.7, 50)

Z=np.array([[force(g,h) for g in X] for h in Y])
X, Y = np.meshgrid(X, Y)
maximum=Z.max()
surf = ax.contourf(X, Y, Z, np.linspace(0, maximum, 20), rstride=1, cstride=1, cmap=cm.jet,linewidth=0, antialiased=False)
surf = ax.contourf(-X, Y, Z, np.linspace(0, maximum, 20), rstride=1, cstride=1, cmap=cm.jet,linewidth=0, antialiased=False)
ax.set_yticks((1,2,3))
plt.ylim(0,3.7)
plt.show()

