from Data_Stores import data_store_defs as d_str
from Processing import main_process as m_pro
from Utilities import subordinate_functions as sbfnc


def execute():

	# define senteces list here
	sentences = getSentences()
	# sentence2 = getSentences(1)

	new_program_branch = d_str.ProgramBranch(sentences, [d_str.Symbol("it", None, 0, None, "var")])

	m_pro.processBranch([new_program_branch], True)


def getSentences() :
	# output_rule = "Print the sum of 678 and 354."
	# output_rule = "Print 5, 7, 99, \"jsdhjs hdj/shd\", 8 and 6."
	# output_rule = "Print 7."
	# output_rule = "Add 5 to 6 and print it."
	# output_rule = "Store 10, 11 and 12 in it and print it."
	# output_rule = "Store the multiplication of 10 and 11 as pikachu. Print pikachu. Print \"pikachu is God\". Store 10, 11 and 12 in it. Print it. Store it in temp1. Print temp1. Store \"abcdefg\" in pikachu."

	# output_rule = "Store \"le qt a pa\" in temp. print temp."
	# output_rule = "Store the product of 6 and 7 in temp and store the sum of 5 and 6 in temp2. Print temp, temp2, the sum of 5 and 6, \"jump man\" and 8."
	# output_rule = "Print the product of 5 and the sum of 5 and the multiplication of 5 and 6."
	# output_rule = "Print the sum of 5 and the sum of 5 and the sum of 5 and 6."

	# output_rule = "Print \"ji\" and Print \"terminal\"."

	# output_rule = "Add 4 to 6, Store the multiplication of 5 and 4 in temp, print temp, print \"lol : \" and Print \"Ha\"."
	output_rule = "Add 4 to 8, print it, store the sum of 5 and 6 in temp and print \"temp :\" and temp."

	# output_rule = "print the sum of 1 and the product of 1 and 1."
	# output_rule = "Print \"teml\", \"temli\" and \"temlp\"."
	# output_rule = "Print 2 + 3."

	output_rule = sbfnc.separateCommas(output_rule)
	sentence_list = sbfnc.extractKeywordsFromScratched(output_rule)
	true_sentences = sbfnc.populateSentenceObjs(sentence_list)

	return true_sentences


execute()
