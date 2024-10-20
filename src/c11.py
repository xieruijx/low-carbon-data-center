import numpy as np
import matplotlib.pyplot as plt

from utils.settings import Settings
from utils.optimization import Optimization
from utils.simulation import Simulation

param, data = Settings().benchmark(Num_T=100)
sol = Optimization().opt_param(param, theta_E=26)
traj = Simulation.simulate(param, sol, data)

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['q_F'][0, :])
plt.xlabel('Time')
plt.ylabel('q_F 0')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['q_B'][0, :])
plt.xlabel('Time')
plt.ylabel('q_B 0')

plt.figure(figsize=(8, 6))
plt.plot(range(data['Num_T'] + 1), traj['e_S'][0, :])
plt.xlabel('Time')
plt.ylabel('e_S 0')

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
plt.plot(range(data['Num_T']), traj['p_B'][0, :])
plt.xlabel('Time')
plt.ylabel('p_B 0')

plt.show()