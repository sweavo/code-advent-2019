#!python3
import math
import re

RE_QCOMMAW=re.compile(r'\s*(\d+)\s+(\w+)\s*')

EXAMPLE_NANOFACTORY="""
    10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL
"""

def parse_quantity_comma_what( ss ):
    """
    >>> parse_quantity_comma_what('10 ORE')
    (10, 'ORE')
    >>> parse_quantity_comma_what(' 10  ORE ')
    (10, 'ORE')
    """
    q,w = RE_QCOMMAW.match(ss).groups()
    return (int(q),w)

def parse_list_of_qcw( liststring ):
    """
    >>> parse_list_of_qcw( ' 1 A, 2 B' )
    [(1, 'A'), (2, 'B')]
    """
    as_list=liststring.split(',')
    return list(map( parse_quantity_comma_what, as_list ) )

def parse_productions( ss ):
    """
    >>> parse_productions( EXAMPLE_NANOFACTORY )
    [([(10, 'ORE')], (10, 'A')), ([(1, 'ORE')], (1, 'B')), ([(7, 'A'), (1, 'B')], (1, 'C')), ([(7, 'A'), (1, 'C')], (1, 'D')), ([(7, 'A'), (1, 'D')], (1, 'E')), ([(7, 'A'), (1, 'E')], (1, 'FUEL'))]
    """
    result=[]
    lines = map(str.strip, ss.strip().split('\n'))
    for line in lines:
        lhs,_,rhs=map(str.strip, line.partition('=>'))
        result.append( (parse_list_of_qcw(lhs),parse_quantity_comma_what(rhs)) )
    return result

def prepare_factory( reactions ):
    """
    Given the result of the parsed productions, create a reverse lookup: to get X you 
    need Y,Z,... and you will get x of them.
    >>> prepare_factory( [([(1,'A')],(1,'B'))] )
    {'B': (1, [(1, 'A')])}
    """
    result = {}
    for inputs,output in reactions:
        quantity, ingredient = output
        result[ingredient]=(quantity,inputs)
    return result

def ceildiv( needed, per_run ):
    """ Calculate the number of runs needed if you need x and each run yields y
    >>> ceildiv( 1, 1)
    1
    >>> ceildiv( 3, 2)
    2
    >>> ceildiv( 10, 20)
    1
    """
    return math.ceil( needed / per_run )

class Factory( object ):
    """
    >>> import collections
    >>> collections.Counter( Factory( EXAMPLE_NANOFACTORY ).require(1,'FUEL').bill_of_materials( ['ORE'] ) )
    Counter({'ORE': -31})
    """
    def __init__( self, program ):
        self._productions = prepare_factory( parse_productions( program ) )
        self._inventory={}
  
    def require(self, quantity, chemical ):
        """ Mark in the inventory that a quantity of a chemical is wanted. """
        result = self._inventory.get(chemical,0)-quantity
        if result == 0:
            del self._inventory[chemical]
        else:
            self._inventory[chemical] = result
        return self

    def credit( self, quantity, chemical ):
        result = self._inventory.get(chemical,0)+quantity
        if result == 0:
            del self._inventory[chemical]
        else:
            self._inventory[chemical] = result
        return self
 
    def first_deficit( self, terminals ):
        """ return a chemical that is lacking in the inventory, and how many
            units of same, or (None, 0) if no such chemical.
        """
        for chemical, quantity in self._inventory.items():
            if chemical in terminals:
                continue
            if quantity >= 0:
                continue
            return chemical, quantity
        return None, 0

    def bill_of_materials( self, terminals):
        """
        >>> Factory( "1 A => 1 B" ).require( 1, 'B' ).bill_of_materials( ['A'] )
        {'A': -1}
        >>> Factory( "1 A => 1 B" ).require( 2, 'B' ).bill_of_materials( ['A'] )
        {'A': -2}
        >>> Factory( "1 A, 2 B => 1 C" ).require( 2, 'C').bill_of_materials( ['A', 'B'] )
        {'A': -2, 'B': -4}
        >>> Factory( "1 A, 2 B => 2 C" ).require( 4, 'C').bill_of_materials( ['A', 'B'] )
        {'A': -2, 'B': -4}
        >>> Factory( "1 A, 2 B => 3 C" ).require( 4, 'C').bill_of_materials( ['A', 'B'] )
        {'A': -2, 'B': -4}
        >>> Factory( "1 A, 2 B => 4 C" ).require( 4, 'C').bill_of_materials( ['A', 'B'] )
        {'A': -1, 'B': -2}
        >>> Factory( "1 A, 2 B => 4 C\\n 4 A => 1 B" ).require( 4, 'C').bill_of_materials( ['A', 'B'] )
        {'A': -1, 'B': -2}
        >>> Factory( "1 A, 2 B => 4 C\\n 4 A => 1 B" ).require( 4, 'C').bill_of_materials( ['A'] )
        {'A': -9}
        """
 
        chemical, quantity = self.first_deficit( terminals )
        while quantity<0:
            run_yield, recipe = self._productions[chemical]
            runs=ceildiv( -quantity, run_yield )
            for q, c in recipe:
                self.require( q*runs, c )
            self.credit( run_yield*runs, chemical)
            chemical, quantity = self.first_deficit( terminals )

        return { k: v for k, v in self._inventory.items() if v < 0 }
