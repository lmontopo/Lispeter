#holder = "(/ (+ 3  ( * 2 3 )) (- -4 2))"
holder = '(define x 3)(* (+ 3 2) x)'

holder = holder.replace( '(' , ' ( ' )
holder = holder.replace( ')', ' ) ' )

holder = holder.split(' ')
holder = filter(lambda a: a != '', holder)
print holder

var_dict = { }

def is_number(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

switch = 1
while switch == 1: 

	for place in range(0,len(holder)): #Remember range doesn't include the upper bound!!!
		if  holder[place] == ')':
			
			#create an array containing the indices where '(' were found before ')'
			a = []	
			for position in range(0,place-1): 
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
				print part
			
			
				
			elif opp == 'define':
				temp_var = holder[biggest+2]
				temp_val = holder[biggest+3]
				var_dict[temp_var] = temp_val
				part = None
			
			#making the new array with one part calculated
			
			how_far = place - biggest
			how_far = int(how_far)
				
			part = str(part) # so that it can go back into the array with other string types
			temp = holder[:biggest] 
			if opp != 'define':
				temp.append(part)
			temp = temp + holder[biggest + how_far +1:]
			print temp
			
			
			holder = temp
			break
			
	if not '(' in holder: 
		switch = 0 
		print "done"
			 
			
			

	
	


						
		
		

