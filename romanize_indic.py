import sys,codecs,re
from indic_transliteration.xsanscript import *


param_len = len(sys.argv)
if param_len>=3 and param_len%2==0:
	input_path = sys.argv[1]
	i = 2
	schemes = []
	langs = []
	cols = []
	while i<param_len:
		lang = sys.argv[i]
		col = sys.argv[i+1]
		langs.append(lang)
		cols.append(int(col))
		if lang == "hin":
			schemes.append(SchemeMap(SCHEMES[DEVANAGARI],SCHEMES[HK]))
		elif lang == "mar":
			schemes.append(SchemeMap(SCHEMES[DEVANAGARI],SCHEMES[HK]))
		elif lang == "guj":
			schemes.append(SchemeMap(SCHEMES[GUJARATI],SCHEMES[HK]))


		i=i+2
else:
	print("Usage: python3 romanize_indic.py input_file lang col [lang col]....")
	sys.exit(0)


input_file = codecs.open(input_path,mode="r",encoding="utf-8").readlines()


processed = []
for line in input_file[1:]:
	line = re.split("\t",line[:-1])
	# print(line)
	words = []
	romans= []
	for i,col in enumerate(cols):
		words.append(line[col])
		romans.append(transliterate(line[col],scheme_map=schemes[i]))

	processed.append((words,romans))

# print(processed)

for element in processed:
	words = element[0]
	romans = element[1]
	for w,r in zip(words,romans):
		print(w+"\t"+r,end="\t")
	print("\n",end="")

