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

def count_visible_rocks( rocklist, looker ):
    """
    >>> rocklist=find_rocks(tidy_map(MAP1))
    >>> count_visible_rocks( rocklist, (3, 4) )
    8
    """
    result=set()
    for candidate in filter( lambda x: x!=looker, rocklist ):
        result.add(actually_sees( rocklist, looker, candidate ) )
    return len(result)

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

def day10part1():
    """
    >>> day10part1()
    (14, 17, 260)
    """
    print( best_spot( find_rocks( tidy_map( """
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
    """ ) ) ) )


 
