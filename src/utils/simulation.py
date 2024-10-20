## Simulation
import numpy as np
import gurobipy as gp
from gurobipy import GRB

class Simulation(object):
    """
    Simulation class
    """

    @staticmethod
    def simulate(param, sol, data):
        """
        Simulate the real-time operation
        """
        traj = {}
        traj['a'] = np.zeros((param['Num_F'], data['Num_T']))
        traj['m'] = np.zeros((param['Num_F'], param['Num_B'], data['Num_T']))
        traj['p_B'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['q_F'] = np.zeros((param['Num_F'], data['Num_T'] + 1))
        traj['q_B'] = np.zeros((param['Num_B'], data['Num_T'] + 1))
        traj['p_SC'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['p_SD'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['e_S'] = np.zeros((param['Num_B'], data['Num_T'] + 1))
        traj['e_S'][:, 0] = param['E_Su']
        traj['q_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_E'] = np.zeros(data['Num_T'] + 1)

        for t in range(data['Num_T']):
            model = gp.Model('opt_real_time')

            # Variables
            a = model.addMVar((param['Num_F'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            m = model.addMVar((param['Num_F'], param['Num_B']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_B = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_SC = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_SD = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)

            # Constraint
            # 1c
            for i in range(param['Num_F']):
                model.addConstr(a[i] >= 0)
                model.addConstr(a[i] <= data['A_F'][i, t])
            # 1d
            for i in range(param['Num_F']):
                for j in range(param['Num_B']):
                    model.addConstr(m[i, j] >= 0)
                    model.addConstr(m[i, j] <= param['M_Ro'][i, j])
            # 1e
            for j in range(param['Num_B']):
                model.addConstr(p_B[j] >= 0)
                model.addConstr(p_B[j] <= param['P_Bo'][j])
            # 3b
            for j in range(param['Num_B']):
                model.addConstr(p_SC[j] >= 0)
                model.addConstr(p_SC[j] <= param['P_SCo'][j])
            # 3c
            for j in range(param['Num_B']):
                model.addConstr(p_SD[j] >= 0)
                model.addConstr(p_SD[j] <= param['P_SDo'][j])

            # Objective
            tq_F = traj['q_F'][:, t] + sol['theta_F']
            tq_B = traj['q_B'][:, t] + sol['theta_B']
            tq_S = traj['e_S'][:, t] + sol['theta_S']
            tq_E = traj['q_E'][t]
            I = tq_F @ (a - m @ np.ones((param['Num_B'],))) + tq_B @ (m.T @ np.ones((param['Num_F'],)) - p_B) + tq_S @ (p_SC * param['eta_SC'] - p_SD / param['eta_SD']) + tq_E * (data['gamma_E'][:, t] @ (p_B + p_SC - p_SD) - param['C_Eo'])
            J = sum(sum(param['gamma_R'] * m)) + param['gamma_F'] @ (data['A_F'][:, t] - a) + param['gamma_S'] @ (p_SC + p_SD) + data['gamma_P'][:, t] @ (p_B + p_SC - p_SD)
            model.setObjective(I + sol['V'] * J, GRB.MINIMIZE)

            # Optimize
            model.setParam('OutputFlag', 0)
            model.optimize()

            # Update queues
            traj['q_F'][:, t + 1] = traj['q_F'][:, t] + a.X - m.X @ np.ones((param['Num_B'],))
            traj['q_B'][:, t + 1] = traj['q_B'][:, t] + m.X.T @ np.ones((param['Num_F'],)) - p_B.X
            traj['e_S'][:, t + 1] = traj['e_S'][:, t] + p_SC.X * param['eta_SC'] - p_SD.X / param['eta_SD']
            traj['q_E'][t + 1] = np.maximum(traj['q_E'][t] + data['gamma_E'][:, t] @ (p_B.X + p_SC.X - p_SD.X), 0)

            traj['a'][:, t] = a.X
            traj['m'][:, :, t] = m.X
            traj['p_B'][:, t] = p_B.X
            traj['p_SC'][:, t] = p_SC.X
            traj['p_SD'][:, t] = p_SD.X
            traj['sum_E'][t + 1] = traj['sum_E'][t] + data['gamma_E'][:, t] @ (p_B.X + p_SC.X - p_SD.X)

        print(max(traj['q_E']))
            
        return traj

 