import codecs,sys,re

# from Lookups import names_strong

bible_filename = sys.argv[1]
names_filename = sys.argv[2]

greek_bible= codecs.open(bible_filename,mode="r",encoding="utf-8").readlines()

names_file = codecs.open(names_filename,mode="r",encoding="utf-8").readlines()


name_refs={}

for name in names_file[1:]:
	name_line = name[:-1]
	name_all = re.split("\t",name_line)
	name_refs[name_all[0]] = {"all":name_all ,  "refs":[]	}
		
# print("okay")
# print(len(name_refs))

pattern = re.compile("<s snum=\d+>")
for ref,verse in enumerate(greek_bible):
	verse = re.sub(pattern," ",verse,0)
	verse = verse.replace("</s>"," ")
	verse = verse.strip()
	verse = re.split("\s+",verse)
	for name in name_refs:
		
		if name in verse:
			# name_refs.append((name_all[0],name_all[1],name_all[2],name_all[3],ref+23146))
			name_refs[name]["refs"].append(ref+23146)
	
# name_refs.sort()

names_file_appended = codecs.open(names_filename[:-3]+"ref.csv",mode="w",encoding="utf-8")
names_file_appended.write("strongs\tGreek\tGreek_roman\tEnglish\tFrequency\trefs\n")
for name in name_refs:
	names_file_appended.write(name_refs[name]["all"][0]+"\t"+name_refs[name]["all"][1]+"\t"+name_refs[name]["all"][2]+"\t"+name_refs[name]["all"][3]+"\t"+str(len(name_refs[name]["refs"]))+"\t"+str(name_refs[name]["refs"])+"\n")
names_file_appended.close()


