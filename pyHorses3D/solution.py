# solution.py

import numpy as np

class Horses3DSolution:
    def __init__(self):
        self.solution = []
        self.magnitudes = {'rho': 0, 'rhou': 1, 'rhov': 2, 'rhow': 3, 'rhoe': 4}
        self.gamma = 1.4
        self.R     = 287.1
    
    def loadAllSolutions(self, allSolutionFiles):
        for solutionFile in allSolutionFiles:
            print(solutionFile)
            self.solution.append(self._Q_from_file(solutionFile).transpose(0,2,3,4,1))

    def loadSolutionsInRange(self, allSolutionFiles, first_filename, last_filename, skip=0):
        first_index = allSolutionFiles.index(first_filename)
        last_index = allSolutionFiles.index(last_filename)

        for solutionFile in allSolutionFiles[first_index:last_index + 1:skip + 1]:
            print(solutionFile)
            self.solution.append(self._Q_from_file(solutionFile).transpose(0,2,3,4,1))

    def loadSingleSolution(self, solutionFileName):
        self.solution.append(self._Q_from_file(solutionFileName).transpose(0,2,3,4,1))

    def computeVelocityMagnitude(self, idx):
        # Extract the velocity components
        rhou = self.solution[idx][..., self.magnitudes['rhou']]
        rhov = self.solution[idx][..., self.magnitudes['rhov']]
        rhow = self.solution[idx][..., self.magnitudes['rhow']]
        
        V = np.sqrt(rhou**2 + rhov**2 + rhow**2)
        
        self.solution[idx] = np.concatenate((self.solution[idx], V[..., np.newaxis]), axis=-1)

        self.magnitudes['V'] = self.solution[idx].shape[-1] - 1

    def computePressure(self, idx):
        rho  = self.solution[idx][..., self.magnitudes['rho']]
        rhou = self.solution[idx][..., self.magnitudes['rhou']]
        rhov = self.solution[idx][..., self.magnitudes['rhov']]
        rhow = self.solution[idx][..., self.magnitudes['rhow']]
        rhoe = self.solution[idx][..., self.magnitudes['rhoe']]
        
        u = rhou / rho
        v = rhov / rho
        w = rhow / rho
        kinetic_energy = 0.5 * (u**2 + v**2 + w**2)
        
        p = (self.gamma - 1) * (rhoe - rho * kinetic_energy)
        
        self.solution[idx] = np.concatenate((self.solution[idx], p[..., np.newaxis]), axis=-1)
        self.magnitudes['p'] = self.solution[idx].shape[-1] - 1

    def computeTemperature(self, idx):
        if 'p' not in self.magnitudes:
            self.computePressure(idx)

        rho = self.solution[idx][..., self.magnitudes['rho']]
        p = self.solution[idx][..., self.magnitudes['p']]
        
        T = p / (self.R * rho)
        
        self.solution[idx]   = np.concatenate((self.solution[idx], T[..., np.newaxis]), axis=-1)
        self.magnitudes['T'] = self.solution[idx].shape[-1] - 1

    def computeSpeedOfSound(self, idx):
        if 'p' not in self.magnitudes:
            self.computePressure(idx)

        rho = self.solution[idx][..., self.magnitudes['rho']]
        p = self.solution[idx][..., self.magnitudes['p']]
        
        a = np.sqrt(self.gamma * p / rho)
        
        self.solution[idx] = np.concatenate((self.solution[idx], a[..., np.newaxis]), axis=-1)
        self.magnitudes['a'] = self.solution[idx].shape[-1] - 1

    def computeMach(self, idx):
        if 'V' not in self.magnitudes:
            self.computeVelocityMagnitude(idx)
        if 'a' not in self.magnitudes:
            self.computeSpeedOfSound(idx)

        V = self.solution[idx][..., self.magnitudes['V']]
        a = self.solution[idx][..., self.magnitudes['a']]
        
        Mach = V / a
        
        self.solution[idx] = np.concatenate((self.solution[idx], Mach[..., np.newaxis]), axis=-1)
        self.magnitudes['M'] = self.solution[idx].shape[-1] - 1

    def _Q_from_file(self, fname):
        v1 = np.fromfile(fname, dtype=np.int32, count=2, sep='', offset=136)
        No_of_elements = v1[0]
        Iter = v1[1]
        
        time = np.fromfile(fname, dtype=np.float64, count=1, sep='', offset=144)
        
        ref_values = np.fromfile(fname, dtype=np.float64, count=6, sep='', offset=152)
        
        Mesh = []
        
        offset_value = 152+6*8+4
        
        for i in range(0,No_of_elements):
            
            Ind = 0
            
            Local_storage = self.storage()     

            offset_value = offset_value + 4
            P_order = np.fromfile(fname, dtype=np.int32, count=4, sep='', offset=offset_value) #208
            offset_value = offset_value + 4*4   
            size = P_order[0]*P_order[1]*P_order[2]*P_order[3]
            
            Q = np.fromfile(fname, dtype=np.float32, count=size , sep='', offset=offset_value).reshape(P_order,order='F')
            
            Q1 = np.zeros( (Q.shape[0], Q.shape[1], Q.shape[2], Q.shape[3] )   )
            size1 = P_order[0]*P_order[1]*P_order[2]*P_order[3] 
            Q1 = Q

            if (i==0):
                Sol = np.zeros((No_of_elements,P_order[0],P_order[1],P_order[2],P_order[3]))
            else:
                Ind = 0

            Local_storage.Q = Q1.reshape(size1,order='F')
            
            Sol[i,:,:,:,:] = Q1[:,:,:,:]
            
            offset_value = offset_value + size*8
            
        return Sol

    class storage():
        Q = []
