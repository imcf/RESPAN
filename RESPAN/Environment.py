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
from IPython.display import clear_output, display
from matplotlib.pyplot import figure
from scipy import ndimage as ndi  # Distance transformation
from skimage import exposure, segmentation
from skimage.io import imsave, imshow, util
from skimage.util import img_as_ubyte

# image processing
import RESPAN.ImageAnalysis.ImageAnalysis as imgan

# low-level helpers used by GUI and scripts
import RESPAN.ImageAnalysis.IO as respan_io
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
from RESPAN.ImageAnalysis.IO import imread

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
    "respan_io",
    "sr",
]
