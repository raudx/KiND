# defining symbol class
class Symbol:
	def __init__(self, name, value, scope_level, var_type, root_type):
		self.name = name
		self.value = value
		self.scope_level = scope_level
		self.var_type = var_type
		self.root_type = root_type


# defining ProgramBranch class
class ProgramBranch :
	def __init__(self, sentences, sym_table) :
		self.number = 0
		self.sentences = sentences
		self.current_level = 0
		self.result = None
		self.symbols = sym_table


# defining Sentence class 
class Sentence :
	def __init__(self, words, keyword_list) :
		self.words = words
		self.keyword_list = keyword_list
		self.rules = []
		self.current = words
		self.processed_index = -1
		self.process_order = None


# defining Rule class
class Rule :
	def __init__(self, keyword, rule, repository, keyword_index) :
		self.keyword = keyword
		self.sentence = rule
		self.repo = repository
		self.keyword_index = keyword_index
		self.match_indices = []
		self.partial_match = False

		self.dict = {}

		for i in range(len(rule)) :
			self.dict[rule[i]] = []



class stack:
	def __init__(self):
		self.list = []

	def push(self, string):
		self.list.append(string)

	def pop(self):
		self.list = self.list[:len(self.list)-1]

	def multiPop(self, num):
		for i in range(num):
			self.list.pop()


def push(item,stack):
	stack.append(item)


def pop(stack):
	if len(stack) == 0:
		return None
	item = stack[len(stack)-1]
	del stack[len(stack)-1]
	return item


		