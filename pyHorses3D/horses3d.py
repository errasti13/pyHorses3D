# horses3d.py

import subprocess
from .control import Horses3DControl
from .plot import Horses3DPlot
from .mesh import Horses3DMesh
from .solution import Horses3DSolution

class Horses3D:
    def __init__(self, solverPath, controlFilePath):
        self.control = Horses3DControl(controlFilePath)
        self.plot = Horses3DPlot()
        self.mesh = Horses3DMesh()
        self.solution = Horses3DSolution()

        self.horses3dPath = solverPath
    
    def runHorses3D(self):
        config_file = self.control.saveControlFile('control_generated.control')
        command = f"{self.horses3dPath} {config_file}"
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Error during simulation: {e.stderr.decode()}")
    
    def loadHorsesSolution(self, solution_file):
        self.solution.load(solution_file)

