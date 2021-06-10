import pickle
from jinja2 import Environment, FileSystemLoader
# from google.transliteration import transliterate_text
# from indic_transliteration import sanscript
# from indic_transliteration.sanscript import transliterate
# import translators as ts
# from deep_translator import GoogleTranslator
# from translation import google, ConnectError
# from anuvaad import Anuvaad
# telugu = Anuvaad('english-telugu')
# from deeptranslit import DeepTranslit
# translit = DeepTranslit('telugu').transliterate

from genXML import tewiki, writePage

import ast

def spliting(row):
    li =[]
    date = row.split(",")
    li.append(date[-1])
    year = date[0].split("at")
    li.append(year[-1])
    against = year[0].split("vs")
    li.append(against[-1])

    return li


def getData(row):
	# global translit
	# # Translation and Transliteration
	# try:
	# 	title = row.title.values[0]
	# 	# anu_title = telugu.anuvaad(row.title.values[0])
	# 	deep = translit(title)[0]['pred']
	# 	# if float(deep['prob']) >= 0.070:
	# 	# 	title = deep['pred']
	# 	# else:
	# 	# 	title = anu_title		
	# except:
	# 	title =row.title.values[0]

	# Data dictionary 
	tropies = row["Major trophies"].values[0]
	if tropies != 'nan':
		tropies = ast.literal_eval(row["Major trophies"].values[0])
	AWARDS = row["AWARDS"].values[0]
	if AWARDS != 'nan':
		AWARDS = ast.literal_eval(row["AWARDS"].values[0])
	records = row["Records"].values[0]
	if records != 'nan':
		records = ast.literal_eval(row["Records"].values[0])
	Test_Matches_debut = spliting(row['Test Matches_debut'].values[0])
	ODI_Matches_debut= spliting(row['ODI Matches_debut'].values[0])
	T20I_Matches_debut = spliting(row['T20I Matches_debut'].values[0])
	# FC_Matches_debut = spliting(row['FC Matches_debut'].values[0])
	# List_A_Matches_debut = spliting(row['List A Matches_debut'].values[0])
	# T20_Matches_debut = spliting(row['T20 Matches_debut'].values[0])
	Test_Matches_last_appearance = spliting(row['Test Matches_last_appearance'].values[0])
	ODI_Matches_last_appearance = spliting(row['ODI Matches_last_appearance'].values[0])
	T20I_Matches_last_appearance = spliting(row['T20I Matches_last_appearance'].values[0])
	# FC_Matches_last_appearance = spliting(row['FC Matches_last_appearance'].values[0])
	# List_A_Matches_last_appearance = spliting(row['List A Matches_last_appearance'].values[0])
	# T20_Matches_last_appearance = spliting(row['T20 Matches_last_appearance'].values[0])
	print(row['Relations'].values[0])
	data = {
		#{%- macro info(title, id, year, genre, actors, duration, country, original_title) -%}
		'Full_Name':row['Full Name'].values[0],
		'Player_Name':row['Player_Name'].values[0],
		'Nationality':row['Nationality'].values[0],
		'Born':row['Born'].values[0],
		'Died':row['Died'].values[0],
		'age':row['Age'].values[0],
		'Relations':row['Relations'].values[0],
		'career_span':row['career_span'].values[0],
		'Batting_Style':row['Batting Style'].values[0],
		'Bowling_Style':row['Bowling Style'].values[0],
		'Height':row['Height'].values[0],
		'Jersey_Number':row['Jersey_Number'].values[0],
		'Gender':row['Gender'].values[0],
		'Playing_Role':row['Playing Role'].values[0],
		'Teams':ast.literal_eval(row['Teams'].values[0]),
		'testdebutdate':Test_Matches_debut[1],
		'testdebutyear':Test_Matches_debut[0],
		'testdebutagainst':Test_Matches_debut[-1],
		'odidebutdate':ODI_Matches_debut[1],
		'odidebutyear':ODI_Matches_debut[0],
		'odidebutagainst':ODI_Matches_debut[-1],
		'T20Idebutdate':T20I_Matches_debut[1],
		'T20Idebutyear':T20I_Matches_debut[0],
		'T20Idebutagainst':T20I_Matches_debut[-1],
		'lasttestdate':Test_Matches_last_appearance[1],
		'lasttestyear':Test_Matches_last_appearance[0],
		'lasttestagainst':Test_Matches_last_appearance[-1],
		'lastodidate':ODI_Matches_last_appearance[1],
		'lastodiyear':ODI_Matches_last_appearance[0],
		'lastodiagainst':ODI_Matches_last_appearance[-1],
		'lastT20Idate':T20I_Matches_last_appearance[1],
		'lastT20Iyear':T20I_Matches_last_appearance[0],
		'lastT20Iagainst':T20I_Matches_last_appearance[-1],
		'Major_trophies':tropies,
		'Records':records,
		"AWARDS" :AWARDS


	}

	return data

def main():
	file_loader = FileSystemLoader('./template')
	env = Environment(loader=file_loader)
	template = env.get_template('template.j2')

	moviesDF =pickle.load(open('./data/cricket_players_DF.pkl', 'rb'))
	moviesDF.fillna(value="nan", inplace=True)
	# ids = moviesDF.Cricinfo_id.tolist()
	# ids =ids[3:4] #remove this to generate articles for all movies

	# Initiate the file object
	# fobj = open('movies.xml', 'w',encoding="utf-8")
	# fobj.write(tewiki+'\n')

	# for i, movieId in enumerate(ids):
	# 	row = moviesDF.loc[moviesDF['Cricinfo_id']==movieId]
	# 	title = row['AWARDS'].values[0]
	# 	# text = template.render(getData(row))

		# writePage(title, text, fobj)	
	fobj = open('infoandoverview.xml', 'w', encoding='utf-8')
	fobj.write(tewiki+'\n')	
	row = moviesDF.head(12).tail(1)
	text = template.render(getData(row))
	player_name = row["Full Name"].values[0]
	# print(player_name)
	# x = ast.literal_eval(player_name)
	# print(type(x))
	# print(x.keys())
	# for key,vale in x.items():
	# 	print(key)
	writePage(player_name, text, fobj)
	
   
	fobj.write('</mediawiki>')
	fobj.close()

if __name__ == '__main__':
	main()