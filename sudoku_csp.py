'''
Construct and return hitori CSP models.
'''

from cspbase import *
import itertools



def init_vars(initial_hitori_board):
    '''
    Helper function that returns all Variables in initial_hitori_board.
    '''
    size = len(initial_hitori_board)
    vars_all = []
    vars_row = []
    
    for row in range(size):
        for col in range(size):
            init_value = initial_hitori_board[row][col]
            var_name = 'V' + str(row) + str(col)
            var_init_domain = [0, init_value]
            var = Variable(var_name, var_init_domain)
            vars_row.append(var)
        vars_all.append(vars_row)
        vars_row = []
        
    return vars_all



def get_row(vars_all, row_i):
    '''
    Helper function that returns the ith row.
    '''
    return vars_all[row_i]



def get_col(vars_all, col_j):
    '''
    Helper function that returns the ith column.
    '''
    col = []
    for i in range(len(vars_all)):
        col.append(vars_all[i][col_j])
    return col



def check_constraints(lst):
    '''
    Helper function to determine if all constraints are satisfied 
    on certain row or column.
    '''
    if 0 not in lst: # check duplicates
        return len(set(lst)) == len(lst)
    else:
        for i in range(len(lst)-1):
            if lst[i] == 0 and lst[i+1] == 0: # check adjacent black squares
                return False
        tmp = lst
        while 0 in tmp: # remove all the non-adjacent black squares
            tmp.remove(0)
        return len(set(tmp)) == len(lst) - lst.count(0)
        
    
       

def hitori_csp_model_1(initial_hitori_board):
    '''Return a CSP object representing a hitori CSP problem along 
       with an array of variables for the problem. That is return

       hitori_csp, variable_array

       where hitori_csp is a csp representing hitori using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the hitori board (indexed from (0,0) to (8,8))

       
       
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

##IMPLEMENT
    size = len(initial_hitori_board)
    vars_all = init_vars(initial_hitori_board)
    vars = list(itertools.chain(*vars_all))
    hitori_csp = CSP('hitori_csp_model_1', vars)
    
    for i in range(size):
        row_i = get_row(vars_all, i)
        for j in range(size):
            for k in range(j + 1, size):
                cell_j = row_i[j]
                cell_k = row_i[k]
                con_name = 'C_Row' + cell_j.name + cell_k.name
                con_scope = [cell_j, cell_k]
                con = Constraint(con_name, con_scope)   
                
                if k == j + 1: # adjacent cells must be distinct        
                    sat_tup = [[x,y] 
                                for x in cell_j.cur_domain()
                                for y in cell_k.cur_domain() 
                                if x != y ]
                else: # non-adjacent cells
                    sat_tup = [[x,y] 
                                for x in cell_j.cur_domain()
                                for y in cell_k.cur_domain() 
                                if x != y or x == 0 or y == 0]
                    
                con.add_satisfying_tuples(sat_tup)                    
                hitori_csp.add_constraint(con)
                
    for i in range(size):
        col_i = get_col(vars_all, i)
        for j in range(size):
            for k in range(j + 1, size):
                cell_j = col_i[j]
                cell_k = col_i[k]
                con_name = 'C_Col' + cell_j.name + cell_k.name
                con_scope = [cell_j, cell_k]
                con = Constraint(con_name, con_scope)    
                
                if k == j + 1: # adjacent cells must be distinct        
                    sat_tup = [[x,y] 
                                for x in cell_j.cur_domain()
                                for y in cell_k.cur_domain() 
                                if x != y ]
                else: # non-adjacent cells
                    sat_tup = [[x,y] 
                                for x in cell_j.cur_domain()
                                for y in cell_k.cur_domain() 
                                if x != y or x == 0 or y == 0]
                    
                con.add_satisfying_tuples(sat_tup)
                hitori_csp.add_constraint(con)   
                
    return hitori_csp, vars_all
    



##############################

def hitori_csp_model_2(initial_hitori_board):
    '''Return a CSP object representing a hitori CSP problem along 
       with an array of variables for the problem. That is return

       hitori_csp, variable_array

       where hitori_csp is a csp representing hitori using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the hitori board (indexed from (0,0) to (8,8))

       
       
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
       specifying the board as hitori_csp_model_1).
   
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

###IMPLEMENT 
    size = len(initial_hitori_board)
    vars_all = init_vars(initial_hitori_board)
    vars = list(itertools.chain(*vars_all))
    hitori_csp = CSP('hitori_csp_model_2', vars)
    
    for i in range(size):
        row_i = get_row(vars_all, i)
        con_name = 'C_Row' + str(i)
        con_scope = row_i
        con = Constraint(con_name, con_scope) 
        
        sat_tup = []
        row_vars_domains = [var.cur_domain() for var in con_scope]
        row_tuple = list(itertools.product(*row_vars_domains))
        for t in row_tuple:
            if check_constraints(list(t)):
                sat_tup.append(t)
        con.add_satisfying_tuples(sat_tup)
        hitori_csp.add_constraint(con)
             
    for i in range(size):
        col_i = get_col(vars_all, i)
        con_name = 'C_Col' + str(i)
        con_scope = col_i
        con = Constraint(con_name, con_scope) 
        
        sat_tup = []
        col_vars_domains = [var.cur_domain() for var in con_scope]
        col_tuple = list(itertools.product(*col_vars_domains))
        for t in col_tuple:
            if check_constraints(list(t)):
                sat_tup.append(t)
        con.add_satisfying_tuples(sat_tup)
        hitori_csp.add_constraint(con)
        
    return hitori_csp, vars_all
