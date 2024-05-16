# control.py

class Horses3DControl:
    def __init__(self, filepath=None):
        self.parameters = {}
        self.blocks = {}
        self.controlFilePath = filepath

        if filepath:
            self.loadControlFile()
        else:
            self.create_default()

    def loadControlFile(self):
        filepath = self.controlFilePath
        with open(filepath, 'r') as file:
            current_block = None
            for line in file:
                line = line.strip()
                if line.startswith('#define boundary'):
                    current_block = line.split(' ')[2]
                    self.blocks[current_block] = []
                elif line.startswith('#end'):
                    current_block = None
                elif current_block:
                    self.blocks[current_block].append(line.strip())
                elif line and not line.startswith('!') and '=' in line:
                    key, value = line.split('=', 1)
                    self.parameters[key.strip()] = value.strip()

    def saveControlFile(self, filepath):
        with open(filepath, 'w') as file:
            for key, value in self.parameters.items():
                file.write(f"{key} = {value}\n")
            for block, lines in self.blocks.items():
                file.write(f"#define boundary {block}\n")
                for line in lines:
                    file.write(f"  {line}\n")
                file.write("#end\n")
        return filepath

    def createDefaultControl(self):
        self.parameters = {
            'Flow equations': '"NS"',
            'mesh file name': '"MESH/myMesh.mesh"',
            'solution file name': '"RESULTS/mySol.hsol"',
            'simulation type': 'time-accurate',
            'time integration': 'explicit',
            'Polynomial order': '2',
            'restart': '.false.',
            'cfl': '0.3',
            'dcfl': '0.3',
            'final time': '5.0',
            'Number of time steps': '10000',
            'Output Interval': '50',
            'Convergence tolerance': '1.d-10',
            'mach number': '0.3',
            'Reynolds number': '200.0',
            'Prandtl number': '0.72',
            'AOA theta': '0.0',
            'AOA phi': '90.0',
            'LES model': 'Smagorinsky',
            'save gradients with solution': '.true.',
            'riemann solver': 'roe'
        }

    def set_parameter(self, key, value):
        self.parameters[key] = value

    def get_parameter(self, key):
        return self.parameters.get(key, None)
