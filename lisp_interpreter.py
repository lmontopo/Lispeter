#holder = "((lambda (a b) (+ a b)) 5 6)"
#holder = '(define x 3)(* (+ 3 2) x)'
#holder = '((lambda (a) a) "blahblahblahblahblah")'
#holder = '((define add3 (lambda (x) (+ x 3))) (add3 3))'
#holder = '(+ 1 (abs -1))'
holder = '(list 1 (+ 1 1) 3 4)'

# ---- TOKENIZE ------ 
holder = '(' + holder + ')'							#adding extra outer brackets
holder = holder.replace( '(' , ' [ ' )
holder = holder.replace( ')', ' ] ' )
holder = holder.split(' ')
holder = filter(lambda a: a != '', holder)
print holder, 'before parsing'


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


# ---- PARSER ----- 
def parse(holder):
	if len(holder) == 0:
		raise SyntaxError('unexpectedly entered function')
	
	token = holder[0]
	holder = holder[1:]

	if token == '[':
		new_holder = [] #sets new holder as an array
		
		while holder[0] != ']':
			to_append, holder = parse(holder)
			new_holder.append(to_append)
		holder = holder[1:]							#pops off the ')' part
		
		#we add a condition to check if last return
		if len(holder) > 0:
			return new_holder , holder 				#if not last return, need to return current version of holder
		elif len(holder) == 0 :
			return new_holder						#if last return, only want to return new_holder
	else:
		return check_type(token), holder 			#this is never last return, so we always need both
	
holder = parse(holder)
print holder, 'after parsing'

# --- DICTIONARY OF VARIABLES --- 
var_dict = { }
	


# ----- INTERPRETER ------- 
def evaluate(list_input):
	
	#base case
	if not type(list_input) is list:
		if is_number(list_input) == True:
			return list_input
		elif is_number(list_input) == False:
			return var_dict[list_input]
	
	#evaluation
	opp = list_input[0]

	#removes any outermost brackets that are redundant
	if type(opp) is list and len(list_input) == 1:
		return evaluate(list_input[0])
	
	#---if operator is not list---
	if not type(opp) is list:
		
		#basic math operations
		if opp in ['+', '-', '*', '/']:
			
			#recursion	
			result = eval(str(evaluate(list_input[1])) + opp + str(evaluate(list_input[2])))
			return result
			
		#absolute value
		if opp == 'abs':
			if len(list_input) == 2:
				return abs(evaluate(list_input[1]))
			else:
				raise SyntaxError('abs takes only one operand!')
		
		#lists
		if opp == 'list':
			python_list = []
			list_size = len(list_input)
			i = 1
			while i < len(list_input):
				item = evaluate(list_input[i])
				python_list.append(item)
				i += 1
			return python_list
			
	
		
		#finding defined functions:
		else: 
			speed = var_dict[opp]
			list_input[0] = speed
			return evaluate(list_input)
		
	#---if operator is list----
	if type(opp) is list:
	
		#handling lambdas
		if opp[0] == 'lambda':
			size_opp = len(opp[1])
			size_list_input = len(list_input)-1
			if size_opp != size_list_input:
				raise SyntaxError("number of variables must = number of assignments")
			i = 0
			while i < size_opp:
				what = list_input[i+1] #accessing variable assignments
				what_2 = opp[1][i] #accessing variables
				var_dict[what_2] = what
				i += 1
			return evaluate(opp[2])
		
		
		#handling definitions
		if opp[0] == 'define':
			def_name = opp[1]
			expression = opp[2]
			var_dict[def_name] = expression
			print var_dict, 'dictionnary'
			list_input = list_input[1:]
			return evaluate(list_input)

		
print evaluate(holder)
