#!python3
"""
    Starting at each body that orbits anything, count its direct and indirect orbits.  We do this by first
    extracting the relationship "directly_orbits".  Then for each key in that map, we count the steps to get
    to the COM. Summing the lengths of those paths gives us the answer. Right?

"""
import collections
import functools
import operator

def map_orbitees( pairs ):
    """ Return a map with orbiters as keys and orbitees as values.  This can be used to traverse towards root.
    >>> map_orbitees( ['A)B','A)C','C)D' ] )
    {'B': 'A', 'C': 'A', 'D': 'C'}
    """
    return dict( [ (orbiter, orbitee) for orbitee, orbiter in map( lambda x: x.split(')'), pairs ) ] )

def path_to_root( orbits, start ):
    """ The list of orbitees. Note: does not include the orbiter.
    >>> path_to_root( {'B': 'A', 'C': 'A', 'D': 'C'}, 'D' )
    ['C', 'A']
    """
    path=[]
    cursor = start
    while cursor in orbits:
        cursor = orbits[cursor]
        path.append(cursor)
    return path

def walk_map( direct_orbiters ):
    """ For each leaf and internal node, traverse to the root and return the path traversed.
    >>> list(walk_map( {'B': 'A', 'C': 'A', 'D': 'C'} ))
    [['A'], ['A'], ['C', 'A']]
    """
    for orbiter in direct_orbiters:
        yield path_to_root( direct_orbiters, orbiter )

def count_orbits( direct_orbiters ):
    """ The number of orbits in a path is one less than the number of bodies in it.
    >>> count_orbits( map_orbitees( ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L' ] ) )
    42
    """
    return sum( map( lambda path: len(path),walk_map( direct_orbiters ) ) )

def part1():
    """
    >>> part1()
    358244
    """
    with open('input.txt','r') as f:
        print( count_orbits( map_orbitees( map( str.strip, f ) ) ) )

def chop_common_tails( l1, l2 ):
    """ The paths to me and to santa will end at COM. Here we chop off common tails between two lists
    >>> chop_common_tails( 'ABCDE','ZXCDE' )
    ('AB', 'ZX')
    >>> chop_common_tails( 'ZXABCDE','ZXCDE' )
    ('ZXAB', 'ZX')
    """
    chop=-1
    while l1[chop]==l2[chop]:
        chop-=1
    chop+=1
    return l1[:chop],l2[:chop]
 
if __name__ == "__main__":
    with open('input.txt','r') as f:
        puzzle_input = map_orbitees( map( str.strip, f ) )
    print (sum(map(len, chop_common_tails( path_to_root( puzzle_input, 'YOU' ), path_to_root( puzzle_input, 'SAN' ) ) ) ))

