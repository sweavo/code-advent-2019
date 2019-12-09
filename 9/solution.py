#!python3
import functools
import io
import itertools
import sys

PROGRAM_TAPE='3,225,1,225,6,6,1100,1,238,225,104,0,1101,69,55,225,1001,144,76,224,101,-139,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,60,49,225,1102,51,78,225,1101,82,33,224,1001,224,-115,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,1102,69,5,225,2,39,13,224,1001,224,-4140,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,101,42,44,224,101,-120,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,68,49,224,101,-3332,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,50,27,225,1102,5,63,225,1002,139,75,224,1001,224,-3750,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,102,79,213,224,1001,224,-2844,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1,217,69,224,1001,224,-95,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,36,37,225,1101,26,16,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,102,2,223,223,1006,224,329,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,359,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,677,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,434,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,449,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,464,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,479,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,107,677,677,224,1002,223,2,223,1006,224,509,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,539,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,584,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,599,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,644,1001,223,1,223,108,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226'
DAY9PART1_PROGRAM_TAPE='1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,902,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,26,0,1015,1101,29,0,1010,1102,1,24,1013,1102,1,33,1008,1102,36,1,1012,1101,0,572,1023,1101,35,0,1014,1101,0,38,1019,1102,1,30,1006,1101,0,890,1029,1101,34,0,1011,1101,28,0,1002,1102,1,1,1021,1101,0,37,1001,1101,0,197,1026,1101,22,0,1017,1102,1,895,1028,1101,0,20,1007,1102,21,1,1004,1102,1,39,1016,1101,0,0,1020,1102,1,190,1027,1101,0,775,1024,1102,31,1,1018,1101,0,23,1003,1101,0,25,1009,1101,770,0,1025,1101,0,27,1000,1102,1,575,1022,1101,0,32,1005,109,27,2106,0,0,1001,64,1,64,1106,0,199,4,187,1002,64,2,64,109,-18,21101,40,0,5,1008,1014,39,63,1005,63,219,1106,0,225,4,205,1001,64,1,64,1002,64,2,64,109,-6,1201,-1,0,63,1008,63,28,63,1005,63,251,4,231,1001,64,1,64,1105,1,251,1002,64,2,64,109,5,21102,41,1,3,1008,1011,38,63,1005,63,271,1105,1,277,4,257,1001,64,1,64,1002,64,2,64,109,-7,2102,1,1,63,1008,63,28,63,1005,63,299,4,283,1106,0,303,1001,64,1,64,1002,64,2,64,109,-7,1207,10,22,63,1005,63,321,4,309,1106,0,325,1001,64,1,64,1002,64,2,64,109,16,2107,31,-4,63,1005,63,345,1001,64,1,64,1105,1,347,4,331,1002,64,2,64,109,-9,1201,3,0,63,1008,63,18,63,1005,63,371,1001,64,1,64,1106,0,373,4,353,1002,64,2,64,109,7,1202,-7,1,63,1008,63,40,63,1005,63,393,1106,0,399,4,379,1001,64,1,64,1002,64,2,64,109,-5,1208,5,33,63,1005,63,417,4,405,1106,0,421,1001,64,1,64,1002,64,2,64,109,1,1202,2,1,63,1008,63,30,63,1005,63,443,4,427,1105,1,447,1001,64,1,64,1002,64,2,64,109,-7,2102,1,10,63,1008,63,19,63,1005,63,471,1001,64,1,64,1105,1,473,4,453,1002,64,2,64,109,6,2108,21,0,63,1005,63,489,1105,1,495,4,479,1001,64,1,64,1002,64,2,64,109,9,21108,42,42,0,1005,1012,513,4,501,1105,1,517,1001,64,1,64,1002,64,2,64,109,7,21107,43,44,-1,1005,1018,535,4,523,1106,0,539,1001,64,1,64,1002,64,2,64,109,-5,21101,44,0,2,1008,1016,44,63,1005,63,561,4,545,1105,1,565,1001,64,1,64,1002,64,2,64,2105,1,9,1106,0,581,4,569,1001,64,1,64,1002,64,2,64,109,13,21107,45,44,-9,1005,1018,597,1105,1,603,4,587,1001,64,1,64,1002,64,2,64,109,-25,2101,0,3,63,1008,63,32,63,1005,63,625,4,609,1105,1,629,1001,64,1,64,1002,64,2,64,109,7,1208,-7,30,63,1005,63,645,1105,1,651,4,635,1001,64,1,64,1002,64,2,64,109,-2,21102,46,1,9,1008,1016,46,63,1005,63,677,4,657,1001,64,1,64,1106,0,677,1002,64,2,64,109,-2,21108,47,48,9,1005,1014,697,1001,64,1,64,1105,1,699,4,683,1002,64,2,64,109,14,1205,2,713,4,705,1105,1,717,1001,64,1,64,1002,64,2,64,109,-7,1206,8,735,4,723,1001,64,1,64,1106,0,735,1002,64,2,64,109,-18,2101,0,6,63,1008,63,24,63,1005,63,759,1001,64,1,64,1106,0,761,4,741,1002,64,2,64,109,29,2105,1,1,4,767,1106,0,779,1001,64,1,64,1002,64,2,64,109,-5,1206,3,791,1106,0,797,4,785,1001,64,1,64,1002,64,2,64,109,-12,2107,31,-1,63,1005,63,819,4,803,1001,64,1,64,1105,1,819,1002,64,2,64,109,7,1205,7,835,1001,64,1,64,1105,1,837,4,825,1002,64,2,64,109,-11,1207,7,24,63,1005,63,853,1106,0,859,4,843,1001,64,1,64,1002,64,2,64,109,4,2108,27,-6,63,1005,63,881,4,865,1001,64,1,64,1106,0,881,1002,64,2,64,109,24,2106,0,-2,4,887,1106,0,899,1001,64,1,64,4,64,99,21102,27,1,1,21101,0,913,0,1106,0,920,21201,1,61934,1,204,1,99,109,3,1207,-2,3,63,1005,63,962,21201,-2,-1,1,21101,0,940,0,1106,0,920,21202,1,1,-1,21201,-2,-3,1,21101,0,955,0,1105,1,920,22201,1,-1,-2,1105,1,966,22102,1,-2,-2,109,-3,2105,1,0'

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
    return next(Intputer( PROGRAM_TAPE, [5]))


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
    with open( 'tape.txt','r' ) as f:
        # amplifier is an Amplifier, programmed with the puzzle input tape
        amplifier=functools.partial( Amplifier, f.read() )
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
    with open( 'tape.txt','r' ) as f:
        # amplifier is an Amplifier, programmed with the puzzle input tape
        amplifier=functools.partial( Amplifier, f.read() )
    # phase tester is an amp_chain of amplifier. So it takes a list of phases and runs the chain
    phase_tester=functools.partial( feedback_amp_chain, amplifier )

    return functools.reduce(max,map(phase_tester,phase_permutations))
    
def day9part1():
    """
    >>> day9part1()
    [2406950601]
    """
    return list( Intputer( DAY9PART1_PROGRAM_TAPE, [1] ) )

def day9part2():
    """
    >>> day9part2()
    0
    """
    return next( Intputer( DAY9PART1_PROGRAM_TAPE, [2] ) )
 
