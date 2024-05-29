# solution.py

import numpy as np

class Horses3DSolution:
    def __init__(self):
        self.solution = []
        self.derivedFields = {}
    
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

    def add_computed_field(self, name, data):
        self.computed_fields[name] = data

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
            
            Q = np.fromfile(fname, dtype=np.float64, count=size , sep='', offset=offset_value).reshape(P_order,order='F')
            
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
