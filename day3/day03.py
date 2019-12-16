#!python3

class Turtle(object):
    def __init__(self,tape):
        self.location=(0,0)
        self.tape = tape
    
    def U( self, dy):
        for x in range( dy):
            self.location=(self.location[0],self.location[1]+1)
            yield self.location

    def D( self, dy):
        for x in range( dy):
            self.location=(self.location[0],self.location[1]-1)
            yield self.location

    def L( self, dx):
        for x in range( dx):
            self.location=(self.location[0]-1,self.location[1])
            yield self.location

    def R( self, dx):
        for x in range( dx):
            self.location=(self.location[0]+1,self.location[1])
            yield self.location

    def play( self ):
        for instruction in self.tape.split(','):
            op=instruction[0]
            parm=instruction[1:]
            for location in eval(f"self.{op}({parm})"):
                yield location

def manhattan_distance( point ):
    """
    >>> manhattan_distance( (10, 0) )
    10
    >>> manhattan_distance( (3,4) )
    7
    >>> manhattan_distance( (10, -2) )
    12
    >>> manhattan_distance( (-3,4) )
    7
    """
    return sum(map(abs,point))

def get_crossings( pointses ):
    pointsets = list(map(set,pointses))
    return pointsets[0].intersection( pointsets[1] )

def day3part1():
    """
    >>> day3part1()
    731
    """
    with open('wires.txt','r') as f:
        tapes = f.readlines()

    turtles = map(Turtle,tapes)

    pointses = map(Turtle.play,turtles)
   
    crossings = get_crossings( pointses ) 
   
    return manhattan_distance(sorted(crossings,key=manhattan_distance)[0])
def day3part2():
    """
    >>> day3part2()
    5672
    """
    with open('wires.txt','r') as f:
        tapes = f.readlines()
    print (calc_cheapest_crossing( tapes ))


