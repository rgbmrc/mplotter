import logging
import sys

import matplotlib.pyplot as plt
import numpy as np

import src.mplotter as plotter

# capture mplotter logs
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# load example style sheets & set savefig.directory
plotter.use_style(['styles/rgbmrc.mplstyle', 'styles/quanthep.mplstyle'])
plotter.use_style({'savefig.directory': 'demo'})

fig = plt.figure('demo')
gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[7, 1], hspace=0.33)

# showcase cycler
plt.subplot(gs[1])
for x in range(len(plt.rcParams['axes.prop_cycle'])):
    plt.axvspan(x - 0.5, x + 0.5, fc=f'C{x}')  # cycle style colors
plt.yticks([])
plt.xlabel('palette color number')

# monochrome colormap with transparency
dat = np.random.random((5, 7))
plt.register_cmap(cmap=plotter.coloring.lucid_cmap('C0'))
plt.subplot(gs[0])
plt.rc('image', cmap='C0_lucid')  # make the default cmap
plt.imshow(dat, aspect='auto')

# enumerate subplots
lbls = plotter.annotating.enum_axes(fig.get_axes(), loc='center')
if np.take(dat, dat.size // 2) > 0.66:
    lbls[1].txt._text.set_color('C5')

# set actual size of the figure in figure.figsize (slide) units
plotter.set_fig_size(fig, width=0.33, ratio=1)  # 1/3 width, 2:3 aspect

# save using the figure's label as name, and the directory and format
# from the rc parameters
plotter.save_fig(fig)
