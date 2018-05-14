import re
import json
import sys
import operator
import random
from pprint import pprint
path =sys.argv[1]
tagged_data_file = open(path)
tagged_data = tagged_data_file.readlines()
model = dict()
#word_freq = dict()
weight_1 = dict()
weight_2 = dict()
average_class_1 = dict()
average_class_2= dict()
word_total = dict()
for val in tagged_data:
	line = val.split()
	new_line = line[3:]
	new_line = re.findall(r"[\w']+|[.,!?;():]", " ".join(new_line))	
	for word in new_line:
		word = word.lower()
		if word not in word_total:
			#word_freq[word]=0
			word_total[word]=1
			weight_1[word]=0
			weight_2[word]=0
			average_class_1[word]=0
			average_class_2[word]=0			
		else:
			word_total[word]=word_total[word]+1

sorted_x = sorted(word_total.items(), key=operator.itemgetter(1))
sorted_x.reverse()
sorted_x = sorted_x[:5]
sorted_x=dict(sorted_x[:len(sorted_x)])
			
b_1=0
b_2=0
b_1_avg=0
b_2_avg=0
#number_of_iterations=30
#vanilla_iter=30
#average_iter=30
#if vanilla_iter>average_iter:
#	max = vanilla_iter
#else:
#	max = average_iter	
c=1
flag=0
for i in range(0,30):
	random.seed(12)
	random.shuffle(tagged_data)	
	if i%7 == 0:
		tagged_data = tagged_data[::-1]	
	for val in tagged_data:
		line = val.split()
		class_1 = line[1]
		class_2 = line[2]
		new_list = line[3:]
		word_freq={}
		new_list = re.findall(r"[\w']+|[.,!?;():]", " ".join(new_list))	
		if class_1 == "True":
			y=1
		else: 
			y=-1
		
		if class_2 == "Pos":
			z= 1
		else:
			z=-1
			
		for word in new_list:
			word=word.lower()
			if word not in word_freq:
				word_freq[word]=0
			word_freq[word]=word_freq[word]+1
		
		sum_1=0
		sum_2=0
		for word in word_freq:
			sum_1 = sum_1 + weight_1[word]*word_freq[word]
			sum_2 = sum_2 + weight_2[word]*word_freq[word]			
		
		sum_1+=b_1
		sum_2+=b_2
		
		a_1 = sum_1*y
		a_2 = sum_2*z
		
		if a_1 <= 0:
			for word in word_freq:
				weight_1[word]+=y*word_freq[word]
				average_class_1[word]=average_class_1[word]+y*(c)*word_freq[word]
			b_1+=y
			b_1_avg=b_1_avg+ y*c
		
		if a_2 <= 0:	
			for word in word_freq:
				weight_2[word]+=z*word_freq[word]
				average_class_2[word]=average_class_2[word]+z*c*word_freq[word]
			b_2+=z
			b_2_avg=b_2_avg+ z*c
	c=c+1		

for word in word_total:
	word = word.lower()
	average_class_1[word]= weight_1[word]- (average_class_1[word]/float(c))
	average_class_2[word]= weight_2[word]- (average_class_2[word]/float(c))	

b_1_avg=b_1-(b_1_avg/float(c))
b_2_avg=b_2-(b_2_avg/float(c)) 

average_class_1['bias']=b_1_avg
average_class_2['bias']=b_2_avg
	
#weight_1 = {k:v for k,v in weight_1.items() if v != 0}
weight_1['bias']=b_1
#weight_2 = {k:v for k,v in weight_2.items() if v != 0}
weight_2['bias']=b_2

vanilla_model = dict()
vanilla_model['class_1']=weight_1
vanilla_model['class_2']=weight_2
vanilla_model['highFreq']=sorted_x

average_model = dict()
average_model['class_1']=average_class_1
average_model['class_2']=average_class_2
average_model['highFreq']=sorted_x

with open('vanillamodel.txt','w') as fp:
	json.dump(vanilla_model,fp)
fp.close()

with open('averagedmodel.txt','w') as fx:
	json.dump(average_model,fx)
fx.close()
		
tagged_data_file.close()			