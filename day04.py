#!python3

def remainder( first, digits ):
    for head in range(first,10):
        if digits > 1:
            for tail in remainder( head, digits-1):
                yield str(head)+tail
        else:
            yield str(head)

def has_double_part_1( digits ):
    for i in range(len(digits)-1):
        if digits[i] == digits[i+1]:
            return True
    return False

def has_double( digits ):
    """
    >>> has_double( '11' )
    True
    >>> has_double( '112' )
    True
    >>> has_double( '211' )
    True
    >>> has_double( '121' )
    False
    >>> has_double( '111' )
    False
    >>> has_double( '11122111' )
    True
    """
    val=digits[0]
    runl=1
    for i in range(1,len(digits)):
        if digits[i] == val:
            runl=runl+1
        else:
            if runl==2:
                return True
            else:
                runl=1
                val=digits[i]
    if runl==2:
        return True
    else:
        return False 

if __name__ == "__main__":
    count=0
    count2=0
    for combo in remainder( 0, 6 ):
        if int(combo) >= 616492:
            print (f'Count={count}\nPart2={count2}')
            exit()
        
        print ( combo )
        if int(combo) >= 145852 and has_double_part_1(combo):
            count = count + 1
        if int(combo) >= 145852 and has_double(combo):
            count2 = count2 + 1

