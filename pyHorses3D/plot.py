# plot.py

import matplotlib.pyplot as plt

class Horses3DPlot:
    def plot_solution(self, data):
        plt.plot(data['x'], data['y'])
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Simulation Results')
        plt.show()
    
    def plot_residuals(self, residuals):
        plt.plot(residuals['iterations'], residuals['values'])
        plt.xlabel('Iterations')
        plt.ylabel('Residuals')
        plt.title('Residuals Over Iterations')
        plt.show()
