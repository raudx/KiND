from Data_Stores import data_store_definitions as d_str
from Processing import fixing_sequences as fixs
from Post_Processing import io 

output = []

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

def substituteValuesInOutputRule(output_rule, num_table):
	pound = "#"
	new_rule = ""
	index = 0
	while(True):
		if output_rule[index] == pound:
			index = index + 1
			begin_index = index
			num, end_index = formNumberV2(output_rule,begin_index)
			index = end_index
			new_rule = new_rule + num_table[num-1]
		else:
			new_rule = new_rule + output_rule[index]	
		index += 1
		if index > (len(output_rule)-1):
			break	
	answer = postfix(new_rule)
	return answer

# substituteValuesInOutputRule(output_rule, num_table)

# CONVERT MATH OPS TO NUMBERS IN SENTENCE 
def calcDollarExpressions(sentence_list) :
	sentence = ""
	for word in sentence_list :
		sentence = sentence + word + " "
	sentence = sentence[:-1]
	index = 0
	new_sentence = ""
	while (index < len(sentence)) :
		if sentence[index] == "$" :
			dollar_seq = ""
			index_2 = index + 1
			while not (sentence[index_2] == "@") :
				dollar_seq = dollar_seq + sentence[index_2]
				index_2 = index_2 + 1
			num = postfix(dollar_seq)
			index = index_2 + 1
			new_sentence = new_sentence + str(num)

		else :
			new_sentence = new_sentence + sentence[index]
			index = index + 1

	return new_sentence.split()


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
			return None
		i += 1
	output = evaluate(postfix_form)
	return output

# postfix("( 1 /2*332*4+555-(625+72))")


def substituteHashValues(output_rule, num_table):
	pound = "#"
	at_sign = "&"
	new_rule = ""
	index = 0
	while(True):
		if output_rule[index] == pound:
			index = index + 1
			begin_index = index
			num, end_index = formNumberV2(output_rule,begin_index)
			# print "shdsgdsgdhsdghsd : ", num, end_index
			index = end_index
			new_rule = new_rule + num_table[0][num-1]
		elif output_rule[index] == at_sign:
			index = index + 1
			begin_index = index
			num, end_index = formNumberV2(output_rule,begin_index)
			# print "shdsgdsgdhsdghsd : ", num, end_index
			index = end_index
			new_rule = new_rule + num_table[1][num-1]
		else:
			new_rule = new_rule + output_rule[index]	
		index += 1
		if index > (len(output_rule)-1):
			break	
	return new_rule


def numTableCreator(sentence) :
	num_table = [[], []]
	for word in sentence.split() :
		# print "W ", word, word[-1] == "n"
		if word.isdigit() :
			num_table[0].append(word)
		elif word[-1] == "\"" and word[0] == "\"":
			num_table[1].append(word)
	# print "Table : ", num_table
	return num_table


# # Makes piped Strings as a single entity from a print string entry
# def makeStringSentence(in_str):
# 	quote_indices = []
# 	sentence_list = []
# 	for index in range(len(in_str)):
# 		if in_str[index] == "\"":
# 			quote_indices.append(index)
# 	# print "tytytyty : ",quote_indices
# 	sentence_list.append(in_str[:quote_indices[0]])
# 	string = in_str[quote_indices[0]:quote_indices[1]+1].split()
# 	# print "hththt : ", string
# 	string = "|".join(string)
# 	sentence_list.append(string)
# 	sentence_list.append(in_str[quote_indices[1] + 1:])
# 	return sentence_list


def makeStringSentence(in_str) :
	in_quote = False

	for i in range(len(in_str)) :
		if in_str[i] == "\"" :
			in_quote = not in_quote
		if in_quote == True :
			if in_str[i] == " ":
				in_str = in_str[:i] + "|" + in_str[i+1:]

	return in_str

# Convert the stream of Input Sequence into sentences seperated by
# (.)'s
def makeSentences(in_str) :
	in_str = makeStringSentence(in_str)
	in_str = in_str.split()
	
	# in_str = in_str.lower().split()
	sentences = [[]]
	for word in in_str :
		if (word[len(word)-1] == ".") :
			sentences[len(sentences)-1].append(word[:len(word)-1])
			sentences.append([])
		else :
			sentences[len(sentences)-1].append(word)

	sentences = sentences[:len(sentences)-1]

	sentence_list = []

	for sentence in sentences :
		sentence_class = d_str.sentenceClass(sentence)
		sentence_list.append(sentence_class)

	return sentence_list


# SEQUENCES TO PROCESS MATH OPS
def processMathWithSentence(sentence):
	dollar_indices = []
	for index in range(len(sentence)) :
		if sentence[index] == "$" :
			dollar_indices.append(index)
	# print dollar_indices
	# print len(dollar_indices)
	for index in range(len(dollar_indices)-1) :
		dollar_1 = dollar_indices[index]
		dollar_2 = dollar_indices[index+1]
		subs = "".join(sentence[dollar_1+1:dollar_2])
		# print "index : ", index
		# print "dollar_1 : ", dollar_1
		# print "dollar_2 : ", dollar_2
		# print "trial  : ",subs
		# print
		answer = postfix(subs)
		# print "received  :",subs
		# print "answer : ",answer
		if answer is not None:
			sentence = sentence[:dollar_1]+str(answer)+sentence[dollar_2+1:]
			# print "sentence after mofification : ", sentence
			return sentence
		# print "String : ",sentence
		# print
	return sentence


# SEQUENCES TO EXECUTE IO OPS 
def processIOWithSentence(sentence, symbol_table, scope, para_object):
	global output
	sentence = sentence[1:len(sentence)-1]
	# print "received sentence : ",sentence
	# print "Control is Here"
	# io_keywords = ["print", "in", "as"] 
	if "print" in sentence :
		# print sentence.split()[1]
		if sentence.split()[1].isdigit() :
			output.append(sentence.split()[1])
			print sentence.split()[1]
		else:
			output.append((" ").join(sentence.split()[1][1:-1].split("|")))
			print (" ").join(sentence.split()[1][1:-1].split("|"))
	elif "in" in sentence:
		sentence_splice = sentence.split()
		number = sentence_splice[0]
		symbol = sentence_splice[2]
		io.storeInVariable(int(number), symbol, scope)
	elif "as" in sentence:
		sentence_splice = sentence.split()
		number = sentence_splice[0]
		symbol = sentence_splice[2]
		io.storeAsConstant(int(number), symbol)	
	else:
		sentence_splice = sentence.split()
		exp = " ".join(sentence_splice[1:])
		io.returnValue(exp, para_object)	
	sentence = ""
	return sentence


#
def IOCheck(sentence):
	io_keywords = ["print", "in", "as"]
	dollar_count = 0
	for char in sentence:
		if char == "$":
			dollar_count += 1
	for word in io_keywords:
		if word in sentence:
			flag = True
			break
		else:
			flag = False
	return dollar_count, flag


# EXECUTE LEGAL DOLLAR RULES WITHIN SENTENCE
def processDollarSentence(string_to_process, symbol_table, scope, para_object):
	while(not(string_to_process is "" or string_to_process.isdigit() == True)):
		dollar_count, flag = IOCheck(string_to_process)

		if dollar_count == 2 and flag == True:
			string_to_process = processIOWithSentence(string_to_process, symbol_table, scope, para_object)
		else:
			string_to_process = processMathWithSentence(string_to_process)
	# print "121212121 : ", string_to_process
	return string_to_process

# processDollarSentence("$$6+$4$$ in var$")
# print "Only MATH"
# print "testttttt : ",processDollarSentence("$qwertyui$",None,None,None)


# REPLACE DOLLAR RULES WITH THEIR PROCESSED OUTPUTS WITHIN SENTENCE 
def sentenceFixer(sentence, symbol_table, scope, para_object):
	not_done = True

	while not_done == True :
		for i in range(len(sentence)+1) :
			if i == len(sentence) :
				not_done = False
				return sentence
			elif sentence[i] == "$":
				start = i
			elif sentence[i] == "@" :
				end = i
				break
		if not_done == True and not len(sentence[start+1:end]) == 0 :
			# print processDollarSentence("$" + sentence[start+1:end] + "$")
			sentence = sentence[:start] + processDollarSentence("$" + sentence[start+1:end] + "$", symbol_table, scope, para_object) + sentence[end+1:]
		elif len(sentence[start+1:end]) == 0:
			sentence = sentence[:start] + sentence[end+1:]
		# sentence = fixSpacesInSentence(sentence) 
	return sentence
# processDollarSentence("$$6+$4$$ in var$")
# print "Only MATH"
# processDollarSentence("$2+8#")
# sentenceFixer("$#$2+$5*8##")