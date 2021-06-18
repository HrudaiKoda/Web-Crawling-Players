import pickle
from jinja2 import Environment, FileSystemLoader
from google.transliteration import transliterate_text
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import json
#import translators as ts
#from deep_translator import GoogleTranslator
#from translation import google, ConnectError


from genXML import tewiki, writePage

import ast

def getData(row):
	# Translation and Transliteration
	try:
		player_name = transliterate_text(row.Player_Name.values[0].strip('[]'), lang_code='te')
	except:
		player_name = transliterate(row.Player_Name.values[0].lower(), sanscript.HK, sanscript.TELUGU)


	all_records = str(row.records_telugu.values[0])
	test_records = str(row.test_records_telugu.values[0])
	odi_records = str(row.odi_records_telugu.values[0])
	t20i_records = str(row.t20i_records_telugu.values[0])
	awards = str(row.awards_telugu.values[0])
	gender = row.Gender.values[0]
	references = ast.literal_eval(row.References.values[0])


	if(all_records !='nan'):
		try:
			all_records = ast.literal_eval(all_records)
		except:
			all_records = ast.literal_eval(row.records.values[0])

	
	if(test_records != 'nan'):
		try:
			test_records = ast.literal_eval(test_records)
		except:
			test_records = ast.literal_eval(row.test_records.values[0])

	
	if(odi_records != 'nan'):
		try:
			odi_records = ast.literal_eval(odi_records)
		except:
			odi_records = ast.literal_eval(row.odi_records.values[0])

	
	if(t20i_records != 'nan'):
		try:
			t20i_records = ast.literal_eval(t20i_records)
		except:
			t20i_records = ast.literal_eval(row.t20i_records.values[0])


	if(awards != 'nan'):
		try:
			awards = ast.literal_eval(awards)
		except:
			awards = ast.literal_eval(row.awards.values[0])




	# Data dictionary 
	data = {
		
		'player_name':player_name,
		'all_records': all_records, 
		'test_records': test_records, 
		'odi_records': odi_records,
		't20i_records': t20i_records,
		'awards': awards,
		'gender': gender,
		'references': references
	  }

	return data



def getData2(row):
	data = {
		
		'player_name':row.Player_Name.values[0],
		'all_records': ast.literal_eval(row.records.values[0]), 
		'test_records': ast.literal_eval(row.test_records.values[0]), 
		'odi_records': ast.literal_eval(row.odi_records.values[0]),
		't20i_records': ast.literal_eval(row.t20i_records.values[0]),
		'awards':ast.literal_eval(row.awards.values[0]),
		'gender': row.Gender.values[0],
		'references': ast.literal_eval(row.References.values[0])
	  }

	return data



def get_matches_ref(matches_ref, player_name):
	required_ref = [r for r in matches_ref if "records" in r]
	if len(required_ref) == 0:
		return ''
	return "<ref>[" + required_ref[0] + " " + player_name + " రికార్డులు]</ref>"



def main():
	file_loader = FileSystemLoader('./templates')
	env = Environment(loader=file_loader)
	template = env.get_template('records.j2')

	cricketDF =pickle.load(open('./data/cricket_players.pkl', 'rb'))


	func_dict = {
		"get_matches_ref": get_matches_ref
	}
	template.globals.update(func_dict)
	
	#cricketDF.rename(columns={'Records' : 'records'}, inplace=True)
	
	# Initiate the file object
	fobj = open('recordsAwards.xml', 'w', encoding='utf-8')
	fobj.write(tewiki+'\n')

	#row = cricketDF.head(12).tail(1)
	row = cricketDF.loc[cricketDF['Cricinfo_id'] == 253802]
	#row = cricketDF.loc[cricketDF['Cricinfo_id'] == 54950]

	text = template.render(getData(row))
	player_name = row.Player_Name.values[0]
	all_records = row.records.values[0]	
	
	writePage(player_name, text, fobj)
	
	fobj.write('</mediawiki>')

	fobj = open('recordsAwards.txt', 'w', encoding='utf-8')
	fobj.write(text)
   
	fobj.close()

if __name__ == '__main__':
	main()
