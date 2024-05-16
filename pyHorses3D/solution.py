# solution.py

import numpy as np

class Horses3DSolution:
    def __init__(self):
        self.data = {}
    
    def load(self, filepath):
        self.data = np.loadtxt(filepath, delimiter=',', skiprows=1, dtype={'names': ('x', 'y'), 'formats': (np.float, np.float)})
    
    def save(self, filepath):
        np.savetxt(filepath, self.data, delimiter=',', header='x,y')
