import re
import json
import sys
import operator
from pprint import pprint
#path='dev-text.txt'
path_model = sys.argv[1]
path_input = sys.argv[2]

raw_data_file=open(path_input)
raw_data = raw_data_file.readlines()
with open(path_model, 'r') as fp:
	complete_dict = json.load(fp)

f= open("percepoutput.txt","w+",encoding='utf8')	
	
class_1 = dict()
class_1 = complete_dict['class_1']
class_2 = dict()
class_2 = complete_dict['class_2']
highFreq=complete_dict['highFreq']


for x,val in enumerate(raw_data):
	line = val.split()
	#line = line.strip()
	unique_code = line[0]
	new_list = line[1:]
	new_list = re.findall(r"[\w']+|[.,!?;():]", " ".join(new_list))
	sum_1=0
	sum_2=0
	for y, word in enumerate(new_list):
		#if word not in highFreq:
		word=word.lower()
		if word in class_1:
			sum_1= sum_1+class_1[word]
		if word in class_2:
			sum_2= sum_2+class_2[word]
		
	sum_1=sum_1+class_1['bias']	
	sum_2=sum_2+class_2['bias']
	
	if sum_1<=0:
		c_1 = 'Fake'
	else:
		c_1 = 'True'
		
	if sum_2<=0:
		c_2 = 'Neg'
	else:
		c_2 = 'Pos'
	
	string_to_write = unique_code+" "+c_1+" "+c_2+"\n"	
	f.write(string_to_write)
f.close()