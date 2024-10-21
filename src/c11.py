import numpy as np
import matplotlib.pyplot as plt

from utils.settings import Settings
from utils.optimization import Optimization
from utils.simulation import Simulation

param, data = Settings().benchmark(Num_T=10000)
sol = Optimization().opt_param(param, theta_E=25)
traj = Simulation.simulate(param, sol, data)

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['q_F'][0, :])
plt.plot(range(data['Num_T'] + 1), traj['q_F'][1, :])
plt.xlabel('Time')
plt.ylabel('q_F')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['q_B'][0, :])
plt.plot(range(data['Num_T'] + 1), traj['q_B'][1, :])
plt.plot(range(data['Num_T'] + 1), traj['q_B'][2, :])
plt.xlabel('Time')
plt.ylabel('q_B')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['e_S'][0, :])
plt.plot(range(data['Num_T'] + 1), traj['e_S'][1, :])
plt.plot(range(data['Num_T'] + 1), traj['e_S'][2, :])
plt.xlabel('Time')
plt.ylabel('e_S')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['tau_H'][0, :])
plt.plot(range(data['Num_T'] + 1), traj['tau_H'][1, :])
plt.plot(range(data['Num_T'] + 1), traj['tau_H'][2, :])
plt.xlabel('Time')
plt.ylabel('tau_H')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['sum_E'])
plt.plot(range(data['Num_T'] + 1), np.array(range(data['Num_T'] + 1)) * param['C_Eo'])
plt.xlabel('Time')
plt.ylabel('Emission')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['q_E'])
plt.xlabel('Time')
plt.ylabel('q_E')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T']), data['A_F'][0, :])
plt.plot(range(data['Num_T']), traj['a'][0, :])
plt.xlabel('Time')
plt.ylabel('A_F, a')

plt.show()