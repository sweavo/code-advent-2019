#!python3

DAY16_SIGNAL='59768092839927758565191298625215106371890118051426250855924764194411528004718709886402903435569627982485301921649240820059827161024631612290005106304724846680415690183371469037418126383450370741078684974598662642956794012825271487329243583117537873565332166744128845006806878717955946534158837370451935919790469815143341599820016469368684893122766857261426799636559525003877090579845725676481276977781270627558901433501565337409716858949203430181103278194428546385063911239478804717744977998841434061688000383456176494210691861957243370245170223862304663932874454624234226361642678259020094801774825694423060700312504286475305674864442250709029812379'

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
    >>> day16part1()
    '76892664'
    """
    signal=DAY16_SIGNAL
    for x in range(100):
        signal=fft(signal)
    return signal[:8]

if __name__ == "__main__":
    print (day16part1())
