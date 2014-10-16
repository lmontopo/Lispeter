holder = "(/ (+ 3  ( * 2 3 )) (- -4 2))"
#holder = '(define x 3)(* (+ 3 2) x)'

holder = holder.replace( '(' , ' [ ' )
holder = holder.replace( ')', ' ] ' )

holder = holder.split(' ')
holder = filter(lambda a: a != '', holder)
print holder, 'before parsing'
#def parse(list):
#	if not list: 
#		return
#		raise ValueError('function being wierd')
#	new_holder = []
#	love = 0 
#	for i in range(0,len(list)):
#		if holder[i] == '[':
#			love +=1
#		elif holder[i] == ']':
#			love -=1
#		if love ==  0 :
#			new_holder.append(list[i])
#		elif love > 0:
#			while love > 0:
#				parse(new_holder)
#	return new_holder		
		
#print parse(holder)



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
		holder = holder[1:]			 #pops off the ')' part
		
		#we add a condition to check if last return
		if len(holder) > 0:
			return new_holder , holder #if not last return, need to return current version of holder
		elif len(holder) == 0 :
			return new_holder			#if last return, only want to return new_holder
	else:
		return token, holder 			#this is never last return, so we always need both

		
print parse(holder)


	

# a dictionary where we will add any variable declarations
var_dict = { }

#checks if our operands are numbers
def is_number(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

#switch is 1 by default, but changes to 0 when there are no brackets left.
#then switch =0 ends the while loop
switch = 1
while switch == 1: 

	for place in range(0,len(holder)): #range doesn't include the upper bound!
		if  holder[place] == ')':
			
			#create an array of the indices where '(' are found before the current ')'
			a = []	
			for position in range(0,place): 
				if holder[position] == '(':
					a.append(position)
				else: 
					pass
			#finding the maximum element in list a
			biggest = max(a)
			
			
			opp = holder[biggest+1]
			
			
			
			if opp in ['+', '-', '/', '*']:
				
				if is_number(holder[biggest+2]) == True:
					num1 = holder[biggest+2]
				elif holder[biggest+2] in var_dict.keys():
					num1 = var_dict[holder[biggest+2]]
				else:
					break
					print "you have not defined holder[biggest+2]"
				if is_number(holder[biggest+3]) == True:
					num2 = holder[biggest+3]
				elif holder[biggest+3] in var_dict.keys():
					num2 = var_dict[holder[biggest+3]]
				else:
					break
					print "you have not defined holder[biggest+3]"
				
				part = eval(num1 + opp + num2)
				part = float(part) #So that i can divide and get 4.5 instead of 4
				print part
			
			
			
			elif opp == 'abs':
				
				if is_number(holder[biggest+2]) == True:
					num1 = holder[biggest+2]
				elif holder[biggest+2] in var_dict.keys():
					num1 = var_dict[holder[biggest+2]]
				else:
					break
					print "you have not defined holder[biggest+2]"
				
				num1 = float(num1) #since abs only works on numbers
				part = abs(num1)
				print part #our evaluation of what is in this part
			
			
				
			elif opp == 'define':
				temp_var = holder[biggest+2]
				temp_val = holder[biggest+3]
				var_dict[temp_var] = temp_val
				part = None
			
			#making the new array without the part we just analyzed
			how_far = place - biggest
			how_far = int(how_far)
				
			part = str(part) # so that it can go back into the array with other string types
			temp = holder[:biggest] 
			if opp != 'define':
				temp.append(part)
			temp = temp + holder[biggest + how_far +1:]
			holder = temp
			break
			
	if not '(' in holder: 
		switch = 0 
		print "done"
			 
			
			

	
	


						
		
		

