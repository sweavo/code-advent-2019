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
        total=0
        for n, m in zip( digits_of(signal), pattern_for_phase( p, length ) ):
            if m>0:
                total+=n
            elif m<0:
                total-=n
        response+=(last_digit( total ) )
    return response

def fftXn( signal,n=100 ):
    """
    >>> fftXn( 80871224585914546619083218645595 )
    '24176176'
    >>> fftXn( '19617804207202209144916044189917' )
    '73745418'
    >>> fftXn( '69317163492948606335995924319873' )
    '52432133'
    """
    for x in range(n):
        signal=fft(signal)
    return signal[:8]
    
def day16part1():
    """
    >>> day16part1()
    '11833188'
    """
    return fftXn( DAY16_SIGNAL )

if __name__ == "__main__":
    #print (day16part1())
    import cProfile, pstats
    pr=cProfile.Profile()
    pr.enable()
    fft( DAY16_SIGNAL )
    pr.disable()
    pr.print_stats()
     
