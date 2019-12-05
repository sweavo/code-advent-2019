#!python3
import sys

PROGRAM_TAPE='1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,10,23,2,13,23,27,1,5,27,31,2,6,31,35,1,6,35,39,2,39,9,43,1,5,43,47,1,13,47,51,1,10,51,55,2,55,10,59,2,10,59,63,1,9,63,67,2,67,13,71,1,71,6,75,2,6,75,79,1,5,79,83,2,83,9,87,1,6,87,91,2,91,6,95,1,95,6,99,2,99,13,103,1,6,103,107,1,2,107,111,1,111,9,0,99,2,14,0,0'

class Intputer( object ):

    def __init__(self, tape=None, instream=None, outstream=None ):
        self._pc = 0
        self._memory={}
        self._in = instream
        self._out = outstream
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
               99: 0 }
 
    def execute(self, instruction ):
        print ( f'Intstr: {instruction}', file=sys.stderr )
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
            self._memory[ parameters[2] ] = self._memory[ parameters[0] ] + self._memory[ parameters[1] ]
        elif opcode==2:
            self._memory[ parameters[2] ] = self._memory[ parameters[0] ] * self._memory[ parameters[1] ]
        elif opcode==3:
            self._memory[ parameters[0] ] = int( self._in.readline() )
        elif opcode==4:
            self._out.write(f'{self._memory[ parameters[0] ]}')
        elif opcode==99:
            return False
        else:
            raise KeyError(f'{opcode} is not a valid opcode.')
        return True

    def run( self ):
        """
        >>> poot = Intputer( '1,0,0,0,99' )
        >>> poot.run()
        >>> poot.print_tape()
        '2,0,0,0,99'
        >>> import io
        >>> poot = Intputer( '3,3,99', instream=io.StringIO('32\\n') )
        >>> poot.run()
        >>> poot.peek(3)
        32
        >>> poot = Intputer( '4,3,99,1010', outstream=io.StringIO())
        >>> poot.run()
        >>> poot._out.getvalue()
        '1010'
        >>> poot = Intputer( '1002,4,3,4,33,99' )
        >>> poot.run()
        >>> poot.peek(4)
        99
        >>> poot = Intputer( '102,4,3,5,99,33' )
        >>> poot.run()
        >>> poot.peek(5)
        20
        >>> poot = Intputer( '10002,4,3,4,99' )
        >>> poot.run()
        >>> poot.print_tape()
        '10002,4,3,396,99'
        """
        while self.execute( self.fetch() ):
            pass


if __name__ == "__main__":
    poot = Intputer( PROGRAM_TAPE )
    poot.poke(1,12)
    poot.poke(2,2)
    poot.run()
    print (poot.peek(0) )

