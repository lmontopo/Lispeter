#------GlOBAL ARRAYS------

symbol = ['+', '-', '*', '/', '<', '>','<=', '=','>=', 'abs', 'list', 'if', 'not',
			'set!', 'begin', 'let', 'define', 'lambda']


special = ['set!', 'begin', 'let', 'define', 'lambda', 'cond']



# ---- TOKENIZE ------ 
def tokenizer(holder):
	holder = '(' + holder + ')'
	holder = holder.replace( '(' , ' ( ' )
	holder = holder.replace( ')', ' ) ' )
	final = filter(lambda a: a != '', holder.split(' '))
	return final


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
# ---- PARSER ----- 
# ---- PARSER ----- 
def parse(tokens):
	if len(tokens) == 0:
		raise SyntaxError('unexpectedly entered function')
	

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
	
	
# ----- USEFUL GLOBAL FUNCTIONS ----- 
def check_type(x):
	try:
		return float(x)
	except ValueError:
		return str(x)
		
			
def is_number(x):
	print x, type(x), 'this is what were is_num testing'
	try:
		float(x)
		return True
	except ValueError:
		return False	
	except TypeError:
		return False	




# --- DICTIONARY OF VARIABLES --- 

class Scope(object):
	def __init__(self, env, parent):
		self.env = env
		self.parent = parent

	def add_values(self,key,value):
		self.env[key] = value

	def fetch(self, key):
		if key in self.env.keys():
			return self.env[key]
		elif self.parent != None:
			return self.parent.fetch(key)


# ----- INTERPRETER -------
def outter_evaluate(list_input,env):
	evaluated_list = []
	scope = Scope({}, None)

	for expression in list_input:
		evaluated_list.append(evaluate(expression,scope))

	return evaluated_list[-1] 



def evaluate(list_input,env):

	if not type(list_input) is list:
	 	return is_atom(list_input,env)
	
	elif type(list_input) is list:		
		return is_cons(list_input,env)
		
		


def is_atom(list_input,env):
	
	if is_number(list_input):			
		return float(list_input)
	elif list_input[0] == "'":   				
		return list_input[1:]
	elif list_input == 'else': 				
		return True	
	elif list_input in symbol:
		return list_input
	else: 
		try:
			print 'try to fetch value for:', list_input
			value = env.fetch(list_input)
			if is_number(value):
				return value
			elif len(value) == 2:
				return list_input
			else:
				print 'we should not have gotten here'
				return none
		except KeyError: 
			print 'keyerror'
		 	return list_input
		except TypeError:
			print 'TypeError'
		 	return list_input




def is_cons(list_input,env):

	head, rest = list_input[0], list_input[1:]
	
	if head in special:
		return call_special(list_input,env)
	else:
		return call_regular(list_input,env)




def call_special(list_input, env):

	head, rest = list_input[0], list_input[1:]
	
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
			name, exp = rest[0] , rest[1]
			fn , params = name[0], name[1:]
			env.add_values(fn, (params, exp))
			return None
		else:
			raise SyntaxError('too many arguments')


	
	
	
def call_regular(list_input,env):
	new_list_input =[]

	for term in list_input:
		new_list_input.append(evaluate(term,env))
	
	list_input = new_list_input
	head, rest = list_input[0], list_input[1:]
	print head, rest, 'our new head rest in call regular'

	

	#basic math and boolean operations
	if head in ['+', '-', '*', '/', '<', '>', '<=', '=','>=']:
		if head == '=':
			result = eval(str(rest[0]) + '==' + str(rest[1]))
			return result
		else:
			result = eval(str(rest[0]) + head + str(rest[1]))
			return result
	if head == 'not':
		result = not rest[0]  #without the added space python sees 'notTrue' instead of 'not True'
		return result


	#conditional statements	
	if head == 'if':
		condition = rest[0] 
		consequence = rest[1]
		alt = rest[2]
		if evaluate(condition, env):
			return eval(str(consequence))
		elif not evaluate(condition, env):
			return eval(str(alt))


	#absolute value
	if head == 'abs':
		if len(rest) == 1:
			return abs(rest[0])
		else:
			raise SyntaxError('abs takes only one operand!')


	#quote
	if head == 'quote':
		if len(list_input) == 2:
			return rest[0]
		else:
			raise SyntaxError('quote only takes one operand')

	#lists
	if head == 'list':
		python_list = []
		list_size = len(list_input)
		i = 1
		while i < len(list_input):
			item = evaluate(list_input[i],env)
			python_list.append(item)
			i += 1
		return python_list

	#finding functions we defined
	else:
		func_statement = env.fetch(head)
		params = func_statement[0]
		exp = func_statement[1]
		zipped = zip(params, rest)
		inner_scope = Scope({},env)
		for first, second in zipped:
 			inner_scope.add_values(first,second)
 		return evaluate(exp, inner_scope)




#------ Putting Everything Together ------ 
def interpret(input):
	output = outter_evaluate(parse(tokenizer(input)), env={})
	return output

input = '(define (func x y) (+ x y))(func 4 1)'
print interpret(input)
