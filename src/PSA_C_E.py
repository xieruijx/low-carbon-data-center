import numpy as np

from utils.settings import Settings
from utils.optimization import Optimization
from utils.simulation import Simulation

C_Eo = 1.6
Max_Iter = 10
random_seed = 0

param, data = Settings().benchmark(random_seed=random_seed, Num_T=1000)
param['C_Eo'] = C_Eo
set_theta_E = np.zeros((Max_Iter,))
for iter in range(Max_Iter):
    sol = Optimization().opt_param(param, theta_E=set_theta_E[iter])
    print('V: {}'.format(sol['V']))
    traj = Simulation.simulate(param, sol, data)
    print('Max q_E: {}'.format(max(traj['q_E'])))
    if abs(max(traj['q_E'] - set_theta_E[iter])) < 0.2 or iter == Max_Iter - 1:
        break
    else:
        set_theta_E[iter + 1] = max(traj['q_E'])
set_theta_E = set_theta_E[:(iter + 1)]
print('Iter of q_E: {}'.format(set_theta_E))

param, data = Settings().benchmark(Num_T=9000)
param['C_Eo'] = C_Eo
sol = Optimization().opt_param(param, theta_E=set_theta_E[-1])
traj = Simulation.simulate(param, sol, data)

print('Test average cost rate: {} $/h'.format(traj['sum_cost'][-1] / 9000 * 10))
print('Test average emission rate: {} tCO2/h'.format(traj['sum_E'][-1] / 9000))