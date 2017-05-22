assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross('ABCDEFGHI','123456789')
row_units = [cross(alp,'123456789') for alp in 'ABCDEFGHI']
column_units = [cross(col,'ABCDEFGHI') for col in '123456789']
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
    # Eliminate the naked twins as possibilities for their peers

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
                    values[p] = reduce(lambda x,y:x+y,diff_set,'')
        else:
            continue
    return values

def only_choice(values):
    return values

def reduce_puzzle(values):
    return values

def search(values):
    return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return grid_values(grid)

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
