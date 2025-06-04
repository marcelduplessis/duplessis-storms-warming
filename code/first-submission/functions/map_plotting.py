import cartopy
import cartopy.crs as ccrs
import matplotlib.path as mpath
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# create a function to add gridlines and labels to cartopy plots

import matplotlib.ticker as mticker
import numpy as np

def gridlines(ax):
    
    # Add gridlines and labels
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0, color='gray', alpha=0, linestyle='--', zorder=110)
    
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False 

    gl.xlocator = mticker.FixedLocator([-45, -135, 45, 135])
    
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    gl.ylabel_style = {'fontsize': 10, 'alpha': 0}
    gl.xlabel_style = {'fontsize': 10, 'rotation': 'horizontal'}

    return gl

# function that plots a southern ocean map using cartopy

def southern_ocean_map(ax):

    # load some constants that we use for plotting Southern Ocean maps using Cartopy

    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    ax.set_extent([-180, 180, -90, -40], ccrs.PlateCarree())

    gl = gridlines(ax)   
    
    ax.set_boundary(circle, transform=ax.transAxes)
    ax.add_feature(cfeature.LAND, zorder=100, edgecolor='black', color='0.85')
    ax.add_feature(cfeature.COASTLINE, zorder=100, linewidth=0.25)

    return ax