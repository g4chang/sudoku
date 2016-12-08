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
                temp = Variable('V' + str(row) + str(col), range(1,10))
                vars_all[row][col] = temp
            else:
                temp = Variable('V' + str(row) + str(col), [init_value])
                vars_all[row][col] = temp
                
    return vars_all            



def get_row(board, i):
    '''Gets the row i of the board'''
    return board[i]



def get_col(board, i):
    '''Gets the col i of the board'''
    return [board[k][i] for k in range(len(board))]


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
    #IMPLEMENT
    i = 0
    dom = [1,2,3,4,5,6,7,8,9]
    #construct variables
    vars = []
    #get fixed points => these variables' domain have only one value
    i_index = 0
    
    fix_points = []
    for i in initial_sudoku_board:
        j_index = 0
        for j in i:
            if j != 0:
                fix_points.append((i_index, j_index, j))
            j_index += 1
        i_index += 1
    
    print("ban var finished...")
    #construct all variables, set each variables' domain based on fixed points
    i_index = 0
    for i in initial_sudoku_board:
        j_index = 0
        #ban list of values in every variable in this row
        r_baned = [el[2] for el in fix_points if (el[0] == i_index)]
        for j in i:
            #ban list of values in every variable in this column
            c_baned = [el[2] for el in fix_points if (el[1] == j_index)]
            if j == 0:
                vars.append(Variable("({}, {})".format(i_index, j_index), dom))
                for val_index in range(9):
                    if (dom[val_index] in r_baned) or (dom[val_index] in c_baned):
                        vars[-1].curdom[val_index] = False
            else:
                vars.append(Variable("({}, {})".format(i_index, j_index), [j]))
            j_index += 1
        i_index += 1
    #ban fixed values in each small square
    for i in range(9):
        scope = get_square(vars, i)
        buf = []
        for var in scope:
            if len(var.domain()) == 1:
                buf.append(var.domain()[0])
        for var in scope:
            if len(var.domain()) != 1:
                cur_dom = var.cur_domain()
                for baned_val in buf:
                    if baned_val in cur_dom:
                        var.curdom[var.domain().index(baned_val)] = False
                    
                    
            
    print("cosntruct var finished...")
    #construct constrains
    cons = []
    #construct constrains representing each row
    for i in range(9):
        con = Constraint("C Row{}".format(i), vars[(i * 9) : ((i+1) * 9)])
        sat_tuples = []
        nmb = []
        for var in con.scope:
            nmb.append(var.cur_domain())
        for t in itertools.product(nmb[0], nmb[1], nmb[2], nmb[3], nmb[4], nmb[5], nmb[6], nmb[7], nmb[8]):
            if len(set(t)) == 9:
                sat_tuples.append(t)
        if i == 0:
            print(nmb[0])
            print(nmb[1])
            print(nmb[2])
            print(nmb[3])
            print(nmb[4])
            print(nmb[5])
            print(nmb[6])
            print(nmb[7])
            print(nmb[8])
            print("Constrain", i, " --- ",sat_tuples)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    print("row finished...")
    #construct constrains representing each row
    for i in range(9):
        scope = []
        for j in range(9):
            scope.append(vars[i + (j * 9)])
        con = Constraint("C Col{}".format(i), scope)
        sat_tuples = []
        nmb = []
        for var in con.scope:
            nmb.append(var.cur_domain())
        for t in itertools.product(nmb[0], nmb[1], nmb[2], nmb[3], nmb[4], nmb[5], nmb[6], nmb[7], nmb[8]):
            if len(set(t)) == 9:
                sat_tuples.append(t)
        print("Constrain", i, " --- ",len(sat_tuples))
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    print("col finished...")  
    #construct constrains representing each row
    for i in range(9):
        scope = get_square(vars, i)
        '''
        for j in range(3):
            scope.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 0])
            scope.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 1])
            scope.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 2])
        '''
        con = Constraint("C sqr{}".format(i), scope)
        sat_tuples = []
        nmb = []
        for var in con.scope:
            nmb.append(var.cur_domain())
        for t in itertools.product(nmb[0], nmb[1], nmb[2], nmb[3], nmb[4], nmb[5], nmb[6], nmb[7], nmb[8]):
            if len(set(t)) == 9:
                sat_tuples.append(t)
        print("Constrain", i, " --- ",len(sat_tuples))
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    print("sqr finished...")   
    #construct CSP  
    sudoku_csp = CSP("sudoku_csp_all_diff_model", vars)
    for c in cons:
        sudoku_csp.add_constraint(c)
    variable_array = []
    for i in range(9):
        variable_array.append(vars[(i * 9) : ((i+1) * 9)])
    wcnmb = BT(sudoku_csp)
    wcnmb.restore_all_variable_domains()
    print("all done...")
    return sudoku_csp, variable_array

def get_square(vars, n):
    if n == 0:
        s = 0
    if n == 1:
        s = 3
    if n == 2:
        s = 6
    if n == 3:
        s = 27
    if n == 4:
        s = 30
    if n == 5:
        s = 33
    if n == 6:
        s = 54
    if n == 7:
        s = 57
    if n == 8:
        s = 60
        
    ss = s + 9
    sss = ss + 9
    return [vars[s], vars[s + 1], vars[s + 2],
            vars[ss], vars[ss + 1], vars[ss + 2],
            vars[sss], vars[sss + 1], vars[sss + 2]]