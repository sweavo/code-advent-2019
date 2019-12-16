#!python3
import functools

class Turtle(object):
    def __init__(self,tape):
        self.location=(0,0)
        self.tape = tape
        self.locations=list(self.play())

    def get_locations( self ):
        return self.locations

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

    def distance_at_location( self, point ):
        return self.locations.index(point)+1

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

    pointses = map(Turtle.get_locations,turtles)
   
    crossings = get_crossings( pointses ) 
   
    return manhattan_distance(sorted(crossings,key=manhattan_distance)[0])

def get_crossing_sum( turtles, point ):
    return sum( [ turtle.distance_at_location(point) for turtle in turtles ] )

def calc_cheapest_crossing( tapes ):
    """ 
    >>> calc_cheapest_crossing( [ 'R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83' ] )
    610
    >>> calc_cheapest_crossing( [ 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7' ] )
    410
    """
    turtles = list(map(Turtle,tapes))

    pointses = [ t.locations for t in turtles ]
   
    crossings = get_crossings( pointses ) 

    distances = map( functools.partial( get_crossing_sum, turtles ), crossings )

    return sorted(distances)[0]

def day3part2():
    """
    >>> day3part2()
    5672
    """
    with open('wires.txt','r') as f:
        tapes = f.readlines()
    print (calc_cheapest_crossing( tapes ))

