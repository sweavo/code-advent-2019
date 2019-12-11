#!python3
import math

MAP1=""".#..#
        .....
        #####
        ....#
        ...##"""

def tidy_map( space_map ):
    """
    >>> tidy_map(MAP1)
    ['.#..#', '.....', '#####', '....#', '...##']
    """
    return list(map(str.strip,space_map.strip().split('\n')))

def find_rocks( tidy_map ):
    """
    >>> list(find_rocks(['#']))
    [(0, 0)]
    >>> list(find_rocks(['.#']))
    [(1, 0)]
    >>> list(find_rocks(['..','#.']))
    [(0, 1)]
    >>> list(find_rocks(['#.', '.#']))
    [(0, 0), (1, 1)]
    """
    for y,line in enumerate(tidy_map):
        for x,char in enumerate(line):
            if char!='.':
                yield x,y

def sightline( source, dest ):
    """
    >>> list(sightline( (0,0),(1,1) ) )
    []
    >>> list(sightline( (0,0),(2,2) ) )
    [(1, 1)]
    >>> list(sightline( (1,0),(3,2) ) )
    [(2, 1)]
    >>> list(sightline( (0,1),(2,3) ) )
    [(1, 2)]
    >>> list(sightline( (0,0), (6,3) ) )
    [(2, 1), (4, 2)]
    >>> list(sightline( (0,0), (8,6) ) )
    [(4, 3)]
    >>> list(sightline( (0,0), (-8,6) ) )
    [(-4, 3)]
    >>> list(sightline( (0,0), (8,-6) ) )
    [(4, -3)]
    >>> list(sightline( (0,0), (-8,-6) ) )
    [(-4, -3)]
    """
    delta_x = dest[0]-source[0]
    delta_y = dest[1]-source[1]
    step=math.gcd(delta_x, delta_y)
    step_x=delta_x/step
    step_y=delta_y/step
    for ii in range(1,step):
        yield ( int(source[0] + step_x * ii), int(source[1] + step_y * ii ))
