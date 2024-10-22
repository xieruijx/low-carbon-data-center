## Optimization
import numpy as np
import gurobipy as gp
from gurobipy import GRB

class Optimization(object):
    """
    Optimization class
    """

    @staticmethod
    def opt_param(param, theta_E=0.0):
        """
        Optimize the Lyapunov optimization parameters
        """
        model = gp.Model('opt_param')

        ## Variables
        theta_F = model.addMVar((param['Num_F'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        theta_B = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        theta_S = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        theta_H = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        V = model.addVar(lb=-float('inf'), ub=1e5, vtype=GRB.CONTINUOUS)

        ## Objective
        model.setObjective(V, GRB.MAXIMIZE)

        ## Constraints
        # a
        sum_m_j = np.sum(param['M_Ro'], axis=1)
        for i in range(param['Num_F']):
            for j in range(param['Num_B']):
                model.addConstr(- theta_F[i] - sum_m_j[i] + theta_B[j] + V * param['gamma_R'][i, j] >= 0)
        # # b
        # for i in range(param['Num_F']):
        #     model.addConstr(theta_F[i] + param['Q_Fo'][i] - param['A_Fo'][i] - V * param['gamma_F'][i] >= 0)
        # c
        for j in range(param['Num_B']):
            model.addConstr(- theta_B[j] - param['P_Bo'][j] + (param['T_Hu'][j] + theta_H[j]) * param['alpha_B'][j] + V * param['gamma_Pu'][j] >= 0)
        # # d
        # sum_m_i = np.sum(param['M_Ro'], axis=0)
        # for i in range(param['Num_F']):
        #     for j in range(param['Num_B']):
        #         model.addConstr(- param['Q_Fo'][i] - theta_F[i] + theta_B[j] + param['Q_Bo'] - sum_m_i[j] + V * param['gamma_R'][i][j] >= 0)
        # e
        for j in range(param['Num_B']):
            model.addConstr(- (theta_S[j] + param['E_Su'][j] + param['P_SDo'][j] / param['eta_SD'][j]) / param['eta_SD'][j] - theta_E * param['gamma_Eo'][j] + V * param['gamma_S'][j] - V * param['gamma_Po'][j] >= 0)
        # f
        for j in range(param['Num_B']):
            model.addConstr((theta_S[j] + param['E_So'][j] - param['P_SCo'][j] * param['eta_SC'][j]) * param['eta_SC'][j] + V * param['gamma_S'][j] + V * param['gamma_Pu'][j] >= 0)
        # g
        for j in range(param['Num_B']):
            model.addConstr(- (theta_H[j] + param['T_Hu'][j] + param['alpha_C'][j] * param['P_Co'][j]) * param['alpha_C'][j] + V * param['gamma_Pu'][j] >= 0)
        # h
        for j in range(param['Num_B']):
            model.addConstr(- (theta_H[j] + param['T_Ho'][j] - param['alpha_B'][j] * param['P_Bo'][j]) * param['alpha_C'][j] + theta_E * param['gamma_Eo'][j] + V * param['gamma_Po'][j] <= 0)
        
        # model.setParam('OutputFlag', 0)
        model.optimize()

        sol = {}
        sol['V'] = V.X
        sol['theta_F'] = theta_F.X
        sol['theta_B'] = theta_B.X
        sol['theta_S'] = theta_S.X
        sol['theta_H'] = theta_H.X

        return sol
    
    @staticmethod
    def opt_param_noemissioncon(param):
        """
        Optimize the Lyapunov optimization parameters without emission constraints
        """
        model = gp.Model('opt_param')

        ## Variables
        theta_F = model.addMVar((param['Num_F'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        theta_B = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        theta_S = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        theta_H = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        V = model.addVar(lb=-float('inf'), ub=1e5, vtype=GRB.CONTINUOUS)

        ## Objective
        model.setObjective(V, GRB.MAXIMIZE)

        ## Constraints
        # a
        sum_m_j = np.sum(param['M_Ro'], axis=1)
        for i in range(param['Num_F']):
            for j in range(param['Num_B']):
                model.addConstr(- theta_F[i] - sum_m_j[i] + theta_B[j] + V * param['gamma_R'][i, j] >= 0)
        # c
        for j in range(param['Num_B']):
            model.addConstr(- theta_B[j] - param['P_Bo'][j] + (param['T_Hu'][j] + theta_H[j]) * param['alpha_B'][j] + V * param['gamma_Pu'][j] >= 0)
        # e
        for j in range(param['Num_B']):
            model.addConstr(- (theta_S[j] + param['E_Su'][j] + param['P_SDo'][j] / param['eta_SD'][j]) / param['eta_SD'][j] + V * param['gamma_S'][j] - V * param['gamma_Po'][j] >= 0)
        # f
        for j in range(param['Num_B']):
            model.addConstr((theta_S[j] + param['E_So'][j] - param['P_SCo'][j] * param['eta_SC'][j]) * param['eta_SC'][j] + V * param['gamma_S'][j] + V * param['gamma_Pu'][j] >= 0)
        # g
        for j in range(param['Num_B']):
            model.addConstr(- (theta_H[j] + param['T_Hu'][j] + param['alpha_C'][j] * param['P_Co'][j]) * param['alpha_C'][j] + V * param['gamma_Pu'][j] >= 0)
        # h
        for j in range(param['Num_B']):
            model.addConstr(- (theta_H[j] + param['T_Ho'][j] - param['alpha_B'][j] * param['P_Bo'][j]) * param['alpha_C'][j] + V * param['gamma_Po'][j] <= 0)
        
        # model.setParam('OutputFlag', 0)
        model.optimize()

        sol = {}
        sol['V'] = V.X
        sol['theta_F'] = theta_F.X
        sol['theta_B'] = theta_B.X
        sol['theta_S'] = theta_S.X
        sol['theta_H'] = theta_H.X

        return sol
    
    @staticmethod
    def opt_offline(param, data, b_emission=True):
        """
        Optimize the offline problem
        """
        model = gp.Model('opt_offline')

        ## Variables
        a_F = model.addMVar((param['Num_F'], data['Num_T']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        q_F = model.addMVar((param['Num_F'], data['Num_T'] + 1), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        m_R = model.addMVar((param['Num_F'], param['Num_B'], data['Num_T']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        p_B = model.addMVar((param['Num_B'], data['Num_T']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        q_B = model.addMVar((param['Num_B'], data['Num_T'] + 1), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        p_SC = model.addMVar((param['Num_B'], data['Num_T']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        p_SD = model.addMVar((param['Num_B'], data['Num_T']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        e_S = model.addMVar((param['Num_B'], data['Num_T'] + 1), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        p_C = model.addMVar((param['Num_B'], data['Num_T']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
        tau_H = model.addMVar((param['Num_B'], data['Num_T'] + 1), lb=-float('inf'), vtype=GRB.CONTINUOUS)

        ## Objective
        obj = 0
        for t in range(data['Num_T']):
            obj = obj + sum(sum(param['gamma_R'] * m_R[:, :, t])) + param['gamma_F'] @ (data['A_F'][:, t] - a_F[:, t]) + param['gamma_S'] @ (p_SC[:, t] + p_SD[:, t]) + data['gamma_P'][:, t] @ (p_B[:, t] + p_SC[:, t] - p_SD[:, t] + p_C[:, t])
        model.setObjective(obj, GRB.MINIMIZE)

        ## Constraints
        # Initialization
        model.addConstr(q_F[:, 0] == 0)
        model.addConstr(q_B[:, 0] == 0)
        model.addConstr(e_S[:, 0] == (param['E_Su'] + param['E_So']) / 2)
        model.addConstr(tau_H[:, 0] == (param['T_Hu'] + param['T_Ho']) / 2)
        for t in range(data['Num_T']):
            # 1a
            model.addConstr(q_F[:, t + 1] == q_F[:, t] + a_F[:, t] - m_R[:, :, t] @ np.ones((param['Num_B'],)))
            # 1b
            model.addConstr(q_B[:, t + 1] == q_B[:, t] + m_R[:, :, t].T @ np.ones((param['Num_F'],)) - p_B[:, t])
            # 1c
            model.addConstr(a_F[:, t] >= 0)
            model.addConstr(a_F[:, t] <= data['A_F'][:, t])
            # 1d
            for i in range(param['Num_F']):
                model.addConstr(m_R[i, :, t] >= 0)
                model.addConstr(m_R[i, :, t] <= param['M_Ro'][i, :])
            # 1e
            model.addConstr(p_B[:, t] >= 0)
            model.addConstr(p_B[:, t] <= param['P_Bo'])
            # 1f
            model.addConstr(q_F[:, t + 1] >= 0)
            model.addConstr(q_F[:, t + 1] <= param['Q_Fo'])
            # 1g
            model.addConstr(q_B[:, t + 1] >= 0)
            model.addConstr(q_B[:, t + 1] <= param['Q_Bo'])
            # 3a
            model.addConstr(e_S[:, t + 1] == e_S[:, t] + p_SC[:, t] * param['eta_SC'] - p_SD[:, t] / param['eta_SD'])
            # 3b
            model.addConstr(p_SC[:, t] >= 0)
            model.addConstr(p_SC[:, t] <= param['P_SCo'])
            # 3c
            model.addConstr(p_SD[:, t] >= 0)
            model.addConstr(p_SD[:, t] <= param['P_SDo'])
            # 3d
            model.addConstr(e_S[:, t + 1] >= param['E_Su'])
            model.addConstr(e_S[:, t + 1] <= param['E_So'])
            # 5a
            model.addConstr(tau_H[:, t + 1] == tau_H[:, t] + param['alpha_B'] * p_B[:, t] - param['alpha_C'] * p_C[:, t] - data['beta_C'][:, t])
            # 5b
            model.addConstr(p_C[:, t] >= 0)
            model.addConstr(p_C[:, t] <= param['P_Co'])
            # 5c
            model.addConstr(tau_H[:, t + 1] >= param['T_Hu'])
            model.addConstr(tau_H[:, t + 1] <= param['T_Ho'])
        # 8
        if b_emission:
            model.addConstr(sum(sum(data['gamma_E'] * (p_B + p_SC - p_SD + p_C))) <= param['C_Eo'] * data['Num_T'])
        # Finalization
        model.addConstr(q_F[:, data['Num_T']] == 0)
        model.addConstr(q_B[:, data['Num_T']] == 0)
        model.addConstr(e_S[:, data['Num_T']] == (param['E_Su'] + param['E_So']) / 2)
        model.addConstr(tau_H[:, data['Num_T']] == (param['T_Hu'] + param['T_Ho']) / 2)
        
        # model.setParam('OutputFlag', 0)
        model.optimize()

        traj = {}
        traj['a_F'] = a_F.X
        traj['q_F'] = q_F.X
        traj['m_R'] = m_R.X
        traj['p_B'] = p_B.X
        traj['q_B'] = q_B.X
        traj['p_SC'] = p_SC.X
        traj['p_SD'] = p_SD.X
        traj['e_S'] = e_S.X
        traj['p_C'] = p_C.X
        traj['tau_H'] = tau_H.X

        traj['q_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_cost'] = np.zeros(data['Num_T'] + 1)
        for t in range(data['Num_T']):
            traj['q_E'][t + 1] = np.maximum(traj['q_E'][t] + data['gamma_E'][:, t] @ (traj['p_B'][:, t] + traj['p_SC'][:, t] - traj['p_SD'][:, t] + traj['p_C'][:, t]) - param['C_Eo'], 0)
            traj['sum_E'][t + 1] = traj['sum_E'][t] + data['gamma_E'][:, t] @ (traj['p_B'][:, t] + traj['p_SC'][:, t] - traj['p_SD'][:, t] + traj['p_C'][:, t])
            traj['sum_cost'][t + 1] = traj['sum_cost'][t] + sum(sum(param['gamma_R'] * traj['m_R'][:, :, t])) + param['gamma_F'] @ (data['A_F'][:, t] - traj['a_F'][:, t]) + param['gamma_S'] @ (traj['p_SC'][:, t] + traj['p_SD'][:, t]) + data['gamma_P'][:, t] @ (traj['p_B'][:, t] + traj['p_SC'][:, t] - traj['p_SD'][:, t] + traj['p_C'][:, t])

        return traj
    
    @staticmethod
    def opt_greedy(param, data):
        """
        Optimize using the greedy algorithm
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
        traj['e_S'][:, 0] = (param['E_Su'] + param['E_So']) / 2
        traj['p_C'] = np.zeros((param['Num_B'], data['Num_T']))
        traj['tau_H'] = np.zeros((param['Num_B'], data['Num_T'] + 1))
        traj['tau_H'][:, 0] = (param['T_Hu'] + param['T_Ho']) / 2
        traj['q_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_E'] = np.zeros(data['Num_T'] + 1)
        traj['sum_cost'] = np.zeros(data['Num_T'] + 1)

        for t in range(data['Num_T']):
            model = gp.Model('opt_real_time')

            # Variables
            a_F = model.addMVar((param['Num_F'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            m_R = model.addMVar((param['Num_F'], param['Num_B']), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_B = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_SC = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_SD = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)
            p_C = model.addMVar((param['Num_B'],), lb=-float('inf'), vtype=GRB.CONTINUOUS)

            # Constraint
            # 1c
            model.addConstr(a_F >= 0)
            model.addConstr(a_F <= data['A_F'][:, t])
            # 1d
            for i in range(param['Num_F']):
                model.addConstr(m_R[i, :] >= 0)
                model.addConstr(m_R[i, :] <= param['M_Ro'][i, :])
            # 1e
            model.addConstr(p_B >= 0)
            model.addConstr(p_B <= param['P_Bo'])
            # 1a, 1f
            model.addConstr(traj['q_F'][:, t] + a_F - m_R @ np.ones((param['Num_B'],)) >= 0)
            model.addConstr(traj['q_F'][:, t] + a_F - m_R @ np.ones((param['Num_B'],)) <= param['Q_Fo'])
            # 1b, 1g
            model.addConstr(traj['q_B'][:, t] + m_R.T @ np.ones((param['Num_F'],)) - p_B >= 0)
            model.addConstr(traj['q_B'][:, t] + m_R.T @ np.ones((param['Num_F'],)) - p_B <= param['Q_Bo'])
            # 3b
            model.addConstr(p_SC >= 0)
            model.addConstr(p_SC <= param['P_SCo'])
            # 3c
            model.addConstr(p_SD >= 0)
            model.addConstr(p_SD <= param['P_SDo'])
            # 3a, 3d
            model.addConstr(traj['e_S'][:, t] + p_SC * param['eta_SC'] - p_SD / param['eta_SD'] >= param['E_Su'])
            model.addConstr(traj['e_S'][:, t] + p_SC * param['eta_SC'] - p_SD / param['eta_SD'] <= param['E_So'])
            # 5b
            model.addConstr(p_C >= 0)
            model.addConstr(p_C <= param['P_Co'])
            # 5a, 5c
            model.addConstr(traj['tau_H'][:, t] + param['alpha_B'] * p_B - param['alpha_C'] * p_C - data['beta_C'][:, t] >= param['T_Hu'])
            model.addConstr(traj['tau_H'][:, t] + param['alpha_B'] * p_B - param['alpha_C'] * p_C - data['beta_C'][:, t] <= param['T_Ho'])
            # 8
            model.addConstr(traj['sum_E'][t] + data['gamma_E'][:, t] @ (p_B + p_SC - p_SD + p_C) <= param['C_Eo'] * (t + 1))

            # Objective
            J = sum(sum(param['gamma_R'] * m_R)) + param['gamma_F'] @ (data['A_F'][:, t] - a_F) + param['gamma_QF'] @ (a_F - m_R @ np.ones((param['Num_B'],))) + param['gamma_QB'] @ (m_R.T @ np.ones((param['Num_F'],)) - p_B) + param['gamma_S'] @ (p_SC + p_SD) + data['gamma_P'][:, t] @ (p_B + p_SC - p_SD + p_C)
            model.setObjective(J, GRB.MINIMIZE)

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