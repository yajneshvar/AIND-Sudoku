from functools import *
assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross('ABCDEFGHI','123456789')
row_units = [cross(alp,'123456789') for alp in 'ABCDEFGHI']
column_units = [cross('ABCDEFGHI',col) for col in '123456789']
square_units = [cross(row,col) for row in ('ABC','DEF','GHI') for col in ('123','456','789')]
diagonal_unit1 = list(map(lambda x:x[0]+x[1],zip('ABCDEFGHI','123456789')))
diagonal_unit2 = list(map(lambda x:x[0]+x[1],zip('ABCDEFGHI','987654321')))
diagonal_units = [diagonal_unit1,diagonal_unit2]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    for unit in unitlist:
        # find twin in each unit
        twin = [box for box in unit if len(values[box]) == 2 ]
        twinVal_copy = list(map(lambda x: set(values[x]),twin))
        naked_twins = [box for box in twin if twinVal_copy.count(set(values[box])) == 2 ]
        for naked_box in naked_twins:
            unit.remove(naked_box)
        for box in unit:
            tmp_val = values[box]
            for naked_bx in naked_twins:
                tmp_val = list(filter(lambda x: x not in values[naked_bx],tmp_val))
            assign_value(values,box,reduce(lambda acc,x: acc+x,tmp_val,''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    def replaceEmpties(x):
        if x == '.':
            return '123456789'
        else:
            return x
    list_iter = map(replaceEmpties,grid)
    grid_iter = zip(boxes,list_iter)
    return dict(grid_iter)

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    def itemKey(item):
        return item[1]
    longest_box = max(map(lambda x: len(x[1]),values.items()))
    max_width = 1 + longest_box
    seperator = '-'*(max_width*3)
    line = seperator + '+' + seperator + '+' + seperator
    for row in 'ABCDEFGHI':
        print(''.join(values[row+col].center(max_width)+('|' if col in '36' else '')for col in '123456789'))
        if row in 'CF':
            print(line)

def eliminate(values):
    for (k,v) in values.items():
        if len(v) == 1:
            for p in peers[k]:
                if len(values[p]) > 1:
                    curr_set = set(v)
                    new_set = set(values[p])
                    diff_set = new_set.difference(curr_set)
                    assign_value(values,p,reduce(lambda x,y:x+y,diff_set,''))
        else:
            continue
    return values

def only_choice(values):
    for unit in unitlist:
        #print('Unit is ',unit)
        for val in '123456789':
            boxes = [box for box in unit if val in values[box]]
            if len(boxes) == 1:
                assign_value(values,boxes[0],val)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    first_val = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    sortKey = lambda item: len(item[1])
    filter_by_length = lambda item: len(item[1]) > 1
    if first_val:
        sortedvals = sorted(first_val.items(),key=sortKey,reverse=True)
        filteredvals = list(filter(filter_by_length,sortedvals))
        if len(filteredvals) > 0:
            choice = filteredvals.pop()
            for val in choice[1]:
                temp_val = values.copy()
                assign_value(temp_val,choice[0],val)
                result = search(temp_val)
                if result:
                    return result
        else:
            return first_val
    else:
        return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
