import sys
import re
import string
import math

train_text = sys.argv[1]

with open(train_text, 'rb') as fin:
    text = fin.read()

each_row=text.strip().split('\n')

markov_model_dict = {}
all_tag_set = set()
first_word_dict={}	

for indi_row in each_row:
	each_word_with_tag_array=indi_row.split(" ")
	for each_word in each_word_with_tag_array:
		word_tag = each_word.rsplit('/',1)[1]
		if(len(word_tag)==2):
			all_tag_set.add(word_tag)

#Transition Proability

for indi_row in each_row:
	each_word_with_tag_array=indi_row.split(" ")
	first_word_tag = each_word_with_tag_array[0].rsplit('/',1)[1]
	if not (first_word_tag in first_word_dict):
		first_word_dict[first_word_tag]=1.0
	else:
		first_word_dict[first_word_tag]=first_word_dict[first_word_tag]+1.0

markov_model_dict["q0"]=first_word_dict

for indi_row in each_row:
	each_word_with_tag_array=indi_row.split(" ")
	for each_word_with_tag in range(len(each_word_with_tag_array[1:])):
		current_word_tag = each_word_with_tag_array[each_word_with_tag].rsplit('/',1)[1]
		prev_word_tag = each_word_with_tag_array[each_word_with_tag-1].rsplit('/',1)[1]
		if not (prev_word_tag in markov_model_dict):
			current_word_tag_dict={}
			current_word_tag_dict[current_word_tag]=1.0
			markov_model_dict[prev_word_tag]=current_word_tag_dict
		else:
			if not (current_word_tag in markov_model_dict[prev_word_tag]):
				markov_model_dict[prev_word_tag][current_word_tag]=1.0
			else:
				markov_model_dict[prev_word_tag][current_word_tag]=markov_model_dict[prev_word_tag][current_word_tag]+1


for k,v in markov_model_dict.items():
	for tag in all_tag_set:
			if (tag in markov_model_dict[k]):
				markov_model_dict[k][tag]=markov_model_dict[k][tag]+1
			else:
				markov_model_dict[k][tag]=1
	sum=0.0
	for k1,v1 in v.items():
		sum=sum+v1
	for k1,v1 in v.items():
		markov_model_dict[k][k1]=v1/sum

target = open("hmmmodel.txt", 'w')

target.write("\n\n Markov Model Probabilities\n\n")
target.write(str(markov_model_dict))


#Emission Proability

emission_probability_dict = {}
each_tag_count_dict={}
for indi_row in each_row:
	each_word_with_tag_array=indi_row.split(" ")
	for each_word in each_word_with_tag_array:
		each_word_array = each_word.rsplit('/',1)
		each_word_without_tag = each_word_array[0]
		each_word_tag = each_word_array[1]
		if not(each_word_tag in each_tag_count_dict):
			each_tag_count_dict[each_word_tag]=1.0
		else:
			each_tag_count_dict[each_word_tag]=each_tag_count_dict[each_word_tag]+1
		if not(each_word_without_tag in emission_probability_dict):
			each_word_tag_dict = {}
			each_word_tag_dict[each_word_tag]=1.0
			emission_probability_dict[each_word_without_tag]=each_word_tag_dict
		else:
			if not(each_word_tag in emission_probability_dict[each_word_without_tag]):
				emission_probability_dict[each_word_without_tag][each_word_tag]=1.0
			else:
				emission_probability_dict[each_word_without_tag][each_word_tag]=emission_probability_dict[each_word_without_tag][each_word_tag]+1.0

for k,v in emission_probability_dict.items():
	for k1,v1 in v.items():
		emission_probability_dict[k][k1]=math.log(v1/each_tag_count_dict[k1])


target.write("\n\n Emission Probabilities\n\n")
target.write(str(emission_probability_dict))