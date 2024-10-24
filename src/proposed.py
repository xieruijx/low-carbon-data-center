import numpy as np
import matplotlib.pyplot as plt

from utils.settings import Settings
from utils.optimization import Optimization
from utils.simulation import Simulation

fontsize = 12
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
set_theta_E_new = np.zeros(len(set_theta_E) + 1,)
set_theta_E_new[1:] = set_theta_E
plt.figure(figsize=(5, 3))
plt.plot(range(len(set_theta_E_new)), set_theta_E_new, '*-')
plt.xlabel('Iteration')
plt.ylabel('$Q^E$ (tCO$_2$)')
plt.grid(linestyle='--')

param, data = Settings().benchmark(Num_T=9000)
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

print('Test average cost rate: {} $/h'.format(traj['sum_cost'][-1] / 9000 * 10))
print('Test average emission rate: {} tCO2/h'.format(traj['sum_E'][-1] / 9000))

index_tp1 = np.array(range(data['Num_T'] + 1))
index_t = range(data['Num_T'])

index_begin = 5500
index_end = 5600
index_tp1middle = (index_tp1 >= index_begin) & (index_tp1 <= index_end)

fig, axs = plt.subplots(2, 2, figsize=(10, 6))

axs[0, 0].plot(index_tp1[index_tp1middle], np.zeros((len(index_tp1[index_tp1middle],))), 'r--')
axs[0, 0].plot(index_tp1[index_tp1middle], traj['q_F'][0, index_tp1middle])
axs[0, 0].plot(index_tp1[index_tp1middle], traj['q_F'][1, index_tp1middle])
axs[0, 0].set_xlabel('Time slot', fontsize=fontsize)
axs[0, 0].set_ylabel('$q^F$ (MWh)', fontsize=fontsize)
axs[0, 0].tick_params(axis='x', labelsize=fontsize)
axs[0, 0].tick_params(axis='y', labelsize=fontsize)

axs[0, 1].plot(index_tp1[index_tp1middle], np.zeros((len(index_tp1[index_tp1middle],))), 'r--')
axs[0, 1].plot(index_tp1[index_tp1middle], traj['q_B'][0, index_tp1middle])
axs[0, 1].plot(index_tp1[index_tp1middle], traj['q_B'][1, index_tp1middle])
axs[0, 1].plot(index_tp1[index_tp1middle], traj['q_B'][2, index_tp1middle])
axs[0, 1].set_xlabel('Time slot', fontsize=fontsize)
axs[0, 1].set_ylabel('$q^B$ (MWh)', fontsize=fontsize)
axs[0, 1].tick_params(axis='x', labelsize=fontsize)
axs[0, 1].tick_params(axis='y', labelsize=fontsize)

axs[1, 0].plot(index_tp1[index_tp1middle], np.ones((len(index_tp1[index_tp1middle],))) * param['E_Su'][0], 'r--')
axs[1, 0].plot(index_tp1[index_tp1middle], np.ones((len(index_tp1[index_tp1middle],))) * param['E_So'][0], 'r--')
axs[1, 0].plot(index_tp1[index_tp1middle], traj['e_S'][0, index_tp1middle])
axs[1, 0].plot(index_tp1[index_tp1middle], traj['e_S'][1, index_tp1middle])
axs[1, 0].plot(index_tp1[index_tp1middle], traj['e_S'][2, index_tp1middle])
axs[1, 0].set_xlabel('Time slot', fontsize=fontsize)
axs[1, 0].set_ylabel('$e^S$ (MWh)', fontsize=fontsize)
axs[1, 0].tick_params(axis='x', labelsize=fontsize)
axs[1, 0].tick_params(axis='y', labelsize=fontsize)

axs[1, 1].plot(index_tp1[index_tp1middle], np.ones((len(index_tp1[index_tp1middle],))) * param['T_Hu'][0], 'r--')
axs[1, 1].plot(index_tp1[index_tp1middle], np.ones((len(index_tp1[index_tp1middle],))) * param['T_Ho'][0], 'r--')
axs[1, 1].plot(index_tp1[index_tp1middle], traj['tau_H'][0, index_tp1middle])
axs[1, 1].plot(index_tp1[index_tp1middle], traj['tau_H'][1, index_tp1middle])
axs[1, 1].plot(index_tp1[index_tp1middle], traj['tau_H'][2, index_tp1middle])
axs[1, 1].set_xlabel('Time slot', fontsize=fontsize)
axs[1, 1].set_ylabel(r'$\tau^H$ ($^\circ$C)', fontsize=fontsize)
axs[1, 1].tick_params(axis='x', labelsize=fontsize)
axs[1, 1].tick_params(axis='y', labelsize=fontsize)

plt.tight_layout()



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