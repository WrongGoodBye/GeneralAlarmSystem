import os
import sys
from numpy.random import *


def get_status():
    status = 0

    if rand()<0.5:
        status=1
    else:
        status=2
        
    return status



    
