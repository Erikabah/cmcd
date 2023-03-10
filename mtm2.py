#H:\ic-loc-2022\ss7\commodelo\meutestemodelo.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal,optimize

arq = open("mtm2.txt", "w")
L = .45 #altura?
D = .04 #diametro?
rho = 998 #
A = 100 #amplitude?
T = 2 #período
w = 2*np.pi/T
t0 = 0      #primeiro tempo
step = .01  #incremento tempo
tf = 30     #último tempo
t = np.arange(t0,tf,step) #vetor tempo

arq.write("Arq2\n")
arq.write("entre 0 e 1 com step de 0.02\n")
arq.write("Paramêtros:\tL=0.45\tD=0.04\trho=998\nA=100\tT=2\n")

x = lambda t: (A/1000)*np.cos(w*t)  #vetor linha - posição

xdot = lambda t: (-A*w/1000)*np.sin(w*t) # função de velocidade
xdot_check = xdot(t) #vetor velocidade
xddot = lambda t: (-A*w**2/1000)*np.cos(w*t) #função de aceleração
xddot_check = xddot(t) #vetor aceleração

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t, xdot_check)
ax1.set_title('xdot')
ax1.axis([0, 30, -0.5, 0.5])
ax1.grid(which= 'both', axis = 'both')

ax2.plot(t, xddot(t))
ax2.set_title('xddot')
ax2.axis([0, 30, -1, 1])
ax2.set_xlabel('Time [seconds]')
ax2.grid()
plt.tight_layout()
plt.show()

cm_comGJR = 1 #CA CM
cd_comGJR = 2 #CD CM
arq.writelines(['Entrada de CM e CD COM GJR:\n',"CM="+str(cm_comGJR),"\tCD="+str(cd_comGJR)])
cm_semGJR = .6*cm_comGJR #CA SM
cd_semGJR = .2*cd_comGJR #CD SM
arq.writelines(['\nEntrada de CM e CD SEM GJR:\n',"CM="+str(cm_semGJR),"\tCD="+str(cd_semGJR)])
SNR = 2

######## Parte do gráfico
#fig1, ax = plt.subplots(3,1, figsize=(0.27), layout ='constrained')
#ax[0] :'curva x(m)-limpa com A e T claros parte de cima'
#ax[1]:"curvas F(x) no meio "
#ax[2]:"ax2 sincronizado I guess embaixo"
########
arq.write("\n\n\tt_shift\tCD_shift\tCM_shift\tR²_shift")
arq.write("\tCD\tCM\tR²\n")
    #F1 = F_CM
F1 = -.5*rho*L*D*xdot(t)*abs(xdot(t))*cd_comGJR-rho*np.pi*(D**2)/4*L*xddot(t)*cm_comGJR
    #F2 = F_SM
F2 = -.5*rho*L*D*xdot(t)*abs(xdot(t))*cd_semGJR-rho*np.pi*(D**2)/4*L*xddot(t)*cm_semGJR
F3 = F1-F2 #F3 = F_H Carga hidro atuando no modelo GJR
NOISE = np.std(F3)/SNR #ruído de F_H

#coeficientes do filtro:
cf1,cf2 = signal.butter(4,0.1) 
    
#retorna os indices do tempo entre 5 e 25 - "corta" o começo e o final do sinal
ind = np.where((t>5)&(t<25)) 
t1 = t[ind] # 5 < t < 25
x_fit_v , x_fit_a = xdot(t1) , xddot(t1)

def eq(x_fit, CD, CA):
    v,ac = x_fit
    return CD*(round(-.5*rho*L*D,3)*v*abs(v)) + CA*(round(-rho*np.pi*(D**2)/(4*L),3))*ac

tentativas = np.arange(0,1,0.02)
tentativas = [0.2]
n = 1
for i in tentativas:
    
    F = F1 + (np.random.rand(len(x(t)))-.5)*NOISE #F_CM - com ruído
    F_filt = signal.filtfilt(cf1,cf2,F) #F depois do filtro
    
    #popt:{c11.CD, c11.CA ou c22.CD, c22.CA}
    #pcov: gof11.rsquare ou gof22.rsquare
    
###### Coeficientes Sem shift ######
    y_fit = F_filt[ind] #variável dependente F_CM depois do filtro (5<t<25)
    popt,pcov = optimize.curve_fit(eq,(x_fit_v,x_fit_a),y_fit)
    cd_top_fit = popt[0];
    cm_top_fit = popt[1];
    residuals = y_fit- eq((x_fit_v,x_fit_a), *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_fit-np.mean(y_fit))**2)
    r_squared = 1 - (ss_res / ss_tot)
    r2_top = r_squared;
    #print("\nSem shift")
    #print("CD=",popt[0],"\tCM=",popt[1])
    #print("R²=",r2_top)
    
###### Coeficientes Com shift ######
    time_shift = i #"peteleco"
    #retorna os indices do tempo de 5-peteleco<t<25-peteleco - "sincronização"
    ind2 = np.where((t>(5-time_shift))&(t<(25-time_shift)))
    #variável dependente F_CM depois do filtro e depois da sincronização
    y_fit_shift = F_filt[ind2]
    y_fit_shift = y_fit_shift[:1999]

    cd_top_fit_shift = popt[0];
    cm_top_fit_shift = popt[1];
    
    #residual sum of squares (ss_tot)
    residuals = y_fit_shift- eq((x_fit_v,x_fit_a), *popt)
    ss_res = np.sum(residuals**2)
    
    #total sum of squares (ss_tot) with
    ss_tot = np.sum((y_fit_shift-np.mean(y_fit_shift))**2)
    
    #the r_squared-value with,
    r_squared = 1 - (ss_res / ss_tot)
    r2_top_shift = r_squared;
    #print("Com shift")
    #print("CD=",popt[0],"\tCM=",popt[1])
    #print("R²=",r2_top_shift)
    
    arq.writelines([str(n),"\t",str("%.4f" % i),"\t",
                    str("%.4f" % cd_top_fit_shift),"\t",
                    str("%.4f" % cm_top_fit_shift),"\t",
                    str("%.4f" % r2_top_shift)])
    arq.writelines(["\t",str("%.4f" % cd_top_fit),
                    "\t",str("%.4f" % cm_top_fit),
                    "\t",str("%.4f" % r2_top),"\n"])
    #savefigure
    n+=1
    
#forma da equação em str
eq_str = ['CD*'+str(round(-.5*rho*L*D,3))+'*v*abs(v) +CA*'
          +str(round(-rho*np.pi*D**2/(4*L),3))+'*a']

arq.close()
'''

F_fit(:,1) = -.5*rho*L*D.*x_fit(:,1).*abs(x_fit(:,1))*cd_top_fit - rho*pi*D^2/4*L*x_fit(:,2)*cm_top_fit;
F_fit_shift(:,1) = -.5*rho*L*D.*x_fit(:,1).*abs(x_fit(:,1))*cd_top_fit_shift - rho*pi*D^2/4*L*x_fit(:,2)*cm_top_fit_shift;

'''



