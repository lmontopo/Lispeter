from __future__ import division
from termcolor import colored
from sys import exit

from standard_math import (add, subtract, mult, div, equal, less, greater,
                          less_eq, greater_eq, not_func)



SYMBOL = ['+', '-', '*', '/', '<', '>','<=', '=','>=', 'abs', 'list', 'if', 'not',
            'set!', 'begin', 'let', 'define', 'lambda', 'quote']
SPECIAL = ['set!', 'begin', 'let', 'define', 'lambda', 'cond', 'quote', 'if', 
            'list', 'map', 'cons', 'car', 'cdr']



# Pre-defined exceptions will raise if the user inputs erroneous input.  
# In some cases this also prevents the python program from crashing

class SchemeError(Exception):
    def __init__(self, msg):
        self.msg = msg


def tokenizer(holder):
    """splits input into tokens and wraps user input within an outter set of
    brackets so that the interpreter knows when its reached the input's end"""
    
    holder = '(' + holder + ')'
    holder = holder.replace( '(' , ' ( ' )
    holder = holder.replace( ')', ' ) ' )
    return filter(lambda a: a != '', holder.split(' '))
    

def parse(tokens):
    """takes the tokenized input and creates an AST"""

    if len(tokens) == 0:
        raise SchemeError('Error: unexpectedly entered parse function with no input.')
    
    token = tokens[0]
    tokens = tokens[1:]

    if token == '(':
        parsed_input = [] 
        
        while tokens[0] != ')':
            to_append, tokens = parse(tokens)
            parsed_input.append(to_append)
        tokens = tokens[1:]     #pops off the ')' part
        
        if len(tokens) == 0:  #if last return
            return parsed_input #only returns parsed input

        if len(tokens) > 0: #if not last return
            return parsed_input, tokens #returns partially parsed input and stuff to be parsed
                                
    else:
        return check_type(token), tokens  #always return numbers as float
    
    

def check_type(x):
    try:
        return float(x)
    except ValueError:
        return str(x)
        
            
def is_number(x):
    """returns true if is number and false otherwise"""
    try:
        float(x)
        return True
    except ValueError:  #get value error when str inputed
        return False    
     


class Scope(object):
    """Used to keep track of scope while interpreter interprets.  
    All scopes beside the global will point to a parent scope. 
    When a variable is needed the current scope will be
    searched first, followed by the parent scope if necessary.""" 

    def __init__(self, env, parent = None):
        self.env = env
        self.parent = parent

    def add_values(self,key,value):
        self.env[key] = value

    def fetch(self, key): #fetch returns none if it can't find item
        if key in self.env.keys():
            return self.env[key]
        elif self.parent != None:
            return self.parent.fetch(key)




# All standard math and boolean operators are turned into MakePyFun instances
# All user defined functions and lambda calls will be turned into MakeLambda 
# intances.  Both MakeLambda and MakePyFun have 'do_fun' methods, so that they
# can all be executed by calling 'do_fun'.

class MakeLambda(object):
    """User defined function names will map (in the scope's dictionary)
    to a MakeLambda instance containing defined params and expression. """

    def __init__(self, first, second):
        self.params = first
        self.exp = second[-1]  #Scheme accepts > 1 body expressions but only returns result of last

    def do_fun(self, args, env):
        zipped = zip(self.params, args)
        temp_scope = Scope({}, env)
        for param, arg in zipped:
            temp_scope.add_values(param, arg)
        return evaluate(self.exp, temp_scope)


class MakePyFun(object):
    """This is a very simple wrapper around the already defined standard 
    math functions"""

    def __init__(self, everything):
        self. everything = everything

    def do_fun(self, arguments, env):
        if len(arguments) > 1:
            return self.everything(arguments)
        elif len(arguments) == 1:
            return self.everything(*arguments)



def outter_evaluate(list_input,env):
    """Takes a list containing the user input, calls evaluate() on each item
    in the list, and returns the result of the last one"""

    evaluated_list = []
    for expression in list_input:
        evaluated_list.append(evaluate(expression, env))
    return evaluated_list[-1]


def evaluate(list_input,env):
    """Redirects expression to either evaluate_atom or evaluate_cons"""

    if not type(list_input) is list:
        return evaluate_atom(list_input,env)  
    elif type(list_input) is list:      
        return evaluate_cons(list_input,env)
        
        
def evaluate_atom(list_input,env):
    """handles the self evaluating expressions, called atoms"""

    if is_number(list_input):           
        return list_input
    elif list_input[0] == "'":                  
        return list_input[1:]
    elif list_input == 'else':              
        return True 
    elif list_input in SYMBOL:
        return list_input
    else: 
        value = env.fetch(list_input)
        if value != None:  #value is none if not in env
            return value
        else:
            raise SchemeError("Error: can't find element in dictionary. Improper input.")
        

def evaluate_cons(list_input,env):
    """Redirects to either evaluate_special or evaluate_regular 
    depending on whether or not the 'head' is a special form. """

    head, rest = list_input[0], list_input[1:]

    if head in SPECIAL:
        return evaluate_special(list_input,env)
    else:
        return evaluate_regular(list_input,env)



def evaluate_special(list_input, env):
    """Handles all special forms, each special form has
    their own code to execute and handle it"""

    head, rest = list_input[0], list_input[1:]

    if head == "map":
        if len(rest) == 2:
            new_head, list_to_act_on = rest[0], evaluate(rest[1], env)
            new_list = []
            for item in list_to_act_on:
                new_item = interpret("(%s %s)" %(new_head, item), env)
                new_list.append(new_item)
            return new_list
    
    if head == 'cond':
        switch = 1
        while switch == 1:
            for item in rest:
                if evaluate(item[0],env):
                    switch = 0
                    return evaluate(item[1],env)
            break

    if head == 'define':
        if len(rest) == 2:      # name binding
            if type(rest[0]) is str:
                env.add_values(rest[0], evaluate(rest[1], env))   
            else:               # function definition
                name = rest[0][0]
                expression = MakeLambda(rest[0][1:], rest[1:])
                env.add_values(name, expression)
        else:
            raise SchemeError("Error: too many arguments were inputed.")

    if head == 'lambda':
        func = MakeLambda(rest[0],rest[1:])
        env.add_values('lam', func)  
        return 'lam'   
        
    if head == 'if':
        try: 
            condition, consequence, alt = rest[0], rest[1], rest[2]
        except:
            raise SchemeError("Error: must specify a consequence and an alternate.")
        if evaluate(condition, env):
            return evaluate(consequence, env)
        else:
            return evaluate(alt, env)
        
    if head == 'quote':
        if len(list_input) == 2:
            return rest[0]
        else:
            raise SchemeError('Error: quote only takes one operand.')

    if head == 'let':
        local_scope = Scope({},env)
        if type(rest[0][0]) is list:
            for item in rest[0]:
                for a , b in rest[0]:
                    local_scope.add_values(a, evaluate(b, env))
            return evaluate(rest[1], local_scope)
        else:
            raise SchemeError('Error: let must be followed by a list.')


    if head == 'set!':
        if len(rest) == 2:
            name, exp = rest[0], rest[1]
            if name in env.env.keys():
                if type(name) is str:
                    env.add_values(name, exp)
                    return None
                else:
                    fn , params = name[0], name[1:]
                    env.add_values(fn, (fn, params, exp))
            else:
                set_error = SchemeError('Error: %s has not yet been defined' % name)
                raise set_error

    if head == 'begin':
        return outter_evaluate(rest,env)

    if head == 'cons':
        if len(rest) == 2:
            cons_list = []
            for item in rest:
                cons_list.append(evaluate(item,env))
            return cons_list

    if head == 'list':
        python_list = []
        list_size = len(list_input)
        i = 1
        while i < len(list_input):
            item = list_input[i] # has already been evaluated
            python_list.append(evaluate(item, env))
            i += 1
        return python_list

    if head == 'car':
        new_item = evaluate(rest[0], env)
        if type(new_item) is list:
            return new_item[0]

    if head == 'cdr':
        new_item = evaluate(rest[0], env)
        if type(new_item) is list:
            return new_item[1:]


    
def evaluate_regular(list_input,env):
    """handles all normal form operators including user defined functions, 
    and the lambdas which will have been turned into 'lam' and put into environment"""

    new_list_input =[]

    for term in list_input:
        new_list_input.append(evaluate(term,env)) #recursive call

    list_input = new_list_input
    head, rest = list_input[0], list_input[1:]

    try:
        return env.fetch(head).do_fun(rest, env)
    except AttributeError:
        return head.do_fun(rest, env)
    except TypeError:
        raise SchemeError("Error: the wrong number of arguments have been inputed.")



def interpret(input, env):
    return outter_evaluate(parse(tokenizer(input)), env)


#This libary function allows for the global scope to be re-instantiated during
#testing, so that there isn't interactino between tests

def library():
    """creates a dictionary with all of the predifined operators"""

    library = { '+': MakePyFun(add), 
                '-': MakePyFun(subtract), 
                '*': MakePyFun(mult), 
                '/': MakePyFun(div),
                '=': MakePyFun(equal), 
                '<': MakePyFun(less), 
                '<=': MakePyFun(less_eq), 
                '>': MakePyFun(greater), 
                '>=': MakePyFun(greater_eq),
                'abs': MakePyFun(abs),
                'not': MakePyFun(not_func) 
                }

    scheme_library =    {
    '!': MakeLambda(['n'], parse(tokenizer('(if (= n 0)  1 (* n (! (- n 1))))')))
                        }
        
    library.update(scheme_library)
    return library


def repl(env):
    while True:
        try: 
            x = raw_input('> ')
            try:
                print interpret(x, env)
            except SchemeError, e: 
                print(colored(e.msg, 'red')) 
        except KeyboardInterrupt:
            exit()  #exits the program

if __name__ == "__main__":
    global_scope = Scope(library(), None)
    repl(global_scope)
