holder = "(/ (+ 3  ( * 2 3 )) (- 4 2))"

holder = holder.replace( '(' , ' ( ' )
holder = holder.replace( ')', ' ) ' )

holder = holder.split(' ')
holder = filter(lambda a: a != '', holder)
print holder


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
			num1 = holder[biggest+2]
			num2= holder[biggest+3]
			part = eval(num1 + opp + num2)
			part = float(part)
			print part
			
			part = str(part)
		
	
			temp = holder[:biggest] 
			temp.append(part)
			temp = temp + holder[biggest+5:]
			print temp
			
			holder = temp
			break
			
	if not '(' in holder: 
		switch = 0 
		print "done"
			 
			
			

	
	


						
		
		

