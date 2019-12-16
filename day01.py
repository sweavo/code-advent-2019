#!python3
import sys

def calc_fuel( mass ):
    """
    >>> calc_fuel(5)
    0
    >>> calc_fuel(12)
    2
    >>> calc_fuel(14)
    2
    >>> calc_fuel(1969)
    654
    >>> calc_fuel(100756)
    33583
    """
    return max(0,mass // 3 - 2)

def additional_fuel_generator( mass ):
    """
    >>> list(additional_fuel_generator(2))
    []
    >>> list(additional_fuel_generator(654))
    [216, 70, 21, 5]
    >>> list(additional_fuel_generator(33583))
    [11192, 3728, 1240, 411, 135, 43, 12, 2]
    >>> list(additional_fuel_generator(100756))
    [33583, 11192, 3728, 1240, 411, 135, 43, 12, 2]
    """
    fuel = calc_fuel(mass)
    while fuel > 0:
        yield fuel
        fuel = calc_fuel( fuel )
    
def calc_total_fuel( mass ):
    """
    >>> calc_total_fuel( 14 )
    2
    >>> calc_total_fuel( 1969 )
    966
    >>> calc_total_fuel( 100756 )
    50346
    """
    return sum(additional_fuel_generator( mass ))

def day01part2():
    """
    >>> day01part2()
    4739374
    """
    with open( 'modules.txt', 'r') as f:
        mass_strings = map( str.strip, f)
        masses = map( int, mass_strings)
        fuels_for_modules = map( calc_total_fuel, masses )
        print (sum(fuels_for_modules))

