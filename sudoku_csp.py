'''Construct and return sudoku CSP models.'''

from cspbase import *
import itertools



def init_vars(initial_sudoku_board):
    vars_all = [[None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None]]
    
    for row in range(9):
        for col in range(9):
            init_value = initial_sudoku_board[row][col]        
            if init_value == 0:
                vars_all = Variable('V' + str(row) + str(col), range(1,10))
                vars_all[row][col] = vars_all
            else:
                vars_all = Variable('V' + str(row) + str(col), [init_value])
                vars_all[row][col] = vars_all
                
    return vars_all            



def get_row(board, row_i):
    return board[row_i]



def get_col(board, col_j):
    return [board[j][i] for j in range(9)]


def get_subsquare(board, i):
    first_row = (i // 3) * 3
    first_col = (i % 3) * 3
    subsquare = [None] * 9
    for j in range(9):
        subrj = j // 3
        subcj = j % 3
        subsquare[j] = board[first_row + subrj][first_col + subcj]
    return subsquare



def all_diff(lst):
    '''
    Helper function to determine if lst contains duplicates.
    lst is either a row or a column or a subsquare
    '''    
    return len(set(lst)) == len(lst)

       
#Binary
#return csp and all_variables (each varibable's own constrain)
#give actual value or range of values in here
#use sudoku_csp = CSP(asdad)
#    sudoku_csp.add_constraint
def sudoku_csp_binary_model(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudoku board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1--n.
       E.g., the board
    
       -------------------  
       |1|3|4|1|
       |3|1|2|4|
       |2|4|2|3|
       |1|2|3|2|
       -------------------
       would be represented by the list of lists
       
       [[1,3,4,1],
       [3,1,2,4],
       [2,4,2,3],
       [1,2,3,2]]
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {0,i}, with i being
       the initial value of the cell in the board. 
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.)
       
       All of the constraints of Model_1 MUST BE binary constraints 
       (i.e., constraints whose scope includes exactly two variables).
    '''

    size = 9 #len of sudoku board
    vars_all = init_vars(initial_sudoku_board)
    chain_lst = list(itertools.chain(*vars_all))
    sudoku_csp = CSP('sudoku_csp_binary_model', chain_lst)
    
    #Row constraint
    for i in range(size):
        row_i = get_row(vars_all, i)
        for j in range(size):
            for k in range(j + 1, size):
                cell_j = row_i[j]
                cell_k = row_i[k]
                con_name = 'C_Row' + cell_j.name + cell_k.name
                con_scope = [cell_j, cell_k]
                con = Constraint(con_name, con_scope)   
                
      
                sat_tup = [[x,y] 
                            for x in cell_j.cur_domain()
                            for y in cell_k.cur_domain() 
                            if x != y ]
                    
                con.add_satisfying_tuples(sat_tup)                    
                sudoku_csp.add_constraint(con)
                
    #Column constraint            
    for i in range(size):
        col_i = get_col(vars_all, i)
        for j in range(size):
            for k in range(j + 1, size):
                cell_j = col_i[j]
                cell_k = col_i[k]
                con_name = 'C_Col' + cell_j.name + cell_k.name
                con_scope = [cell_j, cell_k]
                con = Constraint(con_name, con_scope)    
                     
                sat_tup = [[x,y] 
                            for x in cell_j.cur_domain()
                            for y in cell_k.cur_domain() 
                            if x != y ]
                    
                con.add_satisfying_tuples(sat_tup)
                sudoku_csp.add_constraint(con)
    
    #Subsqure constraint
    for i in range(size):
            sub_i = get_subsquare(vars_all, i)
            for j in range(size):
                for k in range(j + 1, size):
                    cell_j = sub_i[j]
                    cell_k = sub_i[k]
                    con_name = 'C_Sub' + cell_j.name + cell_k.name
                    con_scope = [cell_j, cell_k]
                    con = Constraint(con_name, con_scope)    
                         
                    sat_tup = [[x,y] 
                                for x in cell_j.cur_domain()
                                for y in cell_k.cur_domain() 
                                if x != y ]
                        
                    con.add_satisfying_tuples(sat_tup)
                    sudoku_csp.add_constraint(con)    
                
    return sudoku_csp, vars_all
    

#All Diff
def sudoku_csp_all_diff_model(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudoku board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1--n.
       E.g., the board
    
       -------------------  
       |1|3|4|1|
       |3|1|2|4|
       |2|4|2|3|
       |1|2|3|2|
       -------------------
       would be represented by the list of lists
       
       [[1,3,4,1],
       [3,1,2,4],
       [2,4,2,3],
       [1,2,3,2]]

       The input board takes the same input format (a list of n lists 
       specifying the board as sudoku_csp_model_1).
   
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0,i}, where i is
       the initial value of the cell.

       However, model_2 has different constraints.  In particular, instead
       of binary not-equals constraints, model_2 has 2n n-ary constraints
       that resemble a modified all-different constraint.  Each constraint
       is over n variables.  For any given row (resp. column), that 
       constraint will incorporate both the adjacent black squares and 
       no repeated numbers rules.
       
    '''

    size = 9
    vars_all = init_vars(initial_sudoku_board)
    vars = list(itertools.chain(*vars_all))
    sudoku_csp = CSP('sudoku_csp_model_2', vars)
    
    for i in range(size):
        row_i = get_row(vars_all, i)
        con_name = 'C_Row' + str(i)
        con_scope = row_i
        con = Constraint(con_name, con_scope) 
        
        sat_tup = []
        row_vars_domains = [var.cur_domain() for var in con_scope]
        row_tuple = list(itertools.product(*row_vars_domains))
        for t in row_tuple:
            if all_diff(list(t)):
                sat_tup.append(t)
        con.add_satisfying_tuples(sat_tup)
        sudoku_csp.add_constraint(con)
             
    for i in range(size):
        col_i = get_col(vars_all, i)
        con_name = 'C_Col' + str(i)
        con_scope = col_i
        con = Constraint(con_name, con_scope) 
        
        sat_tup = []
        col_vars_domains = [var.cur_domain() for var in con_scope]
        col_tuple = list(itertools.product(*col_vars_domains))
        for t in col_tuple:
            if all_diff(list(t)):
                sat_tup.append(t)
        con.add_satisfying_tuples(sat_tup)
        sudoku_csp.add_constraint(con)
        
    for i in range(size):
        sub_i = get_subsquare(vars_all, i)
        con_name = 'C_Sub' + str(i)
        con_scope = sub_i
        con = Constraint(con_name, con_scope) 
        
        sat_tup = []
        sub_vars_domains = [var.cur_domain() for var in con_scope]
        sub_tuple = list(itertools.product(*sub_vars_domains))
        for t in sub_tuple:
            if all_diff(list(t)):
                sat_tup.append(t)
        con.add_satisfying_tuples(sat_tup)
        sudoku_csp.add_constraint(con)    
        
    return sudoku_csp, vars_all
