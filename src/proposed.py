import numpy as np
import matplotlib.pyplot as plt

from utils.settings import Settings
from utils.optimization import Optimization
from utils.simulation import Simulation

Max_Iter = 10
random_seed = 0

# param, data = Settings().benchmark(random_seed=random_seed, Num_T=1000)
# set_theta_E = np.zeros((Max_Iter,))
# for iter in range(Max_Iter):
#     sol = Optimization().opt_param(param, theta_E=set_theta_E[iter])
#     print('V: {}'.format(sol['V']))
#     traj = Simulation.simulate(param, sol, data)
#     print('Max q_E: {}'.format(max(traj['q_E'])))
#     if abs(max(traj['q_E'] - set_theta_E[iter])) < 0.2 or iter == Max_Iter - 1:
#         break
#     else:
#         set_theta_E[iter + 1] = max(traj['q_E'])
# set_theta_E = set_theta_E[:(iter + 1)]
# print('Iter of q_E: {}'.format(set_theta_E))
set_theta_E = [46.15411924329837, 22.152767830002293, 33.580565155606095, 25.019317543890377, 28.69244140910715, 28.89363537541281, 29.007056549718936]

plt.figure(figsize=(5, 3))
plt.plot(np.array(range(len(set_theta_E))) + 1, set_theta_E, '*-')
plt.xlabel('Iteration')
plt.ylabel(r'$\theta^E$')
plt.grid(linestyle='--')

param, data = Settings().benchmark(Num_T=1000)
# sol = Optimization().opt_param(param, theta_E=set_theta_E[-1])
# traj = Simulation.simulate(param, sol, data)
# np.save('./output/traj_q_F.npy', traj['q_F'])
# np.save('./output/traj_q_B.npy', traj['q_B'])
# np.save('./output/traj_e_S.npy', traj['e_S'])
# np.save('./output/traj_tau_H.npy', traj['tau_H'])
# np.save('./output/traj_sum_E.npy', traj['sum_E'])
# np.save('./output/traj_q_E.npy', traj['q_E'])
# np.save('./output/traj_sum_cost.npy', traj['sum_cost'])
traj = {}
traj['q_F'] = np.load('./output/traj_q_F.npy')
traj['q_B'] = np.load('./output/traj_q_B.npy')
traj['e_S'] = np.load('./output/traj_e_S.npy')
traj['tau_H'] = np.load('./output/traj_tau_H.npy')
traj['sum_E'] = np.load('./output/traj_sum_E.npy')
traj['q_E'] = np.load('./output/traj_q_E.npy')
traj['sum_cost'] = np.load('./output/traj_sum_cost.npy')

index_tp1 = range(data['Num_T'] + 1)
index_t = range(data['Num_T'])

index_begin = 500
index_end = 600

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
plt.plot(range(data['Num_T'] + 1), traj['sum_cost'])
plt.xlabel('Time')
plt.ylabel('cost')

plt.show()