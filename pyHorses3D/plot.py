# plot.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

class Horses3DPlot:

    def plot3DField(self, mesh, field, key, cmap = 'jet'):
        fig = plt.figure(figsize=(6, 9))
        ax = fig.add_subplot(111, projection='3d')

        if key not in {'rho', 'rhou', 'rhov', 'rhow', 'rhoe'}:
            raise ValueError("Invalid key. Please provide 'rhou', 'rhov', or 'rhow'.")
        
        magnitudes = {'rho': 0, 'rhou': 1, 'rhov': 2, 'rhow': 3, 'rhoe': 4}
        magnitude_index = magnitudes[key]
        colorbar_label = {0: r'$\rho$', 1: r'$\rho u$', 2: r'$\rho v$', 3: r'$\rho w$', 4: r'$\rho e$'}[magnitude_index]

        scatter = ax.scatter(mesh.reshape(-1, 3)[:, 0], mesh.reshape(-1, 3)[:, 1], mesh.reshape(-1, 3)[:, 2], 
                            c=field[..., magnitude_index].reshape(-1), cmap=cmap)

        # Set labels and titles for the plot
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Create a colorbar for the plot
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, aspect=10, orientation='horizontal')
        cbar.set_label(colorbar_label)

        plt.show()

        return


    def plot2DField(self, mesh, field, key, plane='XY', value=0, cmap='jet'):
        fig, ax = plt.subplots(figsize=(9, 6))

        # Validate the key
        valid_keys = {'rho', 'rhou', 'rhov', 'rhow', 'rhoe'}
        if key not in valid_keys:
            raise ValueError(f"Invalid key. Please provide one of: {', '.join(valid_keys)}.")

        # Define magnitudes and colorbar labels
        magnitudes = {'rho': 0, 'rhou': 1, 'rhov': 2, 'rhow': 3, 'rhoe': 4}
        magnitude_index = magnitudes[key]
        colorbar_labels = {0: r'$\rho$', 1: r'$\rho u$', 2: r'$\rho v$', 3: r'$\rho w$', 4: r'$\rho e$'}

        # Reshape mesh and extract coordinates
        coord_x = mesh.reshape(-1, 3)[:, 0]
        coord_y = mesh.reshape(-1, 3)[:, 1]
        coord_z = mesh.reshape(-1, 3)[:, 2]

        # Flatten field and extract the magnitude of interest
        field = field[..., magnitude_index].reshape(-1)

        # Extract the slice
        if plane == 'XY':
            coord_target = coord_z
            coord_fixed_1, coord_fixed_2 = coord_x, coord_y
            coord_label_1, coord_label_2 = 'X', 'Y'
            coord_slice_label = 'Z'
        elif plane == 'XZ':
            coord_target = coord_y
            coord_fixed_1, coord_fixed_2 = coord_x, coord_z
            coord_label_1, coord_label_2 = 'X', 'Z'
            coord_slice_label = 'Y'
        elif plane == 'YZ':
            coord_target = coord_x
            coord_fixed_1, coord_fixed_2 = coord_y, coord_z
            coord_label_1, coord_label_2 = 'Y', 'Z'
            coord_slice_label = 'X'
        else:
            raise ValueError("Invalid plane. Please provide 'XY', 'XZ', or 'YZ'.")

        closest_idx = np.abs(coord_target - value).argmin()
        closest_value = coord_target[closest_idx]
        idx = np.where(np.isclose(coord_target, closest_value))

        x, y = coord_fixed_1[idx], coord_fixed_2[idx]
        sliced_field = field[idx]

        # Plotting the 2D scatter plot
        scatter = ax.scatter(x, y, c=sliced_field, cmap=cmap)
        ax.set_xlabel(coord_label_1)
        ax.set_ylabel(coord_label_2)
        ax.set_title(f'2D Field Slice for {key} in {plane} plane at {coord_slice_label} = {value}', fontsize=15, pad=20)

        # Create a colorbar for the plot
        cbar = fig.colorbar(scatter, ax=ax, orientation='vertical')
        cbar.set_label(colorbar_labels[magnitude_index], fontsize=12)

        # Show the plot
        plt.show()
        
        return

    def plot2DStreamlines(self, mesh, field, plane='XY', value=0, cmap='jet'):
        # Reshape mesh and extract coordinates
        coord_x = mesh.reshape(-1, 3)[:, 0]
        coord_y = mesh.reshape(-1, 3)[:, 1]
        coord_z = mesh.reshape(-1, 3)[:, 2]

        rhou_field = field[..., 1].reshape(-1)
        rhov_field = field[..., 2].reshape(-1)
        rhow_field = field[..., 3].reshape(-1)

        if plane == 'XY':
            closest_idx = np.abs(coord_z - value).argmin()
            closest_value = coord_z[closest_idx]
            idx = np.isclose(coord_z, closest_value)

            x = coord_x[idx]
            y = coord_y[idx]
            u_slice = rhou_field[idx]
            v_slice = rhov_field[idx]
        elif plane == 'XZ':
            closest_idx = np.abs(coord_y - value).argmin()
            closest_value = coord_y[closest_idx]
            idx = np.isclose(coord_y, closest_value)

            x = coord_x[idx]
            y = coord_z[idx]
            u_slice = rhou_field[idx]
            v_slice = rhow_field[idx]
        elif plane == 'YZ':
            closest_idx = np.abs(coord_x - value).argmin()
            closest_value = coord_x[closest_idx]
            idx = np.isclose(coord_x, closest_value)

            x = coord_y[idx]
            y = coord_z[idx]
            u_slice = rhov_field[idx]
            v_slice = rhow_field[idx]
        else:
            raise ValueError("Invalid plane. Please provide 'XY', 'XZ', or 'YZ'.")

        # Create grid
        xi = np.linspace(x.min(), x.max(), 100)
        yi = np.linspace(y.min(), y.max(), 100)
        X, Y = np.meshgrid(xi, yi)

        # Interpolate velocity components onto regular grid
        U = griddata((x, y), u_slice, (X, Y), method='cubic')
        V = griddata((x, y), v_slice, (X, Y), method='cubic')

        # Calculate the velocity magnitude for coloring
        speed = np.sqrt(U**2 + V**2)

        # Plot streamlines
        plt.figure(figsize=(10, 7))
        plt.streamplot(X, Y, U, V, color=speed, cmap=cmap)
        plt.xlabel('X' if plane != 'YZ' else 'Y')
        plt.ylabel('Y' if plane != 'XZ' else 'Z')
        plt.title(f'Streamlines in {plane} plane at {"Z" if plane == "XY" else ("Y" if plane == "XZ" else "X")} = {value}')
        plt.colorbar(label='Velocity magnitude')
        plt.show()









