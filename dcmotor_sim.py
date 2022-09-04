# Libraries
import numpy as np
import matplotlib.pyplot as plt

# Functions

def check_params(V,kb,kt,R,L):
    print('No Load Response: {}'.format(V/kb))
    print('Stall Torque: {}'.format(kt*(V/R)))
    print('Time Constant: {:2f}'.format(L/R))

def dc_sim(load, N, n, delta_t, V, L, R, kb, kt, I_motor, I_load):
    i_phase = [0.]
    w = [0.]
    theta = [0.]
    theta_output = [0.]
    for i in range(1,50000):
        # Ext Load
        if i == 25000:
            load = 0.23e-3

        # Current 
        i_phase.append((delta_t/L)*(V - i_phase[i-1]*R - kb*w[i-1]) + i_phase[i-1])
        if i_phase[i]>= V/R:
            i_phase[i] = V/R
        elif i_phase[i]<=0:
            i_phase[i] = 0.

        # Angular Speed
        w.append((delta_t/(I_motor + I_load/(N**2))*(kt*i_phase[i-1] - load/(n*N) - b*w[i-1]) + w[i-1]))
        if w[i] <=0:
            w[i] = 0.
        elif w[i] >= V/kb:
            w[i] = V/kb

        # Angular Position    
        theta.append((delta_t)*w[i-1] +theta[i-1])
        theta_output.append(theta[i]*N)

    return i_phase, w, theta_output

def plot_graph(load, N, n, delta_t, V, L, R, kb, kt, I_motor, I_load):
    i_phase, w, theta_output = dc_sim(load, N, n, delta_t, V, L, R, kb, kt, I_motor, I_load)
    time  = delta_t*np.array(range(len(i_phase)))
    fig,ax = plt.subplots(2,2)
    ax[0,0].plot(time, i_phase)
    ax[0,0].set_xlabel('Time (Seconds)')
    ax[0,0].set_ylabel('Current (A)')

    ax[1,0].plot(time, (60./(2*np.pi))*np.array(w))
    ax[1,0].set_xlabel('Time (Seconds)')
    ax[1,0].set_ylabel('Angular Speed (rpm)')

    ax[0,1].plot(time, theta_output)
    ax[0,1].set_xlabel('Time (Seconds)')
    ax[0,1].set_ylabel('Angular Position (rad)')

    ax[1,1].plot((60./(2*np.pi))*np.array(w), 1000*kt*np.array(i_phase))
    ax[1,1].set_xlabel('Angular Speed (rpm)')
    ax[1,1].set_ylabel('Torque (mNm)')

    plt.show()

def controller(kp,ki,kd,error):
    output = kp*error 

if __name__ == '__main__':
    # Parameters
    V = 6.
    R = 12.50
    L = 0.091e-3
    b = 1.38e-8
    kb = 1.05e-3
    kt = 1.05e-3
    I_motor = 0.005e-7
    I_load = 0.
    N = 1
    n = 1
    delta_t = L/(R*4)
    T_load = 0.

    check_params(V,kb,kt,R,L)
    plot_graph(T_load, N, n, delta_t, V, L, R, kb, kt, I_motor, I_load)
