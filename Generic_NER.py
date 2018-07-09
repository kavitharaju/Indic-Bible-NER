# from pyiwn import pyiwn

import codecs, sys, re,string
import ast
from indic_transliteration.xsanscript import *
from soundex import Soundex
from romanize import romanize
import Levenshtein

# from names_ref_list import names_ref_list, names_strong, names_hindi, greek_name_forms
# from mar_stops import STOP_LIST as mar_stopwords

if len(sys.argv)>= 5:

	lang = sys.argv[1]
	path = sys.argv[2]
	reference_path = sys.argv[3]
	col_references = [int(x) for x in sys.argv[4:]]
	# if lang == "mar":
	# 	stopwords = mar_stopwords
		# wordnet = pyiwn.IndoWordNet('marathi')
else:
	print("Usage: Python3 Generic_NER.py lang bible_path names_file romanized_columns")
	sys.exit(0)

lid_col=5

inp_bible = codecs.open(path,mode="r",encoding="utf-8").readlines()


names_reference=[]
temp = codecs.open(reference_path,mode="r",encoding="utf-8").readlines()
titles = temp[0]
for line in temp[1:]:
	name_all = re.split("\t",line[:-1])
	names_reference.append(name_all)

punct = string.punctuation+"“’‘”।"
scheme_dict = {'asm':SCHEMES[BENGALI],'ben':SCHEMES[BENGALI],'guj':SCHEMES[GUJARATI],
            'hin':SCHEMES[DEVANAGARI],'kan':SCHEMES[KANNADA],'mal':SCHEMES[MALAYALAM],
            'mar':SCHEMES[DEVANAGARI],"ori":SCHEMES[ORIYA],'pun':SCHEMES[GURMUKHI],
            'tam':SCHEMES[TAMIL],'tel':SCHEMES[TELUGU],'urd':SCHEMES[DEVANAGARI]}
if lang in scheme_dict:
	src_scheme = scheme_dict[lang] 
scheme_map = SchemeMap(src_scheme,SCHEMES[HK])
instance = Soundex()

findings = {}
for i,line in enumerate(inp_bible):
	curr_line_id = 23146+i
	if line == "" or line=="\n":
		continue

	for index, name in enumerate(names_reference):
		lids = ast.literal_eval(name[lid_col])
		for col in col_references:
			romans = name[col]
			if romans =="":
				continue


			print(".",end="")
			temp =line.strip()
			line = ""
			for char in temp:
				if char not in punct and char !="\n":
					line= line+char


			if curr_line_id in lids:
				words = re.split("\s+",line)

				for word in words:
					# Check if it is a name
					word_roman = transliterate(word, scheme_map=scheme_map)
					for char in word_roman:
						if char > u'\u02AF':
							word_roman = word_roman.replace(char,"")
					if word_roman=="" :
						continue
					try:
						sim_score = instance.compare(romans, word_roman)
						if sim_score in [0,1]:
							if index in findings:
									# if (word,word_roman) not in findings[index]:
									findings[index].append((word,word_roman))
									print("found: "+romans+"-"+word_roman)
							else:
								findings[index] = [(word,word_roman)]
								print("found: "+romans+"-"+word_roman)
						
					except Exception as e:
						print(romans)
						print(word)
						print("\""+word_roman+"\"")
						print(words)
						print("\""+line+"\"")
						raise e
print(len(findings))
# refined_findings={}

# for index in findings:


output_file = codecs.open(reference_path[:-3]+"added_"+lang+".csv",mode="w",encoding="utf-8")

index=0
output_file.write(titles[:-1]+"\t"+lang+"\t"+lang+"_roman\n")
for index,name_all in enumerate(names_reference):
	for name in name_all:
		output_file.write(name+"\t")
	lang_word = []
	lang_roman_word = []

	median_word = ""
	median_roman = ""
	if index in findings:

		for pair in findings[index]:
			lang_word.append(pair[0])
			lang_roman_word.append(pair[1].lower())
			try:
				if len(lang_word)>3:
					
					median_roman = Levenshtein.median(lang_roman_word)
					pos = lang_roman_word.index(median_roman)
					median_word = lang_word[pos]
					print("Got one median")
				else:
					median_word =", ".join(lang_word)
					median_roman=", ".join(lang_roman_word)	
			except Exception as e:
				median_word =", ".join(lang_word)
				median_roman=", ".join(lang_roman_word) 


	output_file.write(median_word+"\t"+median_roman+"\n")
output_file.close()




## to get the romanized form of all greek names we have
# for strng , greek_forms in zip(names_strong,greek_name_forms):
# 	greek_romans = []
# 	for form in greek_forms:
# 		greek_romans.append(romanize(form))
# 	print(strng+"\t"+str(greek_romans))
# sys.exit(0)



# blacklist_strongs = ["G51830","G41930","G34340","G31980","G30990","G28570","G22810","G21660","G21037","G20960","G16380","G04910"]



# line_count = 0
# output = []
# for triplet in names_ref_list:
# 	curr_line_id = triplet[0]
# 	strong = triplet[1]
# 	name_id = triplet[2]
# 	try:
# 		hindi_name = names_hindi[name_id]
# 		greek_forms = greek_name_forms[name_id]
		
# 	except Exception as e:
# 		print(triplet)
# 		raise e

# 	hindi_roman = transliterate(hindi_name, scheme_map=scheme_map)
# 	greek_romans = []
# 	for form in greek_forms:
# 		greek_romans.append(romanize(form))


# 	if curr_line_id != line_count:
# 		while(line_count!=curr_line_id):
# 			line =inp_file.readline()
# 			line_count=line_count+1
# 		temp = line
# 		line = ''
# 		for char in temp:
# 			if char not in punct:
# 				line= line+char

# 		line = re.sub("\d+","",line)

# 		line = re.split("\s+",line.strip())
	


# 	# to manually pick out unidentified words
# 	if strong in blacklist_strongs:
# 		print(strong+"\t"+str(greek_romans)+"\t"+str(curr_line_id)+"\t"+ str(line))
# 	continue


# 	for word in line:
# 		try:
# 			if word == "":
# 				continue
# 			word_roman = transliterate(word, scheme_map=scheme_map)
# 			sim_score = []
# 			sim_score.append(instance.compare(hindi_roman, word_roman))
# 			for greek_roman in greek_romans:
# 				sim_score.append(instance.compare(greek_roman, word_roman))


# 			if 0 in sim_score or 1 in sim_score:
# 				# pass
# 				output.append((strong,str(greek_romans),hindi_name,hindi_roman,word_roman,word))
			
# 		except Exception as e:
# 			print(e)
# 			print(hindi_roman+"\t"+word_roman+"\n\n\n")

	


# output.sort()
# for items in output:
# 	for item in items:
# 		print(item+"\t",end="")
# 	print("\n",end="")

