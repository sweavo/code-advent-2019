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
        yield images_chars[ii:ii+size]

def day8part1question( chars, w, h ):
    """ chars contains several images.  Generate a sequence of 
        tuples (x,y) where x is the number of zeroes in the image
        and y is the product of the number of 1s and 2s in the image.
    >>> list(day8part1question( '012012234123012345', 3, 2))
    [(2, 4), (0, 2), (1, 1)]
    """
    for counts in  map( count_pixels, split_layers( chars, w * h ) ):
        yield (counts['0'], counts['1']*counts['2'])

def day8part1( chars, width, height ):
    """
    >>> day8part1( '123456789012', 3, 2)
    1
    """
    results = sorted( day8part1question( chars, width, height ), reverse=True )
    return results[0][1]

    
