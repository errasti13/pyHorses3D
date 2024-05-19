# control.py

class Horses3DControl:
    def __init__(self, filepath=None):
        self.parameters = {}
        self.boundaries = {}
        self.monitors = {}
        self.controlFilePath = filepath

        if filepath:
            self.loadControlFile()
        else:
            self.createDefaultControl()

    def loadControlFile(self):
        filepath = self.controlFilePath
        with open(filepath, 'r') as file:
            current_boundary = None
            current_monitor = None
            for line in file:
                line = line.strip()

                if line.startswith('#define boundary'):
                    current_boundary = self.extract_boundary_name(line)
                    self.boundaries[current_boundary] = []
                elif line.startswith('#end'):
                    current_boundary = None
                elif line.startswith('#define volume monitor'):
                    current_monitor = self.extract_monitor_name(line)
                    self.monitors[current_monitor] = {}
                elif current_boundary:
                    self.process_boundary_line(current_boundary, line)
                elif current_monitor:
                    self.process_monitor_line(current_monitor, line)
                elif '=' in line:
                    self.process_parameter_line(line)

    def extract_boundary_name(self, line):
        return line.split(' ')[2]

    def extract_monitor_name(self, line):
        return line.split(' ')[3]

    def process_boundary_line(self, current_boundary, line):
        self.boundaries[current_boundary].append(line.strip())

    def process_monitor_line(self, current_monitor, line):
        if '=' in line:
            key, value = line.split('=', 1)
            self.monitors[current_monitor][key.strip()] = value.strip()

    def process_parameter_line(self, line):
        key, value = line.split('=', 1)
        self.parameters[key.strip()] = value.strip()

    def saveControlFile(self, filepath):
        with open(filepath, 'w') as file:
            self.write_parameters(file)
            self.write_boundaries(file)
            self.write_monitors(file)
            # Write an empty line to preserve formatting
            file.write("\n")
        return filepath

    def write_parameters(self, file):
        for key, value in self.parameters.items():
            file.write(f"{key} = {value}\n")

    def write_boundaries(self, file):
        for boundary, lines in self.boundaries.items():
            file.write(f"#define boundary {boundary}\n")
            for line in lines:
                file.write(f"  {line}\n")
            file.write("#end\n")
            file.write("\n")

    def write_monitors(self, file):
        for monitor, properties in self.monitors.items():
            file.write(f"#define volume monitor {monitor}\n")
            for key, value in properties.items():
                file.write(f"  {key} = {value}\n")
            file.write("#end\n")
            file.write("\n")

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

