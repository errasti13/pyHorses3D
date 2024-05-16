# mesh.py

class Horses3DMesh:
    def __init__(self, filepath=None):
        self.mesh_data = {}
        if filepath:
            self.load(filepath)
    
    def load(self, filepath):
        with open(filepath, 'r') as file:
            self.mesh_data = file.readlines()
    
    def save(self, filepath):
        with open(filepath, 'w') as file:
            file.writelines(self.mesh_data)
