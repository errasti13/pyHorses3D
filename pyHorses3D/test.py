"""
Test script for the pyHorses3D package.

This script demonstrates how to use pyHorses3D to interface with the 
Horses3D CFD solver, analyze and visualize results.
"""

import os
import platform
from pyHorses3d import Horses3D, examples

# Path configuration
if platform.system() == 'Windows':
    # Windows paths
    control_file = 'TaylorGreen_HO.control'
    # Windows path pointing to WSL
    solver_wsl_path = '/mnt/c/Users/Jon/Desktop/MUMI/TFM/horses3d_Fernando/horses3d/Solver/bin/horses3d.ns'
    # Native Windows path if you have native Windows build of horses3d
    solver_win_path = 'C:\\Users\\Jon\\Desktop\\MUMI\\TFM\\horses3d_Fernando\\horses3d\\Solver\\bin\\horses3d.ns'
    
    # Use WSL path for demonstration
    solver_path = solver_wsl_path
else:
    # Linux/Mac paths
    control_file = 'TaylorGreen_HO.control'
    solver_path = '/path/to/horses3d/bin/horses3d.ns'

# Basic usage example
def basic_example():
    print("=== Basic usage example ===")
    solver = Horses3D(solver_path, control_file)
    
    # Load and display control file settings
    solver.control.loadControlFile()
    print("Control file parameters:")
    for key, value in solver.control.parameters.items():
        print(f"  {key}: {value}")
    
    # Run the simulation (commented out to avoid actual execution during test)
    # solver.runHorses3D()
    
    print("Basic example completed")

# Advanced post-processing example
def advanced_post_processing():
    print("\n=== Advanced post-processing example ===")
    # Assuming solution files already exist
    solver = Horses3D(solver_path, control_file)
    solver.control.loadControlFile()
    
    try:
        # Try to get solution files (this may fail if no simulation was run)
        solution_files = solver.getSolutionFileNames()
        print(f"Found {len(solution_files)} solution files")
        
        # If solution files exist, load and process
        if solution_files:
            solver.solution.loadSingleSolution(solution_files[-1])
            
            # Compute derived quantities
            solver.solution.computeVelocityMagnitude(0)
            solver.solution.computePressure(0)
            solver.solution.computeTemperature(0)
            solver.solution.computeSpeedOfSound(0)
            solver.solution.computeMach(0)
            
            print("Computed derived quantities:")
            for key in solver.solution.magnitudes.keys():
                print(f"  {key} at index {solver.solution.magnitudes[key]}")
            
            # Get mesh files (this may fail if no mesh files exist)
            try:
                mesh_files = solver.getHMeshFileName()
                print(f"Found {len(mesh_files)} mesh files")
            except FileNotFoundError:
                print("No mesh files found. Skipping visualization.")
        else:
            print("No solution files found. Skipping post-processing.")
    except FileNotFoundError:
        print("No solution files found. Skipping post-processing.")
    
    print("Post-processing example completed")

# Examples module demonstration
def examples_demonstration():
    print("\n=== Examples module demonstration ===")
    print("The examples module provides the following functions:")
    print("  - setup_taylor_green_vortex: Configure a solver for Taylor-Green vortex simulation")
    print("  - run_simulation_and_visualize: Run simulation and create visualizations")
    print("  - analyze_time_evolution: Analyze how variables change over time")
    print("  - full_workflow_example: Complete workflow from setup to visualization")
    
    # Note: Actual execution is commented out to avoid simulation during test
    print("\nTo run a full workflow example:")
    print(f"  examples.full_workflow_example('{control_file}', '{solver_path}')")
    
    print("Examples demonstration completed")

if __name__ == "__main__":
    print("pyHorses3D Test Script")
    print("======================\n")
    
    basic_example()
    advanced_post_processing()
    examples_demonstration()
    
    print("\nAll tests completed!")