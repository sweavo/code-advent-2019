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

def walk_map( direct_orbiters ):
    """ For each leaf and internal node, traverse to the root and return the path traversed.
    >>> list(walk_map( {'B': 'A', 'C': 'A', 'D': 'C'} ))
    [['B', 'A'], ['C', 'A'], ['D', 'C', 'A']]
    """
    for orbiter in direct_orbiters:
        path=[orbiter]
        cursor = orbiter
        while cursor in direct_orbiters:
            cursor = direct_orbiters[cursor]
            path.append(cursor)
        yield path

def count_orbits( direct_orbiters ):
    """ The number of orbits in a path is one less than the number of bodies in it.
    >>> count_orbits( map_orbitees( ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L' ] ) )
    42
    """
    return sum( map( lambda path: len(path)-1,walk_map( direct_orbiters ) ) )

if __name__ == "__main__":
    with open('input.txt','r') as f:
        print( count_orbits( map_orbitees( map( str.strip, f ) ) ) )

