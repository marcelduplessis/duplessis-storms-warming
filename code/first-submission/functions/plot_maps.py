import numpy as np
import matplotlib.path as mpath

def circular_boundary(ax):
    """
    Create a circular boundary for a map plot.

    This function computes a circular boundary in axes coordinates, which can be used as a boundary
    for a map plot. It allows for panning and zooming, ensuring that the boundary remains circular.

    Parameters:
    -----------
    ax : matplotlib.axes._subplots.AxesSubplot
        The axis to which the circular boundary will be applied.

    Returns:
    --------
    None

    Notes:
    ------
    The circular boundary is set using the `set_boundary` method of the provided axis.

    Example:
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    >>> circular_boundary(ax)
    >>> ax.set_theta_zero_location('N')
    >>> ax.set_theta_direction(-1)
    >>> ax.set_rmax(1)
    >>> plt.show()
    """
    # Generate theta values for a complete circle
    theta = np.linspace(0, 2 * np.pi, 100)

    # Define the center and radius of the circle in axes coordinates
    center, radius = [0.5, 0.5], 0.5

    # Calculate the vertices of the circular path
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T

    # Create a matplotlib Path object representing the circular boundary
    circle = mpath.Path(verts * radius + center)

    # Set the circular boundary for the specified axis
    ax.set_boundary(circle, transform=ax.transAxes)
    
    return ax