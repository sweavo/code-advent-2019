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

