from Headers import populate_repositories as repos
from Data_Stores import data_store_defs as d_str
import re

def retZeroIndex(sentence, key_index):
	# print sentence.current, "subfncs line 4"\

	keyword = sentence.keyword_list[key_index][0]
	skip_count = 0

	for i in range(key_index) :
		if (sentence.keyword_list[i][0] == keyword and sentence.keyword_list[i][1] == False) :
			skip_count = skip_count + 1

	for i in range(len(sentence.current)):
		if (sentence.current[i] == keyword):
			skip_count = skip_count - 1

			if (skip_count < 0) :
				return i

	return -1

def toNum(string):
		# print string
	try :
		return float(string)
		# return True
	except ValueError :
		return False


def retZeroIndexInRule(keyword, rule) :
	for i in range(len(rule)) : 
		if (rule[i] == keyword) :
			# print i,"line 15"
			return i


def isAnyVar(name, branch) :
	for symbol in branch.symbols :
		if (symbol.name == name and symbol.scope_level <= branch.current_level) :
			return True

	return False


def isTypeVar(var_type, name, branch) :
	for symbol in branch.symbols :
		# print 41, name, symbol.scope_level, branch.current_level
		if (symbol.name == name and symbol.scope_level <= branch.current_level) :
			return True

	return False


def isNumber(string) :
	# print string
	try :
		float(string)
		return True
	except ValueError :
		return False


def getRuleList(keyword, repository, keyword_index):
	# print "58, sbfnc", keyword, repository, keyword_index

	key_index = -1
	reference_repository = None
	# print keyword

	if (repository == "math"):	
		reference_repository = repos.Math
	elif (repository == "io"):
		reference_repository = repos.Io
	elif (repository == "control"):
		reference_repository = repos.Control

	# print 71, keyword

	for i in range(len(reference_repository)):
		if(reference_repository[i].key == keyword):
			# print 73, keyword

			key_index = i
			break

	keyword_rule_list = []
	# print 79, reference_repository[key_index].rule_list

	for rule_item in reference_repository[key_index].rule_list :

		for i in range(2, len(rule_item)):
			keyword_rule_list.append(d_str.Rule(keyword, rule_item[i].split(), repository, keyword_index))

	# print keyword_rule_list
	return keyword_rule_list


def getKeywordRetValue(keyword, repository, rule) :
	# print "86, sbfnc", keyword, repository, rule
	reference_repository = None

	if (repository == "math"):
		reference_repository = repos.Math
	elif (repository == "io"):
		reference_repository = repos.Io
	elif (repository == "control"):
		reference_repository = repos.Io

	for i in range(len(reference_repository)) :
		if (reference_repository[i].key == keyword) :
			for item in reference_repository[i].rule_list:
				if (rule in item) :
					if (item[0] == "null") :
						return item[0]
					elif (item[0] == "integer") :
						return "0"
					elif (item[0] == "bool") :
						return "true"


def getKeywordOutput(keyword, repository, rule) :
	# print keyword, repository, rule

	reference_repository = None

	if (repository == "math"):	
		reference_repository = repos.Math
	elif (repository == "io"):
		reference_repository = repos.Io
	elif (repository == "control"):
		reference_repository = repos.Control

	for i in range(len(reference_repository)) :
		if (reference_repository[i].key == keyword) :
			for item in reference_repository[i].rule_list:
				if (rule in item) :
					return item[1]
			print "Not Found" #Error


def isSentenceConsumed(words) :
	if (len(words) == 1) :
		# len == 1 ie. only "null"
		if (words[0] == "null") :
			return True
		else :
			return False

	else :
		# Cases : null and null / null, null, null...null and null

		index = 0

		while (words[index] == "null" and words[index + 1] == ",") :
			index = index + 2

		if (words[index] == "null" and words[index + 1] == "and" and words[index + 2] == "null") :
			return True
		else :
			return False


def sentenceSeparator(str):
    # here we are excluding the decimals and separating an string based on full stops.
    # append a space in the end to the string recieved
    # str="Add 2 to 5.0. Ad 4 to 9. "
    str = str + ' '

    location=[i for i, letter in enumerate(str) if letter == "."]
    full_stop= []
    for i in location:
        if (47 < ord(str[i-1]) < 58 and 47<ord(str[i+1])<58):
            pass
        else:
            full_stop.append(i)

    # here we are having a index of full stops in full_stop array, and based on that we are separating.
    sentence = []
    # the if here is to append the substring from zeroth index to first full stop.
    if ((str[0:full_stop[0]])):
        sentence.append(str[0:full_stop[0]])

    for i in xrange(len(full_stop)-1):
        sentence.append(str[full_stop[i]+1:full_stop[i+1]].strip())
        
    return sentence


def extractKeywordsFromScratched(scratch):
    # uses sentenceSeparator()
    # uses RetkeywordsAndNot_KeywordFromRepository
    # when u include more repositories please include an corresponding block in "for i in iSplitted"

	io_keys, io_notkeys = RetKeywordsAndNot_KeywordFromRepository('io_repository.txt')
	math_keys, math_notkeys = RetKeywordsAndNot_KeywordFromRepository('math_repository.txt')
	control_keys, control_notkeys = RetKeywordsAndNot_KeywordFromRepository('control_repository.txt')

	sentences=sentenceSeparator(scratch)
    twoDkeyArray=[]

    for i in sentences:
        tempsDad=[]
        # print i
        iSplitted=i.split()
        for j in iSplitted:
            temp=['', '']

            if(j in io_keys):

                temp[0]=j
                temp[1]='io'

            elif(j in math_keys):

                temp[0]=j
                temp[1]='math'

            elif(j in control_keys):

                temp[0]=j
                temp[1]='control'

            else:
                continue

            tempsDad.append(temp)
        twoDkeyArray.append(tempsDad)

    array = []

    for i in range(len(sentences)) :
        array.append([sentences[i].split(), twoDkeyArray[i]])

    return array
# print extractKeywordsFromScratched("Print Add two to 5.0 and 4.0. Multiply of 3 and 5..")


def RetKeywordsAndNot_KeywordFromRepository(filename):
    # todo
    # 1.take input from header repository-done
    # 2.parse it for keywords and not_keywords-done
    tmp = open (filename,"r")# here change the name of the file from where you are taking input
    readLinesFromFile = tmp.readlines()
    tmp.close()
     # section for keywords
    keywords=[]
    not_keywords=['define']
    for i in xrange(len(readLinesFromFile)):
        readLinesFromFile[i]=readLinesFromFile[i].split(" ")
        if(readLinesFromFile[i][0]=='define'):
            keywords.append(readLinesFromFile[i][1])
        else:
            not_keywords.append(readLinesFromFile[i])
    keywords.sort()

    # section for not_keywords

    temp = open (filename,"r")# here change the name of the file from where you are taking input
    readFromFile = temp.read()
    temp.close()
    # credits+ for the following artistic display of temp goes to Q.
    not_keywords=[]
    temp1= readFromFile.split('.')
    temp2= ' '.join(temp1)
    temp3= temp2.split('[')
    temp4= ''.join(temp3)
    temp5= temp4.split(']')
    temp6= ''.join(temp5)
    temp7= temp6.split(':')
    temp8= ''.join(temp7)
    temp9= temp8.split()
    temp10= ' '.join(temp9)
    readFromFile=temp10
    readFromFile=readFromFile.split()
    #regex use starting here
    temp11=re.compile('[a-z]+',re.IGNORECASE)
    for i in xrange(len(readFromFile)):
        temp12=temp11.match(readFromFile[i])
        if (temp12):
            not_keywords.append(readFromFile[i])
    # removes duplicates and keywords from not keywords
    not_keywords=list(set(not_keywords) - set(keywords))
    not_keywords.sort()

    # returning
    return keywords,not_keywords
# keywords,not_keywords=RetKeywordsAndNot_KeywordFromRepository()
# takeInputFromUserAndReturnSentences()


def populateSentenceObjs(some_list):
	global_list = []
	
	for item in some_list:
		senten = item[0]
		keyword_list = []
		for each in item[1] :
			keyword_list.append(each)
		global_list.append(d_str.Sentence(senten, keyword_list))

	return global_list


def separateCommas(sentence) :
	sent = ""

	for char in sentence :
		if (char == ",") :
			sent = sent + " ,"
		else :
			sent = sent + char

	return sent


def retAllKeysNotKeys() :

	io_keys, io_notkeys = RetKeywordsAndNot_KeywordFromRepository('io_repository.txt')
	math_keys, math_notkeys = RetKeywordsAndNot_KeywordFromRepository('math_repository.txt')
	control_keys, control_notkeys = RetKeywordsAndNot_KeywordFromRepository('control_repository.txt')

	all_keys = []
	not_keys = []

	# appending keys -----
	for i in range(io_keys) :
		all_keys.append(io_keys[i])

	for i in range(math_keys) :
		all_keys.append(math_keys[i])

	for i in range(control_keys) :
		all_keys.append(control_keys[i])
	# ------

	# appending not_keys -----
	for i in range(io_keys) :
		all_keys.append(io_keys[i])

	for i in range(math_keys) :
		all_keys.append(math_keys[i])

	for i in range(control_keys) :
		all_keys.append(control_keys[i])
	# -----

	return all_keys, not_keys


def isProbableVar(word) :
	all_keys, not_keys = retAllKeysNotKeys()

	if ( word not in all_keys and word not in not_keys ) :
		return True

	return False

