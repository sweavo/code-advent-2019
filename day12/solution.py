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
    def __init__( self, pos ):
        self._pos=pos
        self._vel=(0, 0, 0)
    
    def gravitate( self, other ):
        accel=compare_triple( self._pos, other._pos )
        self._vel = add_triple( self._vel, accel )

