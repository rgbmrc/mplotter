import logging
import sys

import matplotlib.pyplot as plt
import numpy as np

import mplotter as plotter

# capture mplotter logs
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# load example style sheets & set savefig.directory
plotter.use_style(["styles/rgbmrc.mplstyle", "styles/quanthep.mplstyle"])
plotter.use_style({"savefig.directory": "demo"})

# create figure with label "demo" and set its size in
# figure.figsize (slide) units (1/3 width, 1:1 aspect)
fig = plt.figure("demo", figsize=plotter.fig_size(width=0.33, ratio=1))
gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[7, 1], hspace=0.33)

# showcase cycler
plt.subplot(gs[1])
for x in range(len(plt.rcParams["axes.prop_cycle"])):
    plt.axvspan(x - 0.5, x + 0.5, fc=f"C{x}")  # cycle style colors
plt.yticks([])
plt.xlabel("palette color number")

# monochrome colormap with transparency
plt.register_cmap(cmap=plotter.coloring.lucid_cmap("C0"))
plt.rc("image", cmap="C0_lucid")  # make the default cmap
plt.subplot(gs[0])
dat = np.random.random((5, 7))
plt.imshow(dat, aspect="auto")

# enumerate subplots and change the color of one label
lbls = plotter.annotating.enum_axes(fig.get_axes(), loc="center")
if np.take(dat, dat.size // 2) > 0.66:
    lbls[1].txt._text.set_color("C5")

# adjust size so that the saved figure has the desired size
plotter.set_fig_size(fig)

# save using the figure's label as name, and the directory and format
# from the rc parameters
plotter.save_fig(fig)
