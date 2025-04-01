# pyHorses3D API Documentation

This document provides a comprehensive overview of the pyHorses3D API.

## Main Modules

### horses3d.py

The main interface to the Horses3D solver.

#### `Horses3D` Class

**Constructor**:
```python
Horses3D(solverPath, controlFilePath=None)
```
- `solverPath`: Path to the Horses3D solver executable
- `controlFilePath`: Path to the control file (optional)

**Methods**:

- `runHorses3D(plotResiduals=False)`: Run the Horses3D solver
  - `plotResiduals`: Whether to plot residuals after the simulation

- `plot_residuals()`: Plot the residuals from the simulation

- `getSolutionFileNames()`: Get the names of solution files
  - Returns: List of solution file names

- `getHMeshFileName()`: Get the names of mesh files
  - Returns: List of mesh file names

### control.py

Manages Horses3D control file parameters.

#### `Horses3DControl` Class

**Constructor**:
```python
Horses3DControl(filepath=None)
```
- `filepath`: Path to the control file (optional)

**Methods**:

- `loadControlFile()`: Load a control file and parse its contents
  - Raises: `FileNotFoundError` if the file doesn't exist, `IOError` for reading errors

- `saveControlFile(filepath)`: Save the current control parameters to a file
  - `filepath`: Path where the control file will be saved
  - Returns: The path of the saved file

- `set_parameter(key, value)`: Set a control parameter
  - `key`: Parameter name
  - `value`: Parameter value

- `get_parameter(key)`: Get a control parameter value
  - `key`: Parameter name
  - Returns: Parameter value or None if not found

- `createDefaultControl()`: Create a default set of control parameters

### solution.py

Process solution data.

#### `Horses3DSolution` Class

**Constructor**:
```python
Horses3DSolution()
```

**Methods**:

- `loadAllSolutions(allSolutionFiles)`: Load all solution files
  - `allSolutionFiles`: List of solution files to load

- `loadSolutionsInRange(allSolutionFiles, first_filename, last_filename, skip=0)`: Load a range of solution files
  - `allSolutionFiles`: List of all solution files
  - `first_filename`: First file to load
  - `last_filename`: Last file to load
  - `skip`: Number of files to skip between loads

- `loadSingleSolution(solutionFileName)`: Load a single solution file
  - `solutionFileName`: Path to the solution file

- `computeVelocityMagnitude(idx)`: Compute velocity magnitude for a solution
  - `idx`: Index of the solution

- `computePressure(idx)`: Compute pressure for a solution
  - `idx`: Index of the solution

- `computeTemperature(idx)`: Compute temperature for a solution
  - `idx`: Index of the solution

- `computeSpeedOfSound(idx)`: Compute speed of sound for a solution
  - `idx`: Index of the solution

- `computeMach(idx)`: Compute Mach number for a solution
  - `idx`: Index of the solution

### mesh.py

Handle mesh data.

#### `Horses3DMesh` Class

**Constructor**:
```python
Horses3DMesh()
```

**Methods**:

- `loadMesh(filepath)`: Load a mesh file
  - `filepath`: Path to the mesh file

### plot.py

Create visualizations.

#### `Horses3DPlot` Class

**Constructor**:
```python
Horses3DPlot()
```

**Methods**:

- `modifyMagnitudes(magnitudes)`: Update the magnitudes dictionary
  - `magnitudes`: Dictionary mapping variable names to indices

- `plot3DField(mesh, field, key, cmap='jet')`: Plot a 3D field
  - `mesh`: Mesh data
  - `field`: Field data
  - `key`: Variable to plot
  - `cmap`: Colormap to use

- `plot2DField(mesh, field, key, plane='XY', value=0, cmap='jet', isocontours=False, contour_levels=10)`: Plot a 2D slice
  - `mesh`: Mesh data
  - `field`: Field data
  - `key`: Variable to plot
  - `plane`: Plane to plot (XY, XZ, or YZ)
  - `value`: Position of the slice
  - `cmap`: Colormap to use
  - `isocontours`: Whether to plot contour lines
  - `contour_levels`: Number of contour levels

- `plot2DStreamlines(mesh, field, plane='XY', value=0, cmap='jet')`: Plot streamlines
  - `mesh`: Mesh data
  - `field`: Field data
  - `plane`: Plane to plot (XY, XZ, or YZ)
  - `value`: Position of the slice
  - `cmap`: Colormap to use

- `plot3DIsoSurface(mesh, field, key, isovalue, cmap='jet')`: Plot a 3D isosurface
  - `mesh`: Mesh data
  - `field`: Field data
  - `key`: Variable to plot
  - `isovalue`: Value of the isosurface
  - `cmap`: Colormap to use

- `plotResiduals(residuals_data)`: Plot residuals
  - `residuals_data`: Residuals data to plot

### examples.py

Ready-to-use example workflows.

**Functions**:

- `setup_taylor_green_vortex(control_file_path, solver_path)`: Set up a Taylor-Green vortex simulation
  - `control_file_path`: Path to the control file
  - `solver_path`: Path to the Horses3D solver executable
  - Returns: Configured Horses3D solver interface

- `run_simulation_and_visualize(solver, plot_residuals=True)`: Run a simulation and visualize the results
  - `solver`: Configured Horses3D solver interface
  - `plot_residuals`: Whether to plot residuals after the simulation

- `analyze_time_evolution(solver, solution_files, variable='V')`: Analyze the time evolution of a variable
  - `solver`: Configured Horses3D solver interface
  - `solution_files`: List of solution files to analyze
  - `variable`: Variable to analyze

- `full_workflow_example(control_file, solver_path)`: Complete workflow example from setup to visualization
  - `control_file`: Path to the control file
  - `solver_path`: Path to the Horses3D solver executable 