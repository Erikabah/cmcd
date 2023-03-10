
import random
import numpy as np
from scipy import optimize, signal
from sympy import symbols, Eq, solve

L = .45 #
D = .04 #diametro?
rho = 998 #
A = 100 #amplitude?
T = 2
w = 2*np.pi/T
t0 = 0      #primeiro
step = .01  #incremento
tf = 30     #último
t = np.arange(t0,tf,step) #vetor tempo
x = (A/1000)*np.cos(w*t)  #vetor linha
#x.ravel()

xdot = lambda t: (-A*w/1000)*np.sin(w*t)
#xdot.ravel()

xddot = lambda t: (-A*w**2/1000)*np.cos(w*t)
#xddot.ravel()

cm_comGJR = 1
cd_comGJR = 2

cm_semGJR = .6*cm_comGJR
cd_semGJR = .2*cd_comGJR

SNR = 2

time_shift = .2
########
fig1 = 'figura/janela pra por os 3 grafs'
Hax = .27 #tamanho da figura
ax1 ='curva x(m)-limpa com A e T claros parte de cima'
ax2="curvas F(x) no meio "
ax3="ax2 sincronizado I guess embaixo"
########
F1 = -.5*rho*L*D*xdot(t)*abs(xdot(t))*(cd_comGJR-rho*np.pi*D**2)/4*L*xddot(t)*cm_comGJR
F2 = -.5*rho*L*D*xdot(t)*abs(xdot(t))*(cd_semGJR-rho*np.pi*D**2)/4*L*xddot(t)*cm_semGJR
F3 = F1-F2
NOISE = np.std(F3)/SNR
F = F1 + (np.random.rand(len(x))-.5)*NOISE

b,a = signal.butter(4,5/(100/2))
F_filt = signal.filtfilt(b,a,F)
########
ind = np.where((t>5)&(t<25))
t1 = t[ind]
# eq = CD* + (round(-.5*rho*L*D,3))*v*abs(v) + CA*(round(-rho*np.pi*D**2/4*L,3))*a


x_fit_v,x_fit_a = xdot(t1),xddot(t1)

y_fit = F_filt[ind] #lista da variável dependente F_CM depois do filtro (5<t<25)

#retorna os indices do tempo de 5-peteleco<t<25-peteleco - sincronização
ind2 = np.where((t>5-time_shift)&(t<25-time_shift))
##lista da variável dependente F_CM depois do filtro e depois da sincronização
y_fit_shift = F_filt[ind2]

def eq(x_fit, CD, CA):
    v,ac = x_fit
    return CD*(round((-.5)*rho*L*D,3)*v*abs(v)) + CA*(round(-rho*np.pi*(D**2)/(4*L),3))*ac


popt,pcov = optimize.curve_fit(eq,(x_fit_v,x_fit_a),y_fit_shift)

cd_top_fit_shift = popt[0];
cm_top_fit_shift = popt[1];
r2_top_shift = pcov;

popt,pcov = optimize.curve_fit(eq,(x_fit_v,x_fit_a),y_fit)

cd_top_fit = popt[0];
cm_top_fit = popt[1];
r2_top = pcov;



print(popt)



#ft = fittype https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html#scipy.optimize.least_squares

#ft = optimize.least_squares(eq,)


