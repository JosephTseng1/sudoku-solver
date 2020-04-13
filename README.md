# sudoku-solver

Basically, to prepare the input file, you have to use spaces to separate the numbers. If a space is blank, it is 0, else there is a number. Make sure each row is on a different line. It is assumed to be digits from 0-9 and the dimensions are 9 X 9. Also, the input is assumed to be a text file. 

For example, “input_1.txt”, “file.txt”, etc. 

The repository has several examples of valid test files for the sudoku solver. 

To run the program, type “python3 sudoku_solver.py” You will be prompted to type the name of your text file. Please type the name of the text file for your input. Once you do, there will be a message that indicates whether or not there is a solution. Regardless of the result, open up “output.txt” and it will show you the solution in the same format as your input file. If there is no solution, “output.txt” will be the same as your input file. Note that the program creates the out file called “output.txt”! Also, the program assumes the input file is valid like the one above and if the file does not exist there will be an error message!
