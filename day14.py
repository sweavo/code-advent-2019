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
    >>> collections.Counter( Factory( EXAMPLE_NANOFACTORY ).bill_of_materials( { 'FUEL': -1 }, ['ORE'] ) )
    Counter({'ORE': -31})
    """
    def __init__( self, program ):
        self._productions = prepare_factory( parse_productions( program ) )
    
    def bill_of_materials( self, inventory, terminals):
        """ Inventory is a defaultdict(int), representing the number of doses of each chemical
            available.  A negative amount represents the need to produce a chemical, unless its
            name appears in terminals.
        >>> Factory( "1 A => 1 B" ).bill_of_materials( {'B': -1}, ['A'] )
        {'A': -1}
        >>> Factory( "1 A => 1 B" ).bill_of_materials( {'B': -2}, ['A'] )
        {'A': -2}
        >>> Factory( "1 A, 2 B => 1 C" ).bill_of_materials( {'C': -2}, ['A', 'B'] )
        {'A': -2, 'B': -4}
        >>> Factory( "1 A, 2 B => 2 C" ).bill_of_materials( {'C': -4}, ['A', 'B'] )
        {'A': -2, 'B': -4}
        >>> Factory( "1 A, 2 B => 3 C" ).bill_of_materials( {'C': -4}, ['A', 'B'] )
        {'A': -2, 'B': -4}
        >>> Factory( "1 A, 2 B => 4 C" ).bill_of_materials( {'C': -4}, ['A', 'B'] )
        {'A': -1, 'B': -2}
        >>> Factory( "1 A, 2 B => 4 C\\n 4 A => 1 B" ).bill_of_materials( {'C': -4}, ['A', 'B'] )
        {'A': -1, 'B': -2}
        >>> Factory( "1 A, 2 B => 4 C\\n 4 A => 1 B" ).bill_of_materials( {'C': -4}, ['A'] )
        {'A': -9}
        """
        def first_deficit( inventory, terminals ):
            for chemical, quantity in inventory.items():
                if chemical in terminals:
                    continue
                if quantity >= 0:
                    continue
                return chemical, quantity
            return None, 0
 
        chemical, quantity = first_deficit( inventory, terminals )
        while quantity<0:
            have_doubts=True
            run_yield, recipe = self._productions[chemical]
            runs=ceildiv( -quantity, run_yield )
            for q, c in recipe:
                inventory[c]=inventory.get(c,0)-q
            inventory[chemical]=inventory.get(chemical,0)+run_yield
            chemical, quantity = first_deficit( inventory, terminals )

        return { k: v for k, v in inventory.items() if v < 0 }
