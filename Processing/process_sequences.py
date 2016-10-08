from Data_Stores import data_store_defs as d_str


#RETURNS THE NUMBER BY APPENDING TO IT ALL CONSECUTIVE DIGITS
def formNumberV2(inp, index):
	tmp_arr = ["0","1","2","3","4","5","6","7","8","9"] 
	tmp_str = inp[index]
	if index == len(inp) -1:
		index = index + 1
	else:
		index += 1
		while( inp[index] in tmp_arr):
			tmp_str = tmp_str + inp[index]
			index += 1
	return int(tmp_str), index-1 #index-1 IS THE INDEX OF LAST DIGIT OF THE NUMBER FORMED


# EVALUATES THE EXPRESSION ALREADY IN POST-FIX NOTATION
def evaluate(postfix_expression):
	stack = []
	postfix_expression.append(")")
	i = 0
	while(postfix_expression[i] != ")"):
		if type(postfix_expression[i]) is int :
			d_str.push(postfix_expression[i],stack)
		else :
			op1 = d_str.pop(stack)
			op2 = d_str.pop(stack)
			operator = postfix_expression[i]
			if op1 is None or op2 is None:
				return None
			if "+" == operator :
				d_str.push(op1 + op2, stack)
			elif "-" == operator :
				d_str.push(op2 - op1, stack)
			elif "*" == operator :
				d_str.push(op1 * op2, stack)
			else :
				d_str.push(op2 / op1, stack)
		i += 1

	return d_str.pop(stack)
	# print d_str.pop(stack)


# CONVERT THE INPUT FROM IN-FIX TO POST-FIX NOTATION TO GET RID OF THE BRACKETS

def postfix(inp):
	# todo add functionality for decimal numbers.
	# print "inp",inp
	postfix_form = []
	stack = []
	op_array = ["/","*","+","-"]
	d_str.push("(",stack)
	inp = inp + ")"
	i = 0
	while(len(stack) != 0):
		char = inp[i]
		if (char == "("):
			d_str.push(char,stack)
		elif (char in op_array):
			j = len(stack) - 1
			while ( True ):
				if stack[j] == "(":
					d_str.push(char, stack)
					break
				elif op_array.index(stack[j]) <= op_array.index(char):
					# REMOVING OPERATORS OF HIGHER OR EQUAL PRIORITY AND PUTTING THEM IN POST ARRAY
					postfix_form.append(d_str.pop(stack))
					j -= 1
					if (stack[j] == "("):
						d_str.push(char, stack)
						break
				else :
					d_str.push(char, stack)
					break
		elif (char == ")"):
			# d_str.POP STACK TO POST UNTILL ) IS FOUND
			item = d_str.pop(stack)
			while (item != "("):
				postfix_form.append(item)
				item = d_str.pop(stack)
		elif (char == " "):
			pass
		elif (type(int(char)) is int) :
			val,i = formNumberV2(inp,i)
			postfix_form.append(val)                        
		else:
			# print "Unidentified statement"
			return str(None)
		i += 1
	output = evaluate(postfix_form)
	# print "postfix", output
	return str(output)

# postfix("( 1 /2*332*4+555-(625+72))")


