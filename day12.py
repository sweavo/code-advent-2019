#!python3

import operator

def sgn( x ):
    """ UNBELIEVABLY python3 does not have sgn, nor 
        does it have cmp with which to implement it.
    >>> sgn(0)
    0
    >>> sgn(-2)
    -1
    >>> sgn(200)
    1
    """
    return 1 if x>0 else 0 if x==0 else -1

def relsgn(lhs, rhs):
    """ sign as a binary operator that tells 
        you which way the rhs is from the lhs
    """
    return sgn(rhs-lhs)

def compare_triple( us, them ):
    """ 
    >>> compare_triple((0, 0, 0), (1, 1, 1))
    (1, 1, 1)
    >>> compare_triple((1, 1, 1), (1, 1, 1))
    (0, 0, 0)
    >>> compare_triple((2, 2, 2), (1, 1, 1))
    (-1, -1, -1)
    >>> compare_triple((-10, 20, 0), (0, 10, 10))
    (1, -1, 1)
    """ 
    return tuple_binop( relsgn, us, them)

def tuple_binop( binop, lhs ,rhs ):
    return tuple([ binop(lhv, rhv) for lhv, rhv in zip(lhs, rhs)])

def add_triple( t1, t2 ):
    return  tuple_binop( operator.add, t1, t2 )

def sub_triple( t1, t2 ):
    return  tuple_binop( operator.sub, t1, t2 )

class Moon(object):
    def __init__(self, pos):
        self._pos=pos
        self._vel=(0, 0, 0)
    
    def gravitate(self, other):
        accel=compare_triple(self._pos, other._pos)
        self._vel=add_triple(self._vel, accel)
        other._vel=sub_triple(other._vel, accel)

    def move(self):
        self._pos=add_triple(self._pos, self._vel)
    
    def energy(self):
        return sum(map(abs,self._pos)) * sum(map(abs,self._vel))
 
FIRST_EXAMPLE=[
    (-1,0,2),
    (2,-10,-7),
    (4,-8,8),
    (3,5,-1) ]

SECOND_EXAMPLE=[
    (-8,-10,0),
    (5,5,10),
    (2,-7,3),
    (9,-8,-3) ]

PUZZLE_INPUT=[ 
    (-16, -1, -12),
    (0, -4, -17),
    (-11, 11, 0),
    (2, 2, -6 ) ]

class Universe( object ):
    """
    >>> u=Universe( FIRST_EXAMPLE )
    >>> u.dump()
    (-1, 0, 2, 0, 0, 0)
    (2, -10, -7, 0, 0, 0)
    (4, -8, 8, 0, 0, 0)
    (3, 5, -1, 0, 0, 0)
    >>> u.tick()
    >>> u.dump()
    (2, -1, 1, 3, -1, -1)
    (3, -7, -4, 1, 3, 3)
    (1, -7, 5, -3, 1, -3)
    (2, 2, 0, -1, -3, 1)
    >>> u.tick()
    >>> u.dump()
    (5, -3, -1, 3, -2, -2)
    (1, -2, 2, -2, 5, 6)
    (1, -4, -1, 0, 3, -6)
    (1, -4, 2, -1, -6, 2)
    >>> u.tick()
    >>> u.tick()
    >>> u.tick()
    >>> u.tick()
    >>> u.tick()
    >>> u.tick()
    >>> u.tick()
    >>> u.tick()
    >>> u.dump()
    (2, 1, -3, -3, -2, 1)
    (1, -8, 0, -1, 1, 3)
    (3, -6, 1, 3, 2, -3)
    (2, 0, 4, 1, -1, -1)
    >>> u.energy()
    179
    >>> u=Universe( SECOND_EXAMPLE )
    >>> for i in range(100): u.tick()
    >>> u.energy()
    1940
    """ 
    def __init__(self, moon_locations ):
        self._moons=list(map(Moon, moon_locations))

    def tick( self ):
        for ii, moon in enumerate(self._moons):
            for j in range(ii+1, len(self._moons)):
                moon.gravitate( self._moons[j] )
        list(map(Moon.move, self._moons))

    def dump( self ):
        for moon in self._moons:
            print( moon._pos + moon._vel )

    def energy( self ):
        return sum( map(Moon.energy, self._moons) )

def day12part1():
    """
    >>> day12part1()
    5517
    """
    u=Universe(PUZZLE_INPUT)
    for ii in range(1000):
        u.tick()
    return u.energy()
