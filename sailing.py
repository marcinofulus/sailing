from __future__ import division
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
x, y, z = symbols('x,y,z')

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
# note that this is valid for gamma=0..pi
up=Matrix([-v*sin(gamma),v*cos(gamma)+v_w])
force1=trigsimp( (up.normalized().dot(ev))*u.norm()**2*Cz )
force2=trigsimp(-u.normalized().dot(ev)*u.norm()**2*Cx)
simpleeq =  factor (  ( (force1-force2)/u.norm() ) ) # without vehicle drag (CHx)
fulleq = factor (  (force1-force2)/u.norm() ) - CHx*v**2/u.norm()

## rotor blades (not clear with 3 RF)
beta=Symbol('beta')
U=Symbol('U')
UP=Symbol('UP')
U=Matrix([v_w + v*cos(gamma)*cos(beta),v*cos(gamma)*sin(beta)])
UP=-Matrix([-U[1],U[0]])

## geting forces for Newton eq. 
u1=-Matrix([vx+v_w,vy])
up1=Matrix([-u1[1],u1[0]])
F_D=Cx*u1*u1.norm()
F_L=Cz*u1.norm()**2*up1
F_tot = F_D + F_L


print simpleeq
print fulleq

r = Wild("r")
p = Wild("p")
q = Wild("q")

pattern= p+q/sqrt(r)
repl=fulleq.match( pattern )
pattern2= p**2*r-q**2
eqv=pattern2.subs(repl)


def Cx_fun(alpha):
    return alpha**4+0.15
def Cz_fun(alpha):
    return alpha



def Funv(values):
    """ Function that solves equilibrium condition
    for given set of parameters
    it uses both 4th order equation for root finding
    and checks if solution are also solving the force equation
    """
    # calculate all complex roots of eqv


    x=np.array(map(complex,N( eqv.subs(values)).as_poly(v).nroots()))

    # extract only positive and real roots
    xr=x.round(decimals=5)
    sorted=np.sort(np.real(x[np.logical_and(xr.imag==0,xr.real>=0)]))
    # check if root of polynomial eqv fullfill original equation
    fulleq_chk=np.array([N(fulleq.subs(values).subs({v:sorted[i]})) for i in range(0,sorted.size)],dtype=np.double).round(decimals=5)
    sorted_fulleq= sorted[(np.abs(fulleq_chk)<1e-5).nonzero()]
    # silently assume one or zero physical solution
    if sorted_fulleq.size > 0:
        return sorted_fulleq[0] 
    else:
        return 0.0



def AAW(xx,yy):
    return xx[yy>0]-np.arctan2(yy[yy>0]*np.sin(xx[yy>0]),yy[yy>0]*np.cos(xx[yy>0])+1.0)

def ROT(x):
    return Matrix([[cos(x),-sin(x)],[sin(x),cos(x)]])

def Funv_gamma(x):
    """ Making Funv function of gamma
    """
    values[gamma]=x
    return Funv(values)


xx=np.linspace(0,np.pi-0.001,50)
values={Cz:5.5,Cx:1,CHx:0.5,v_w:1.0}
force=lambdify((gamma,v),(force1-force2 - CHx*v**2).subs(values))
force_simp=lambdify((gamma,v),(force1-force2).subs(values))
yy=np.array(map(Funv_gamma,xx),dtype=np.double)



if __name__ == '__main__':
    # plt.ion()
    # plt.clf()
    plt.figure(figsize=(3,3))

    ax = plt.subplot(111,polar=True)
    ax.plot(xx,yy,'b',-xx,yy,'b',xx,abs(cos(xx))*yy,"g",-xx,abs(cos(xx))*yy,"g",)
    ax.plot(xx*2,np.ones_like(xx),'r')

    ax.plot(xx[yy>0],AAW(xx,yy),'k')
    ax.plot(-xx[yy>0],AAW(xx,yy),'k')
    
#    plt.title("Sailing speeds: "+"".join([ "%s=%0.2f " %  (k,vv) for k,vv in values.items()]))

    ax.set_yticks((1,2,3))    
    plt.ylim(0,3.7)
    plt.savefig("sailing_on_ice.png",transparent=True,dpi=150)
#    plt.show()


#plt.figure(2)
#plt.plot(xx[yy>0],xx[yy>0]-np.arctan2(yy[yy>0]*np.sin(xx[yy>0]),yy[yy>0]*np.cos(xx[yy>0])+1.0))
#plt.show()


# print "Starting ANIMATION"
# for par in np.linspace(0.0,3,10):
#     values={Cz:8.0,Cx:1.0,CHx:par,v_w:1.0}
#     yy=np.array(map(lambda gval:Funv(gval,values),xx),dtype=np.double)
#     plt.ion()
#     plt.clf()
#     plt.polar(xx,yy,'b',-xx,yy,'b',xx,abs(cos(xx))*yy,"g",-xx,abs(cos(xx))*yy,"g",)
#     plt.polar(xx*2,np.ones_like(xx),'r')
#     plt.title("Sailing speeds: "+"".join([ "%s=%0.2f " %  (k,vv) for k,vv in values.items()]))
#     plt.draw()
