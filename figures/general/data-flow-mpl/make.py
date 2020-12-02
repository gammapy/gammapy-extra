import logging
import click
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.transforms as mtrans
from matplotlib.patches import Polygon, FancyArrow, PathPatch, FancyArrowPatch
from matplotlib.text import TextPath
from matplotlib.ticker import MultipleLocator
from astropy import units as u
from gammapy.estimators import LightCurve, FluxPoints
from gammapy.maps import Map
from curly_brace import curlyBrace

u.imperial.enable()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Gammapy logo font
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', **{'family': "sans-serif"})
params = {'text.latex.preamble': [r'\usepackage{amsmath}']}
plt.rcParams.update(params)


FIGSIZE_MM = [180, 111] * u.mm
FIGSIZE = FIGSIZE_MM.to_value("inch")

FOLDER_ICON = np.array([(0, 0), (0, 0.8), (0.08, 1), (0.5, 1), (0.58, 0.8), (0.93, 0.8), (0.93, 0)])


def axis_to_fig(axis):
    fig = axis.figure

    def transform(coord):
        return fig.transFigure.inverted().transform(
            axis.transData.transform(coord))

    return transform


def add_sub_axes(axis, rect):
    fig = axis.figure
    left, bottom, width, height = rect
    trans = axis_to_fig(axis)
    figleft, figbottom = trans((left, bottom))
    figwidth, figheight = trans([width,height]) - trans([0,0])
    return fig.add_axes([figleft, figbottom, figwidth, figheight])


def plot_sub_package_icon(ax, offset=(0.5, 0.5), name=".makers", size=(22, 14), color="#3D3D3D", classes=[]):
    p = Polygon(offset + size * FOLDER_ICON, fc="None", ec=color, lw=1, transform=ax.transData)
    ax.add_artist(p)

    fontsize_gp = 32
    ax.text(offset[0] + 1, offset[1] + 5, s="$\gamma$", size=fontsize_gp, va="bottom", color="#FC3617")
    ax.text(offset[0] + 6, offset[1] + 5, s="$\pi$", size=fontsize_gp, color=color)
    ax.text(offset[0] + 1, offset[1] + 1, s=name, size=12, color=color)

    for idx, cls in enumerate(classes):
        ax.text(offset[0], offset[1] - 4 - 4.2 * idx, s=cls, size=8, color=color)


def plot_brace(ax, x, y, scale):
    tp = TextPath((0, 0), "}", size=1)
    trans = (
            mtrans.Affine2D().scale(1, scale)
            + mtrans.Affine2D().rotate(-90)
            + mtrans.Affine2D().translate(x, y)
            + ax.transData
    )
    pp = PathPatch(tp, lw=1, fc="k", transform=trans)
    ax.add_artist(pp)


def plot_arrow(ax, offset, dx=10, dy=0, **kwargs):
    kwargs.setdefault("fc", "#3D3D3D")
    kwargs.setdefault("ec", "None")
    kwargs.setdefault("head_width", 3)
    kwargs.setdefault("head_length", 3)
    kwargs.setdefault("length_includes_head", True)
    kwargs.setdefault("width", 1)

    arrow = FancyArrow(offset[0], offset[1], dx=dx, dy=dy, transform=ax.transData, **kwargs)
    ax.add_artist(arrow)


def plot_curved_arrow(ax, posA, posB, **kwargs):
    kwargs.setdefault("connectionstyle", "bar,angle=90,fraction=-0.3")
    kwargs.setdefault("fc", "#3D3D3D")
    kwargs.setdefault("ec", "gray")
    kwargs.setdefault("lw", 3)
    kwargs.setdefault("arrowstyle", "-|>, head_length=3.5, head_width=2")
    kwargs.setdefault("capstyle", "butt")
    kwargs.setdefault("joinstyle", "miter")

    arrow = FancyArrowPatch(posA=posA, posB=posB, transform=ax.transData, **kwargs)
    ax.add_artist(arrow)


def format_dl5_ax(ax):
    for key, spine in ax.spines.items():
        spine.set_color("#3D3D3D")
        spine.set_lw(1)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.patch.set_alpha(0)

    ax.tick_params(axis="both", direction="in", which="both")

    ax.set_xticklabels([])
    ax.set_yticklabels([])


def plot_lightcurve(ax):
    filename = "data/light_curve.fits"
    log.info(f"Reading: {filename}")

    lc = LightCurve.read(filename)
    lc.plot(ax=ax, marker="o", ms=1)
    format_dl5_ax(ax=ax)
    ax.set_title("Lightcurves", color="#3D3D3D")
    ax.get_legend().remove()


def plot_sed(ax):
    filename = "data/flux_points.fits"
    log.info(f"Reading: {filename}")
    flux_points = FluxPoints.read(filename)
    flux_points.table["is_ul"] = flux_points.table["ts"] < 4
    flux_points.plot(
        ax=ax, energy_power=2, flux_unit="erg-1 cm-2 s-1", color="darkorange", elinewidth=1,
        markeredgewidth=1
    )

    flux_points.to_sed_type("e2dnde").plot_ts_profiles(ax=ax, add_cbar=False)
    format_dl5_ax(ax=ax)
    ax.set_title("SEDs", color="#3D3D3D")


def plot_image(ax):
    filename = "data/flux_image.fits"
    log.info(f"Reading: {filename}")
    m = Map.read(filename)
    m.plot(ax=ax, cmap="inferno", stretch="sqrt")
    ax.set_title("Flux maps")
    format_dl5_ax(ax=ax)


@click.command()
@click.option("--draft", is_flag=True)
def main(draft=True):
    fig = plt.figure(figsize=FIGSIZE)

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIGSIZE_MM[0].value)
    ax.set_ylim(0, FIGSIZE_MM[1].value)

    ax.tick_params(axis="both", direction="in", pad=-20)
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(10))

    classes = ["DataStore", "Observations", "Observation"]
    plot_sub_package_icon(ax, offset=(5, 50), name=".data", classes=classes)

    classes = [
        "MapDatasetMaker",
        "SafeMaskMaker",
        "FoVBackgroundMaker",
        "RingBackgroundMaker",
        "etc."
    ]
    plot_sub_package_icon(ax, offset=(37.5, 50), name=".makers", color="gray", classes=classes)

    classes = ["Datasets", "MapDataset", "MapDatasetOnOff"]
    plot_sub_package_icon(ax, offset=(70, 50), name=".datasets", classes=classes)

    classes = ["FluxPointsEstimator", "FluxMapEstimator"]
    plot_sub_package_icon(ax, offset=(105, 35), name=".estimators", color="gray", classes=classes)

    classes = ["Fit", "Models", "SkyModel", "FoVBackgroundModel"]
    plot_sub_package_icon(ax, offset=(105, 75), name=".modeling", color="gray", classes=classes)

    plot_sub_package_icon(ax, offset=(55, 2), name=".analysis")

    # data levels
    color = "#3D3D3D"
    ypos = 105
    ax.text(15, ypos, "DL3", size=24, transform=ax.transData, va="center", ha="center", color=color)
    ax.text(80, ypos, "DL4", size=24, transform=ax.transData, va="center", ha="center", color=color)
    ax.text(160, ypos, "DL5", size=24, transform=ax.transData, va="center", ha="center", color=color)
    plot_arrow(ax, offset=(27.5, ypos), dx=40, fc="gray")
    plot_arrow(ax, offset=(92.5, ypos), dx=55, fc="gray")

    ypos = 100
    ax.text(47.5, ypos, "Data reduction", size=12, transform=ax.transData, va="center", ha="center", color="gray")
    ax.text(117.5, ypos, "MLE fitting", size=12, transform=ax.transData, va="center", ha="center", color="gray")

    ax.text(15, ypos, "$\gamma$-like events", size=12, transform=ax.transData, va="center", ha="center", color=color)
    ax.text(80, ypos, "Binned datasets ", size=12, transform=ax.transData, va="center", ha="center", color=color)
    ax.text(160, ypos, "Science products", size=12, transform=ax.transData, va="center", ha="center", color=color)

    plot_arrow(ax, offset=(27, 56), fc="gray")
    plot_arrow(ax, offset=(59, 56))

    plot_curved_arrow(ax, posA=(91, 56), posB=(105, 82))

    connectionstyle = "bar,angle=-90,fraction=-0.259"
    plot_curved_arrow(ax, posA=(91, 56), posB=(105, 42), connectionstyle=connectionstyle)

    if draft:
        plt.grid(alpha=0.2, lw=0.5)
    else:
        ax.set_axis_off()

    ax_image = add_sub_axes(ax, [145, 58, 30, 20])
    plot_image(ax=ax_image)

    ax_fp = add_sub_axes(ax, [145, 30, 30, 20])
    plot_sed(ax=ax_fp)

    ax_lc = add_sub_axes(ax, [145, 2, 30, 20])
    plot_lightcurve(ax=ax_lc)

    p2 = (5, 25)
    p1 = (125, 25)
    curlyBrace(fig, ax, p1, p2, k_r=0.03, bool_auto=True, color=color, lw=2, int_line_num=1)

    filename = "overview.pdf"
    log.info(f"Writing {filename}")
    plt.savefig(filename, dpi=300)


if __name__ == "__main__":
    main()