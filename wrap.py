#!/usr/bin/env python

import numpy as np

############################################################### Periodic boundary utility
#periodic boundary for relative position vector
def wrap( vector, box ):
    return vector - np.floor( vector / box + 0.5 ) * box
