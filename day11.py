#!python3
import collections
import functools
import numpy as NP

from tapes import DAY11_PROGRAM
import sys
import day09 as day9

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
    >>> hpr=HullPaintingRobot( )
    >>> hpr.print_map((-2,-2),(2,2))
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
    >>> hpr.print_map((-2,-2),(2,2))
    ,,,,,
    ,,,,,
    ,<#,,
    ,,,,,
    ,,,,,
    >>> hpr.consume( [0,0,1,0,1,0,0,1,1,0,1,0] )
    >>> hpr.print_map((-2,-2),(2,2))
    ,,,,,
    ,,<#,
    ,,,#,
    ,##,,
    ,,,,,
    >>> hpr.count_painted()
    6
    """
    COLOR_BLACK=0
    COLOR_WHITE=1
    def __init__(self):
        self._ground=set()
        self._painted_coords=set()
        self._position=(0,0)
        self._facing=(0,-1)
    def __iter__(self):return self
    def __next__(self): 
        return 1 if self._position in self._ground else 0
    
    def paint(self, color ):
        if color:
            self._ground.add( self._position )
        else:
            self._ground.discard( self._position )
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
        except StopIteration:
            pass

    def showbot(self):
        if self._facing==(0,-1): return '^'
        elif self._facing==(0,1): return 'v'
        elif self._facing==(-1,0): return '<'
        elif self._facing==(1,0): return '>'

    def print_map( self, mincorner, maxcorner ):
        for y in range( mincorner[1], maxcorner[1]+1 ):
            for x in range( mincorner[0], maxcorner[0]+1 ):
                if (x,y) == self._position:
                    print (self.showbot(),end="")
                else:
                    print ('#' if (x,y) in self._ground else ',',end="")
            print ('')

    def print_whole_map( self ):
        minx=functools.reduce(min,map(lambda t:t[0], self._ground))
        maxx=functools.reduce(max,map(lambda t:t[0], self._ground))
        miny=functools.reduce(min,map(lambda t:t[1], self._ground))
        maxy=functools.reduce(max,map(lambda t:t[1], self._ground))
        self.print_map( (minx,miny), (maxx,maxy) )

def run_hpr( tape, start=0 ):
    hpr=HullPaintingRobot( )
    hpr.paint(start)
    brain=day9.Intputer(tape,inputs=hpr )
    hpr.consume(brain)
    return hpr
    
def day11part1():
    """
    >>> day11part1()
    2539
    """
    hpr=run_hpr( DAY11_PROGRAM )
    return hpr.count_painted()

def day11part2():
    """
    >>> day11part2()
    ####,#,,,,####,###,,#,,#,,,##,###,,,##,
    ,,,#,#,,,,#,,,,#,,#,#,#,,,,,#,#,,#,#,,#
    ,,#,,#,,,,###,,###,,##,,,,,,#,#,,#,#,,#
    ,#,,,#,,,,#,,,,#,,#,#,#,,,,,#,###,,####
    #,,,,#,,,,#,,,,#,,#,#,#,,#,,#,#,#,,#,,#
    ####,####,####,###,,#,,#,,##,,#,,#,#,,#
    """
    hpr=run_hpr( DAY11_PROGRAM,1 )
    hpr.print_whole_map()

