#!python3

""" Find the closest (manhattan distance) intersection of two wires.
    https://adventofcode.com/2019/day/3

    model a line as a list of (x,y) tuples.
"""

def pointabs( point ):
    """
    >>> pointabs((-1,1))
    (1, 1)
    >>> pointabs((1,-1))
    (1, 1)
    """
    return tuple(map(abs,point))

def manhattan_distance( point ):
    """
    >>> manhattan_distance( ( 10,10 ) )
    20
    >>> manhattan_distance( ( -10,-10 ) )
    20
    >>> manhattan_distance( ( 10,-10 ) )
    20
    >>> manhattan_distance( ( -10,10 ) )
    20
    """
    return sum( pointabs( point ))

def up_one( point ):
    return  ( point[0], point[1]+1 )

def down_one( point ):
    return  ( point[0], point[1]-1 )

def left_one( point ):
    return  ( point[0]-1, point[1] )

def right_one( point ):
    return  ( point[0]+1, point[1] )

COMMANDS = { 'U': up_one,
             'D': down_one,
             'L': left_one,
             'R': right_one }
def draw( from_point, command ):
    """
    >>> list(draw( (0,0), 'R4' ))
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    """
    direction = COMMANDS[command[0] ]
    distance = int(command[1:])
    point=from_point
    yield point
    for location in range(distance):
        point = direction( point )
        yield point

def common_points( line1, line2 ):
    """
    >>> list( common_points( [ (0,0),(0,1),(0,2) ], [ (1,1),(0,1),(-1,1) ] ))
    [(0, 1)]
    """
    A = set( line1 )
    B = set( line2 )
    return A.intersection( B )

def draw_multi( description ):
    """
    >>> set(draw_multi( "R3,U2,L2,D1" ))
    {(1, 2), (3, 2), (0, 0), (3, 0), (3, 1), (2, 0), (2, 2), (1, 0), (1, 1)}
    """
    commands = description.split(',')
    cursor = (0,0)
    for command in commands:
        for point in draw( cursor, command ):
            yield point
        cursor = point

if __name__ == "__main__":
    with open( 'input.txt', 'r') as f:
        inputs = f.readlines() 

    draw_pointses = map( draw_multi, inputs )
    points = common_points( *draw_pointses )
 
    distances = sorted(map( manhattan_distance, points ))

    print( distances[1] ) # discard 0 b/c it is the origin.

