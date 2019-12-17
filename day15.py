#!python3
""" So it looks like the map is stored inside the intcode program. Thus I'm looking for a way to backtrackingly search for 
    the value 2.

    I will do a depth-first search: at each location I can search all the directions that weren't the one I entered by.

    So it'll be a recursive program that quizzes the droid.

"""
import tapes_day15
import day09
import day13

class FIFO( object ):
    def __init__(self):
        self._queue=[]
    def __iter__(self): return self
    def __next__(self): return self._queue.pop(0)
    def append(self,item): self._queue.append(item)

OPPOSITE_DIRECTION=[None, 2, 1, 4, 3]

class Fifoputer( day09.Intputer ):
    def __init__(self, program ):
        super().__init__( program, FIFO() )

    def interact( self, input_item ):
        self._in.append(input_item)
        return next(self)

def search_directions( fifoputer, entered_by=None ):
    for direction in [1,2,3,4]:
        if direction==entered_by: 
            continue
        result=fifoputer.interact( direction )
        if result==2: # found it!
            # no need to move the bot; we will just pop the stack to measure the distance. 
            return 1 # it was 1 unit away from here

        elif result==1: # We moved; recurse
            result=search_directions( fifoputer, entered_by=OPPOSITE_DIRECTION[direction] )
            if result is not None: # found the goal that way
                return result+1
        else:
            pass
    fifoputer.interact( entered_by ) # If we are backtracking, better put the bot back where we found it.
    return None
   
def day15part1():
    """
    >>> day15part1()
    212
    """
    return search_directions(Fifoputer(tapes_day15.PROGRAM) )

MOVE=[None,
        lambda xy: (xy[0], xy[1]-1),
        lambda xy: (xy[0], xy[1]+1),
        lambda xy: (xy[0]-1, xy[1]),
        lambda xy: (xy[0]+1, xy[1])]

def map_area( fifoputer, area_map={}, location=(0,0), entered_by=None ):
    """
    >>> a={}
    >>> map_area( Fifoputer( tapes_day15.PROGRAM ), a )
    >>> print(day13.render_screen( a, GFX='# *' ))
    """
    
    for direction in [1,2,3,4]:
        if direction==entered_by: 
            continue
        result=fifoputer.interact( direction )
        area_map[MOVE[direction](location)] = result 
        if result > 0: # then we did move
            map_area( fifoputer, area_map, MOVE[direction](location), entered_by=OPPOSITE_DIRECTION[direction] )
    if entered_by is not None:
        fifoputer.interact( entered_by ) # go back whence we came

