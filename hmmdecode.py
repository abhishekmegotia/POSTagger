import sys
import re
import string
import math
 

train_text = sys.argv[1]

with open("hmmmodel.txt", 'rb') as fin:
    model = fin.read()

markov_model = model.split("Emission Probabilities")[0].split("Markov Model Probabilities")[1].strip()
emission_model = model.split("Emission Probabilities")[1].strip()

markov_model_dict = eval(markov_model)
emission_model_dict = eval(emission_model)

with open(train_text, 'rb') as fin:
    raw_data = fin.read()

each_line_array = raw_data.split('\n')

probability_dict = {}

target = open("hmmoutput.txt", 'w')

for each_line in each_line_array:
	word_with_tag = {}
	probability_dict = {}
	previous_word_prob = 0.0
	each_word_array = each_line.split(" ")
	possible_tags_dict = {}
	first_word = each_word_array[0]
	previous_word = first_word
	max_prob = -999999
	selected_tag = ""
	if first_word in emission_model_dict:
		for each_tag in emission_model_dict[first_word]:
			if not(first_word in probability_dict):
				probability_dict[first_word]={}
			probability_dict[first_word][each_tag] = previous_word_prob+markov_model_dict["q0"][each_tag]+emission_model_dict[first_word][each_tag]
			if probability_dict[first_word][each_tag] > max_prob:
				max_prob = probability_dict[first_word][each_tag]
				selected_tag = each_tag
		previous_word_prob = max_prob
		word_with_tag[first_word] = selected_tag
	else:
		for each_tag in markov_model_dict["q0"]:
			if not(first_word in probability_dict):
						probability_dict[first_word]={}
			probability_dict[first_word][each_tag] = markov_model_dict["q0"][each_tag]
			if probability_dict[first_word][each_tag] > max_prob:
			 	max_prob = probability_dict[first_word][each_tag]
			 	selected_tag = each_tag
        word_with_tag[first_word] = selected_tag

	for each_word in each_word_array[1:]:
		max_prob = -9999999
		selected_tag = ""
		previous_tag = word_with_tag[previous_word]
		if each_word in emission_model_dict:
			for each_tag in emission_model_dict[each_word]:
				if not(each_word in probability_dict):
					probability_dict[each_word]={}
				probability_dict[each_word][each_tag] = previous_word_prob + markov_model_dict[previous_tag][each_tag]+emission_model_dict[each_word][each_tag]
				if probability_dict[each_word][each_tag] > max_prob:
					max_prob = probability_dict[each_word][each_tag]
					selected_tag = each_tag
			previous_word_prob = max_prob
			word_with_tag[each_word] = selected_tag
		else:
			for each_tag in markov_model_dict[previous_tag]:
				if not(each_word in probability_dict):
						probability_dict[each_word]={}
				probability_dict[each_word][each_tag] =  markov_model_dict[previous_tag][each_tag]	
				if probability_dict[each_word][each_tag] > max_prob:
					max_prob = probability_dict[each_word][each_tag]
					selected_tag = each_tag
        	word_with_tag[each_word] = selected_tag

		previous_word = each_word

	for each_word in each_word_array:
		printVariable = each_word+"/"+word_with_tag[each_word]+" "
		target.write(printVariable)

	target.write('\n')		