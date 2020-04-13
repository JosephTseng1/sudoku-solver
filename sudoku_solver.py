#Removes the value from the constrained spaces and updates the remain_values_list
def reduce_values(row, column, value, remain_values_list):
    
    remain_values_list[column+row*9] = [0]
                                                                                                                                                                            
    for x in remain_values_list[row*9:row*9+9]:
        try:                                                                                                                                                                
            x.remove(value)                                                                                                                                                 
        except ValueError:                                                                                                                                                  
           pass                                                                                                                                                             
                                                                                                                                                                            
    for i in range(9):                                                                                                                                                      
        try:                                                                                                                                                                
            remain_values_list[column+9*i].remove(value)
        except ValueError:                                                                                                                                                  
            pass                                                                                                                                                            
                                                                                                                                                                            
    block_row = row//3
    block_column = column//3
                                                                                                                                                      
    for i in range(3):                                                                                                                                                      
        for j in range(3):                                                                                                                                                  
            try:                                                                                                                                                            
                remain_values_list[block_column*3+j+(block_row*3+i)*9].remove(value)
            except ValueError:                                                                                                                                              
                pass                                                                                                                                                        
                                                                                                                                                                            
    return remain_values_list
                                 
#For every space in the grid, it has a list of every possible remaining value
def obtain_remain_values(sudoku_grid):

    remain_values_list = []

    [remain_values_list.append(list(range(1,10))) for i in range(81)]

    for row in range(len(sudoku_grid)):
        for column in range(len(sudoku_grid[1])):
            if sudoku_grid[row][column] != 0:
                value = sudoku_grid[row][column]
                remainValuesList = reduce_values(row, column, value, remain_values_list)

    return remain_values_list

#For each contrained cell, we want to see the frequency for each  value
def obtain_least_constrain_values(row, column, values, remain_values_list):

    least_constrain_vals_list = []

    for value in values:
        count = 0

        for i in range(9):
            if i == column:
                continue
            x = remain_values_list[row*9+i]
            if value in x:
                count += 1

        for i in range(9):
            if i == row:
                continue
            x = remain_values_list[column+9*i]
            if value in x:
                count += 1

        block_row = row//3
        block_column = column//3

        for i in range(3):
            for j in range(3):
                if [block_row*3+i, block_column*3+j] == [row, column]:
                    continue
                x = list(remain_values_list[block_column*3+j+(block_row*3+i)*9])
                if value in x:
                    count += 1

        least_constrain_vals_list.append(count)

    return least_constrain_vals_list

#Getting the degree value, AKA the number of values
#that the space is contrained by
def obtain_degree_value(space, sudoku_grid):

    row = space[0]
    column = space[1]

    degree_value = 0

    for i in range(9):
        if i == column:
            continue
        if sudoku_grid[row][i] == 0:
            degree_value+=1

    for i in range(9):
        if i == row:
            continue
        if sudoku_grid[i][column] == 0:
            degree_value+=1

    block_row = row//3
    block_column = column//3

    for i in range(3):
        for j in range(3):
            if [block_row*3+i, block_column*3+j] == [row, column]:
                continue
            if sudoku_grid[block_row*3+i][block_column*3+j] == 0:
                degree_value+=1

    return degree_value

#It checks to see if the removed value is the only one remaining
def forward_checking_heuristic(row, column, value, remain_values_list):

    for i in range(9):
        if i == column:
            continue

        x = remain_values_list[row*9+i]

        if len(x) == 1:
            if x[0] == value:
                return False

    for i in range(9):
        if i == row:
            continue

        x = remain_values_list[column+9*i]
        if len(x) == 1:
            if x[0] == value:
                return False

    block_row = row//3
    block_column = column//3

    for i in range(3):
        for j in range(3):

            if [block_row*3+i, block_column*3+j] == [row, column]:
                continue

            x = remain_values_list[block_column*3+j+(block_row*3+i)*9]

            if len(x) == 1:
                if x[0] == value:
                    return False
    return True

#Backtracking sudoku solver with forward checking, degree, and MRV heuristics
def sudoku_solver(sudoku_grid):
    empty_spaces = []
    
    #Getting empty spaces
    for row in range(len(sudoku_grid)):
        for column in range(len(sudoku_grid[1])):
            if sudoku_grid[row][column] == 0:
                empty_spaces.append([row, column])
    
    #Once there are no more empty spaces, the grid is solved
    if len(empty_spaces) == 0:
        return True
    
    #get the square with the least remaining values
    remain_values_list = obtain_remain_values(sudoku_grid)
    min_remain_values_list = []

    [min_remain_values_list.append(len(remain_values_list[space[0]*9+space[1]])) for space in empty_spaces]

    min_remain_value_spaces = []
    
    #creating the list of spaces with the minimum remaning values
    minimum = min(min_remain_values_list)
    for i in range(len(min_remain_values_list)):
        value = min_remain_values_list[i]
        if value == minimum:
            min_remain_value_spaces.append(empty_spaces[i])
    
    #Assuming there are no ties, get the space with the minimum remanining values
    if len(min_remain_value_spaces) == 1:
        space = min_remain_value_spaces[0]
    else:
        #else, we find the most constrained element with degree heuristic
        degrees_list = []
        for cell in min_remain_value_spaces:
            degree = obtain_degree_value(cell, sudoku_grid)
            degrees_list.append(degree)
            
            max_degree = max(degrees_list)
            max_degree_spaces = []
            for i in range(len(degrees_list)):
                if degrees_list[i] == max_degree:
                    max_degree_spaces.append(min_remain_value_spaces[i])
                  
            space = max_degree_spaces[0]
     
    row = space[0]
    column = space[1]
          
    values = list(remain_values_list[column+row*9])
    
    while len(values) != 0:        
        least_constrain_vals_list = obtain_least_constrain_values(row, column, values, remain_values_list)
        
        #Obtain the least value that is contrained
        value = values[least_constrain_vals_list.index(min(least_constrain_vals_list))]
        values.remove(value)        

        if forward_checking_heuristic(row, column, value, remain_values_list):
            sudoku_grid[row][column] = value
            #Perform backtracking process and repeat!
            if sudoku_solver(sudoku_grid):
                return True
            else:
                sudoku_grid[row][column] = 0
                
    return False

#Obtaining the file from the user, gives error if it does not exist.
#Creates an "output.txt" file that has the solution result. if no solution,
#it will be the same as the input file
sudoku_grid = []

try:
    file_name = input("Enter the file name:" )
except FileNotFoundError:
    pass


with open(file_name, "r") as ins:
    content = ins.readlines()
    content = [x.strip() for x in content]


for line in content:
    row = line.split(' ')
    row = [int(i) for i in row]
    sudoku_grid.append(row)

print("The solution result: ", sudoku_solver(sudoku_grid))

file = open("output.txt", "w")

for i in range(9):
    for j in range(9):
        file.write(str(sudoku_grid[i][j]) + " ")
    file.write("\n")
file.close()
