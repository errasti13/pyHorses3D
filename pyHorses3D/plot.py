import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

class Horses3DPlot:

    def __init__(self):
        self.magnitudes = {'rho': 0, 'rhou': 1, 'rhov': 2, 'rhow': 3, 'rhoe': 4}
        self.colorbar_labels = {0: r'$\rho$', 1: r'$\rho u$', 2: r'$\rho v$', 3: r'$\rho w$', 4: r'$\rho e$'}

    def _validate_key(self, key):
        if key not in self.magnitudes:
            raise ValueError(f"Invalid key. Please provide one of: {', '.join(self.magnitudes.keys())}.")
        
    def modifyMagnitudes(self, magnitudes):
        self.magnitudes = magnitudes
        for key, index in magnitudes.items():
            if index not in self.colorbar_labels:
                self.colorbar_labels[index] = f'{key}'

    def _extract_coordinates(self, mesh):
        coords = mesh.reshape(-1, 3)
        return coords[:, 0], coords[:, 1], coords[:, 2]

    def _is_2d_mesh(self, mesh):
        try:
            _ = mesh.reshape(-1, 3)[:, 2]
            return False
        except IndexError:
            return True

    def _extract_slice(self, coord_target, value):
        closest_idx = np.abs(coord_target - value).argmin()
        closest_value = coord_target[closest_idx]
        return np.where(np.isclose(coord_target, closest_value))

    def _create_grid(self, x, y):
        num_x = len(np.unique(x))
        num_y = len(np.unique(y))
        xi = np.linspace(x.min(), x.max(), num_x)
        yi = np.linspace(y.min(), y.max(), num_y)
        return np.meshgrid(xi, yi)

    def plot3DField(self, mesh, field, key, cmap='jet'):
        self._validate_key(key)

        if self._is_2d_mesh(mesh):
            self.plot2DField(mesh, field, key, plane='XY', value=0, cmap=cmap)
            return

        fig = plt.figure(figsize=(6, 9))
        ax = fig.add_subplot(111, projection='3d')

        magnitude_index = self.magnitudes[key]
        colorbar_label = self.colorbar_labels[magnitude_index]

        scatter = ax.scatter(mesh.reshape(-1, 3)[:, 0], mesh.reshape(-1, 3)[:, 1], mesh.reshape(-1, 3)[:, 2],
                             c=field[..., magnitude_index].reshape(-1), cmap=cmap)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, aspect=10, orientation='horizontal')
        cbar.set_label(colorbar_label)

        plt.show()

    def plot2DField(self, mesh, field, key, plane='XY', value=0, cmap='jet', isocontours=False, contour_levels=10):
        self._validate_key(key)

        coord_x, coord_y, coord_z = self._extract_coordinates(mesh)
        field = field[..., self.magnitudes[key]].reshape(-1)

        if self._is_2d_mesh(mesh):
            plane = 'XY'
            coord_z = np.zeros_like(coord_x)

        if plane == 'XY':
            idx = self._extract_slice(coord_z, value)
            x, y = coord_x[idx], coord_y[idx]
        elif plane == 'XZ':
            idx = self._extract_slice(coord_y, value)
            x, y = coord_x[idx], coord_z[idx]
        elif plane == 'YZ':
            idx = self._extract_slice(coord_x, value)
            x, y = coord_y[idx], coord_z[idx]
        else:
            raise ValueError("Invalid plane. Please provide 'XY', 'XZ', or 'YZ'.")

        X, Y = self._create_grid(x, y)
        Z = griddata((x, y), field[idx], (X, Y), method='cubic')

        plt.figure(figsize=(10, 7))
        heatmap = plt.imshow(Z, extent=(x.min(), x.max(), y.min(), y.max()), origin='lower', cmap=cmap, aspect='auto')
        cbar = plt.colorbar(heatmap)
        cbar.ax.set_ylabel(self.colorbar_labels[self.magnitudes[key]])
        
        if isocontours:
            plt.contour(X, Y, Z, levels=contour_levels, colors='k')

        plt.xlabel('X' if plane != 'YZ' else 'Y')
        plt.ylabel('Y' if plane != 'XZ' else 'Z')
        plt.title(f'Heatmap in {plane} plane at {"Z" if plane == "XY" else ("Y" if plane == "XZ" else "X")} = {value}')
        plt.show()

    def plot2DStreamlines(self, mesh, field, plane='XY', value=0, cmap='jet'):
        coord_x, coord_y, coord_z = self._extract_coordinates(mesh)
        rhou_field = field[..., self.magnitudes['rhou']].reshape(-1)
        rhov_field = field[..., self.magnitudes['rhov']].reshape(-1)
        rhow_field = field[..., self.magnitudes['rhow']].reshape(-1)

        if self._is_2d_mesh(mesh):
            plane = 'XY'
            coord_z = np.zeros_like(coord_x)

        if plane == 'XY':
            idx = self._extract_slice(coord_z, value)
            x, y, u_slice, v_slice = coord_x[idx], coord_y[idx], rhou_field[idx], rhov_field[idx]
        elif plane == 'XZ':
            idx = self._extract_slice(coord_y, value)
            x, y, u_slice, v_slice = coord_x[idx], coord_z[idx], rhou_field[idx], rhow_field[idx]
        elif plane == 'YZ':
            idx = self._extract_slice(coord_x, value)
            x, y, u_slice, v_slice = coord_y[idx], coord_z[idx], rhov_field[idx], rhow_field[idx]
        else:
            raise ValueError("Invalid plane. Please provide 'XY', 'XZ', or 'YZ'.")

        X, Y = self._create_grid(x, y)
        U = griddata((x, y), u_slice, (X, Y), method='cubic')
        V = griddata((x, y), v_slice, (X, Y), method='cubic')

        speed = np.sqrt(U**2 + V**2)

        plt.figure(figsize=(10, 7))
        plt.streamplot(X, Y, U, V, color=speed, cmap=cmap)
        plt.xlabel('X' if plane != 'YZ' else 'Y')
        plt.ylabel('Y' if plane != 'XZ' else 'Z')
        plt.title(f'Streamlines in {plane} plane at {"Z" if plane == "XY" else ("Y" if plane == "XZ" else "X")} = {value}')
        plt.colorbar(label='Velocity magnitude')
        plt.show()

        return
    
    def plot3DIsoSurface(self, mesh, field, key, isovalue, cmap='jet'): 
        self._validate_key(key)

        # Extract coordinates and field values
        x, y, z = self._extract_coordinates(mesh)
        magnitude_index = self.magnitudes[key]
        field_values = field[..., magnitude_index].reshape(-1)

        # Create a smaller grid for interpolation to reduce memory usage
        num_points = 50  # Adjust this number based on your memory constraints
        xi = np.linspace(x.min(), x.max(), num_points)
        yi = np.linspace(y.min(), y.max(), num_points)
        zi = np.linspace(z.min(), z.max(), num_points)
        X, Y, Z = np.meshgrid(xi, yi, zi)

        # Interpolate field values onto the grid
        field_interp = griddata((x, y, z), field_values, (X, Y, Z), method='linear')

        # Create a 3D plot with isosurfaces
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the isosurface
        try:
            isosurface = ax.contour3D(X, Y, Z, field_interp, levels=[isovalue], cmap=cmap)
        except Exception as e:
            print(f"Error creating isosurface: {e}")
            return

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{self.colorbar_labels[magnitude_index]} Isosurface at Value {isovalue}')

        # Create a colorbar
        mappable = plt.cm.ScalarMappable(cmap=cmap)
        mappable.set_array(field_interp)
        cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, aspect=10)
        cbar.set_label(self.colorbar_labels[magnitude_index])

        plt.show()
        return


    def plotResiduals(self, residuals_data):
        # Initialize lists to store data
        iterations = []
        times = []
        continuity = []
        x_momentum = []
        y_momentum = []
        z_momentum = []
        energy = []

        # Parse residuals data
        for line in residuals_data:
            if line.startswith('#'):  # Skip comment lines
                continue
            # Split the line into columns
            columns = line.split()
            # Extract data from columns
            iterations.append(int(columns[0]))
            times.append(float(columns[1]))
            continuity.append(float(columns[4]))
            x_momentum.append(float(columns[5]))
            y_momentum.append(float(columns[6]))
            z_momentum.append(float(columns[7]))
            energy.append(float(columns[8]))

        # Plot residuals
        plt.figure(figsize=(12, 8))
        plt.semilogy(iterations, continuity, label='Continuity')
        plt.semilogy(iterations, x_momentum, label='X-Momentum')
        plt.semilogy(iterations, y_momentum, label='Y-Momentum')
        plt.semilogy(iterations, z_momentum, label='Z-Momentum')
        plt.semilogy(iterations, energy, label='Energy')
        plt.xlabel('Iterations')
        plt.ylabel('Residuals')
        plt.title('Residuals over Iterations')
        plt.legend()
        plt.grid(True)
        plt.show()