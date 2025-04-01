# cli.py

"""
Command-line interface for pyHorses3D.

This module provides a command-line interface to the pyHorses3D package,
allowing users to run simulations, process results, and create visualizations
directly from the command line.
"""

import argparse
import os
import sys
import platform
from .horses3d import Horses3D
from .examples import full_workflow_example

def main():
    """
    Main entry point for the pyHorses3D command-line interface.
    """
    parser = argparse.ArgumentParser(description='pyHorses3D - Python interface for the Horses3D CFD solver')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Run simulation command
    run_parser = subparsers.add_parser('run', help='Run a Horses3D simulation')
    run_parser.add_argument('solver', help='Path to the Horses3D solver executable')
    run_parser.add_argument('control', help='Path to the control file')
    run_parser.add_argument('--residuals', action='store_true', help='Plot residuals after simulation')
    
    # Process simulation command
    process_parser = subparsers.add_parser('process', help='Process simulation results')
    process_parser.add_argument('solver', help='Path to the Horses3D solver executable')
    process_parser.add_argument('control', help='Path to the control file')
    process_parser.add_argument('--vtk', action='store_true', help='Generate VTK files for visualization')
    
    # Visualize simulation command
    viz_parser = subparsers.add_parser('visualize', help='Visualize simulation results')
    viz_parser.add_argument('solver', help='Path to the Horses3D solver executable')
    viz_parser.add_argument('control', help='Path to the control file')
    viz_parser.add_argument('--variable', default='V', help='Variable to visualize (V, p, T, M)')
    viz_parser.add_argument('--plane', default='XY', help='Plane to visualize (XY, XZ, YZ)')
    viz_parser.add_argument('--value', type=float, default=0, help='Position value for plane')
    viz_parser.add_argument('--streamlines', action='store_true', help='Plot streamlines')
    
    # Example workflow command
    example_parser = subparsers.add_parser('example', help='Run an example workflow')
    example_parser.add_argument('solver', help='Path to the Horses3D solver executable')
    example_parser.add_argument('control', help='Path to the control file')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    # Handle commands
    if args.command == 'run':
        run_simulation(args.solver, args.control, args.residuals)
    elif args.command == 'process':
        process_simulation(args.solver, args.control, args.vtk)
    elif args.command == 'visualize':
        visualize_simulation(args.solver, args.control, args.variable, args.plane, args.value, args.streamlines)
    elif args.command == 'example':
        run_example(args.solver, args.control)

def run_simulation(solver_path, control_file, plot_residuals=False):
    """
    Run a Horses3D simulation.
    
    Args:
        solver_path (str): Path to the Horses3D solver executable
        control_file (str): Path to the control file
        plot_residuals (bool, optional): Whether to plot residuals after the simulation.
                                        Defaults to False.
    """
    print(f"Running simulation with control file: {control_file}")
    solver = Horses3D(solver_path, control_file)
    solver.control.loadControlFile()
    solver.runHorses3D(plotResiduals=plot_residuals)
    print("Simulation completed successfully")

def process_simulation(solver_path, control_file, generate_vtk=False):
    """
    Process simulation results.
    
    Args:
        solver_path (str): Path to the Horses3D solver executable
        control_file (str): Path to the control file
        generate_vtk (bool, optional): Whether to generate VTK files for visualization.
                                      Defaults to False.
    """
    print(f"Processing simulation results for control file: {control_file}")
    solver = Horses3D(solver_path, control_file)
    solver.control.loadControlFile()
    
    try:
        # Get solution files
        solution_files = solver.getSolutionFileNames()
        print(f"Found {len(solution_files)} solution files")
        
        # Load the most recent solution
        if solution_files:
            solver.solution.loadSingleSolution(solution_files[-1])
            
            # Compute derived quantities
            print("Computing derived quantities...")
            solver.solution.computeVelocityMagnitude(0)
            solver.solution.computePressure(0)
            solver.solution.computeTemperature(0)
            solver.solution.computeSpeedOfSound(0)
            solver.solution.computeMach(0)
            
            print("Derived quantities computed:")
            for key in solver.solution.magnitudes.keys():
                print(f"  {key} at index {solver.solution.magnitudes[key]}")
            
            # Generate VTK files if requested
            if generate_vtk:
                print("VTK file generation is not yet implemented")
                # TODO: Implement VTK file generation
        else:
            print("No solution files found")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

def visualize_simulation(solver_path, control_file, variable='V', plane='XY', value=0, streamlines=False):
    """
    Visualize simulation results.
    
    Args:
        solver_path (str): Path to the Horses3D solver executable
        control_file (str): Path to the control file
        variable (str, optional): Variable to visualize. Defaults to 'V'.
        plane (str, optional): Plane to visualize. Defaults to 'XY'.
        value (float, optional): Position value for plane. Defaults to 0.
        streamlines (bool, optional): Whether to plot streamlines. Defaults to False.
    """
    print(f"Visualizing simulation results for control file: {control_file}")
    solver = Horses3D(solver_path, control_file)
    solver.control.loadControlFile()
    
    try:
        # Get solution files
        solution_files = solver.getSolutionFileNames()
        print(f"Found {len(solution_files)} solution files")
        
        # Load the most recent solution
        if solution_files:
            solver.solution.loadSingleSolution(solution_files[-1])
            
            # Compute derived quantities if needed
            if variable == 'V' and 'V' not in solver.solution.magnitudes:
                solver.solution.computeVelocityMagnitude(0)
            elif variable == 'p' and 'p' not in solver.solution.magnitudes:
                solver.solution.computePressure(0)
            elif variable == 'T' and 'T' not in solver.solution.magnitudes:
                solver.solution.computeTemperature(0)
            elif variable == 'M' and 'M' not in solver.solution.magnitudes:
                solver.solution.computeMach(0)
            
            # Get mesh files
            mesh_files = solver.getHMeshFileName()
            if mesh_files:
                solver.mesh.loadMesh(mesh_files[0])
                
                # Update plot magnitudes
                solver.plot.modifyMagnitudes(solver.solution.magnitudes)
                
                # Plot requested variable
                if variable in solver.solution.magnitudes:
                    print(f"Plotting {variable} in {plane} plane at value {value}")
                    solver.plot.plot2DField(solver.mesh.mesh[0], solver.solution.solution[0], variable, 
                                           plane=plane, value=value, cmap='jet', isocontours=True)
                else:
                    print(f"Variable {variable} not available. Available variables:")
                    for key in solver.solution.magnitudes.keys():
                        print(f"  {key}")
                
                # Plot streamlines if requested
                if streamlines:
                    print(f"Plotting streamlines in {plane} plane at value {value}")
                    solver.plot.plot2DStreamlines(solver.mesh.mesh[0], solver.solution.solution[0], 
                                                 plane=plane, value=value, cmap='cool')
            else:
                print("No mesh files found")
        else:
            print("No solution files found")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

def run_example(solver_path, control_file):
    """
    Run an example workflow.
    
    Args:
        solver_path (str): Path to the Horses3D solver executable
        control_file (str): Path to the control file
    """
    print(f"Running example workflow with control file: {control_file}")
    try:
        full_workflow_example(control_file, solver_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 