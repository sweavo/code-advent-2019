#!python3
import functools
import io
import itertools
import sys

import tapes


class Intputer( object ):
    """
        Here is an inputer drawing its input from another intputer
    >>> wputer = Intputer( "4,3,99,14" ) 
    >>> rputer=Intputer( "3,3,99,88", wputer )
    >>> rputer.peek(3)
    88
    >>> list(rputer)
    []
    >>> rputer.peek(3)
    14
    >>> wputer = Intputer( "4,3,99,14" ) 
    >>> rputer=Intputer( "3,3,99,88" )
    >>> rputer._in=wputer
    >>> rputer.peek(3)
    88
    >>> list(rputer)
    []
    >>> rputer.peek(3)
    14
    >>> list(Intputer( "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99" ) ) # day9.1 relative address test
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    >>> len(str(next(Intputer( "1102,34915192,34915192,7,4,7,99,0" )))) # day9.1 big numbers test
    16
    >>> next(Intputer( "104,1125899906842624,99" ) )
    1125899906842624
    """ 
    def __init__(self, tape=None, inputs=[], outstream=None ):
        self._pc=0
        self._relative_base=0
        self._memory={}
        self._in = iter(inputs)
        self._out = outstream or io.StringIO()
        if tape is not None:
            self.load_tape( tape )

    def poke(self,addr,val):
        """
        >>> poot=Intputer()
        >>> poot.poke(100,5)
        >>> poot.peek(100)
        5
        """
        self._memory[addr] = val

    def peek(self,addr):
        """
        >>> poot=Intputer()
        >>> poot.peek(0)
        0
        >>> poot.peek(100)
        0
        """
        return self._memory.get(addr,0)

    def load_tape( self, tape ):
        """ 
        >>> poot = Intputer( "1,0,0,3" )
        >>> poot._memory
        {0: 1, 1: 0, 2: 0, 3: 3}
        """
        self._memory = { k: v for k,v in enumerate( map( int, tape.split(',') ) ) }

    def print_tape( self ):
        """
        >>> poot = Intputer( )
        >>> poot._memory = {0: 1, 2: 3, 1: 0, 3: 4}
        >>> poot.print_tape()
        '1,0,3,4'
        >>> poot._memory = {0: 1, 2: 3, 5: 2, 3: 4}
        >>> poot.print_tape()
        '1,0,3,4,0,2'
        """
        addresses = range(max(self._memory.keys())+1)
        return ','.join([ str(self._memory.get(k,0)) for k in addresses])

    def pcinc(self):
        ret=self._pc
        self._pc+=1
        return ret

    def fetch(self):
        byte = self.peek(self._pc)
        self._pc+=1
        return byte

    PCOUNT = {  1: 3, 
                2: 3, 
                3: 1, 
                4: 1,
                5: 2,
                6: 2,
                7: 3,
                8: 3,
                9: 1,
               99: 0 }
 
    def execute(self, instruction ):
        """
        >>> poot = Intputer('109,19,204,-34,99')
        >>> poot._relative_base=2000
        >>> poot.poke(1985,1234)
        >>> next(poot)
        1234
        >>> poot._relative_base
        2019
        
        """
        opcode=instruction%100
        pmodes=instruction//100
        parameters = []
        for p in range(self.PCOUNT[opcode]):
            pmode=pmodes % 10
            if pmode==2:
                parameters.append( self.fetch() + self._relative_base )
            elif pmode==1:
                parameters.append( self.pcinc() )
            else:
                parameters.append( self.fetch() )
            pmodes = pmodes // 10

        if opcode==1: # ADD
            self.poke( parameters[2], self.peek( parameters[0] ) + self.peek( parameters[1] ) )
        elif opcode==2: # MUL
            self.poke( parameters[2], self.peek( parameters[0] ) * self.peek( parameters[1] ) )
        elif opcode==3: # RD
            self.poke( parameters[0], next( self._in ) )
        elif opcode==4: # WR
            return self.peek( parameters[0] )
        elif opcode==5: # JNZ
            if self.peek( parameters[0] ):
                self._pc = self.peek( parameters[1] ) 
        elif opcode==6: # JZ
            if not self.peek( parameters[0] ):
                self._pc = self.peek( parameters[1] )
        elif opcode==7: # LT
            self.poke( parameters[2], 1 if self.peek( parameters[0] ) < self.peek( parameters[1] ) else 0 )
        elif opcode==8: # EQ
            self.poke( parameters[2], 1 if self.peek( parameters[0] ) == self.peek( parameters[1] ) else 0 )
        elif opcode==9: # Adjust Relative Base
            self._relative_base = self._relative_base + self.peek( parameters[0] )
        elif opcode==99:
            return False
        else:
            raise KeyError(f'{opcode} is not a valid opcode.')
        return True

    def __iter__( self ): return self # support iterator interface
    def __next__( self ):
        """ run until an output statement or halt """
        out=self.execute( self.fetch() )
        while out is True:
            out=self.execute( self.fetch() )
        if out is False:
            raise StopIteration
        return out

    def run( self ):
        """
        >>> Intputer( '1,0,0,0,99').run().print_tape()
        '2,0,0,0,99'
        >>> import io
        >>> Intputer( '3,3,99', [32]).run().peek(3)
        32
        >>> Intputer( '3,3,99',[23]).run().peek(3)
        23
        >>> next(Intputer( '4,3,99,1010' ))
        1010
        >>> next(Intputer( '4,3,99,1010' ))
        1010
        >>> Intputer( '1002,4,3,4,33,99' ).run().peek(4)
        99
        >>> Intputer( '102,4,3,5,99,33' ).run().peek(5)
        20
        >>> Intputer( '10002,4,3,4,99' ).run().print_tape()
        '10002,4,3,396,99'
        >>> next(Intputer( '3,9,8,9,10,9,4,9,99,-1,8', [7] ))
        0
        >>> next(Intputer( '3,9,8,9,10,9,4,9,99,-1,8', [8]))
        1
        """
        out = self.execute( self.fetch() )
        while out is not False:
            if out is not True: # i.e. it is a number
                self._out.write( f"{out}\n" ) 
            out = self.execute( self.fetch() )
        return self #for chaining

def day5part2():
    """
    >>> day5part2()
    7873292
    """
    return next(Intputer( tapes.DAY5_TAPE, [5]))


class Amplifier( Intputer ):
    """
    >>> AmplifierTest1( 4 )( 0 )
    4
    >>> AmplifierTest1( 3 )( 4 )
    43
    >>> AmplifierTest1( 2 )( 43 )
    432
    >>> AmplifierTest1( 1 )( 432 )
    4321
    >>> AmplifierTest1( 0 )( 4321 )
    43210
    """
    def __init__( self, tape, phase ):
        self._inpqueue = [phase]
        super(Amplifier,self).__init__( tape, self._inpqueue )
        self._phase =phase

    def __call__( self, value ):
        self._inpqueue.append( value )
        return next(self)

    def append( self, value ):
        self._inpqueue.append( value )

def amp_factory( tape ):
    return functools.partial( Amplifier, tape )
AmplifierTest1=amp_factory( "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0" )
AmplifierTest2=amp_factory("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0" )
AmplifierTest3=amp_factory("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0" )
AmplifierPart2Test1=amp_factory("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
AmplifierPart2Test2=amp_factory("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")

def amp_chain( amp_class, phases ):
    """
    >>> amp_chain( AmplifierTest1, [4,3,2,1,0] )
    43210
    >>> amp_chain( AmplifierTest2, [0,1,2,3,4] )
    54321
    >>> amp_chain( AmplifierTest3, [1,0,4,3,2] )
    65210
    """
    chain = list(map( amp_class, phases ))
    return functools.reduce( lambda a,f: f(a), chain, 0 )

def day7part1():
    """
    >>> day7part1()
    17440
    """
    phase_permutations = itertools.permutations(range(5))
    # amplifier is an Amplifier, programmed with the puzzle input tape
    amplifier=functools.partial( Amplifier, tapes.DAY7_TAPE )
    # phase tester is an amp_chain of amplifier. So it takes a list of phases and runs the chain
    phase_tester=functools.partial( amp_chain, amplifier )

    return functools.reduce(max,map(phase_tester,phase_permutations))

def feedback_amp_chain( amp_class, phases ):
    """
    >>> feedback_amp_chain( AmplifierPart2Test1, [9,8,7,6,5] )
    139629729
    >>> feedback_amp_chain( AmplifierPart2Test2, [9,7,8,5,6] )
    18216
    """
    out=0
    chain = list(map( amp_class, phases ) )
    try:
        while True:
            out = functools.reduce( lambda a,f: f(a), chain, out)
    finally:
        return out

def day7part2():
    """
    >>> day7part2()
    27561242
    """
    phase_permutations = itertools.permutations(range(5,10))
    # amplifier is an Amplifier, programmed with the puzzle input tape
    amplifier=functools.partial( Amplifier, tapes.DAY7_TAPE)
    # phase tester is an amp_chain of amplifier. So it takes a list of phases and runs the chain
    phase_tester=functools.partial( feedback_amp_chain, amplifier )

    return functools.reduce(max,map(phase_tester,phase_permutations))
    
def day9part1():
    """
    >>> day9part1()
    [2406950601]
    """
    return list( Intputer( tapes.DAY9_TAPE, [1] ) )

def day9part2():
    """
    >>> day9part2()
    83239
    """
    return next( Intputer( tapes.DAY9_TAPE, [2] ) )
 
