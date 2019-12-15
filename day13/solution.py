#!python3
import functools

# pull in an Intputer
import sys
sys.path.append('..')
import day9.solution as day9

from tapes import DAY13_PROGRAM

class Cabinet( object ):
    """ This takes an iterator (e.g. Intputer) and draws the results.
    >>> Cabinet( [1,2,3,6,5,4] ).run().show()
    +------+
    |-     |
    |      |
    |      |
    |     O|
    +------+
    """
    def __init__(self,iterable):
        self._iterable=iter(iterable)
        self._screen={} # key=tuple for coords, val = item at that location
   
    def run( self ):
        try:
            while True:
                x=next(self._iterable)
                y=next(self._iterable)
                v=next(self._iterable)
                self._screen[(x,y)] = v
        except StopIteration:
            pass
        return self

    def show( self ):
        GFX=' @#-O'
        minx=functools.reduce(min,map(lambda t:t[0], self._screen))
        maxx=functools.reduce(max,map(lambda t:t[0], self._screen))
        miny=functools.reduce(min,map(lambda t:t[1], self._screen))
        maxy=functools.reduce(max,map(lambda t:t[1], self._screen))
        print('+' + '-'*(maxx-minx) + '-+' )
        for y in range(miny, maxy+1):
            print('|', end='')
            for x in range(minx, maxx+1):
                print ( GFX[self._screen.get( (x,y), 0 ) ], end='' )
            print ('|')
        print('+' + '-'*(maxx-minx) + '-+' )

