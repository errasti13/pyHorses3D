# examples.py

"""
Examples and tutorials for using the pyHorses3D package.

This module provides example workflows and tutorials for common
tasks when working with the Horses3D solver interface.
"""

import os
import matplotlib.pyplot as plt
from .horses3d import Horses3D

def setup_taylor_green_vortex(control_file_path, solver_path):
    """
    Set up a Taylor-Green vortex simulation.
    
    Args:
        control_file_path (str): Path to the control file
        solver_path (str): Path to the Horses3D solver executable
        
    Returns:
        Horses3D: Configured Horses3D solver interface
    """
    # Create the solver interface
    solver = Horses3D(solver_path, control_file_path)
    
    # Load the control file
    solver.control.loadControlFile()
    
    # Modify some parameters for the Taylor-Green vortex case
    solver.control.set_parameter('Flow equations', '"NS"')
    solver.control.set_parameter('simulation type', 'time-accurate')
    solver.control.set_parameter('time integration', 'explicit')
    solver.control.set_parameter('Polynomial order', '4')
    solver.control.set_parameter('restart', '.false.')
    solver.control.set_parameter('cfl', '0.4')
    solver.control.set_parameter('final time', '10.0')
    solver.control.set_parameter('Number of time steps', '2000')
    solver.control.set_parameter('Output Interval', '100')
    solver.control.set_parameter('mach number', '0.1')
    solver.control.set_parameter('Reynolds number', '1600.0')
    
    return solver

def run_simulation_and_visualize(solver, plot_residuals=True):
    """
    Run a simulation and visualize the results.
    
    Args:
        solver (Horses3D): Configured Horses3D solver interface
        plot_residuals (bool, optional): Whether to plot residuals after the simulation.
                                        Defaults to True.
    """
    # Run the solver
    solver.runHorses3D(plotResiduals=plot_residuals)
    
    # Get solution files
    solution_files = solver.getSolutionFileNames()
    print(f"Found {len(solution_files)} solution files")
    
    # Load the last solution
    if solution_files:
        solver.solution.loadSingleSolution(solution_files[-1])
        
        # Compute derived quantities
        solver.solution.computeVelocityMagnitude(0)
        solver.solution.computePressure(0)
        solver.solution.computeMach(0)
        
        # Get mesh files
        mesh_files = solver.getHMeshFileName()
        if mesh_files:
            solver.mesh.loadMesh(mesh_files[0])
            
            # Plot velocity magnitude
            solver.plot.modifyMagnitudes(solver.solution.magnitudes)
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], 'V', 
                                   plane='XY', value=0, cmap='jet', isocontours=True)
            
            # Plot pressure
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], 'p', 
                                   plane='XY', value=0, cmap='viridis')
            
            # Plot streamlines
            solver.plot.plot2DStreamlines(solver.mesh.mesh[0], solver.solution.solution[0], 
                                         plane='XY', value=0, cmap='cool')

def analyze_time_evolution(solver, solution_files, variable='V'):
    """
    Analyze the time evolution of a variable.
    
    Args:
        solver (Horses3D): Configured Horses3D solver interface
        solution_files (list): List of solution files to analyze
        variable (str, optional): Variable to analyze. Defaults to 'V' (velocity magnitude).
    """
    # Ensure we have the required variable in magnitudes
    if variable not in solver.solution.magnitudes and variable == 'V':
        solver.solution.computeVelocityMagnitude(0)
    elif variable not in solver.solution.magnitudes and variable == 'p':
        solver.solution.computePressure(0)
    elif variable not in solver.solution.magnitudes and variable == 'M':
        solver.solution.computeMach(0)
    
    # Load solutions for different time steps
    time_steps = min(5, len(solution_files))  # Limit to 5 time steps for simplicity
    selected_files = solution_files[::len(solution_files)//time_steps][:time_steps]
    
    solver.solution.solution = []  # Clear previous solutions
    solver.solution.loadAllSolutions(selected_files)
    
    # Get mesh
    mesh_files = solver.getHMeshFileName()
    if mesh_files:
        solver.mesh.loadMesh(mesh_files[0])
        
        # Plot the variable at different time steps
        plt.figure(figsize=(15, 10))
        for i in range(len(solver.solution.solution)):
            # Compute the required variable if not already present
            if variable == 'V' and 'V' not in solver.solution.magnitudes:
                solver.solution.computeVelocityMagnitude(i)
            elif variable == 'p' and 'p' not in solver.solution.magnitudes:
                solver.solution.computePressure(i)
            elif variable == 'M' and 'M' not in solver.solution.magnitudes:
                solver.solution.computeMach(i)
            
            plt.subplot(1, len(solver.solution.solution), i+1)
            solver.plot.modifyMagnitudes(solver.solution.magnitudes)
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[i], variable, 
                                   plane='XY', value=0, cmap='jet')
            plt.title(f"Time step {i}")
        
        plt.tight_layout()
        plt.show()

def full_workflow_example(control_file, solver_path):
    """
    Complete workflow example from setup to visualization.
    
    Args:
        control_file (str): Path to the control file
        solver_path (str): Path to the Horses3D solver executable
    """
    print("1. Setting up the simulation...")
    solver = setup_taylor_green_vortex(control_file, solver_path)
    
    print("2. Running the simulation...")
    solver.runHorses3D(plotResiduals=True)
    
    print("3. Processing the results...")
    solution_files = solver.getSolutionFileNames()
    if solution_files:
        solver.solution.loadSingleSolution(solution_files[-1])
        
        # Compute all derived quantities
        solver.solution.computeVelocityMagnitude(0)
        solver.solution.computePressure(0)
        solver.solution.computeTemperature(0)
        solver.solution.computeSpeedOfSound(0)
        solver.solution.computeMach(0)
        
        # Get mesh files
        mesh_files = solver.getHMeshFileName()
        if mesh_files:
            solver.mesh.loadMesh(mesh_files[0])
            
            print("4. Visualizing the results...")
            solver.plot.modifyMagnitudes(solver.solution.magnitudes)
            
            # Create multiple visualizations
            print("   - Velocity magnitude:")
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], 'V', 
                                   plane='XY', value=0, cmap='jet', isocontours=True)
            
            print("   - Pressure field:")
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], 'p', 
                                   plane='XY', value=0, cmap='viridis')
            
            print("   - Mach number:")
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], 'M', 
                                   plane='XY', value=0, cmap='plasma')
            
            print("   - Temperature:")
            solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], 'T', 
                                   plane='XY', value=0, cmap='hot')
            
            print("   - Streamlines:")
            solver.plot.plot2DStreamlines(solver.mesh.mesh[0], solver.solution.solution[0], 
                                         plane='XY', value=0, cmap='cool')
            
            # If multiple solutions exist, analyze time evolution
            if len(solution_files) > 1:
                print("5. Analyzing time evolution...")
                analyze_time_evolution(solver, solution_files, variable='V')
        else:
            print("No mesh files found.")
    else:
        print("No solution files found.") 