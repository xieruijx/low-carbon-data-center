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
        # b
        for i in range(param['Num_F']):
            model.addConstr(theta_F[i] + param['Q_Fo'][i] - param['A_Fo'][i] - V * param['gamma_F'][i] >= 0)
        # c
        for j in range(param['Num_B']):
            model.addConstr(- theta_B[j] - param['P_Bo'][j] + (param['T_Hu'][j] + theta_H[j]) * param['alpha_B'][j] + V * param['gamma_Pu'][j] >= 0)
        # d
        sum_m_i = np.sum(param['M_Ro'], axis=0)
        for i in range(param['Num_F']):
            for j in range(param['Num_B']):
                model.addConstr(- param['Q_Fo'][i] - theta_F[i] + theta_B[j] + param['Q_Bo'] - sum_m_i[j] + V * param['gamma_R'][i][j] >= 0)
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
    def opt_offline(param, data):
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
        model.addConstr(e_S[:, 0] == param['E_Su'])
        model.addConstr(tau_H[:, 0] == param['T_Hu'])
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
            model.addConstr(q_F[:, t] >= 0)
            model.addConstr(q_F[:, t] <= param['Q_Fo'])
            # 1g
            model.addConstr(q_B[:, t] >= 0)
            model.addConstr(q_B[:, t] <= param['Q_Bo'])
        
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

        return traj
 