#holder = "((lambda (a b) (+ a b)) 5 6)"
#holder = '(define (func x)(+ x 2))(func 2)'
#holder = '((( + 2 3 )))'
#holder = '(define (func x)(+ x 2))'
#holder = '((lambda (a) a) "blahblahblahblahblah")'
#holder = '((define add3 (lambda (x) (+ x 3))) (add3 3))'
#holder = '(+ 1 (abs -1))'
#holder = '(list 1 (+ 1 1) 3 4)'
#holder = '(not (< 10 (- 20 10)))'
#holder = "(if (not(< 10 20)) yes (+ 3 3))"
#holder = '(if (< 10 20) ((lambda (a b) (+ a b)) 5 6) (+ 3 3))'
#holder = "(cond ((> 0 0) 1)(else 'bloobloobloo))"
#holder = '(quote hlallallaa)'
holder = '(define x 3)(set! x (+ x 1))x'
#holder = '(define (fib n)(cond ((= n 1) 0)((= n 2) 1)(else (+ (fib (- n 1)) (fib (- n 2))))))(fib 3'


# ---- TOKENIZE ------ 
holder = '(' + holder + ')'							#adding extra outer brackets
holder = holder.replace( '(' , ' [ ' )
holder = holder.replace( ')', ' ] ' )
holder = holder.split(' ')
holder = filter(lambda a: a != '', holder)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

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
print holder, 'parsed holder'



# --- DICTIONARY OF VARIABLES --- 
main_dict = { }
	


# ----- INTERPRETER ------- 
def evaluate(list_input):
	
	print list_input, 'list_input'
	
	if list_input == []:
		return None
	
	#base case
	if not type(list_input) is list:
		if is_number(list_input) == True:			#number
			return list_input
		
		elif is_number(list_input) == False:
			if list_input[0] == "'":   				#quote
				return list_input[1:]
			elif list_input == 'else': 				#so that 'else' isn't evaluated
				return False
				
			else:
				try:
					return main_dict[list_input]			#checks dict
				except KeyError: 
					return "inputed element is not number, not quote, and not in dict"
			
				
	#evaluation
	opp = list_input[0]

	
	
	#----if operator is not contained in another list---
	if not type(opp) is list:
	
		#check if we've gotten final answer:
		if is_number(opp) == True:
			return opp
			
		
		#basic math and boolean operations
		if opp in ['+', '-', '*', '/', '<', '>', '<=', '=','>=']:
			if opp == '=':
				result = eval(str(evaluate(list_input[1])) + '==' + str(evaluate(list_input[2])))
			else:
				result = eval(str(evaluate(list_input[1])) + opp + str(evaluate(list_input[2])))
			return result
		
		if opp == 'not':
			result = eval(opp + ' ' + str(evaluate(list_input[1])))  #without the added space python sees 'notTrue' instead of 'not True'
			return result
		
		
		
		#conditional statements	
		if opp == 'if':
			condition = list_input[1] 
			consequence = list_input[2]
			alt = list_input[3]
			if evaluate(condition) == True:
				return eval(str(evaluate(consequence)))
			elif evaluate(condition) == False:
				return eval(str(evaluate(alt)))
		
		if opp == 'cond':
			for i in range(1, len(list_input)):
				if evaluate(list_input[i][0]) == True:
					return evaluate(list_input[i][1])
				elif list_input[i][0] == 'else':
					return evaluate(list_input[i][1])
		
		if opp == 'else': 
			return evaluate(list_input[1])
					
				
						
		#absolute value
		if opp == 'abs':
			if len(list_input) == 2:
				return abs(evaluate(list_input[1]))
			else:
				raise SyntaxError('abs takes only one operand!')
		
		
		#quote
		if opp == 'quote':
			if len(list_input) == 2:
				return list_input[1]
			else:
				raise SyntaxError('quote only takes one operand')
		
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
			
	
	
	
		#finding defined functions in dictionary:
		else: 
			name = main_dict[opp]
			list_input[0] = name
			return evaluate(list_input)
		
	#--- if operator is within another list----
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
				main_dict[what_2] = what
				i += 1
			return evaluate(opp[2])
		
		
		#handling definitions
		if opp[0] == 'define':
			if type(opp[1]) is list:
				
				if len(opp[1]) == 1:
					def_name = opp[1][0]
					expression = opp[2]
					main_dict[def_name] = expression
					list_input = list_input[1:]
					return evaluate(list_input)
				
				
				if len(opp[1]) > 1:
					def_name = opp[1][0]
					expression = opp[2]
					dict = ['lambda']
					dict_var = []
					for i in range(1,len(opp[1])):
						dict_var.append(opp[1][i])
					dict.append(dict_var)
					dict.append([expression])
					main_dict[def_name] = dict
					list_input = list_input[1:] #gets rid of entire define expression
					return evaluate(list_input)
			
			elif not type(opp[1]) is list:
				def_name = opp[1]
				expression = opp[2]
				main_dict[def_name] = expression
				list_input = list_input[1:]
				return evaluate(list_input)
				
		if opp[0] == 'set!':
			print opp[0],'opp[0]'
			#check already been defined:
			if opp[1] in main_dict.keys():
				expression = evaluate(opp[2])
				main_dict[opp[1]] = expression
				list_input = list_input[1:]
				return evaluate(list_input)
			else:
				print "this should result in an error."
			
			
			
			
			
			
		#removes any redundant outermost brackets 
		if type(opp) is list and len(list_input) == 1:
			return evaluate(list_input[0])
		

	
	
		
print evaluate(holder)
