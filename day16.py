#!python3

def pattern_for_phase( p, size ):
    """ Generator function for the repeating pattern for Flawed Frequency Transmission algorithm
    >>> list(pattern_for_phase( 0, 5 ))
    [1, 0, -1, 0, 1]
    >>> list(pattern_for_phase( 0, 15 ))
    [1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1]
    >>> list(pattern_for_phase( 1, 15 ))
    [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1]
    >>> list(pattern_for_phase( 2, 15 ))
    [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1]
    """
    for c in range(1,size+1):
        yield [0,1,0,-1][(c//(p+1))%4]

def last_digit( ii ):
    """
    >>> last_digit( 12 )
    '2'
    >>> last_digit( -17 )
    '7'
    >>> last_digit( 0 )
    '0'
    """
    return str(ii)[-1]
