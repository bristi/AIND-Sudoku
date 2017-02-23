assignments = []

# init constants
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
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

    for unit in unitlist:

        boxes_with_two_options = [box for box in unit if len(values[box]) == 2]

        for i, box in enumerate(boxes_with_two_options):
            # Check if the two values are identical to the values of another
            # box with only two possible values
            for alt_box in boxes_with_two_options[i+1:]:
                if values[box] == values[alt_box]:
                    # We have a set of naked twins
                    twins = set([box, alt_box])

                    # Take all other boxes in unit and remove the values of the naked twins
                    non_twins = set(unit).difference(twins)

                    for peer in non_twins:
                        for digit in values[box]:
                            replacement_string = values[peer].replace(digit, '')
                            assign_value(values, peer, replacement_string)

    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."

    return [s + t for s in A for t in B]

# calculated constants
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in
                ('123', '456', '789')]
diag_units = [[r + c for r,c in zip(rows, cols)], [r + c for r,c in zip(rows[::-1], cols)]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

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

    assert len(grid) == 81
    grid_dict = {k: '123456789' if v == '.' else v for k, v in zip(boxes, grid)}

    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            replacement_string = values[peer].replace(digit, '')
            assign_value(values, peer, replacement_string)

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            # Boxes in unit that contain digit
            dplaces = [box for box in unit if digit in values[box]]

            # See if box is the only choice for digit
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    stalled = False

    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Use implemented methods to reduce sudoku
        values = eliminate(values)
        values = only_choice(values)

        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Check if we are stalled, either because sudoku is solved or because
        # we are not able to reduce further using the implemented methods
        stalled = solved_values_before == solved_values_after

        # See if any box has been reduced to zero possible values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    """ Using a depth-first approach search through possible solutions
    for the given sudoku puzzle.

    An unfilled box, preferrably one with a minimum amount of possible values,
    is selected and each possible value is tested. The search tree is built
    recursively and the first found solution is returned.

    For each recursion the sudoku is reduced using the implemented methods called
    by `reduce_puzzle`.

    If no solution is found then False is returned.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        # Not a solution
        return False
    if all(len(values[s]) == 1 for s in boxes):
        # Sudoku is solved
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

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

    print("")
    print("The unsolved sudoku (diagonal task):")
    display(grid_values(diag_sudoku_grid))

    print("")
    print("The solved sudoku (diagonal task):")
    display(solve(diag_sudoku_grid))

    # Visualize solution
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


    before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1',
                            'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3',
                            'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
                            'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237',
                            'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23',
                            'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8',
                            'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6',
                            'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8',
                            'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9',
                            'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2',
                            'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3',
                            'B9': '4', 'D1': '5'}

    print("")
    print("The unsolved sudoku (naked twins task):")
    display(before_naked_twins_1)

    print("")
    print("The 'solved' sudoku (naked twins task):")
    # We reset assignments so the earlier diagonal solution is removed from
    # visualization with pygame
    assignments = []
    display(naked_twins(before_naked_twins_1))

    # Visualize solution
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
