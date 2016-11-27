#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''
#IMPLEMENT
    unasgn_vars = csp.get_all_unasgn_vars()
    min_domain_size = 10000
    min_unasgn_var = None
    for unasgn_var in unasgn_vars:
        if unasgn_var.cur_domain_size() < min_domain_size:
            min_domain_size = unasgn_var.cur_domain_size()
            min_unasgn_var = unasgn_var
    return min_unasgn_var


def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node, 
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''    
#IMPLEMENT
    cons = csp.get_all_cons()
    var_to_degree = {}
    for con in cons:
        for var in con.get_unasgn_vars():
            if var not in var_to_degree:
                var_to_degree[var] = con.get_n_unasgn()
            else:
                var_to_degree[var] += con.get_n_unasgn()    
    return max(var_to_degree, key=var_to_degree.get)


def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain values in other 
    variables that share at least one constraint with var.
    '''    
#IMPLEMENT
    val_to_eliminate = {}
    # dict that stores the length of the current domain of other variables 
    # before assigning var a val
    before_asgn_len = {}
    # dict that stores the length of the current domain of other variables
    # after assigning var a val
    after_asgn_len = {}
    
    domain = var.cur_domain()
    cons = csp.get_cons_with_var(var)
    
    for val in domain:
        
        var.assign(val)
        for con in cons:
            for other_var in con.get_unasgn_vars():
                if other_var not in after_asgn_len:
                    after_asgn_len[other_var] = len(other_var.cur_domain())
                elif len(other_var.cur_domain()) < after_asgn_len[other_var]:
                    after_asgn_len[other_var] = len(other_var.cur_domain())
                    
        var.unassign()
        for con in cons:
            for other_var in list(after_asgn_len.keys()):
                if other_var not in before_asgn_len:
                    before_asgn_len[other_var] = len(other_var.cur_domain())
                elif len(other_var.cur_domain()) < before_asgn_len[other_var]:
                    before_asgn_len[other_var] = len(other_var.cur_domain())
         
        total_eliminate = 0            
        for other_var in list(after_asgn_len.keys()):
            total_eliminate += before_asgn_len[other_var] - after_asgn_len[other_var]
        val_to_eliminate[val] = total_eliminate
        
    return sorted(val_to_eliminate, key=val_to_eliminate.get)


def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    '''    
#IMPLEMENT
    # Use Degree Heuristic as a tier breaker 
    for i in csp.get_all_unsign_vars():
        for j in csp.get_all_unsign_vars():
            if i != j and i.cur_domain_size() != j.cur_domain_size():
                return ord_mrv(csp)
    return ord_dh(csp)
