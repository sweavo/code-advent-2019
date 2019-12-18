#!python3

from signal_day16 import DAY16_SIGNAL

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

def digits_of( signal ):
    """ each digit, treated numerically
    >>> list(digits_of( 123456 ))
    [1, 2, 3, 4, 5, 6]
    >>> list(digits_of( '051627' ))
    [0, 5, 1, 6, 2, 7]
    """
    return map(int,str(signal))

def fft( signal ):
    """
    >>> fft( 12345678 )
    '48226158'
    >>> fft( '48226158' )
    '34040438'
    >>> fft( '34040438' )
    '03415518'
    """ 
    response = ''
    length=len(str(signal))
    for p in range(length):
        pairs_to_multiply=zip( digits_of(signal), pattern_for_phase( p, length ) )
        multiplied=map( lambda tup: tup[0] * tup[1], pairs_to_multiply )
        response+=(last_digit( sum( multiplied ) ) )
    return response

def day16part1():
    """
    #>>> day16part1()
    #'76892664'
    """
    signal=DAY16_SIGNAL
    for x in range(100):
        signal=fft(signal)
    return signal[:8]

if __name__ == "__main__":
    print (day16part1())
