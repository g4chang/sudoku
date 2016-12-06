'''
propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]
'''


# Backtracking propagation
def prop_BT(csp, newVar=None):
    # Just check fully instantiated constraints
    if not newVar:
        return True, []
    for constraint in csp.get_cons_with_var(newVar):
        if constraint.get_n_unasgn() == 0:
            vals = []
            vars = constraint.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not constraint.check(vals):
                return False, []
    return True, []


# Forward checking propagation
def prop_FC(csp, newVar=None):
    constraints = []
    if newVar:
        constraints = csp.get_cons_with_var(newVar)
    else:
        constraints = csp.get_all_cons()

    prune_list = []  # output prune_list


    for constraint in constraints:
        if constraint.get_n_unasgn() == 1:
            # unassigned constrain case
            uv = constraint.get_unasgn_vars()[0]
            curr_dom = uv.cur_domain()
            for dom in curr_dom:
                if not constraint.has_support(uv, dom):
                    prune_list.append((uv, dom))
                    # Prune from current dom
                    uv.prune_value(dom)

            # Check for DWO
            if uv.cur_dom_size() == 0:
                return False, prune_list

    return True, prune_list

# GAC propagation
def prop_FC(csp, newVar=None):
    GACQ = []
    prune_list = []
    if newVar:
        GACQ.extend(csp.get_cons_with_var(newVar))
    else:
        GACQ.extend(csp.get_all_cons())

    while len(GACQ) > 0:
        constraint = GACQ.pop(0)    # getting a constraint
        for var in constraint.get_scope():
            for domain in var.cur_domain():
                if not constraint.has_support(var, domain):
                    # Current domain does not work, Prune from domain
                    prune_list.append((var, domain))
                    var.prune_value(domain)

                    if var.cur_domain_size() == 0:
                        # DWO case
                        return False, prune_list

                    # Appened the new constraint if not on queue
                    for constraint2 in csp.get_cons_with_var(var):
                        if not constraint2 in GACQ:
                            GACQ.append(constraint2)

    return True, prune_list

