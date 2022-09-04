import numpy as np

# Define Constants
V = 6. #Volts
R = 12.5 # Ohms
kb = 1.05e-3
ke = kb #Volts/sec
kt = 1.05e-3 #Nm/A
b = 1.38e-8 #
I = 0.005e-7
L = 0.091e-3
p = 1
T_load = 0.
delta_t = L/(R*20)
total_time = delta_t*1000


def back_emf_func(theta):
    if theta <0.:
        print('Check')
        theta = theta + 2*np.pi

    if theta >= 0.0 and theta < 2*np.pi/3.:
        return 1
    elif theta >= 2*np.pi/3. and theta < np.pi:
        return 1 - (6/np.pi)*(theta - 2*np.pi/3.)
    elif theta >= np.pi and theta < 5*np.pi/3.:
        return -1
    elif theta >= 5*np.pi/3. and theta < 12*np.pi/6.:
        return -1 + (6/np.pi)*(theta - 5*np.pi/3.)

V_seq = {'1':[V,-V/2.,0],'2':[V/2.,0.,-V/2],'3':[0.,V/2.,-V/2.],'4':[-V/2.,V/2.,0],'5':[-V/2.,0.,V/2.],'6':[0, -V/2., V/2.]}
i_phase = [[0.],[0.],[0.]]

w = [0]
back_emf_a = [0.0]
theta_m = [0.]
theta_e = [0.]
theta_e_2pi_list = [0.]
torque_list =[0.]
w_rpm = [0.]

import math
print(kt*(V/R), V/kb)

def back_emf_phase(theta,w_inst,ke):
    return (ke/2)*w_inst*back_emf_func(theta),(ke/2)*w_inst*back_emf_func(theta-2*np.pi/3.),(ke/2)*w_inst*back_emf_func(theta-4*np.pi/3.)

for i in range(1,200000):
    #Electrical Angle = P*Mechanical Angle
    theta_e_2pi = (theta_e[i-1])%(2*math.pi)
    theta_m_2pi = (theta_m[i-1])%(2*math.pi)
    #print(theta_m[i-1])

################### 0 -60 #########################
    if theta_e_2pi >= 0.0 and theta_e_2pi < np.pi/3. and i_phase[1][i-1] <=0 and i_phase[2][i-1]<=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = V
        V_bc = 0.5*(-V + e_a + e_b - 2*e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 0.0 and theta_e_2pi < np.pi/3. and i_phase[1][i-1] <=0 and i_phase[2][i-1]>0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = V
        V_bc = 0.

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 0.0 and theta_e_2pi < np.pi/3. and i_phase[1][i-1]>0 and i_phase[2][i-1]>=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = V
        V_bc = 0.5*(-V + e_a + e_b -2*e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 0.0 and theta_e_2pi <= np.pi/3. and i_phase[1][i-1] >0 and i_phase[2][i-1]<0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = V
        V_bc = -V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

################### 60 - 120 #########################
    elif theta_e_2pi >= np.pi/3. and theta_e_2pi < 2*np.pi/3. and i_phase[0][i-1] >=0 and i_phase[1][i-1]>=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)

        V_ab = 0.5*(V + e_a - 2*e_b +e_c)
        V_bc = 0.5*(V - e_a + 2*e_b - e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= np.pi/3. and theta_e_2pi < 2*np.pi/3. and i_phase[0][i-1] >=0 and i_phase[1][i-1]<0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.
        V_bc = V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= np.pi/3. and theta_e_2pi < 2*np.pi/3. and i_phase[0][i-1]<0 and i_phase[1][i-1]<=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.5*(V + e_a - 2*e_b +e_c)
        V_bc = 0.5*(V - e_a + 2*e_b -e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])
    elif theta_e_2pi >= np.pi/3. and theta_e_2pi <= 2*np.pi/3. and i_phase[0][i-1] <0 and i_phase[1][i-1]>0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = V
        V_bc = 0.

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

################### 120 - 180 #########################s
    elif theta_e_2pi >= 2*np.pi/3. and theta_e_2pi < 3*np.pi/3. and i_phase[0][i-1] <=0 and i_phase[2][i-1]<=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)

        V_ab = 0.5*(-V + 2*e_a - e_b - e_c)
        V_bc = V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 2*np.pi/3. and theta_e_2pi < 3*np.pi/3. and i_phase[0][i-1] >0 and i_phase[2][i-1]<=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = -V
        V_bc = V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 2*np.pi/3. and theta_e_2pi < 3*np.pi/3. and i_phase[0][i-1]>=0 and i_phase[2][i-1]>0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.5*(-V+2*e_a - e_b - e_c)
        V_bc = V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 2*np.pi/3. and theta_e_2pi <= 3*np.pi/3. and i_phase[0][i-1] <0 and i_phase[2][i-1]>0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.
        V_bc = V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

################### 180 - 240 #########################
    elif theta_e_2pi >= 3*np.pi/3. and theta_e_2pi < 4*np.pi/3. and i_phase[1][i-1] >=0 and i_phase[2][i-1]>=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)

        V_ab =-V
        V_bc = 0.5*(V +e_a + e_b -2*e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 3*np.pi/3. and theta_e_2pi < 4*np.pi/3. and i_phase[1][i-1] >=0 and i_phase[2][i-1]<0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = -V
        V_bc = 0.

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 3*np.pi/3. and theta_e_2pi < 4*np.pi/3. and i_phase[1][i-1]<0 and i_phase[2][i-1]<=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = -V
        V_bc = 0.5*(V + e_a + e_b - 2*e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 3*np.pi/3. and theta_e_2pi <= 4*np.pi/3. and i_phase[1][i-1] <0 and i_phase[2][i-1]>0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = -V
        V_bc = V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

################### 240 - 300 #########################
    elif theta_e_2pi >= 4*np.pi/3. and theta_e_2pi < 5*np.pi/3. and i_phase[0][i-1] <=0 and i_phase[1][i-1] <=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)

        V_ab = 0.5*(-V +e_a - 2*e_b +e_c)
        V_bc = 0.5*(-V -e_a + 2*e_b -e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 4*np.pi/3. and theta_e_2pi < 5*np.pi/3. and i_phase[0][i-1] <=0 and i_phase[1][i-1]>0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.
        V_bc = -V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 4*np.pi/3. and theta_e_2pi < 5*np.pi/3. and i_phase[0][i-1]>0 and i_phase[1][i-1]>=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.5*(-V + e_a - 2*e_b + e_c)
        V_bc = 0.5*(-V - e_a + 2*e_b - e_c)

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 4*np.pi/3. and theta_e_2pi <= 5*np.pi/3. and i_phase[0][i-1] >0 and i_phase[1][i-1]<0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = -V
        V_bc = 0.

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

################### 300 - 360 #########################
    elif theta_e_2pi >= 5*np.pi/3. and theta_e_2pi < 6*np.pi/3. and i_phase[0][i-1] >=0 and i_phase[2][i-1] >=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)

        V_ab = 0.5*(V + 2*e_a - e_b - e_c)
        V_bc = -V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 5*np.pi/3. and theta_e_2pi < 6*np.pi/3. and i_phase[0][i-1] <0 and i_phase[2][i-1]>=0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = V
        V_bc = -V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 5*np.pi/3. and theta_e_2pi < 6*np.pi/3. and i_phase[0][i-1]<=0 and i_phase[2][i-1]<0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.5*(V + 2*e_a - e_b - e_c)
        V_bc = -V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    elif theta_e_2pi >= 5*np.pi/3. and theta_e_2pi <= 6*np.pi/3. and i_phase[0][i-1] >0 and i_phase[2][i-1]<0:
        e_a,e_b,e_c = back_emf_phase(theta_e_2pi,w[i-1],ke)
        V_ab = 0.
        V_bc = -V

        i_phase[0].append((delta_t/(3*L))*(2*V_ab + V_bc - 3*R*i_phase[0][i-1] - (2*e_a - e_b - e_c)) + i_phase[0][i-1])
        i_phase[1].append((delta_t/(3*L))*(-V_ab + V_bc - 3*R*i_phase[1][i-1] - (-e_a + 2*e_b - e_c)) + i_phase[1][i-1])
        i_phase[2].append(-i_phase[0][i]-i_phase[1][i])

    torque_a = (kt*i_phase[0][i-1]*back_emf_func(theta_e_2pi))
    torque_b = (kt*i_phase[1][i-1]*back_emf_func(theta_e_2pi- 2*np.pi/3.))
    torque_c = (kt*i_phase[2][i-1]*back_emf_func(theta_e_2pi- 4*np.pi/3.))

    torque = 1*(torque_a + torque_b + torque_c)

    if i == 120000:
        T_load = 0.23e-3

    w.append((delta_t/I)*(torque -T_load - b*w[i-1]) + w[i-1])
    if w[i]<= 0:
        w[i] = 0.
    elif w[i] >= V/kb:
        w[i] = V/kb
    torque_list.append(torque*1000)
    theta_m.append(delta_t*(w[i-1]) + theta_m[i-1])
    theta_e.append(theta_m[i]*p)
    theta_e_2pi_list.append(theta_e_2pi)
    w_rpm.append(w[i]*60/(2*np.pi))    #print(w[i])

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(range(len(i_phase[1])), i_phase[1])
#ax1.set_ylim([0,50000])
plt.show()
