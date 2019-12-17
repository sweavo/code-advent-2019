#!python3
""" So it looks like the map is stored inside the intcode program. Thus I'm looking for a way to backtrackingly search for 
    the value 2.

    I will do a depth-first search: at each location I can search all the directions that weren't the one I entered by.

    So it'll be a recursive program that quizzes the droid.

"""
import tapes_day15
import day09

class FIFO( object ):
    def __init__(self):
        self._queue=[]
    def __iter__(self): return self
    def __next__(self): return self._queue.pop(0)
    def append(self,item): self._queue.append(item)

OPPOSITE_DIRECTION=[None, 2, 1, 4, 3]

fifo=FIFO()
intputer=day09.Intputer( tapes_day15.PROGRAM, fifo )

def request_movement( direction ):
    fifo.append( direction )
    return next(intputer)

def search_directions( request_movement, entered_by=None ):
    for direction in [1,2,3,4]:
        if direction==entered_by: 
            continue
        result=request_movement( direction )
        if result==2: # found it!
            # no need to move the bot; we will just pop the stack to measure the distance. 
            return 1 # it was 1 unit away from here

        elif result==1: # We moved; recurse
            result=search_directions( request_movement, entered_by=OPPOSITE_DIRECTION[direction] )
            if result is not None: # found the goal that way
                return result+1
        else:
            pass
    request_movement( entered_by ) # If we are backtracking, better put the bot back where we found it.
    return None
   
def day15part1():
    """
    >>> day15part1()
    212
    """
    return search_directions(request_movement) 

        
if __name__ == "__main__":
    print (day15part1())

