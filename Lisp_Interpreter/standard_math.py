# The following functions allow addition, subtraction, mult, etc
# to take an arbitrary number of arguments (as opposed to just two)

def add(args):
    return sum(args)

def subtract(args):
    return reduce(lambda x,y: x-y, args)

def mult(args):
    return reduce(lambda x,y: x*y, args)

def div(args):
    return reduce(lambda x,y: x/y, args)

def equal(args):
    return args[1:] == args[:-1]

def less(args):
    return args[:-1] < args[1:]

def less_eq(args):
    return args[:-1] <= args[1:]

def greater(args):
    return args[:-1] > args[1:]

def greater_eq(args):
    return args[:-1] >= args[1:]

def not_func(args):
    return not(args)