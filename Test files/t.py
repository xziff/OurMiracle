import math
from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

mu0 = 4 * math.pi * (10 ** (-7))
tau = 1.775
l = 3.5
wc = 14
wr = 24
delta = 0.065
Rc = 1
Rr = 2
Lcs = 0.00126
Lrs = 0.00126*2
J = 0.1
p = 2
D = 2*tau/math.pi*p
pi = math.pi

kcc = p*(4*wc*wc*tau*l*mu0)/(pi*delta*pi)
krc = p*(4*wr*wc*tau*l*mu0)/(pi*delta*pi)
krr = p*(4*wr*wr*tau*l*mu0)/(pi*delta*pi)

t_max = 4
t_del = 500000
t = np.linspace(0, t_max, t_del)

y0 = [0, 0, 0, 0, 0, 0, 0, 0]

Uc = 400
fc = 50
phic = 0

def B_delta(Ica, Icb, Icc, Ira, Irb, Irc, x, phi):
    return (2*mu0/(math.pi*delta)*(wc*Ica*math.cos(math.pi/tau*x)+wc*Icb*math.cos(math.pi/tau*x-2*math.pi/3)+wc*Icc*math.cos(math.pi/tau*x+2*math.pi/3)+wr*Ira*math.cos(math.pi/tau*x-phi*p)+wr*Irb*math.cos(math.pi/tau*x-phi*p-2*math.pi/3)+wr*Irc*math.cos(math.pi/tau*x-phi*p+2*math.pi/3)))

def f(input_variable, t):
    main_det = [[-kcc*(math.sin(pi/2) - (-1)*math.sin(pi/6)) - Lcs, -kcc*(math.sin(pi/2 + 2*pi/3) - (-1)*math.sin(pi/6 - 2*pi/3)) + Lcs, -kcc*(math.sin(pi/2 - 2*pi/3) - (-1)*math.sin(pi/6 + 2*pi/3)), -krc*(math.sin(pi/2 + input_variable[7]*p) - (-1)*math.sin(pi/6 - input_variable[7]*p)), -krc*(math.sin(pi/2 + input_variable[7]*p + 2*pi/3) - (-1)*math.sin(pi/6 - input_variable[7]*p - 2*pi/3)), -krc*(math.sin(pi/2 + input_variable[7]*p - 2*pi/3) - (-1)*math.sin(pi/6 - input_variable[7]*p + 2*pi/3))],
                [-kcc*((-1)*math.sin(pi/6) - math.sin(-pi/6)), -kcc*((-1)*math.sin(pi/6 - 2*pi/3) - math.sin(-pi/6 - 2*pi/3)) - Lcs, -kcc*((-1)*math.sin(pi/6 + 2*pi/3) - math.sin(-pi/6 + 2*pi/3)) + Lcs, -krc*((-1)*math.sin(pi/6 - input_variable[7]*p) - math.sin(-pi/6 - input_variable[7]*p)), -krc*((-1)*math.sin(pi/6 - input_variable[7]*p - 2*pi/3) - math.sin(-pi/6 - input_variable[7]*p - 2*pi/3)), -krc*((-1)*math.sin(pi/6 - input_variable[7]*p + 2*pi/3) - math.sin(-pi/6 - input_variable[7]*p + 2*pi/3))],
                [-kcc*math.sin(-pi/6), -kcc*math.sin(-pi/6 - 2*pi/3), -kcc*math.sin(-pi/6 + 2*pi/3) - Lcs, -krc*math.sin(-pi/6 - input_variable[7]*p), -krc*math.sin(-pi/6 - input_variable[7]*p - 2*pi/3), -krc*math.sin(-pi/6 - input_variable[7]*p + 2*pi/3)],
                [-krc*math.sin(pi/2-input_variable[7]*p-0), -krc*math.sin(pi/2-input_variable[7]*p+2*pi/3), -krc*math.sin(pi/2-input_variable[7]*p-2*pi/3), -krr*math.sin(pi/2-0) - Lrs, -krr*math.sin(pi/2+2*pi/3), -krr*math.sin(pi/2-2*pi/3)],
    			[-krc*(-1)*math.sin(pi/6+input_variable[7]*p-0), -krc*(-1)*math.sin(pi/6+input_variable[7]*p-2*pi/3), -krc*(-1)*math.sin(pi/6+input_variable[7]*p+2*pi/3), -krr*(-1)*math.sin(pi/6+0), -krr*(-1)*math.sin(pi/6-2*pi/3) - Lrs, -krr*(-1)*math.sin(pi/6+2*pi/3)],
    			[-krc*math.sin(-pi/6+input_variable[7]*p-0), -krc*math.sin(-pi/6+input_variable[7]*p-2*pi/3), -krc*math.sin(-pi/6+input_variable[7]*p+2*pi/3), -krr*math.sin(-pi/6+0), -krr*math.sin(-pi/6-2*pi/3), -krr*math.sin(-pi/6+2*pi/3) - Lrs]
               ]

    own_matrix = [input_variable[0]*Rc + Uc*(math.sin(2*math.pi*fc*t + phic) - math.sin(2*math.pi*fc*t + phic - 2*pi/3)) - input_variable[1]*Rc + krc*p*input_variable[6]*(input_variable[3]*math.cos(pi/2 + input_variable[7]*p) + input_variable[4]*math.cos(pi/2 + input_variable[7]*p + 2*pi/3) + input_variable[5]*math.cos(pi/2 + input_variable[7]*p - 2*pi/3) + (-1)*input_variable[3]*math.cos(pi/6 - input_variable[7]*p) + (-1)*input_variable[4]*math.cos(pi/6 - input_variable[7]*p - 2*pi/3) + (-1)*input_variable[5]*math.cos(pi/6 - input_variable[7]*p + 2*pi/3)),
                input_variable[1]*Rc + Uc*(math.sin(2*math.pi*fc*t + phic - 2*pi/3) - math.sin(2*math.pi*fc*t + phic + 2*pi/3)) - input_variable[2]*Rc + krc*p*input_variable[6]*(input_variable[3]*math.cos(pi/6 - input_variable[7]*p) + input_variable[4]*math.cos(pi/6 - input_variable[7]*p - 2*pi/3) + input_variable[5]*math.cos(pi/6 - input_variable[7]*p + 2*pi/3) + input_variable[3]*math.cos(-pi/6 - input_variable[7]*p) + input_variable[4]*math.cos(-pi/6 - input_variable[7]*p - 2*pi/3) + input_variable[5]*math.cos(-pi/6 - input_variable[7]*p + 2*pi/3)),
                input_variable[2]*Rc + Uc*math.sin(2*math.pi*fc*t + phic + 2*pi/3) - krc*p*input_variable[6]*(input_variable[3]*math.cos(-pi/6 - input_variable[7]*p) + input_variable[4]*math.cos(-pi/6 - input_variable[7]*p - 2*pi/3) + input_variable[5]*math.cos(-pi/6 - input_variable[7]*p + 2*pi/3)),
                input_variable[3]*Rr-input_variable[6]*krc*p*(input_variable[0]*math.cos(pi/2-input_variable[7]*p)+input_variable[1]*math.cos(pi/2-input_variable[7]*p+2*pi/3)+input_variable[2]*math.cos(pi/2-input_variable[7]*p-2*pi/3)),
                input_variable[4]*Rr+input_variable[6]*krc*p*(-1)*(input_variable[0]*math.cos(pi/6+input_variable[7]*p)+input_variable[1]*math.cos(pi/6+input_variable[7]*p-2*pi/3)+input_variable[2]*math.cos(pi/6+input_variable[7]*p+2*pi/3)),
                input_variable[5]*Rr+input_variable[6]*krc*p*(input_variable[0]*math.cos(-pi/6+input_variable[7]*p)+input_variable[1]*math.cos(-pi/6+input_variable[7]*p-2*pi/3)+input_variable[2]*math.cos(-pi/6+input_variable[7]*p+2*pi/3))
                ]
    
    Melmag = D*l*wr*(input_variable[3]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], tau/pi*input_variable[7]*p-tau/2, input_variable[7])+input_variable[4]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], tau/pi*input_variable[7]*p+tau/6, input_variable[7])+input_variable[5]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], tau/pi*input_variable[7]*p-7*tau/6, input_variable[7]))

    derw = (-0*math.tanh(input_variable[6]) - p*Melmag)/J


    solve_matrix = np.linalg.solve(main_det, own_matrix)
    print(t/t_max*100)
    return [solve_matrix[0],
    solve_matrix[1],
    solve_matrix[2],
    solve_matrix[3],
    solve_matrix[4],
    solve_matrix[5],
    derw,
    input_variable[6]]

ww = odeint(f, y0, t)

m_f = []

for i in range(len(t)):
    m_f.append(ww[:, 6][i]/2/pi)

plt.subplot(3, 1, 1)
plt.plot(t, ww[:, 0], linewidth=1, color='red')
plt.xlabel('Время, с', fontsize=12, color='black')
plt.ylabel('Ток статора, А', fontsize=12, color='black')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, ww[:, 3], linewidth=1, color='red')
plt.xlabel('Время, с', fontsize=12, color='black')
plt.ylabel('Ток ротора, А', fontsize=12, color='black')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t, m_f, linewidth=1, color='red')
plt.xlabel('Время, с', fontsize=12, color='black')
plt.ylabel('Частота, Гц', fontsize=12, color='black')
plt.grid(True)
plt.show()