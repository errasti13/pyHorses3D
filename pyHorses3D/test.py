from pyHorses3d import Horses3D

control_file = 'TaylorGreen_HO.control'
solver_path  = '/mnt/c/Users/Jon/Desktop/MUMI/TFM/horses3d_Fernando/horses3d/Solver/bin/horses3d.ns'
solver = Horses3D(solver_path, control_file)

solver.control.controlFilePath = control_file
solver.control.loadControlFile()

solver.runHorses3D()