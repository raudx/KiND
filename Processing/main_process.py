from Headers import populate_repositories as repos                                                                  
from Compatibility import compatibility_checks as cmpts
from copy import deepcopy
from Data_Stores import data_store_defs as d_str
from Utilities import subordinate_functions as sbfnc
from Processing import post_process as pstp

def processBranch(branches, root_branch):

	# branches will be formed when for a single sentence there are multiple interpretations.
	# Each branch will be contain the remaining part of the entire program, after the branching occured, 
	# and will be processed independently.
	branch_index = 0
	while (branch_index < len(branches)):

		if (root_branch == True) :
			print "Branch Output : #" + str(branch_index + 1)

		for i in range(len(branches[branch_index].sentences)) :

			if (len(branches[branch_index].sentences[i].rules) == 0) :
				prioritizeSentence(branches[branch_index].sentences[i], branches, branch_index, i)

			# print 22, branches[branch_index].sentences[i].rules, branches[branch_index].sentences[i].current

			# revitalising sentence.current
			branches[branch_index].sentences[i].current = branches[branch_index].sentences[i].words

			# print 27, branches[branch_index].sentences[i].current, branches[branch_index].sentences[i].rules

			# print 28,"haaa", branches
			processEachRule(branches[branch_index].sentences[i], branches[branch_index], branches)
			# print 30, branches[branch_index].symbols[1].value

		if (branches[branch_index].result == None) :
			branches[branch_index].result = "null"

		branch_index = branch_index + 1

		# return "null"


def prioritizeSentence(sentence, branches, branch_index, sentence_index):

	index = 0
	probable_list = makeProbableList(sentence)
	largest = 0
	consumed_list = []

	while (index < len(probable_list)) :

		key_index = probable_list[index].processed_index + 1

		while(key_index < len(sentence.keyword_list)) :
			# print "line 30", probable_list[index].current , key_index

			keyword_matched = cmpts.matchKeyword(probable_list[index], key_index, probable_list, branches[branch_index], index)

			if (keyword_matched == True) :
				keyword_index = probable_list[index].process_order[key_index]
				probable_list[index].keyword_list[keyword_index][1] = True

			# print "55", probable_list[index].rules

			# print "line 34", key_index, keyword_matched

			key_index = key_index + 1
			probable_list[index].processed_index = key_index

		# print "changing branch"

		if (sbfnc.isSentenceConsumed(probable_list[index].current)) :
			list_score = 0

			for j in range(len(probable_list[index].process_order)) :
				list_score = list_score + (probable_list[index].process_order[j] * j )

			if (list_score >= largest) :
				largest = list_score

				# print 81, probable_list[index].words, probable_list[index].current

				consumed_list.append(probable_list[index])
				break

		index = index + 1

	# creating branches -----
	if (len(consumed_list) > 0) :

		current_branch_appended = False 

		for i in range(len(consumed_list)) :
				
			if (current_branch_appended == True) :
				branch_alias = deepcopy(branches[branch_index])
				branch_alias.sentences[sentence_index] = consumed_list[i]
				branches.append(branch_alias)

			else :
				branches[branch_index].sentences[sentence_index] = consumed_list[i]
				current_branch_appended = True
				
		# ----

	else :
		# for i in range(len(probable_list)) :
		# 	print 111, probable_list[i].words, probable_list[i].current

		print "---CANNOT COMPREHEND---"


def getPermuteList(num) :
	p_list = []
	for i in range(num) :
		p_list.append(i)

	import itertools
	return list(itertools.permutations(p_list))


def makeProbableList(sentence) :
	run_order = getPermuteList(len(sentence.keyword_list))

	probable_list = []

	for i in range(len(run_order)) :
		sentence_clone = deepcopy(sentence)
		sentence_clone.process_order = list(run_order[i])

		probable_list.append(sentence_clone)

	return probable_list


def retOptimumProbableList(probable_list) :
	# print 131, probable_list

	true_list = []

	largest = 0
	# calculating score -----
	for i in range(len(probable_list)) :
		list_score = 0

		for j in range(len(probable_list[i].process_order)) :
			list_score = list_score + ( probable_list[i].process_order[j] * j )

		if (list_score >= largest) :
			largest = list_score
			true_list.append(probable_list[i])

		else :
			break

	# -----

	return true_list


# def executeSentence(sentence) :
# 	for i in range(len(sentence.rules)) :
# 		keyword = sentence.keyword_list[sentence.rules[i][0]][0]
# 		repository = sentence.keyword_list[sentence.rules[i][0]][2]
# 		rule = sentence.rules[i][1]

# 		given_raw_sentence = sentence.words[sentence.rules[2][0]:sentence.rules[2][1] + 1]

# 		# getValuesFromInput(given_raw_sentence)

# 		output_stat = sbfnc.getKeywordOutput(keyword, repository, rule).split()

# 		subsituteValsInOutput(output_stat)

# 		raw_sentences = sbfnc.extractKeywordsFromScratched(output_stat)

# 		sentences = []

# 		for j in range(len(raw_sentences)) :
# 			sentences.append(d_str.Sentence(raw_sentences[0], raw_sentences[1]))

# 		program_branch = d_str.ProgramBranch(sentences)


def processEachRule(sentence, proc_branch, branches):
    # print "146", sentence.rules

    # check if partial_match
    sbfnc.checkPartialMatch(sentence.rules)

    sen_list = [sentence]
    proc_bg_list = [proc_branch]

    while(len(sen_list[0].rules) > 0) :
    	# print 151, sen_list[0].rules
    	matched_rule = sen_list[0].rules[0]

    	output_rule = sbfnc.getKeywordOutput(matched_rule.keyword, matched_rule.repo, (" ").join(matched_rule.sentence))
        # print "135 m_pro", output_rule
        output_rule = output_rule.split()
        dictionary = matched_rule.dict

        count = 0
        for sen_obj in sen_list :
        	# print 161, sen_obj == sen_list[0]

        	if ("if" in output_rule):
	            result = pstp.processConditional(sentence, proc_bg_list[count], dictionary)
            
	        else:
	            if (output_rule[0] == "$" and (output_rule[-1] == "@" or output_rule[-1] == "@.")) :

	                words = pstp.substituteValues(output_rule, dictionary, sen_obj)
	                # print 170, words

	                # print 152, dictionary

	                result = pstp.process(words, proc_bg_list[count])

	                match_begin_index = matched_rule.match_indices[0]
	                match_end_index = matched_rule.match_indices[1]

	                sen_obj.current = sen_obj.current[:match_begin_index] + [result] + sen_obj.current[match_end_index + 1:]

	                sen_obj.rules = sen_obj.rules[1:]

	                # print 182, sen_obj.current, sen_obj.rules

	            else :

	                output_rule = pstp.substituteValues(output_rule, dictionary, sentence)
	                sbfnc.separateCommas(output_rule)

	                sentence_list = sbfnc.extractKeywordsFromScratched((" ").join(output_rule))

	                true_sentences = sbfnc.populateSentenceObjs(sentence_list)

	                new_program_branch = d_str.ProgramBranch(true_sentences, proc_bg_list[count].symbols)

	                program_branches = [new_program_branch]

	                processBranch(program_branches, False)

	                match_begin_index = matched_rule.match_indices[0]
	                match_end_index = matched_rule.match_indices[1]

	                for i in range(1,len(program_branches)) :
	                	sen_clone = deepcopy(sen_obj)

	                	sen_clone.current = sen_clone.current[:match_begin_index] + [program_branches[i].result] + sen_clone.current[match_end_index + 1:]

	                	sen_clone.rules = sen_clone.rules[1:]

	                	sen_list.append(sen_clone)
	                	proc_bg_list.append(program_branches[i])

	                sen_obj.current = sen_obj.current[:match_begin_index] + [program_branches[0].result] + sen_obj.current[match_end_index + 1:]
	                sen_obj.rules = sen_obj.rules[1:]

	        # count = count + 1

		# print 215, sen_list[0].rules, len(sen_list[0].rules) > 0

	for i in range(1, len(proc_bg_list)) :
		branches.append(proc_bg_list[i])