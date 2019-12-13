#!python3
import math

MAP1=""".#..#
        .....
        #####
        ....#
        ...##"""

BIG_MAP=""" .#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##"""

def tidy_map( space_map ):
    """
    >>> tidy_map(MAP1)
    ['.#..#', '.....', '#####', '....#', '...##']
    """
    return list(map(str.strip,space_map.strip().split('\n')))

def find_rocks( tidy_map ):
    """
    >>> find_rocks(['#'])
    [(0, 0)]
    >>> find_rocks(['.#'])
    [(1, 0)]
    >>> find_rocks(['..','#.'])
    [(0, 1)]
    >>> find_rocks(['#.', '.#'])
    [(0, 0), (1, 1)]
    """
    return [ (x,y)
        for y,line in enumerate(tidy_map)
            for x,char in enumerate(line)
                if char!='.' ]

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

def actually_sees( rocklist, looker, target ):
    """
    >>> world=find_rocks(tidy_map(MAP1))
    >>> actually_sees( world, (1, 0), (3, 4) )
    (2, 2)
    >>> actually_sees( world, (2, 2), (3, 4) )
    (3, 4)
    """
    for position in sightline( looker, target ):
        if position in rocklist:
            return position
    return target

def enum_visible_rocks( rocklist, looker ):
    """ Extracted from count_visible_rocks
    """
    result=set()
    for candidate in filter( lambda x: x!=looker, rocklist ):
        result.add(actually_sees( rocklist, looker, candidate ) )
    return result

def count_visible_rocks( rocklist, looker ):
    """
    >>> rocklist=find_rocks(tidy_map(MAP1))
    >>> count_visible_rocks( rocklist, (3, 4) )
    8
    """
    return len(enum_visible_rocks( rocklist, looker) )

def visibilities( rocklist ):
    """
    >>> list(visibilities(find_rocks(tidy_map(MAP1))))
    [(1, 0, 7), (4, 0, 7), (0, 2, 6), (1, 2, 7), (2, 2, 7), (3, 2, 7), (4, 2, 5), (4, 3, 7), (3, 4, 8), (4, 4, 7)]
    """
    for candidate in rocklist:
        yield (candidate[0], candidate[1], count_visible_rocks( rocklist, candidate ) )

def best_spot( rocklist ):
    """
    >>> best_spot( find_rocks(tidy_map(MAP1)))
    (3, 4, 8)
    >>> best_spot( find_rocks(tidy_map(BIG_MAP)))
    (11, 13, 210)
    """
    return sorted( visibilities( rocklist ), key=lambda x: x[2], reverse=True )[0]

DAY10_MAP="""
                ##.##..#.####...#.#.####
                ##.###..##.#######..##..
                ..######.###.#.##.######
                .#######.####.##.#.###.#
                ..#...##.#.....#####..##
                #..###.#...#..###.#..#..
                ###..#.##.####.#..##..##
                .##.##....###.#..#....#.
                ########..#####..#######
                ##..#..##.#..##.#.#.#..#
                ##.#.##.######.#####....
                ###.##...#.##...#.######
                ###...##.####..##..#####
                ##.#...#.#.....######.##
                .#...####..####.##...##.
                #.#########..###..#.####
                #.##..###.#.######.#####
                ##..##.##...####.#...##.
                ###...###.##.####.#.##..
                ####.#.....###..#.####.#
                ##.####..##.#.##..##.#.#
                #####..#...####..##..#.#
                .##.##.##...###.##...###
                ..###.########.#.###..#.
    """ 

DAY10_ROCKS=find_rocks( tidy_map( DAY10_MAP) )

def day10part1():
    """
    >>> day10part1()
    (14, 17, 260)
    """
    print( best_spot( DAY10_ROCKS ) )

def angle( origin, point ):
    """
    It doesn't matter what the units of this angle are; it doesn't even have 
    to increase at a constant rate.  But it must keep increasing clockwise from
    north and must have a single unambiguous value for a given angle.
    >>> angle( (0,0),(0,-1) )
    0.0
    >>> angle( (0,0),(0,1) )
    3.141592653589793
    >>> angle( (0,0),(1,0) )
    1.5707963267948966
    >>> angle( (0,0),(-1,0) )
    4.71238898038469
    >>> angle( (3,0),(3,-1) )
    0.0
    >>> angle( (0,-2),(0,-1) )
    3.141592653589793
    >>> angle( (4,4),(6,4) )
    1.5707963267948966
    >>> angle( (1,0),(-1,0) )
    4.71238898038469
    """
    x=point[0]-origin[0]
    y=origin[1]-point[1] # our up is -ve
    radians=math.atan2( x, y) 
    if radians<0.0:
        radians = radians + 2*math.pi
    return radians

def angles_relative( origin, points ):
    """
    >>> list(angles_relative( (0,0), [ (0,0), (0,-1), (0,1), (1,0),(-1,0) ] ))
    [(0, -1, 0.0), (0, 1, 3.141592653589793), (1, 0, 1.5707963267948966), (-1, 0, 4.71238898038469)]
    """
    for point in filter( lambda x: x!=origin, points ):
        yield ( point[0], point[1], angle( origin, point ) )

def shooting_sequence_one_pass( base, points ):
    """
    >>> list(shooting_sequence_one_pass( (8,3), find_rocks( tidy_map( '''
    ...    .#....#####...#..
    ...    ##...##.#####..##
    ...    ##...#...#.#####.
    ...    ..#.....#...###..
    ...    ..#.#.....#....## '''))))[:9]
    [(8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1)]
    """
    for point3 in sorted( angles_relative( base, enum_visible_rocks( points, base ) ), key=lambda x: x[2] ):
        yield ( point3[0], point3[1] )

def shooting_sequence( base, points ):
    """
    >>> sequence = list(shooting_sequence( (11, 13), find_rocks( tidy_map( BIG_MAP ) ) ))
    >>> sequence[0]
    (11, 12)
    >>> sequence[1]
    (12, 1)
    >>> sequence[2]
    (12, 2)
    >>> sequence[9]
    (12, 8)
    >>> sequence[19]
    (16, 0)
    >>> sequence[49]
    (16, 9)
    >>> sequence[99]
    (10, 16)
    >>> sequence[198]
    (9, 6)
    >>> sequence[199]
    (8, 2)
    >>> sequence[200]
    (10, 9)
    >>> sequence[298]
    (11, 1)
    >>> len(sequence)
    299
    """
    universe = set( filter( lambda x: x != base, points ))
    last_len=0 
    while len( universe )!=last_len:
        last_len=len(universe)
        shot_in_this_rotation = list(shooting_sequence_one_pass( base, universe ))
        for result in shot_in_this_rotation:
            yield result
        universe = universe - set(shot_in_this_rotation)
    if last_len != 0:
        raise ValueError( "shooting_sequence missed some rocks: " + repr( universe ) )

def rock_id_as_int( rock ):
    return rock[0]*100 + rock[1]

def day10part2():
    """
    >>> day10part2()
    608
    """
    return rock_id_as_int( list( shooting_sequence( ( 14, 17), DAY10_ROCKS ) )[199] )

