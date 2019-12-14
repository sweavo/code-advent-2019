#!python3
import sys

sys.path.append('../10')

import solution
from tapes import DAY11PROGRAM

TURN_LEFT=0
TURN_RIGHT=1
def turn( facevector, direction ):
    """
    >>> turn( (0,-1), TURN_LEFT)
    (-1, 0)
    >>> turn( (-1,0), TURN_LEFT)
    (0, 1)
    >>> turn( (0,1), TURN_LEFT)
    (1, 0)
    >>> turn( (1,0), TURN_LEFT)
    (0,-1)
    >>> turn( (0,-1), TURN_RIGHT)
    (1, 0)
    >>> turn( (1,0), TURN_RIGHT)
    (0, 1)
    >>> turn( (0,1), TURN_RIGHT)
    (-1, 0)
    >>> turn( (-1,0), TURN_RIGHT)
    (0,-1)
    """
    x,y=facevector
    if direction == TURN_LEFT:
        return ( y, -x )
    else:
        return ( -y, x )

class HullPaintingRobot( object ):
    def __init__(self, ground, position ):
        self._ground=ground
        self._x, self._y=position
        self._facing=(0,-1)

    def __next__(self): 
        return 1 if self._ground[self._y][self._x]=='#' else 0



