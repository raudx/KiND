Math = []
reserved_words_glossary = []
Io = []
Control = []
Object = []

class definition:
	def __init__(self, keyword):
		self.key = keyword
		self.rule_list = []


	def add_syntax(self, return_value, rule, syntax):
		flag = True
		if(len(self.rule_list) == 0):
			flag = False
			self.rule_list.append([return_value, rule,syntax])
		else:
			for i in range(len(self.rule_list)):
				if rule == self.rule_list[i][1]:
					flag = False
					if (syntax in self.rule_list[i]):
						pass
						#Syntax for existing rule added
					else:
						self.rule_list[i].append(syntax)
						#Syntax and the rule specified already exist
					break
		if ( flag == True ):
			self.rule_list.append([return_value, rule,syntax])


def populateRepository(name):
	syntax_table = []
	i = 0
	syn = " "
	fmain = open(name,"r")
	text = fmain.readline() 
	while(text is not ""):
		arr = text.split()
		if (arr[0] == "define"):
			keyword = arr[1]
			syntax_table.append(definition(keyword))
			text = fmain.readline()
			while(text is not ""):
				arr = text.split()
				# print "46", arr[2]
				if(arr[0] == "define"):
					break
				if (len(arr) > 2):
					if ( arr[2] == "output" ):
						return_value = arr[1]
						rule = " ".join(arr[3:])
						text = fmain.readline()
						arr = text.split()
				if (arr[-1] == "]"):
					syn = " ".join(arr[:-1])
				else:
					syn = " ".join(arr)
				syntax_table[i].add_syntax(return_value, rule,syn)
				text = fmain.readline()
		i += 1
	fmain.close()
	return syntax_table


Io = populateRepository("io_repository.txt")
Math = populateRepository("math_repository.txt")
Control = populateRepository("control_repository.txt")
# Object = populateRepository("object_repository.txt")


# for i in range(len(Math)):
# 	print Math[i].key
# 	print Math[i].rule_list
# for i in range(len(Io)):
# 	print Io[i].key
# 	print Io[i].rule_list



def obtainReservedWords(from_repository):
	global reserved_words_glossary
	for i in range(len(from_repository)):
		tmp_arr = from_repository[i].rule_list
		arr  = tmp_arr[0]
		for i in range(1, len(arr)):
			dummy_string = arr[i].split()
			for item in dummy_string:
				if item.isdigit():
					pass
				else :
					if item in reserved_words_glossary:
						pass
					else:
						reserved_words_glossary.append(item)
	# print reserved_words_glossary


obtainReservedWords(Math)
obtainReservedWords(Io)


