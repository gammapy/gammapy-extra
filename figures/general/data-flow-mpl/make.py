import logging
import click
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines as mlines
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
matplotlib.rc("text", usetex=True)
matplotlib.rc("font", **{"family": "sans-serif"})
params = {"text.latex.preamble": [r"\usepackage{amsmath}"]}
plt.rcParams.update(params)


FIGSIZE_MM = [180, 131] * u.mm
FIGSIZE = FIGSIZE_MM.to_value("inch")

FOLDER_ICON = np.array(
    [(0, 0), (0, 0.8), (0.08, 1), (0.5, 1), (0.58, 0.8), (0.93, 0.8), (0.93, 0)]
)

DOC_ICON = np.array(
    [(0, 0), (0, 0.85), (0.15, 1), (0.75, 1), (0.75, 0)]
)

GRAY = "gray"
LIGHT_GRAY = "#ECECEC"
GP_GRAY = "#3D3D3D"
GP_ORANGE = "#FC3617"


def axis_to_fig(axis):
    fig = axis.figure

    def transform(coord):
        return fig.transFigure.inverted().transform(axis.transData.transform(coord))

    return transform


def add_sub_axes(axis, rect):
    fig = axis.figure
    left, bottom, width, height = rect
    trans = axis_to_fig(axis)
    figleft, figbottom = trans((left, bottom))
    figwidth, figheight = trans([width, height]) - trans([0, 0])
    return fig.add_axes([figleft, figbottom, figwidth, figheight])


def plot_sub_package_icon(
    ax, offset=(0.5, 0.5), name=".makers", size=(22, 14), color=GP_GRAY, classes=[]
):
    p = Polygon(
        offset + size * FOLDER_ICON, fc="None", ec=color, lw=1, transform=ax.transData
    )
    ax.add_artist(p)

    fontsize_gp = 32
    ax.text(
        offset[0] + 1,
        offset[1] + 5,
        s="$\gamma$",
        size=fontsize_gp,
        va="bottom",
        color=GP_ORANGE,
    )
    ax.text(offset[0] + 6, offset[1] + 5.5, s="$\pi$", size=fontsize_gp, color=color)
    ax.text(offset[0] + 1, offset[1] + 1.5, s=name, size=12, color=color)

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
    kwargs.setdefault("fc", GP_GRAY)
    kwargs.setdefault("ec", "None")
    kwargs.setdefault("head_width", 3)
    kwargs.setdefault("head_length", 3)
    kwargs.setdefault("length_includes_head", True)
    kwargs.setdefault("width", 1)

    arrow = FancyArrow(
        offset[0], offset[1], dx=dx, dy=dy, transform=ax.transData, **kwargs
    )
    ax.add_artist(arrow)


def plot_curved_arrow(ax, posA, posB, **kwargs):
    kwargs.setdefault("connectionstyle", "bar,angle=90,fraction=-0.25")
    kwargs.setdefault("fc", GP_GRAY)
    kwargs.setdefault("ec", GRAY)
    kwargs.setdefault("lw", 3)
    kwargs.setdefault("arrowstyle", "-|>, head_length=3.5, head_width=2")
    kwargs.setdefault("capstyle", "butt")
    kwargs.setdefault("joinstyle", "miter")

    arrow = FancyArrowPatch(posA=posA, posB=posB, transform=ax.transData, **kwargs)
    ax.add_artist(arrow)


def format_dl5_ax(ax):
    for key, spine in ax.spines.items():
        spine.set_color(GP_GRAY)
        spine.set_lw(1)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.patch.set_alpha(0)

    ax.tick_params(axis="both", direction="in", which="both")

    ax.set_xticklabels([])
    ax.set_yticklabels([])


def plot_catalog(ax):
    ax.set_title("Source Catalogs", color=GP_GRAY, pad=4)
    cell_text = [
        ["Name", "Flux", "Size"],
        ["SNR", 1e-12, "1 deg"],
        ["PWN", 1e-11, "0.2 deg"],
        ["GRB", 1e-10, "0 deg"],
    ]

    format_dl5_ax(ax=ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([1/3, 2/3])
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.grid(lw=1, color=GP_GRAY)
    ax.axvspan(0, 1/3, fc="lightgray", ec="None")
    ax.axhspan(0.75, 1, fc="lightgray", ec="None")
    ax.tick_params(axis="both", direction="in", color=GP_GRAY)

    for idx, xpos in enumerate([1/6, 3/6, 5/6]):
        for jdx, ypos in enumerate([7/8, 5/8, 3/8, 1/8]):
            plt.text(xpos, ypos, s=cell_text[jdx][idx], color=GP_GRAY, va="center", ha="center", size=8)


def plot_lightcurve(ax):
    filename = "data/light_curve.fits"
    log.info(f"Reading: {filename}")

    lc = LightCurve.read(filename)
    lc.plot(ax=ax, marker="None", label="1 TeV")
    format_dl5_ax(ax=ax)
    ax.set_ylim(3e-11, 4e-10)
    ax.set_xlim(53945.85, 53946.09)
    ax.legend(fontsize=8, labelspacing=0.1)


def plot_sed(ax):
    filename = "data/flux_points.fits"
    log.info(f"Reading: {filename}")
    flux_points = FluxPoints.read(filename)
    flux_points.table["is_ul"] = flux_points.table["ts"] < 4
    flux_points.plot(
        ax=ax,
        energy_power=2,
        flux_unit="erg-1 cm-2 s-1",
        color="darkorange",
        elinewidth=1,
        markeredgewidth=1,
    )

    flux_points.to_sed_type("e2dnde").plot_ts_profiles(ax=ax, add_cbar=False)
    format_dl5_ax(ax=ax)
    ax.set_title("SEDs \& Lightcurves", color=GP_GRAY, pad=4)


def plot_image(ax):
    filename = "data/flux_image.fits"
    log.info(f"Reading: {filename}")
    m = Map.read(filename)
    m.plot(ax=ax, cmap="inferno", stretch="sqrt")
    ax.set_title("Flux \& TS Maps", color=GP_GRAY, pad=4)
    format_dl5_ax(ax=ax)


def plot_data_levels(ax, ypos=123):
    # data levels
    kwargs = {}
    kwargs["va"] = "center"
    kwargs["ha"] = "center"
    kwargs["transform"] = ax.transData
    kwargs["color"] = GP_GRAY
    kwargs["size"] = 24

    ax.text(15, ypos, "DL3", **kwargs)
    ax.text(80, ypos, "DL4", **kwargs)
    ax.text(160, ypos, "DL5", **kwargs)

    kwargs["size"] = 12
    ax.text(15, ypos - 5, "$\gamma$-like events", **kwargs)
    ax.text(80, ypos - 5, "Binned data", **kwargs)
    ax.text(160, ypos - 5, "Science products", **kwargs)

    # Arrows
    plot_arrow(ax, offset=(27.5, ypos), dx=41.5, fc=GRAY)
    plot_arrow(ax, offset=(92.5, ypos), dx=50, fc=GRAY)

    kwargs["color"] = GRAY
    ax.text(47.5, ypos - 15, "Data reduction", **kwargs)
    ax.text(117.5, ypos - 15, "Likelihood fitting", **kwargs)


def plot_high_level_interface(fig, ax, ypos=24):
    # color = GRAY
    # p2 = (5, ypos + 0.5)
    # p1 = (135, ypos + 0.5)
    # curlyBrace(
    #     fig, ax, p1, p2, k_r=0.025, bool_auto=True, color=color, lw=2, int_line_num=1
    # )

    x, y = np.array([[5, 5, 135, 135], [ypos, ypos - 2, ypos - 2, ypos]])
    line = mlines.Line2D(x, y, lw=3, color=GRAY)
    ax.add_line(line)

    x, y = np.array([[68, 68], [ypos - 4, ypos - 2]])
    line = mlines.Line2D(x, y, lw=3, color=GRAY)
    ax.add_line(line)

    offset = (40, ypos - 21.5)
    plot_sub_package_icon(ax, offset=(offset[0] + 22, ypos - 21.5), name=".analysis")

    size = 14
    p = Polygon(
        offset + size * DOC_ICON, fc="None", ec=GRAY, lw=1, transform=ax.transData
    )
    ax.add_artist(p)

    ax.text(
        offset[0] + size * 0.75 / 2,
        offset[1] + size / 2,
        "YAML",
        va="center",
        ha="center",
        color=GRAY,
        fontweight="black"
    )

    plot_arrow(ax=ax, offset=(offset[0] + size * 0.74 + 1, offset[1] + size / 2), fc=GRAY)


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

    plot_data_levels(ax=ax)
    plot_high_level_interface(fig=fig, ax=ax)

    ymin = 0.2
    ymax = 0.85
    ax.axvspan(32, 62, fc=LIGHT_GRAY, ec="None", ymin=ymin, ymax=ymax)
    ax.axvspan(100, 135, fc=LIGHT_GRAY, ec="None", ymin=ymin, ymax=ymax)

    kwargs = {}
    kwargs["head_width"] = 13
    kwargs["head_length"] = 3
    plot_arrow(ax, offset=(27.5, 56), dx=41, width=13, fc=LIGHT_GRAY, **kwargs)
    plot_arrow(ax, offset=(93, 56), dx=21, width=13, fc=LIGHT_GRAY, **kwargs)

    xpos = 120
    plot_arrow(ax, offset=(xpos, 35), dx=23, width=13, fc=LIGHT_GRAY, **kwargs)
    plot_arrow(ax, offset=(xpos, 64), dx=23, width=13, fc=LIGHT_GRAY, **kwargs)
    plot_arrow(ax, offset=(xpos, 96), dx=23, width=13, fc=LIGHT_GRAY, **kwargs)

    classes = ["DataStore", "Observations", "Observation", "GTI"]
    plot_sub_package_icon(ax, offset=(5, 50), name=".data", classes=classes)

    classes = [
        "MapDatasetMaker",
        "SafeMaskMaker",
        "FoVBackgroundMaker",
        "RingBackgroundMaker",
        "etc.",
    ]
    plot_sub_package_icon(
        ax, offset=(34, 50), name=".makers", color=GRAY, classes=classes
    )

    classes = ["Datasets", "MapDataset", "MapDatasetOnOff", "etc."]
    plot_sub_package_icon(ax, offset=(70, 50), name=".datasets", classes=classes)

    classes = ["FluxPointsEstimator", "FluxMapEstimator", "etc."]
    plot_sub_package_icon(
        ax, offset=(105, 40), name=".estimators", color=GRAY, classes=classes
    )

    classes = ["Fit, Models, SkyModel", "FoVBackgroundModel", "etc."]
    plot_sub_package_icon(
        ax, offset=(105, 80), name=".modeling", color=GRAY, classes=classes
    )

    if draft:
        plt.grid(alpha=0.2, lw=0.5)
    else:
        ax.set_axis_off()

    ax_image = add_sub_axes(ax, [145, 54, 30, 20])
    plot_image(ax=ax_image)

    ax_fp = add_sub_axes(ax, [145, 25, 30, 20])
    plot_sed(ax=ax_fp)

    ax_lc = add_sub_axes(ax, [145, 4, 30, 20])
    plot_lightcurve(ax=ax_lc)

    ax_cat = add_sub_axes(ax, [145, 86, 30, 20])
    plot_catalog(ax=ax_cat)

    filename = "data-flow-gammapy.pdf"
    log.info(f"Writing {filename}")
    plt.savefig(filename, dpi=300)

    filename = "data-flow-gammapy.png"
    log.info(f"Writing {filename}")
    plt.savefig(filename, dpi=300)


if __name__ == "__main__":
    main()
