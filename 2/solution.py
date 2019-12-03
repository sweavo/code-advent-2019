#!python3

PROGRAM_TAPE='1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,10,23,2,13,23,27,1,5,27,31,2,6,31,35,1,6,35,39,2,39,9,43,1,5,43,47,1,13,47,51,1,10,51,55,2,55,10,59,2,10,59,63,1,9,63,67,2,67,13,71,1,71,6,75,2,6,75,79,1,5,79,83,2,83,9,87,1,6,87,91,2,91,6,95,1,95,6,99,2,99,13,103,1,6,103,107,1,2,107,111,1,111,9,0,99,2,14,0,0'

def load_tape( tape ):
    """
    >>> load_tape( '1,0,0,3' )
    {0: 1, 1: 0, 2: 0, 3: 3}
    """
    return { k: v for k,v in enumerate( map( int, tape.split(',') ) ) }

def print_tape( d ):
    """
    >>> print_tape({0: 1, 2: 3, 1: 0, 3: 4})
    '1,0,3,4'
    >>> print_tape({0: 1, 2: 3, 1: 0, 3: 4})
    '1,0,3,4'
    """
    return ','.join([ str(d[k]) for k in sorted(d.keys())])
        
    
def op_add( memory, pc ):
    """
    >>> print_tape( op_add( load_tape('1,0,0,3'),0 ) )
    '1,0,0,2'
    >>> print_tape( op_add( load_tape('1,3,0,1'),0 ) )
    '1,2,0,1'
    >>> print_tape( op_add( load_tape('1,3,3,0'),0 ) )
    '0,3,3,0'
    """
    memory[memory[pc+3]] = memory[memory[pc+1]] + memory[memory[pc+2]]
    return memory
