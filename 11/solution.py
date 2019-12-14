#!python3
import numpy as NP

from tapes import DAY11_PROGRAM
import sys
sys.path.append('../10')
import solution as day10solution

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
    (0, -1)
    >>> turn( (0,-1), TURN_RIGHT)
    (1, 0)
    >>> turn( (1,0), TURN_RIGHT)
    (0, 1)
    >>> turn( (0,1), TURN_RIGHT)
    (-1, 0)
    >>> turn( (-1,0), TURN_RIGHT)
    (0, -1)
    """
    x,y=facevector
    if direction == TURN_LEFT:
        return ( y, -x )
    else:
        return ( -y, x )

class HullPaintingRobot( object ):
    """ 
    >>> hpr=HullPaintingRobot( [',,,,,',',,,,,',',,,,,',',,,,,',',,,,,'],(2,2))
    >>> hpr.print_map()
    ,,,,,
    ,,,,,
    ,,^,,
    ,,,,,
    ,,,,,
    >>> hpr.count_painted()
    0
    >>> next(hpr)
    0
    >>> hpr.paint(1)
    >>> hpr.count_painted()
    1
    >>> next(hpr)
    1
    >>> hpr.turn(0)
    >>> hpr.step()
    >>> next(hpr)
    0
    >>> hpr.print_map()
    ,,,,,
    ,,,,,
    ,<#,,
    ,,,,,
    ,,,,,
    """
    COLOR_BLACK=0
    COLOR_WHITE=1
    def __init__(self, ground, position ):
        self._ground=ground
        self._position=position
        self._facing=(0,-1)
        self._painted_coords=set()

    def __next__(self): 
        x,y=self._position
        return 1 if self._ground[y][x]=='#' else 0
    
    def paint(self, color ):
        char='x' if color==self.COLOR_BLACK else '#'
        x,y=self._position
        line=self._ground[y]
        line=line[:x]+char+line[x+1:]
        self._ground[y]=line
        self._painted_coords.add( self._position )

    def turn(self, direction ):
        self._facing=turn(self._facing, direction )

    def step(self):
        self._position = tuple(NP.add(self._position, self._facing ))
    
    def count_painted(self):
        return len(self._painted_coords)

    def consume( self, iterable ):
        it=iter(iterable)
        try:
            while True:
                self.paint(next(it))
                self.turn(next(it))
                self.step()
        finally:
            pass

    def showbot(self):
        if self._facing==(0,-1): return '^'
        elif self._facing==(0,1): return 'v'
        elif self._facing==(-1,0): return '<'
        elif self._facing==(1,0): return '>'

    def print_map( self ):
        for y,line in enumerate( self._ground ):
            for x,char in enumerate( line ):
                if (x,y) == self._position:
                    print (self.showbot(),end="")
                else:
                    print (char,end="")
            print ('')

