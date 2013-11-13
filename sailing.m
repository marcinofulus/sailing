clear all;
global v_w=1.;
global gama=(pi/2*0.3); 

global CHx=.0;# hydrodynamic drag coefficient (vehicle drag)
global Cx=1; # aerodynamic drag coefficient
global Cz=2; # aerodynamic lift coefficient

## Assumed constant Cz/Cx ratio  
## additional parameter - angle of attack 
## for real boat should be incorporated

function force = Fz(v)
	global v_w gama Cx Cz;
	force=0;
	force=Cz.*sqrt(v.^2+v_w.^2+2.*v.*v_w.*cos(gama)).*v_w.*sin(gama);
endfunction

function force = Ftot(v)
	global v_w gama Cx Cz CHx;
	force=0;
	force=Cz.*sqrt(v.^2+v_w.^2+2.*v.*v_w.*cos(gama)).*v_w.*sin(gama) \
      - Cx.*sqrt(v.^2+v_w.^2+2.*v.*v_w.*cos(gama)).*(v+v_w.*cos(gama)) \
  	  - CHx.*v.^2;
endfunction

# Angle of Apparent Wind 
function y = AAW(v,gam)
	global  v_w;	
	y=gam-atan2( v.*sin(gam),v.*cos(gam)+v_w);
endfunction

# Solving and Visualisation  procedure
function  [ vboat,gamas]=run(x)

global v_w gama CHx Cx Cz;
# argument can be suited
Cz=x;

Ngama=200;
i=1;
gamas=linspace(1e-4,1*pi-1e-4,Ngama);  
for gama=gamas 
  if (gama>atan(Cx/Cz))
		vboat(i)=fsolve(@Ftot,Cz);
	else
		vboat(i)=0;
	end
	i++; 
end;

# calculate speed up the wind
upwind_vboat= cos(gamas).*vboat;
upwindidx=find( upwind_vboat>0 );
downwindidx=find( upwind_vboat<0 );
[v_upwind_max,v_upwind_imax]=max( upwind_vboat);
[v_max,v_imax]=max( vboat);

# calculate  angle
y2=gamas(find (vboat>0)(1));

figure(1)
        plot(gamas./pi*180,vboat,"b-;V;",\
	     gamas./pi*180,AAW(vboat,gamas),"k-",\
	     gamas(upwindidx)./pi*180,upwind_vboat(upwindidx),"g-;up;",\
	     gamas(downwindidx)./pi*180,upwind_vboat(downwindidx),"r-;down;" )
xlabel("gamma")
print("Sailing_speeds.png","-S300,200")
figure(2)
	polar(gamas(upwindidx),upwind_vboat(upwindidx),"g-")
hold on;
	polar(-gamas(upwindidx),upwind_vboat(upwindidx),"g-"')

	polar(gamas(downwindidx),-upwind_vboat(downwindidx),"r-")
	polar(-gamas(downwindidx),-upwind_vboat(downwindidx),"r-"')


	polar( gamas,vboat);
	polar( -gamas,vboat);

	plot([0,1],[0,tan(y2)])
	plot([0,1],[0,-tan(y2)])

	plot([0,1.2*v_upwind_max*cos(gamas(v_upwind_imax))],[0,1.2*v_upwind_max*sin(gamas(v_upwind_imax))])
	plot([0,1.2*v_max*cos(gamas(v_imax))       ],1.2*v_max*[0,1.2*v_max*sin(gamas(v_imax))])
	plot(cos(0:0.1:2*pi),sin(0:0.1:2*pi),"k-")

hold off
xlabel("Vx")
ylabel("Vy")
print("Sailing_polar.png","-F:24","-S320,240")
endfunction

# here are conditions 
CHx=1.2;
Cx=1.0;
[vboat,gamas]=run(10.0); # Cz=10
