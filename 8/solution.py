#!python3
import collections

def count_pixels( image_chars ):
    """ 
    >>> c=count_pixels('hello')
    >>> c['h']
    1
    >>> c['e']
    1
    >>> c['l']
    2
    >>> c['o']
    1
    """
    return collections.Counter( image_chars )

def split_layers( images_chars, size ):
    """
    >>> list(split_layers( "hellothere!!", 3 ))
    ['hel', 'lot', 'her', 'e!!']
    """
    for ii in range(0,len(images_chars), size):
        this_slice = images_chars[ii:ii+size]
        if len(this_slice) == size:
            yield this_slice

def day8part1question( chars, w, h ):
    """ chars contains several images.  Generate a sequence of 
        tuples (x,y) where x is the number of zeroes in the image
        and y is the product of the number of 1s and 2s in the image.
    >>> list(day8part1question( '012012234123012345', 3, 2))
    [(2, 4), (0, 2), (1, 1)]
    """
    for counts in  map( count_pixels, split_layers( chars, w * h ) ):
        yield (counts['0'], counts['1']*counts['2'])

def day8part1sortlayers( chars, width, height ):
    return sorted( day8part1question( chars, width, height ) )

def day8part1query( chars, width, height ):
    """
    >>> day8part1query( '123456789012', 3, 2)
    1
    >>> 
    """
    results = day8part1sortlayers( chars, width, height )
    return results[0][1]

def day8part1( ):
    """ 
    >>> day8part1()
    1596
    """
    with open( 'input.txt','r') as f:
        image_stream=f.read()
    return day8part1query( image_stream, 25, 6 )

def underlay( pix_top, pix_bottom ):
    """
    >>> underlay('0','1')
    '0'
    >>> underlay('1','2')
    '1'
    >>> underlay('2','0')
    '0'
    >>> underlay('2','2')
    '2'
    """
    return pix_bottom if pix_top=='2' else pix_top

def underlay_layer( upper, lower ):
    """
    >>> underlay_layer('01212', '12012' )
    '01012'
    >>> underlay_layer('21202120', '10200010' )
    '11200110'
    """
    return ''.join(map( lambda tup: underlay(*tup), zip( upper, lower ) )) 

if __name__ == "__main__":
    print( day8part1)

