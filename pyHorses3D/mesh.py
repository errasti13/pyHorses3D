import numpy as np

class Horses3DMesh:
    def __init__(self):
        self.mesh = {}

    def loadMesh(self, filepath):
        self.mesh = self._Q_from_file(filepath).transpose(0,2,3,4,1)

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

