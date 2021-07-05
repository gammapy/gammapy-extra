"""
Script to simulate a gammapy logo shaped source on the sky.
"""

import os

import logging
log = logging.getLogger(__name__)

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

import imageio
import tqdm
from gammapy.maps import Map, WcsGeom
from gammapy.utils.scripts import make_path


EVENTS_PER_TIME_INTERVAL = 6_000
DPI = 100


def get_gp_logo_map():
    data = imageio.imread("/Users/adonath/github/adonath/gammapy-extra/logo/gammapy_logo.png")
    data = np.flipud(data.sum(axis=-1))

    gp_map = Map.create(npix=(527, 369), binsz=0.02)
    gp_map.data = data > 1
    
    geom = WcsGeom.create(npix=(1920, 1080), binsz=0.01)

    gp_map_large = gp_map.interp_to_geom(geom=geom)
    gp_map_large = gp_map_large.smooth("0.15 deg")
    gp_map_large.data = gp_map_large.data / gp_map_large.data.sum()
    return gp_map_large

def animate(n, image, counts, npred):
    events = npred.sample_coord(n_events=EVENTS_PER_TIME_INTERVAL, random_state=n)
    counts.fill_by_coord(events)
    image.set_data(counts.data)
    return image

def main():
    fig = plt.figure(figsize=(6.4, 3.6))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    signal = get_gp_logo_map()
    background = Map.from_geom(signal.geom, data=1)
    background /= background.data.sum()

    npred = (signal + (background * 10)) / 2.
    
    counts = Map.from_geom(geom=npred.geom)

    image = ax.imshow(
        counts.data,
        cmap='afmhot',
        origin='lower',
        vmin=0,
        vmax=7,
        interpolation='None'
    )

    anim = FuncAnimation(fig, animate, fargs=[image, counts, npred],
                         frames=200, interval=50)

    filename = "gammapy_logo.gif"
    anim.save(filename, writer="ffmpeg", dpi=DPI)
	

if __name__ == '__main__':
	main()