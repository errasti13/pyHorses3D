# pyHorses3D/__init__.py

"""
pyHorses3D - Python interface for the Horses3D CFD solver

This package provides tools to interact with the Horses3D CFD solver,
manage control files, process simulation results, and visualize data.
"""

from .horses3d import Horses3D
from .control import Horses3DControl
from .plot import Horses3DPlot
from .mesh import Horses3DMesh
from .solution import Horses3DSolution
from . import examples
from . import cli

__version__ = '0.2.0'
