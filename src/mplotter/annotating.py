# Copyright (c) 2021 Marco Rigobello, MIT License

import math
from itertools import count
from string import ascii_lowercase

import numpy as np
import matplotlib as mpl

__all__ = [
    'enum_axes',
    'SignedScalarFormatter',
    'SSDecimalFormatter',
    'SSFractionFormatter',
]


def enum_axes(axs, loc, fmt='({})', enum='letters', **at_kw):
    """
    Labels subfigures (axes).

    Parameters
    ----------
    axs : iterable[matplotlib.axes.Axes]
        Axes to be labelled.
    loc : str
        Label location, passed to matplotlib.offsetbox.AnchoredText.
    fmt : str, default '({})'
        Label format string.
    enum : str or iterable, default 'letters'
        Provides the labels via iteration. Special values:
        ('letters' | 'numbers') for (alphabetic | numeric) enumeration.
    **at_kw :
        Keyword arguments for matplotlib.offsetbox.AnchoredText.

    Returns
    -------
    list[matplotlib.offsetbox.AnchoredText]
        The added labels.
    """
    axs = np.asanyarray(axs)

    if enum == 'letters':
        enum = ascii_lowercase
    elif enum == 'numbers':
        enum = count(start=1)

    at_kw.setdefault('frameon', False)
    at_kw.setdefault('borderpad', 0)

    return [
        ax.add_artist(mpl.offsetbox.AnchoredText(fmt.format(e), loc, **at_kw))
        for e,
        ax in zip(enum, axs.flat)
    ]


class ScaledFormatter(mpl.ticker.Formatter):

    def __init__(self, unit=1, squeeze=True):
        super().__init__()
        try:
            self.base, self.mark = unit
        except TypeError:
            self.base = unit
            self.mark = ''
        self.squeeze = squeeze

    def __call__(self, val, pos=None):
        val /= self.base
        mark = self.mark
        if self.squeeze:
            if val == 0:
                mark = ''
            elif val == 1 and self.mark:
                val = ''
        return val, mark


class SignedFormatter(mpl.ticker.Formatter):

    def __init__(self, sign=None, sign_zero=True):
        super().__init__()
        self._init_sign = sign
        self.sign_zero = sign_zero

    def set_locs(self, locs):
        super().set_locs(locs)
        sign = self._init_sign
        if sign is None:
            sign = np.any(np.asanyarray(self.locs) < 0)
        self.sign = sign

    def __call__(self, val, pos=None):
        if val < 0:
            return '-'
        elif self.sign and (val > 0 or self.sign_zero):
            return '+'
        else:
            return ''


class SgnScalarFormatter(SignedFormatter, mpl.ticker.ScalarFormatter):

    def __init__(self, sign=None, **kwargs):
        SignedFormatter.__init__(self, sign)
        mpl.ticker.ScalarFormatter.__init__(self, **kwargs)

    def set_locs(self, locs):
        SignedFormatter.set_locs(self, locs)
        mpl.ticker.ScalarFormatter.set_locs(self, locs)
        if self.sign:
            # first replace is likely pointless
            self.format = self.format.replace('%+', '%').replace('%', '%+')


class SSDecimalFormatter(SignedFormatter, ScaledFormatter):

    def __init__(self, digits, sign=None, sign_zero=True, unit=1):
        SignedFormatter.__init__(self, sign, sign_zero)
        ScaledFormatter.__init__(self, unit, squeeze=False)
        self.digits = digits

    def __call__(self, val, pos=None):
        sgn = SignedFormatter.__call__(self, val, pos)
        val, mark = ScaledFormatter.__call__(self, abs(val), pos)
        fmt = '${sgn}{val:' + f'.{self.digits}f' + '}{mark}$'
        return fmt.format(sgn=sgn, val=val, mark=mark)


class SSFractionFormatter(SignedFormatter, ScaledFormatter):

    def __init__(
        self,
        D,
        frac=True,
        sign=None,
        sign_zero=False,
        unit=1,
        squeeze=True,
    ):
        SignedFormatter.__init__(self, sign, sign_zero)
        ScaledFormatter.__init__(self, unit, squeeze)
        self.base /= D
        self.D = D
        self.frac = frac
        self.format = {
            'int':
                r'${sgn}{N}{mark}$',
            'frac':
                r'${sgn}\frac{{{N}{mark}}}{{{D}}}$'
                if frac else r'${sgn}{N}{mark}/{D}$',
        }
        if mpl.rcParams['text.usetex']:
            vspace = self.format['frac']
            vspace = vspace.format(sgn='', N=1, D=1, mark=self.mark)
            self.format['int'] += r'\vphantom{{{}}}'.format(vspace)

    def set_axis(self, axis):
        super().set_axis(axis)
        axis.set_major_locator(mpl.ticker.MultipleLocator(self.base))

    def __call__(self, val, pos=None):
        D = self.D
        if self.squeeze:
            _N = round(val / self.base)
            gcd = math.gcd(_N, D)
            val /= gcd
            D //= gcd
        sgn = SignedFormatter.__call__(self, val, pos)
        N, mark = ScaledFormatter.__call__(self, abs(val), pos)
        try:
            N = round(N)
        except TypeError:
            pass
        if D == 1:
            fmt = self.format['int']
        else:
            fmt = self.format['frac']
        return fmt.format(sgn=sgn, N=N, D=D, mark=mark)
