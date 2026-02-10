# -*- coding: utf-8 -*-
"""
Environment
===========

Initialize spine analysis environment

Note
----
To initialize the main functions in a spine-analysis script use:
>>> from RESPAN.Environment import *
"""

__title__ = "RESPAN"
__author__ = "Luke Hammond <luke.hammond@osumc.edu>"
__license__ = "MIT License (see LICENSE)"
__download__ = "http://www.github.com/lahmmond/RESPAN"


###############################################################################
### Python
###############################################################################


# clean up libraries
import os
import sys

# import pims
import time

import matplotlib.pyplot as plt
import numpy as np
import tifffile
# IPython display helpers are convenient in notebooks but optional for CLI runs
try:
    from IPython.display import clear_output, display
except Exception:
    # Provide simple fallbacks so RESPAN can run without IPython installed
    def clear_output(wait=False):
        # no-op in non-interactive environments
        return

    def display(*args, **kwargs):
        # Lightweight fallback: print first positional argument(s)
        for a in args:
            try:
                print(a)
            except Exception:
                pass

from matplotlib.pyplot import figure
from scipy import ndimage as ndi  # Distance transformation
from skimage import exposure, segmentation
from skimage.io import imread, imsave, imshow, util
from skimage.util import img_as_ubyte

# image processing
import RESPAN.ImageAnalysis.ImageAnalysis as imgan

# low-level helpers used by GUI and scripts
import RESPAN.ImageAnalysis.IO as io
import RESPAN.ImageAnalysis.ModelTraining as mt
import RESPAN.ImageAnalysis.Segmentation_and_Restoration as sr
import RESPAN.ImageAnalysis.SpineTracking as strk
import RESPAN.ImageAnalysis.Validation as val

###############################################################################
### QLEAN
###############################################################################
# Utilities
# Main
import RESPAN.Main.Main as main
import RESPAN.Main.Timer as timer

# analysis


###############################################################################
### All
###############################################################################

__all__ = [
    "sys",
    "os",
    "tifffile",
    "time",
    "np",
    "plt",
    "figure",
    "exposure",
    "segmentation",
    "imread",
    "imsave",
    "imshow",
    "util",
    "img_as_ubyte",
    "ndi",
    "clear_output",
    "display",
    "main",
    "timer",
    "imgan",
    "val",
    "strk",
    "mt",
    "io",
    "sr",
]
