#!python3
"""
>>> import solution
>>> solution.calc_fuel(12)
2
>>> solution.calc_fuel(14)
2
>>> solution.calc_fuel(1969)
654
>>> solution.calc_fuel(100756)
33583
>>>
"""
import sys

def calc_fuel( mass ):
    return mass // 3 - 2

if __name__ == "__main__":  
    with open( 'modules.txt', 'r') as f:
        mass_strings = map( str.strip, f)
        masses = map( int, mass_strings)
        fuels = map( calc_fuel, masses )
        print(sum(fuels))

