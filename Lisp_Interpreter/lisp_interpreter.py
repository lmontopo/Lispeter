from __future__ import division
from termcolor import colored
from sys import exit

# ------ GlOBAL ARRAYS ------

symbol = ['+', '-', '*', '/', '<', '>','<=', '=','>=', 'abs', 'list', 'if', 'not',
			'set!', 'begin', 'let', 'define', 'lambda', 'quote']
special = ['set!', 'begin', 'let', 'define', 'lambda', 'cond', 'quote', 'if', 
			'list', 'map', 'cons', 'car', 'cdr']


# ------ EXCEPTIONs ------
class MyError(Exception):
	def __init__(self, msg):
		self.msg = msg

invalid_input_error = MyError("Error: invalid input type")
arguments_error = MyError("Error: the wrong number of arguments have been inputed.")
if_error = MyError("Error: you need to specify by a consequence and an alternate.")
dict_error = MyError("Error: can't find element in dictionary. Improper input.")
first_error = MyError('Error: unexpectedly entered parse function with no input.')
too_many = MyError("Error: too many arguments were inputed.")
quote_error = MyError('Error: quote only takes one operand.')
let_error = MyError('Error: let must be followed by a list.')

# ------ TOKENIZE ------ 
def tokenizer(holder):
	"""splits input into tokens and wraps user input within an outter set of
	brackets so that the interpreter knows when its reached the input's end"""
	
	holder = '(' + holder + ')'
	holder = holder.replace( '(' , ' ( ' )
	holder = holder.replace( ')', ' ) ' )
	return filter(lambda a: a != '', holder.split(' '))
	
  
# ------ PARSER ------ 
def parse(tokens):
	"""takes the tokenized input and creates an AST"""

	if len(tokens) == 0:
		raise first_error
	
	token = tokens[0]
	tokens = tokens[1:]

	if token == '(':
		parsed_input = [] 
		
		while tokens[0] != ')':
			to_append, tokens = parse(tokens)
			parsed_input.append(to_append)
		tokens = tokens[1:]					#pops off the ')' part
		
		#we add a condition to check if last return
		if len(tokens) > 0:
			return parsed_input, tokens 	#if not last return, need to return current version of holder
		elif len(tokens) == 0 :
			return parsed_input						#if last return, only want to return new_holder			
	else:
		return check_type(token), tokens
	
	
# ------ USEFUL GLOBAL FUNCTIONS ------ 
def check_type(x):
	try:
		return float(x)
	except ValueError:
		return str(x)
		
			
def is_number(x):
	try:
		float(x)
		return True
	except ValueError:
		return False	
	except TypeError:
		return False	


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



# ------ DEFINING SCOPE ------ 
class Scope(object):
	def __init__(self, env, parent = None):
		self.env = env
		self.parent = parent

	def add_values(self,key,value):
		self.env[key] = value

	def fetch(self, key):
		if key in self.env.keys():
			return self.env[key]
		elif self.parent != None:
			return self.parent.fetch(key)


# ------ CLASS OF FUNCTIONS ------
class MakeLambda(object):
	def __init__(self, first, second):
		self.first = first
		self.second = second
		self.params = self.first
		self.exp = self.second[-1]

	def do_fun(self, args, env):
		zipped = zip(self.params, args)
		temp_scope = Scope({}, env)
		for param, arg in zipped:
			temp_scope.add_values(param, arg)
		return evaluate(self.exp, temp_scope)


class MakePyFun(object):
	def __init__(self, everything):
		self. everything = everything

	def do_fun(self, arguments, env):
		if len(arguments) > 1:
			return self.everything(arguments)
		elif len(arguments) == 1:
			return self.everything(*arguments)



# ------ INTERPRETER ------
def outter_evaluate(list_input,env):
	"""Takes a list containing the user input, calls evaluate() on each item
	in the list, and returns the result of the last one"""

	evaluated_list = []
	for expression in list_input:
		evaluated_list.append(evaluate(expression, env))
	return evaluated_list[-1]


def evaluate(list_input,env):
	if not type(list_input) is list:
	 	return is_atom(list_input,env)	
	elif type(list_input) is list:		
		return is_cons(list_input,env)
		
		
def is_atom(list_input,env):
	if is_number(list_input):			
		return list_input
	elif list_input[0] == "'":   				
		return list_input[1:]
	elif list_input == 'else': 				
		return True	
	elif list_input in symbol:
		return list_input
	else: 
		
		value = env.fetch(list_input)
		if is_number(value):
			return value
		if type(value) is list:
			return evaluate(value, env)
		else:
			return list_input  #returns 'bla' for when 'bla' is a user defined function


def is_cons(list_input,env):
	head, rest = list_input[0], list_input[1:]

	if head in special:
		return call_special(list_input,env)
	else:
		return call_regular(list_input,env)



def call_special(list_input, env):
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
		if len(rest) == 2:
			if type(rest[0]) is str:
				env.add_values(rest[0], rest[1])
			else:
				name = rest[0][0]
				expression = MakeLambda(rest[0][1:], rest[1:])
				env.add_values(name, expression)
		else:
			raise too_many

	if head == 'lambda':
		func = MakeLambda(rest[0],rest[1:])
		env.add_values('lam', func)
		return 'lam'
		
	if head == 'if':
		try: 
			condition, consequence, alt = rest[0], rest[1], rest[2]
		except:
			raise if_error
		
		if evaluate(condition, env):
			return evaluate(consequence, env)
		else:
			return evaluate(alt, env)
		
	if head == 'quote':
		if len(list_input) == 2:
			return rest[0]
		else:
			raise quote_error

	if head == 'let':
		local_scope = Scope({},env)
		if type(rest[0][0]) is list:
			for item in rest[0]:
				for a , b in rest[0]:
					local_scope.add_values(a, evaluate(b, env))
			return evaluate(rest[1], local_scope)
		else:
			raise let_error

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
				set_error = MyError('Error: %s has not yet been defined' % name)
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


	
def call_regular(list_input,env):
	new_list_input =[]

	for term in list_input:
		new_list_input.append(evaluate(term,env))

	list_input = new_list_input
	head, rest = list_input[0], list_input[1:]
	for item in rest:
		if not is_number(item):
			raise invalid_input_error
	try:
		print head
		return env.fetch(head).do_fun(rest, env)
	except TypeError:
		raise arguments_error



# ------ Putting Everything Together ------ 
def interpret(input, env):
	return outter_evaluate(parse(tokenizer(input)), env)

def library():
	"""Turns the math non-special operators into MakePyFun Instances
	so that they can all be handled in the same way.
	Turns any defined 'combination' of these into a MakeLambda instance"""

	library = {	'+': MakePyFun(add), 
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

	scheme_library = 	{
	'!': MakeLambda(['n'], parse(tokenizer('(if (= n 0)  1 (* n (! (- n 1))))')))
						}
		
	library.update(scheme_library)
	return library


def repl(env):
	try: 
		x = raw_input('> ')
		try:
			print interpret(x, env)
		except MyError, e: 
			print(colored(e.msg, 'red')) 
		return repl(global_scope)
	except KeyboardInterrupt:
		exit()

if __name__ == "__main__":
	global_scope = Scope(library(), None)
	repl(global_scope)