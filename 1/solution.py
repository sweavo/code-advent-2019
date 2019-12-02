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
def calc_fuel( mass ):
    return mass // 3 - 2

