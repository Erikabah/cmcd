
import numpy as np
import matplotlib.pyplot as plt

#para o vetor tempo
t = np.arange(0,5,0.01)

pho = 998.2 #Water density 998.2 kg/m³ - 1.025
mi = 1 #viscosidade
v = mi/pho #escoamento

D = 43.2 #diametro do modelo 1:30
L = 481.75 # 1:30
A = 15 #amplitude - da serie temporal sqrt(2)*std(signal)
T = 0.5 #periodo de oscilação- da serie temporal
w = 2*np.pi/T

KC = 2*np.pi*A/D    #######
Re = A*w*D/v        #######
'''
equação de Morison
"força em linha em um corpo em fluxo oscilatório"
A equação de Morison contém dois coeficientes hidrodinâmicos empíricos - um
coeficiente de inércia e um coeficiente de arrasto - que são determinados a
partir de dados experimentais.Conforme mostrado pela análise dimensional e em
experimentos de Sarpkaya, esses coeficientes dependem em geral do número de
Keulegan-Carpenter, número de Reynolds e rugosidade da superfície.
'''
#Ca = Cm - 1
Ca = 3 #"depende do KC e de Re"

V = 1 #volume do corpo submerso
dxx = 1 #aceleração imposta

Cd = 2 #"depende do KC e de Re"
dx = 1 #velocidade imposta
mdx = abs(dx)

#carga hidr. atuando no modelo que vai ser decomposta em arrasto e inércia
#F = -Ca*pho*V*dxx - Cd*pho*S*dx*mdx/2

#coeficientes inérciais
#Cm = "Ca" = Fi / (0.5*m*dxx) coef inércial 1:9
#Cm = "Ca" = Fi / (0.5*pho*L*(0.25*np.pi*D**2)*(A*w**2)) 1:30
#coeficientes de arrasto
S1 = D*L #área de referência normal
#Cd = Fd / (0.5*pho*S1*dx*mdx) 1:9
#Cd = Fd/ (0.5*pho*S1*(w*A)**2) 1:30
S2 = np.pi*D*L #área de referência axial
#Cd = Fd / (0.5*pho*S2*dx*mdx)  1:9
#Cd = Fd / (0.5*pho*S1*(w*A)**2)
# o KC muda para/considerando porosidade

a = -Ca*pho*V
d = -Cd*pho*S1/2

t0 = 0  #tempo inicial
tn = 6  #tempo final
h = 0.001 #passo - "dt"

def solver_M (a=2, d=1, #a - dxx e d - dx*|dx|
               x0=0.1 , V0=5, #condições iniciais vir da stemp
               t=  np.arange(t0,tn,h), #vetor tempo vir da série temp
               F0=5, w=0): #parametros da força externa vir da stemp
    
    X = [x0] # lista de posições - solução númerica "eixo y"
    V = [V0]# lista p/ velocidades
    F_H = F0*(np.cos(w*t)) # equação externa - F_H = F_CM + F_SM - F_I(F_I=m*dxx)
    xi = x0 #posições xi
    vi = V0 #velocidades vi
    for it in range(len(t)-1):
        #runge kutta
        Fi = F_H[it]
        
        kv1 = vi
        ka1 = ( -d*vi*abs(vi) + Fi)/a
        
        kv2 = vi + ka1*h/2
        ka2 = (-d*(kv2)*abs(kv2) + (F_H[it] + F_H[it+1])/2  )/(a)
        
        kv3 = vi + ka2*h/2
        ka3 = ( -d*(kv3)*abs(kv3) + (F_H[it] + F_H[it+1])/2 )/(a)
        
        kv4 = vi + ka3*h
        ka4 = ( -d*(kv4)*abs(kv4) + F_H[it+1] )/a

        xi+= (h/6)*(kv1 + 2*kv2 + 2*kv3 + kv4)
        vi+= (h/6)*(ka1 + 2*ka2 + 2*ka3 + ka4)

        X.append(xi) #atualizando a lista de posições
        V.append(vi) #atualizando a lista velocidades
        
    fig, ax = plt.subplots()
    ax.plot(t,X,'g',label='Posição por RK')
    plt.xlabel('tempo [s]')
    plt.ylabel('posições')
    ax.set_title('Equação Morison')
    ax.legend()    
    plt.savefig('morison3')
solver_M()



