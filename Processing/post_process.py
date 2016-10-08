from Utilities import subordinate_functions as sbfnc
from Processing import process_sequences as pscs
from Data_Stores import data_store_defs as d_str
from copy import deepcopy 

words = ["$","2","+","3","@","and","$","it","in","var","@"]


def substituteValues(output_rule, dictionary, sentence):
    # print 10, dictionary, output_rule, sentence.current

    dot_found = False

    key_list = dictionary.keys()

    i = 0

    while (i < len(output_rule)) :
        # print 17, output_rule, output_rule[i]

        if (output_rule[i][0] == "#"):
            if(output_rule[i][-1] == "."):
                indice = output_rule[i][1:-1]
                dot_found = True
            else:
                indice = output_rule[i][1:]
            for key in key_list:
                if (key[:-1] == indice and key[-1] == "m"):
                    start = dictionary[key][0]
                    end = dictionary[key][1]
                    val_at_indice = []

                    for j in range(start, end):
                        val_at_indice.append(sentence.current[j])

                    # print 32, start, end, sentence.current, val_at_indice

                    del output_rule[i]
                    for k in range(i, len(val_at_indice) + i) :
                        output_rule.insert(k, val_at_indice[k - i])

                    # print 38, output_rule

                elif (key[:-1] == indice):
                    start = dictionary[key][0]
                    end = dictionary[key][1]
                    val_at_indice = sentence.current[start:end]

                    # print "lolo", val_at_indice

                    true_val_at_index = ""
                    for j in range(len(val_at_indice)) :
                        true_val_at_index = true_val_at_index + val_at_indice[j]

                    # print 45, true_val_at_index

                    output_rule[i] = true_val_at_index

        elif (output_rule[i] == "<var>" or output_rule[i] == "<var>.") :
            # print 56, "in <var>"

            # var at end of sentence
            if (output_rule[i] == "<var>.") :
                dot_found = True

            indice = "<var>"
            for key in key_list:
                if (key == indice):
                    start = dictionary[key][0]
                    end = dictionary[key][1]
                    val_at_indice = sentence.current[start:end]

                    # print "lololol", val_at_indice, sentence.current

                    true_val_at_index = ""
                    for j in range(len(val_at_indice)) :
                        true_val_at_index = true_val_at_index + val_at_indice[j]

                    output_rule[i] = true_val_at_index

        i = i + 1

    if (dot_found == True) :
        output_rule[-1] = output_rule[-1] + "."
    
    return output_rule


def processConditional(sentence, proc_branch, dictionary):
    if ("if" in sentence.current):
        key_list = dictionary.keys()
        # print "dic", dictionary

        for key in key_list:
            if dictionary[key] == True :
                key_indice = key[:-1]
                index = sbfnc.toNum(key_indice)
                return dictionary[str(index+1)+"S"]



def getAtTheRateIndex(words):
    for i in range(len(words)):
        if words[i] == "@":
            return i
    return None


def process(words, proc_branch):
    # print 91, words
    if ("Print" in words or "in" in words or "as" in words):
        result = processOthers(words[1:-1], proc_branch.symbols, proc_branch.current_level, proc_branch)
    else :
        # print "104", words
        result = processMath(words, proc_branch)

        # result=processMath([ '10', '+', '35' ])

    # print "ks", str(result)
    return str(result)


# processEachRule(sentence, proc_branch)

def isHavingAt(words):
    
    if not ((words[0]=='$') and (words[-1] == '@'  or words[-1] == '@.')):
        words= ['$'] + words[0:] + ['@']
        return words
    
    else:
        return words

# $ 4+4-5 and 6-10 @

def processMath(words, proc_branch):

    # print "words1",words
    
    # words = isHavingAt(words)
    operators = ["+","-","/","*","(",")","."]
    first = 0
    last = 0
    i = 1
    j = 1
    flag = False

    while(i<len(words)):

        if (j > i):
            i = i + 1
            continue
        if(words[i]=="(" or sbfnc.isNumber(words[i])):
            first = i
            last = i

            j = i
            while(j<len(words)):

                if (sbfnc.isNumber(words[j]) or words[j] in operators):
                    last = j
                else:

                    # print "words",words

                    words = words[:first] + [pscs.postfix(" ".join(words[first:last+1]))] + words[last + 1:]

                    # print "words1",("").join(words)

                    flag = True
                    break
                j = j + 1
        i = i + 1
        if flag:

            flag = False
            i = i - (last - first) - 1
    # print "words2", words0
    proc_branch.result = sbfnc.toNum(words[1])
    return " ".join(words[1:-1])


def processOthers(words, sym_table, lvl, proc_branch):
    # print "kya yaha aa rha????", words
    # for symbol in sym_table:
    #     print "akhri ummeeed", symbol.name, ":", symbol.value
    if ("Print" in words):
        # print 162, "aa rha", proc_branch.symbols[0].value

        out_str = ""

        words = words[1:]

        for i in range(len(words)) :

            is_symbol = False
            for symbol in sym_table:
                if symbol.name == words[i] and symbol.scope_level <= lvl:
                    out_str = out_str + str(symbol.value)
                    is_symbol = True
            
            if (is_symbol == False) :
                if (sbfnc.isNumber(words[i])) :
                    out_str = out_str + words[i]

                elif (words[i][0] == "\"" and words[i][-1] == "\"") : # removing quotes from string words
                    out_str = out_str + words[i][1:-1]

                elif (words[i] == ",") :
                    out_str = out_str + " "

                elif (words[i] == "and") :
                    out_str = out_str + " "

                else :
                #ERROR
                    print "The F is this Sh**."
        
        proc_branch.result = "null"
        print out_str
        return "null"

    elif("as" in words):   #CONSTANT
        # print 219, words
        new_root_type = "int"
        vals = []
        if("and" in words): #and indicates multi value input
            and_index = words.index("and")
            for i in range(0,and_index+2,2):
                vals.append(sbfnc.toNum(words[i]))
            var = words[and_index+3]
            new_root_type = "arr"
        else :
            var = words[2]
            if (sbfnc.isNumber(words[0])) :
                vals = sbfnc.toNum(words[0])
                new_root_type = "int"

            else :
                vals = words[0]
                new_root_type = "str"

        # print 165, vals, sym_table

        for symbol in sym_table:
            # print "is here?????"
            if (symbol.name == var and symbol.root_type == "constant"):
                print "Constants cannot be over-written." #ERROR
                return "ERROR"
            elif (symbol.name == var):
                if (symbol.scope_level <= lvl):
                    symbol.value = vals
                    symbol.root_type = new_root_type
                    # print 177, symbol.name, symbol.value
                    
                    proc_branch.result = "null"
                    return "null"
                else :
                    return "ERROR"  #The variable lies outside the scope
            else:
                pass
        # print 182, vals, "name : ", var
        sym_table.append(d_str.Symbol(var,vals,lvl,new_root_type,"constant"))
        # print 195, sym_table
        proc_branch.result = "null"
        return "null"

    elif("in" in words):	#VARIABLE
        # print 262, words
        new_root_type = "int"
        vals = []
        if("and" in words): #and indicates multi value input
            and_index = words.index("and")
            for i in range(0,and_index+2,2):
                vals.append(sbfnc.toNum(words[i]))
            var = words[and_index+3]
            new_root_type = "arr"
        else :
            var = words[2]
            if (sbfnc.isNumber(words[0])) :
                vals = sbfnc.toNum(words[0])
                new_root_type = "int"
            else :
                vals = words[0]
                new_root_type = "str"

        # print 280, vals, var, sym_table

        for symbol in sym_table:
            # print "is here?????"
            if (symbol.name == var and symbol.root_type == "constant"):
                print "Constants cannot be over-written." #ERROR
                return "ERROR"
            elif (symbol.name == var):
                if (symbol.scope_level <= proc_branch.current_level):
                    symbol.value = vals
                    symbol.var_type = new_root_type
                    # print 291, symbol.name, symbol.value
                    
                    proc_branch.result = "null"
                    return "null"
                else :
                    return "ERROR"  #The variable lies outside the scope
            else:
                pass
        # print 299, vals, "name : ", var
        sym_table.append(d_str.Symbol(var,vals,lvl,new_root_type,"variable"))
        # print 301, sym_table
        proc_branch.result = "null"
        return "null"