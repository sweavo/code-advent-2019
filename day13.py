#!python3
import functools

# pull in an Intputer
import sys
sys.path.append('..')
import day09 as day9

from tapes import DAY13_PROGRAM

def render_screen( screen, GFX=' @#-O' ):
    """ take a dict of coords to int, and render as a list of strings ready
        for printing.
    """
    minx=functools.reduce(min,map(lambda t:t[0], screen))
    maxx=functools.reduce(max,map(lambda t:t[0], screen))
    miny=functools.reduce(min,map(lambda t:t[1], screen))
    maxy=functools.reduce(max,map(lambda t:t[1], screen))
    rendered='+' + '-'*(maxx-minx) + '-+\n' 
    for y in range(miny, maxy+1):
        rendered+='|'
        for x in range(minx, maxx+1):
            rendered+=GFX[screen.get( (x,y), 0 ) ]
        rendered+='|\n'
    rendered+='+' + '-'*(maxx-minx) + '-+\n' 
    return rendered

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
        print(self.get_display(), end='' )

    def get_display( self ):
        return render_screen( self._screen )

def day13part1():
    """
    >>> day13part1()
    341
    """
    display = Cabinet( day9.Intputer( DAY13_PROGRAM ) ).run().get_display()
    return len( list(filter(lambda x: x=='#', display ) ) )

