# Parameter settings

import numpy as np

class Settings(object):
    """
    Case settings
    """
    
    @staticmethod
    def benchmark(random_seed:int=42, Num_T:int=10000):
        """
        Benchmark case settings
        """
        np.random.seed(random_seed)

        param = {}
        data = {}

        ## Period
        data['Num_T'] = Num_T

        ## Front end
        param['Num_F'] = 2
        param['A_Fo'] = np.ones((param['Num_F'],)) * 3
        param['Q_Fo'] = np.ones((param['Num_F'],)) * 100
        param['gamma_F'] = np.ones((param['Num_F'],)) * 100
        data['A_F'] = np.random.rand(param['Num_F'], data['Num_T']) * (param['A_Fo'].reshape((-1, 1)) @ np.ones((1, data['Num_T'])))
        ## Back end
        param['Num_B'] = 3
        param['M_Ro'] = np.ones((param['Num_F'], param['Num_B'])) * 10
        param['Q_Bo'] = np.ones((param['Num_B'],)) * 100
        param['P_Bo'] = np.ones((param['Num_B'],)) * 3
        param['gamma_R'] = np.ones((param['Num_F'], param['Num_B']))
        ## Energy storage
        param['eta_SC'] = np.ones((param['Num_B'],)) * 0.95
        param['eta_SD'] = np.ones((param['Num_B'],)) * 0.95
        param['P_SCo'] = np.ones((param['Num_B'],)) * 1
        param['P_SDo'] = np.ones((param['Num_B'],)) * 1
        param['E_Su'] = np.zeros((param['Num_B'],))
        param['E_So'] = np.ones((param['Num_B'],)) * 8
        param['gamma_S'] = np.ones((param['Num_B'],)) * 1
        ## Cooling facility
        param['alpha_B'] = np.ones((param['Num_B'],)) * 0.1
        param['alpha_C'] = np.ones((param['Num_B'],)) * 1
        param['beta_Bo'] = np.ones((param['Num_B'],)) * 1
        data['beta_B'] = np.random.rand(param['Num_B'], data['Num_T']) * (param['beta_Bo'].reshape((-1, 1)) @ np.ones((1, data['Num_T'])))
        param['P_Co'] = np.ones((param['Num_B'],)) * 1
        param['T_Hu'] = np.ones((param['Num_B'],)) * 15
        param['T_Ho'] = np.ones((param['Num_B'],)) * 60
        ## Electricity cost
        param['gamma_Pu'] = np.ones((param['Num_B'],)) * 10
        param['gamma_Po'] = np.ones((param['Num_B'],)) * 15
        data['gamma_P'] = np.random.rand(param['Num_B'], data['Num_T']) * ((param['gamma_Po'].reshape((-1, 1)) - param['gamma_Pu'].reshape((-1, 1))) @ np.ones((1, data['Num_T']))) + param['gamma_Pu'].reshape((-1, 1)) @ np.ones((1, data['Num_T']))
        ## Emission
        param['gamma_Eu'] = np.zeros((param['Num_B'],))
        param['gamma_Eo'] = np.ones((param['Num_B'],)) * 1
        param['gamma_E'] = np.random.rand(param['Num_B'], data['Num_T']) * ((param['gamma_Eo'].reshape((-1, 1)) - param['gamma_Eu'].reshape((-1, 1))) @ np.ones((1, data['Num_T']))) + param['gamma_Eu'].reshape((-1, 1)) @ np.ones((1, data['Num_T']))
        param['C_Eo'] = 3.0

        return param, data
    