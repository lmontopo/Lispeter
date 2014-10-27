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
	try:
		float(x)
		return True
	except ValueError:
		return False	
	except TypeError:
		return False	




# --- DICTIONARY OF VARIABLES --- 



env = { }

class define_function(object):
	def __init__(self, params, exp):
		self.params = params
		self.exp = exp
		self.env = {}

	def set_params(self,values):
			pram_values = zip(self.params, values)
			for i, j in param_values: 
				self.env[i] = j
			return self.env

	def call_fun(self, values):
		return evaluate(self.exp, self.set_params(values))
		
	

# ----- INTERPRETER -------
def outter_evaluate(list_input,env):
	last = len(list_input)
	
	for expression in list_input:
		evaluate(expression, env)

	return evaluate(list_input[last-1], env)



def evaluate(list_input,env):
	print list_input

	if type(list_input) is tuple:
		for item in list_input:
			evaluate(item, env)
	
	if not type(list_input) is list:
	 	return is_atom(list_input,env)
	
	elif type(list_input) is list:		
		return is_cons(list_input,env)
		
		


def is_atom(list_input,env):
	print list_input, env, 'atom'
	
	if is_number(list_input):			
		return float(list_input)
	elif list_input[0] == "'":   				
		return list_input[1:]
	elif list_input == 'else': 				
		return False	
	elif list_input in symbol:
		return list_input
	else:
		try:
			return env[list_input]	
			print env[list_input], 'dict?'		
		except KeyError: 
			return list_input
		except TypeError:
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
			env[fn] = define_function(params, exp)
			print env, 'env'
			return None	
		else:
			raise SyntaxError('too many arguments')
 

	
	
	
def call_regular(list_input,env):
	new_list_input =[]
	
	for term in list_input:
		new_list_input.append(evaluate(term,env))
	
	list_input = new_list_input
	head, rest = list_input[0], list_input[1:]
	

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

	if head in env.keys():
		print 'do we make it here?'
		return head.call_fun(rest)





#input = "(cond ((< 3 2) 1) ((= 3 2) 2) ((> 3 2) (quote here!)))"
#input = '(define (f x y) (+ x y))(f 1 2)' 
#input = '(list)(list)'

#------ Putting Everything Together ------ 
def interpret(input):
	output = outter_evaluate(parse(tokenizer(input)), env={})
	return output


#print interpret(input)
