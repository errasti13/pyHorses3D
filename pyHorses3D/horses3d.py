# horses3d.py

import subprocess
import sys
import os
import glob
from .control import Horses3DControl
from .plot import Horses3DPlot
from .mesh import Horses3DMesh
from .solution import Horses3DSolution

class Horses3D:
    def __init__(self, solverPath, controlFilePath=None):
        self.control = Horses3DControl(controlFilePath)
        self.plot = Horses3DPlot()
        self.mesh = Horses3DMesh()
        self.solution = Horses3DSolution()

        self.horses3dPath = solverPath
        self.solutionFileNames = []
        self.meshFileNames = []
    

    def runHorses3D(self):
        config_file = self.control.saveControlFile('control_generated.control')
        command = f"{self.horses3dPath} {config_file}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            with process.stdout as stdout, process.stderr as stderr:
                for line in iter(stdout.readline, ''):
                    sys.stdout.write(line)
                for line in iter(stderr.readline, ''):
                    sys.stderr.write(line)
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)
        except subprocess.CalledProcessError as e:
            print(f"Error during simulation: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def getSolutionFileNames(self):
        solution_file_name = self.control.parameters["solution file name"]
        base_name = os.path.splitext(solution_file_name)[0][1:]
        if base_name:
            pattern = f"{base_name}_*.hsol"
            matching_files = glob.glob(pattern)

            if not matching_files:
                raise FileNotFoundError(f"No matching hsol files found for {solution_file_name}")
    
            self.solutionFileNames.extend(matching_files)
        return self.solutionFileNames


    def getHMeshFileName(self):
        solution_file_name = self.control.parameters.get("solution file name")

        base_name = os.path.splitext(solution_file_name)[0]
        extracted_name = base_name.split('/')[-1]
        hMeshFile = "MESH/" + extracted_name

        pattern = f"{hMeshFile}_*.hmesh"
        matching_files = glob.glob(pattern)
        
        if not matching_files:
            raise FileNotFoundError(f"No matching hmesh files found for {solution_file_name}")

        self.meshFileNames.extend(matching_files)
        return self.meshFileNames


