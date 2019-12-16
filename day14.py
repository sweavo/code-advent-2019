#!python3
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

def translate_factory_string( ss ):
    """
    >>> translate_factory_string( EXAMPLE_NANOFACTORY )
    [([(10, 'ORE')], (10, 'A')), ([(1, 'ORE')], (1, 'B')), ([(7, 'A'), (1, 'B')], (1, 'C')), ([(7, 'A'), (1, 'C')], (1, 'D')), ([(7, 'A'), (1, 'D')], (1, 'E')), ([(7, 'A'), (1, 'E')], (1, 'FUEL'))]
    """
    result=[]
    lines = map(str.strip, ss.strip().split('\n'))
    for line in lines:
        lhs,_,rhs=map(str.strip, line.partition('=>'))
        result.append( (parse_list_of_qcw(lhs),parse_quantity_comma_what(rhs)) )
    return result
