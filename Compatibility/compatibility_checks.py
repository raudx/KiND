from Utilities import subordinate_functions as sbfnc
from Headers import populate_repositories as repos
from copy import deepcopy


def matchKeyword(sentence, key_index, probable_list, branch, index):
	keyword_index = sentence.process_order[key_index]
	# print "8", sentence.process_order, keyword_index

	zero_index = sbfnc.retZeroIndex(sentence, keyword_index)
	keyword_rule_list = sbfnc.getRuleList(sentence.keyword_list[keyword_index][0], sentence.keyword_list[keyword_index][2], keyword_index)

	rule_match_list = retMatchingRuleList(sentence, zero_index, key_index, keyword_rule_list, branch, probable_list, index)

	if (len(rule_match_list) == 0) :
		return False
	else :
		return True


def retMatchingRuleList(sentence, key_zero_index, key_index, keyword_rule_list, branch, probable_list, index) :
	keyword_rule_list_alias = keyword_rule_list[:]
	match_index_list = []

	# for i in range(len(keyword_rule_list)) :
	# 	print 26, keyword_rule_list[i].sentence

	for i in range(len(keyword_rule_list)) :
		rule_zero_index = sbfnc.retZeroIndexInRule(sentence.current[key_zero_index], keyword_rule_list[i].sentence)
		# print "line 24 ", rule_zero_index

		partial_match, rule_back_matching, backward_index = isRuleBackMatching(sentence.current, key_zero_index, keyword_rule_list[i], rule_zero_index, branch)

		if (rule_back_matching == False) :
			keyword_rule_list_alias.remove(keyword_rule_list[i])

		else :
			# print "back matched"

			if (partial_match == True) :
				index_in_alias_list = keyword_rule_list_alias.index(keyword_rule_list[i])

				keyword_rule_list_alias[index_in_alias_list].partial_match = True

			# checking forward match
			partial_match, rule_front_matching, forward_index = isRuleFrontMatching(sentence.current, key_zero_index, keyword_rule_list[i], rule_zero_index, branch)

			if (rule_front_matching == False) :
				keyword_rule_list_alias.remove(keyword_rule_list[i])

			else :
				if (partial_match == True) :
					index_in_alias_list = keyword_rule_list_alias.index(keyword_rule_list[i])

					keyword_rule_list_alias[index_in_alias_list].partial_match = True

				match_index_list.append([backward_index, forward_index])

	# for i in range(len(keyword_rule_list_alias)) :
	# 	print "50", keyword_rule_list_alias[i].sentence

	if (len(keyword_rule_list_alias) == 0) :
		return keyword_rule_list_alias

	else :

		keyword_index = sentence.process_order[key_index]
		# print "58", sentence.process_order, keyword_index

		for i in range(1, len(keyword_rule_list_alias)) :
			# print "branch created"
			sentence_alias = deepcopy(sentence)

			keyword_rule_list_alias[i].match_indices = match_index_list[i]
			sentence_alias.processed_index = sentence_alias.processed_index + 1
			sentence_alias.rules.append(keyword_rule_list_alias[i])
			sentence_alias.current = sentence_alias.current[:match_index_list[i][0]] + [sbfnc.getKeywordRetValue(sentence_alias.keyword_list[keyword_index][0], sentence_alias.keyword_list[keyword_index][2], (" ").join(keyword_rule_list_alias[i].sentence))] + sentence_alias.current[match_index_list[i][1] + 1:]

			probable_list.insert(index + 1, sentence_alias)

		# making changes to current sentence instance

		keyword_rule_list_alias[0].match_indices = match_index_list[0]
		sentence.rules.append(keyword_rule_list_alias[0])

		sentence.current = sentence.current[:match_index_list[0][0]] + [sbfnc.getKeywordRetValue(sentence.keyword_list[keyword_index][0], sentence.keyword_list[keyword_index][2], (" ").join(keyword_rule_list_alias[0].sentence))] + sentence.current[match_index_list[0][1] + 1:]

		# print "77, current", sentence.current
		return keyword_rule_list_alias


def isRuleFrontMatching(sentence_words, key_zero_index, rule, rule_zero_index, branch) :
	current_index = key_zero_index + 1

	for i in range(rule_zero_index + 1, len(rule.sentence)) :
		# print 94, rule.sentence[i], sentence_words[current_index]

		if (current_index < len(sentence_words)) :

			# something must follow rule
			if (i == len(rule.sentence) - 1 and rule.sentence[i] == "+>") :
				return False, True, current_index - 1 

			# nothing must follow rule
			elif (i == len(rule.sentence) - 1 and rule.sentence[i] == "+x") :
				return True, True, current_index - 1 

			else :
				rule.dict[rule.sentence[i]].append(current_index)
				matched, current_index = checkMatching(False, sentence_words, rule.sentence[i], current_index, branch)
				rule.dict[rule.sentence[i]].append(current_index)

				if (matched == False) :
					return False, False, 0

		else :
			# something must follow rule
			if (i == len(rule.sentence) - 1 and rule.sentence[i] == "+>") :
				return True, True, current_index - 1

			# not must follow rule
			elif (i == len(rule.sentence) - 1 and rule.sentence[i] == "+x") :
				return False, True, current_index - 1 

			else :
				return False, False, 0

	return False, True, current_index - 1


def isRuleBackMatching(sentence_words, key_zero_index, rule, rule_zero_index, branch) :
	# print 106, sentence_words, key_zero_index, rule, rule_zero_index
	current_index = key_zero_index - 1

	for i in range(rule_zero_index-1, -1, -1) :
		# print 94, rule.sentence[i], sentence_words[current_index]

		if (current_index > -1) :

			# something must precede rule
			if (i == 0 and rule.sentence[0] == "<+") :
				return False, True, current_index + 1

			# nothing must precede rule
			elif (i == 0 and rule.sentence[0] == "x+") :
				return True, True, current_index + 1

			else :
				rule.dict[rule.sentence[i]].append(current_index)
				matched, current_index = checkMatching(True, sentence_words, rule.sentence[i], current_index, branch)
				rule.dict[rule.sentence[i]].append(current_index)

				if (matched == False) :
					return False, False, 0

		else :
			# something must precede rule
			if (i == 0 and rule.sentence[0] == "<+") :
				return True, True, current_index + 1

			# nothing must precede rule
			elif (i == 0 and rule.sentence[0] == "x+") :
				return False, True, current_index + 1

			else :
				return False, False, 0

	return False, True, current_index + 1


def checkMatching(backward_dir, input_words, rule_word, current_index, branch) :
	modifier = 1
	if (backward_dir == True) :
		modifier = -1

	if (input_words[current_index] == rule_word) :
		current_index = current_index + modifier
		return True, current_index

	elif ( rule_word[:-1].isdigit() and rule_word[-1] == "n" and (sbfnc.isProbableVar(input_words[current_index]) or sbfnc.isNumber(input_words[current_index]) or sbfnc.isTypeVar("num", input_words[current_index], branch)) ):
		current_index = current_index + modifier
		return True, current_index

	elif rule_word[:-1].isdigit() and rule_word[-1] == "s" and (sbfnc.isProbableVar(input_words[current_index]) or (input_words[current_index][0] == '\"' and input_words[current_index][-1] == '\"') or sbfnc.isTypeVar("str", input_words[current_index], branch))  :
		current_index = current_index + modifier
		return True, current_index

	elif rule_word[:-1].isdigit() and rule_word[-1] == "v" and (sbfnc.isProbableVar(input_words[current_index]) or (input_words[current_index][0] == '\"' and input_words[current_index][-1] == '\"') or sbfnc.isNumber(input_words[current_index]) or sbfnc.isAnyVar(input_words[current_index], branch))  :
		current_index = current_index + modifier
		return True, current_index

	elif rule_word == "<var>" and (sbfnc.isAnyVar(input_words[current_index], branch) or sbfnc.isProbableVar(input_words[current_index])):
		# print "fdsfsdf"
		current_index = current_index + modifier
		return True, current_index

	elif rule_word[:-1].isdigit() and rule_word[-1] == "m" :
		match, current_index = valArrayMatcher(backward_dir, input_words, current_index, branch)

		return match, current_index

	elif ( rule_word[:-1].isdigit() and rule_word[-1] == "c" and ( input_words[current_index] == "true" or input_words[current_index] == "false") ):
		current_index = current_index + modifier
		return True, current_index

	else :
		return False, 0



def valArrayMatcher(backward_dir, input_words, current_index, branch) :
	if (backward_dir == True) :
		if (sbfnc.isProbableVar(input_words[current_index]) or sbfnc.isNumber(input_words[current_index]) or ((input_words[current_index][0] == '\"' and input_words[current_index][-1] == '\"') or sbfnc.isAnyVar(input_words[current_index], branch)) ) :
			current_index = current_index - 1

			# using 'and' as seperator
			if (input_words[current_index] == "and") :

				current_index = current_index - 1
				while (sbfnc.isProbableVar(input_words[current_index]) or sbfnc.isNumber(input_words[current_index]) or ((input_words[current_index][0] == '\"' and input_words[current_index][-1] == '\"') or sbfnc.isAnyVar(input_words[current_index], branch)) ) :
					current_index = current_index - 1

					if (current_index < 0) :
						return False, 0

				return True, current_index + 1

			else :
				return False, 0

		else :
			return False, 0

	
	else :
		# forward direction

		# print 188, input_words, current_index
		while(sbfnc.isProbableVar(input_words[current_index]) or sbfnc.isNumber(input_words[current_index]) or (input_words[current_index][0] == '\"' and input_words[current_index][-1] == '\"') or sbfnc.isAnyVar(input_words[current_index], branch) ):
			current_index = current_index + 1

			if (current_index > len(input_words) - 2) :
				return False, 0

			elif (input_words[current_index] == ",") :
				current_index = current_index + 1

		# using 'and' as seperator
		if (input_words[current_index] == "and") :
			current_index = current_index + 1

			if (sbfnc.isProbableVar(input_words[current_index]) or sbfnc.isNumber(input_words[current_index]) or (input_words[current_index][0] == '\"' and input_words[current_index][-1] == '\"') or sbfnc.isAnyVar(input_words[current_index], branch) ):
				return True, current_index + 1

			else :
				return False, 0

		else :
				return False, 0

