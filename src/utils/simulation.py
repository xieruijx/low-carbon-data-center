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
        traj['a_F'] = np.zeros((param['Num_F'], data['Num_T']))
        traj['m_R'] = np.zeros((param['Num_F'], param['Num_B'], data['Num_T']))
        traj['p_B'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['q_F'] = np.zeros((param['Num_F'], data['Num_T'] + 1))
        traj['q_B'] = np.zeros((param['Num_B'], data['Num_T'] + 1))
        traj['p_SC'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['p_SD'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['e_S'] = np.zeros((param['Num_B'], data['Num_T'] + 1))
        traj['e_S'][:, 0] = param['E_Su']
        traj['p_C'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['tau_H'] = np.zeros((param['Num_B'], data['Num_T'] + 1))
        traj['tau_H'][:, 0] = param['T_Hu']
        traj['q_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_cost'] = np.zeros(data['Num_T'] + 1)

        for t in range(data['Num_T']):
            model = gp.Model('opt_real_time')

            # Variables
            a_F = model.addMVar((param['Num_F'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            m_R = model.addMVar((param['Num_F'], param['Num_B']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_B = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_SC = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_SD = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_C = model.addMVar(( param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)

            # Constraint
            # 1c
            for i in range(param['Num_F']):
                model.addConstr(a_F[i] >= 0)
                model.addConstr(a_F[i] <= data['A_F'][i, t])
            # 1d
            for i in range(param['Num_F']):
                for j in range(param['Num_B']):
                    model.addConstr(m_R[i, j] >= 0)
                    model.addConstr(m_R[i, j] <= param['M_Ro'][i, j])
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
            # 5c
            for j in range(param['Num_B']):
                model.addConstr(p_C[j] >= 0)
                model.addConstr(p_C[j] <= param['P_Co'][j])

            # Objective
            tq_F = traj['q_F'][:, t] + sol['theta_F']
            tq_B = traj['q_B'][:, t] + sol['theta_B']
            tq_S = traj['e_S'][:, t] + sol['theta_S']
            tq_H = traj['tau_H'][:, t] + sol['theta_H']
            tq_E = traj['q_E'][t]
            I = tq_F @ (a_F - m_R @ np.ones((param['Num_B'],))) + tq_B @ (m_R.T @ np.ones((param['Num_F'],)) - p_B) + tq_S @ (p_SC * param['eta_SC'] - p_SD / param['eta_SD']) + tq_H @ (param['alpha_B'] * p_B - param['alpha_C'] * p_C - data['beta_C'][:, t]) + tq_E * (data['gamma_E'][:, t] @ (p_B + p_SC - p_SD + p_C) - param['C_Eo'])
            J = sum(sum(param['gamma_R'] * m_R)) + param['gamma_F'] @ (data['A_F'][:, t] - a_F) + param['gamma_QF'] @ (a_F - m_R @ np.ones((param['Num_B'],))) + param['gamma_QB'] @ (m_R.T @ np.ones((param['Num_F'],)) - p_B) + param['gamma_S'] @ (p_SC + p_SD) + data['gamma_P'][:, t] @ (p_B + p_SC - p_SD + p_C)
            model.setObjective(I + sol['V'] * J, GRB.MINIMIZE)

            # Optimize
            model.setParam('OutputFlag', 0)
            model.optimize()

            # Update queues
            traj['q_F'][:, t + 1] = traj['q_F'][:, t] + a_F.X - m_R.X @ np.ones((param['Num_B'],))
            traj['q_B'][:, t + 1] = traj['q_B'][:, t] + m_R.X.T @ np.ones((param['Num_F'],)) - p_B.X
            traj['e_S'][:, t + 1] = traj['e_S'][:, t] + p_SC.X * param['eta_SC'] - p_SD.X / param['eta_SD']
            traj['tau_H'][:, t + 1] = np.maximum(traj['tau_H'][:, t] + param['alpha_B'] * p_B.X - data['beta_C'][:, t], param['T_Hu']) - param['alpha_C'] * p_C.X
            traj['q_E'][t + 1] = np.maximum(traj['q_E'][t] + data['gamma_E'][:, t] @ (p_B.X + p_SC.X - p_SD.X + p_C.X) - param['C_Eo'], 0)

            traj['a_F'][:, t] = a_F.X
            traj['m_R'][:, :, t] = m_R.X
            traj['p_B'][:, t] = p_B.X
            traj['p_SC'][:, t] = p_SC.X
            traj['p_SD'][:, t] = p_SD.X
            traj['p_C'][:, t] = p_C.X
            traj['sum_E'][t + 1] = traj['sum_E'][t] + data['gamma_E'][:, t] @ (p_B.X + p_SC.X - p_SD.X + p_C.X)
            traj['sum_cost'][t + 1] = traj['sum_cost'][t] + sum(sum(param['gamma_R'] * m_R.X)) + param['gamma_F'] @ (data['A_F'][:, t] - a_F.X) + param['gamma_S'] @ (p_SC.X + p_SD.X) + data['gamma_P'][:, t] @ (p_B.X + p_SC.X - p_SD.X + p_C.X)

        print(max(traj['q_E']))
            
        return traj

 