#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:23:20 2019

@author: MorganFrearson
"""

def test_taboo_cells():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_29.txt")
    # Convert map into single string 
    warehouse_expected = str(wh)
    answer = taboo_cells(wh)
    fcn = test_taboo_cells    
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer==warehouse_expected:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(warehouse_expected)
        print('But, received ');print(answer)
        
def test_check_elem_action_seq():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_29.txt")
    print(str(wh))
    # first test
    answer = check_action_seq(wh, ['Right', 'Right','Down'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n#  $@#\n#  ###\n####  '
    fcn = test_check_elem_action_seq    
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = check_action_seq(wh, ['Right', 'Right','Right'])
    expected_answer = 'Failure'
    fcn = test_check_elem_action_seq    
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
      
def test_solve_sokoban_macro():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    # Convert map into single string 
    warehouse_expected = str(wh)
    print(wh) # DEGBUGGING 
    # first test
    answer=solve_sokoban_macro(wh)
    print(answer)
    
    
def test_solve_sokoban_elem():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")    
    # Convert map into single string 
    warehouse_expected = str(wh)
    print(wh) # DEGBUGGING 
    # first test
    answer = solve_sokoban_elem(wh)
    print(answer)


if __name__ == "__main__":
    pass    
    print(my_team())  # should print your team

#    test_taboo_cells() 
#    test_check_elem_action_seq()
#    test_solve_sokoban_elem()
#    test_can_go_there()
    test_solve_sokoban_macro() 
    