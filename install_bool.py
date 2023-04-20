import sys
from pysmt.shortcuts import Solver, And, Or, Not, BOOL, Symbol, TRUE
import re


def remove_start(s):
    s = s.split(':')
    return "".join(s[1:])


def convert_input_to_list_vars(s):
    # split the: | and , symbols
    vars_list = re.split(r',|\|', s)
    # remove start space
    for i in range(len(vars_list)):
        vars_list[i] = vars_list[i].lstrip()
    # remove duplicates
    vars_list = list(dict.fromkeys(vars_list))
    # convert the vars to BOOL
    vars_list_bool = [Symbol(s, BOOL) for s in vars_list]
    return vars_list_bool


def split_or(vs):
    vars_list = vs.split("|")
    if len(vars_list) == 1:
        return Symbol(vars_list[0].lstrip(), BOOL)
    else:
        return Or([Symbol(s.lstrip(), BOOL) for s in vars_list])


def parse_and_or(s):
    vars_list = s.split(",")
    return And([split_or(vs) for vs in vars_list])


def convert_file_to_sat():
    Package_val = None
    Depends_val = None
    Conflicts_val = None
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for line in lines:
            s = line.rstrip()
            if "Package:" in s:
                s = remove_start(s)
                Package_val = Symbol(s.lstrip(), BOOL)
            elif "Depends:" in s:
                s = remove_start(s)
                Depends_val = parse_and_or(s)
            elif "Conflicts:" in s:
                s = remove_start(s)
                Conflicts_val = Not(parse_and_or(s))
            elif "Install:" in s:
                s = remove_start(s)
                Install_val = parse_and_or(s)
                print(Install_val)
                solver.add_assertion(Install_val)
                break
            else:
                if Package_val is not None and Depends_val is not None and Conflicts_val is not None:
                    equation_to_add = Or(Not(Package_val), And(Depends_val, Conflicts_val))
                elif Package_val is not None and Depends_val is not None:
                    equation_to_add = Or(Not(Package_val), Depends_val)
                elif Package_val is not None and Conflicts_val is not None:
                    equation_to_add = Or(Not(Package_val), Conflicts_val)
                else:
                    continue
                print(equation_to_add)
                solver.add_assertion(equation_to_add)
                Package_val = None
                Depends_val = None
                Conflicts_val = None
    r = solver.check_sat()
    print("result: ", r)

def check_sat():
    if solver.check_sat() == True:
        print("There is an installation plan:")
        list_of_vars = []
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
            for line in lines:
                s = line.rstrip()
                s = remove_start(s)
                if s != "":
                    list_of_vars = list_of_vars + convert_input_to_list_vars(s)
        list_of_vars = list(dict.fromkeys(list_of_vars))
        print(list_of_vars)
        for var in list_of_vars:
            if solver.get_value(var).is_true():
                print(var)
    else:
        print("There is no installation plan")


solver = Solver(name="z3")
convert_file_to_sat()
check_sat()