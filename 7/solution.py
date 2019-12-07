#!python3
import functools
import io
import itertools
import sys

PROGRAM_TAPE='3,225,1,225,6,6,1100,1,238,225,104,0,1101,69,55,225,1001,144,76,224,101,-139,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,60,49,225,1102,51,78,225,1101,82,33,224,1001,224,-115,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,1102,69,5,225,2,39,13,224,1001,224,-4140,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,101,42,44,224,101,-120,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,68,49,224,101,-3332,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,50,27,225,1102,5,63,225,1002,139,75,224,1001,224,-3750,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,102,79,213,224,1001,224,-2844,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1,217,69,224,1001,224,-95,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,36,37,225,1101,26,16,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,102,2,223,223,1006,224,329,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,359,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,677,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,434,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,449,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,464,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,479,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,107,677,677,224,1002,223,2,223,1006,224,509,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,539,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,584,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,599,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,644,1001,223,1,223,108,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226'

class Intputer( object ):

    def __init__(self, tape=None, inputs=[], outstream=None ):
        self._pc = 0
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
               99: 0 }
 
    def execute(self, instruction ):
        opcode=instruction%100
        pmodes=instruction//100
        parameters = []
        for p in range(self.PCOUNT[opcode]):
            if pmodes % 2:
                parameters.append( self.pcinc() )
            else:
                parameters.append( self.fetch() )
            pmodes = pmodes // 10

        if opcode==1:
            self.poke( parameters[2], self.peek( parameters[0] ) + self.peek( parameters[1] ) )
        elif opcode==2:
            self.poke( parameters[2], self.peek( parameters[0] ) * self.peek( parameters[1] ) )
        elif opcode==3:
            self.poke( parameters[0], next( self._in ) )
        elif opcode==4:
            return self.peek( parameters[0] )
        elif opcode==5:
            if self.peek( parameters[0] ):
                self._pc = self.peek( parameters[1] ) 
        elif opcode==6:
            if not self.peek( parameters[0] ):
                self._pc = self.peek( parameters[1] )
        elif opcode==7:
            self.poke( parameters[2], 1 if self.peek( parameters[0] ) < self.peek( parameters[1] ) else 0 )
        elif opcode==8:
            self.poke( parameters[2], 1 if self.peek( parameters[0] ) == self.peek( parameters[1] ) else 0 )
        elif opcode==99:
            return False
        else:
            raise KeyError(f'{opcode} is not a valid opcode.')
        return True

    def __iter__( self ): return self # support iterator interface
    def __next__( self ):
        out=self.execute( self.fetch() )
        while out is True:
            out=self.execute( self.fetch() )
        if out is False:
            raise StopIterator
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

    def output( self ):
        return self._out.getvalue()
    
def day5part2():
    """
    >>> day5part2()
    '7873292\\n'
    """
    return Intputer( PROGRAM_TAPE, [5]).run().output()


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
        super(Amplifier,self).__init__( tape )
        self._phase =phase

    def __call__( self, value ):
        self._in=iter( [self._phase, value] )
        self.run()
        return int(self.output())

AmplifierTest1=functools.partial( Amplifier, "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0" )
AmplifierTest2=functools.partial( Amplifier, "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0" )
AmplifierTest3=functools.partial( Amplifier, "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0" )

def amp_chain( amp_class, phases ):
    """
    >>> amp_chain( AmplifierTest1, [4,3,2,1,0] )
    43210
    >>> amp_chain( AmplifierTest2, [0,1,2,3,4] )
    54321
    >>> amp_chain( AmplifierTest3, [1,0,4,3,2] )
    65210
    """
    chain = map( amp_class, phases )
    return functools.reduce( lambda a,f: f(a), chain, 0 )

def day7part1():
    """
    >>> day7part1()
    17440
    """
    phase_permutations = itertools.permutations(range(5))
    with open( 'tape.txt','r' ) as f:
        # amplifier is an Amplifier, programmed with the puzzle input tape
        amplifier=functools.partial( Amplifier, f.read() )
    # phase tester is an amp_chain of amplifier. So it takes a list of phases and runs the chain
    phase_tester=functools.partial( amp_chain, amplifier )

    return functools.reduce(max,map(phase_tester,phase_permutations))

if __name__ == "__main__":
   print( day7part1() )
 
