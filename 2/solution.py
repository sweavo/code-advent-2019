#!python3
import operator
import functools

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
    >>> print_tape({0: 1, 2: 3, 5: 2, 3: 4})
    '1,0,3,4,0,2'
    """
    addresses = range(max(d.keys())+1)
    return ','.join([ str(d.get(k,0)) for k in addresses])
        

def binop( op, memory, pc ):
    """
    >>> print_tape( binop( operator.add, load_tape('1,0,0,3'),0 ) )
    '1,0,0,2'
    >>> print_tape( binop( operator.add, load_tape('1,3,0,1'),0 ) )
    '1,2,0,1'
    >>> print_tape( binop( operator.add, load_tape('1,3,3,0'),0 ) )
    '0,3,3,0'
    >>> print_tape( binop( operator.add, load_tape('9,1,0,1,5'),0) )
    '9,10,0,1,5'
    >>> print_tape( binop( operator.add, load_tape('9,1,0,1,5'),1) )
    '9,1,0,1,5,10'
    """
    memory[memory[pc+3]] = op( memory[memory[pc+1]],  memory[memory[pc+2]] )
    return memory

op_add=functools.partial( binop, operator.add )
op_mul=functools.partial( binop, operator.mul )

def halt( memory, pc ):
    return memory

OPCODES={ 1: ( op_add, 4 ),
        2: ( op_mul, 4 ),
        99: ( halt, 0 ) } 

def execute( tape ):
    """
    >>> print_tape( execute( '1,0,0,0,99' ) )
    '2,0,0,0,99'
    >>> print_tape( execute( '2,3,0,3,99' ) )
    '2,3,0,6,99'
    >>> print_tape( execute( {0:2,1:3,2:0,3:3,4:99} ) )
    '2,3,0,6,99'
    >>> print_tape( execute( '2,4,4,5,99,0' ) )
    '2,4,4,5,99,9801'
    >>> print_tape( execute( '1,1,1,4,99,5,6,0,99' ) )
    '30,1,1,4,2,5,6,0,99'
    """
    if isinstance( tape, str ):
        memory=load_tape( tape )
    else:
        memory=tape
    pc=0
    op, jmp = OPCODES[memory[pc]]
    while op != halt:
        memory=op(memory,pc)
        pc+=jmp
        op, jmp = OPCODES[memory[pc]]
    return memory 

def execute_prog_with_noun_and_verb( tape, noun, verb ):
    memory=load_tape( tape )
    memory[1]=noun
    memory[2]=verb
    memory=execute( memory )
    return memory[0]

    
if __name__ == "__main__":
    print( execute_prog_with_noun_and_verb( PROGRAM_TAPE, 12, 2 ) )

