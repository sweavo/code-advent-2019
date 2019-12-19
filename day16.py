#!python3

from signal_day16 import DAY16_SIGNAL

def prep( signal ):
    """ turn the input, which might be a large int or string, into a list of ints, one for each digit 
    >>> prep([1,2,5,6])
    [1, 2, 5, 6]
    >>> prep(8934)
    [8, 9, 3, 4]
    >>> prep('4590')
    [4, 5, 9, 0]
    """
    if isinstance(signal, int):
        signal=str(signal)
    if isinstance(signal, str):
        signal=list(map(int,signal))
    return signal

def present( signal_list ):
    """
    >>> present([1,3,2,4,3,5,4,6])
    '13243546'
    """
    return ''.join( map( str, signal_list ) )

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
    return [[0,1,0,-1][(c//(p+1))%4] for c in range(1,size+1)]

def fft( signal ):
    """
    >>> present(fft( [1,2,3,4,5,6,7,8] ))
    '48226158'
    >>> present(fft( [4,8,2,2,6,1,5,8] ))
    '34040438'
    >>> present(fft( [3,4,0,4,0,4,3,8] ))
    '03415518'
    """ 
    response = []
    length=len(signal)
    for p in range(length):
        total=0
        for n, m in zip( signal, pattern_for_phase( p, length ) ):
            if m>0:
                total+=n
            elif m<0:
                total-=n
        response.append( abs(total) % 10 )
    return response

def fftXn( signal,n=100 ):
    """
    >>> present(fftXn( prep(80871224585914546619083218645595) ))
    '24176176'
    >>> present(fftXn( prep('19617804207202209144916044189917') ))
    '73745418'
    >>> present(fftXn( prep('69317163492948606335995924319873') ))
    '52432133'
    """
    if isinstance(signal, str):
        signal = list(map(int,signal))
    for x in range(n):
        signal=fft(signal)
    return signal[:8]
    
def day16part1():
    """
    >>> day16part1()
    '11833188'
    """
    return present(fftXn( prep( DAY16_SIGNAL )))

if __name__ == "__main__":
    #print (day16part1())
    import cProfile, pstats
    pr=cProfile.Profile()
    pr.enable()
    fftXn( DAY16_SIGNAL )
    pr.disable()
    pr.print_stats()
     
