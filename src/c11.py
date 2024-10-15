import numpy as np

from utils.settings import Settings
from utils.optimization import Optimization

param, data = Settings().benchmark()
Optimization().opt_param(param)
