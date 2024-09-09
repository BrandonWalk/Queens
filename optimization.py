from pulp import LpProblem, LpVariable, LpMaximize, value

problem = LpProblem("Queens", LpMaximize)

number_of_rows = 7

def get_cell_id(row, col):
    return row*number_of_rows + col

def get_surrounding_cell_ids(row, col):
    starting_cell_id = get_cell_id(row, col)

    # right
    if col+1<number_of_rows: # checks for overflow (ie edge of the board)
        right = get_cell_id(row, col+1)
    else:
        right = None
    
    # list of the ids
    if row+1<number_of_rows: # checks for overflow (ie edge of the board)
        bottom = get_cell_id(row+1, col)
        if col+1<number_of_rows: # checks for overflow (ie edge of the board)
            bottom_right = get_cell_id(row+1, col+1)
        else:
            bottom_right = None
    else:
        bottom = None
        bottom_right = None

    ids = [starting_cell_id,   right,
           bottom,             bottom_right]
    
    ids = [id for id in ids if id is not None]
    return ids

# define decision variables
variables = {}
for row in range(number_of_rows):
    for col in range(number_of_rows):
        cell_id = get_cell_id(row, col)
        variables[cell_id] = LpVariable(f"var_{cell_id}", cat="Binary")

# constraints for only 1 queen in a row
for row in range(number_of_rows):
    problem += sum([variables[get_cell_id(row, col)] for col in range(number_of_rows)]) == 1

# constraints for only 1 queen in a column
for col in range(number_of_rows):
    problem += sum([variables[col+row*number_of_rows] for row in range(number_of_rows)]) == 1

# no surrounding 1s
for row in range(number_of_rows):
    for col in range(number_of_rows):
        problem += sum([variables[var] for var in get_surrounding_cell_ids(row, col)]) <= 1

# color constraint
from bs4 import BeautifulSoup
soup = BeautifulSoup(open("game.html"))
color_groups = [i["class"][1] for i in soup.find_all("div", {"class": "queens-cell"})]
for color in set(color_groups):
    color_group_constraint = []
    for cell_id,cell_color in enumerate(color_groups):
        if cell_color==color:
            color_group_constraint.append(variables[cell_id])
    problem += sum(color_group_constraint)==1

# objective
problem += sum([variables[var] for var in variables])

# solve
solution = problem.solve()

# print solution
for row in range(number_of_rows):
    for col in range(number_of_rows):
        cell_id = get_cell_id(row, col)
        print(int(value(variables[cell_id])), end =" ")
    print()
