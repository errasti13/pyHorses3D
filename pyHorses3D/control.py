# control.py

import os

class Horses3DControl:
    """
    Class for managing Horses3D control file parameters.
    
    This class provides methods to load, modify, and save control files
    for the Horses3D CFD solver.
    
    Attributes:
        parameters (dict): Dictionary of solver parameters
        boundaries (dict): Dictionary of boundary definitions
        monitors (dict): Dictionary of monitor definitions
        controlFilePath (str): Path to the control file
    """
    def __init__(self, filepath=None):
        """
        Initialize the Horses3DControl object.
        
        Args:
            filepath (str, optional): Path to the control file. If provided,
                                     the file will be loaded. Otherwise, default
                                     parameters will be created.
        """
        self.parameters = {}
        self.boundaries = {}
        self.monitors = {}
        self.controlFilePath = filepath

        if filepath:
            self.loadControlFile()
        else:
            self.createDefaultControl()

    def loadControlFile(self):
        """
        Load a control file and parse its contents.
        
        Raises:
            FileNotFoundError: If the control file does not exist
            IOError: If there is an error reading the file
        """
        filepath = self.controlFilePath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Control file not found: {filepath}")
            
        try:
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
                        current_monitor = None
                    elif line.startswith('#define volume monitor'):
                        current_monitor = self.extract_monitor_name(line)
                        self.monitors[current_monitor] = {}
                    elif current_boundary:
                        self.process_boundary_line(current_boundary, line)
                    elif current_monitor:
                        self.process_monitor_line(current_monitor, line)
                    elif '=' in line:
                        self.process_parameter_line(line)
        except Exception as e:
            raise IOError(f"Error loading control file: {e}")

    def extract_boundary_name(self, line):
        """
        Extract boundary name from a boundary definition line.
        
        Args:
            line (str): The line containing the boundary definition
            
        Returns:
            str: The boundary name
        """
        return line.split(' ')[2]

    def extract_monitor_name(self, line):
        """
        Extract monitor name from a monitor definition line.
        
        Args:
            line (str): The line containing the monitor definition
            
        Returns:
            str: The monitor name
        """
        return line.split(' ')[3]

    def process_boundary_line(self, current_boundary, line):
        """
        Process a line within a boundary definition block.
        
        Args:
            current_boundary (str): Name of the current boundary being processed
            line (str): The line to process
        """
        self.boundaries[current_boundary].append(line.strip())

    def process_monitor_line(self, current_monitor, line):
        """
        Process a line within a monitor definition block.
        
        Args:
            current_monitor (str): Name of the current monitor being processed
            line (str): The line to process
        """
        if '=' in line:
            key, value = line.split('=', 1)
            self.monitors[current_monitor][key.strip()] = value.strip()

    def process_parameter_line(self, line):
        """
        Process a parameter line (key = value).
        
        Args:
            line (str): The line to process
        """
        key, value = line.split('=', 1)
        self.parameters[key.strip()] = value.strip()

    def saveControlFile(self, filepath):
        """
        Save the current control parameters to a file.
        
        Args:
            filepath (str): Path where the control file will be saved
            
        Returns:
            str: The path of the saved file
            
        Raises:
            IOError: If there is an error writing the file
        """
        try:
            with open(filepath, 'w') as file:
                self.write_parameters(file)
                self.write_boundaries(file)
                self.write_monitors(file)
                # Write an empty line to preserve formatting
                file.write("\n")
            return filepath
        except Exception as e:
            raise IOError(f"Error saving control file: {e}")

    def write_parameters(self, file):
        """
        Write parameters to the control file.
        
        Args:
            file (file): File object to write to
        """
        for key, value in self.parameters.items():
            file.write(f"{key} = {value}\n")

    def write_boundaries(self, file):
        """
        Write boundary definitions to the control file.
        
        Args:
            file (file): File object to write to
        """
        for boundary, lines in self.boundaries.items():
            file.write(f"#define boundary {boundary}\n")
            for line in lines:
                file.write(f"  {line}\n")
            file.write("#end\n")
            file.write("\n")

    def write_monitors(self, file):
        """
        Write monitor definitions to the control file.
        
        Args:
            file (file): File object to write to
        """
        for monitor, properties in self.monitors.items():
            file.write(f"#define volume monitor {monitor}\n")
            for key, value in properties.items():
                file.write(f"  {key} = {value}\n")
            file.write("#end\n")
            file.write("\n")

    def createDefaultControl(self):
        """
        Create a default set of control parameters.
        """
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
        """
        Set a control parameter.
        
        Args:
            key (str): Parameter name
            value (str): Parameter value
        """
        self.parameters[key] = value

    def get_parameter(self, key):
        """
        Get a control parameter value.
        
        Args:
            key (str): Parameter name
            
        Returns:
            str: Parameter value or None if not found
        """
        return self.parameters.get(key, None)

