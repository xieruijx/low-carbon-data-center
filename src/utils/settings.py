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
        param['Num_F'] = 2 #
        param['A_Fo'] = np.ones((param['Num_F'],)) * 20
        param['Q_Fo'] = np.ones((param['Num_F'],)) * 2000
        param['gamma_F'] = np.ones((param['Num_F'],)) * 1000
        data['A_F'] = np.random.rand(param['Num_F'], data['Num_T']) * (param['A_Fo'].reshape((-1, 1)) @ np.ones((1, data['Num_T'])))
        ## Back end
        param['Num_B'] = 3 #
        param['M_Ro'] = np.ones((param['Num_F'], param['Num_B'])) * 15
        param['Q_Bo'] = np.ones((param['Num_B'],)) * 2000
        param['P_Bo'] = np.ones((param['Num_B'],)) * 20
        param['gamma_R'] = np.ones((param['Num_F'], param['Num_B'])) * 1
        ## Energy storage
        param['eta_SC'] = np.ones((param['Num_B'],)) * 0.95
        param['eta_SD'] = np.ones((param['Num_B'],)) * 0.95
        param['P_SCo'] = np.ones((param['Num_B'],)) * 5
        param['P_SDo'] = np.ones((param['Num_B'],)) * 5
        param['E_Su'] = np.zeros((param['Num_B'],)) * 0
        param['E_So'] = np.ones((param['Num_B'],)) * 50
        param['gamma_S'] = np.ones((param['Num_B'],)) * 1
        ## Electricity cost
        param['gamma_Pu'] = np.ones((param['Num_B'],)) * 5
        param['gamma_Po'] = np.ones((param['Num_B'],)) * 10
        data['gamma_P'] = np.random.rand(param['Num_B'], data['Num_T']) * ((param['gamma_Po'].reshape((-1, 1)) - param['gamma_Pu'].reshape((-1, 1))) @ np.ones((1, data['Num_T']))) + param['gamma_Pu'].reshape((-1, 1)) @ np.ones((1, data['Num_T']))
        ## Emission
        param['gamma_Eu'] = np.ones((param['Num_B'],)) * 0
        param['gamma_Eo'] = np.ones((param['Num_B'],)) * 1
        data['gamma_E'] = np.random.rand(param['Num_B'], data['Num_T']) * ((param['gamma_Eo'].reshape((-1, 1)) - param['gamma_Eu'].reshape((-1, 1))) @ np.ones((1, data['Num_T']))) + param['gamma_Eu'].reshape((-1, 1)) @ np.ones((1, data['Num_T']))
        param['C_Eo'] = 10

        return param, data
    