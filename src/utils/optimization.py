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
 