import os
import codecs
import re
from romanize import romanize

######## For Strong's numbers identified as NE  ############
names = []

path = "./ugnt"
strng_exp = re.compile("strong=\"(G\d+)\"")
eng_exp = re.compile("/bible/names/(\w+)")
greek_exp = re.compile("lemma=\"(\w+)\"",re.UNICODE)

# iterating through the books
for filename in os.listdir(path):
	f = codecs.open(path+"/"+filename,mode='r',encoding='utf-8')

	print("working on"+filename)
	# checking line by line(word by word in bible text)
	line = f.readline()
	while(line):
		try:
		
		# NE found
			if line.startswith("\w") and ("x-tw=\"rc://*/tw/dict/bible/names" in line):	
				strongs  = strng_exp.search(line).group(1)
				english = eng_exp.search(line).group(1)
				greek = greek_exp.search(line).group(1)
				greek_roman = romanize(greek)
				# if (strongs,greek,greek_roman,english) not in names:
				if strongs not in [element[0] for element in names]:
					names.append((strongs,greek,greek_roman,english))
					# print(strongs)
			
		except Exception as e:
			print(e)
			print("at : "+line)
		line = f.readline()

	f.close()

names.sort()

f = codecs.open("Names.csv",mode="w", encoding="utf-8")

f.write("strongs\tGreek\tGreek_roman\tEnglish\n")
for name in names:
	f.write(name[0]+"\t"+name[1]+"\t"+name[2]+"\t"+name[3]+"\n")

f.close()




