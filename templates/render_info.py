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

def teams(tea,Nationality):
    Iteam = []
    NonIteam = []
    li = []
    for i in tea:
        if Nationality in i:
            Iteam.append(i)
        else:
            NonIteam.append(i)
    if len(Iteam) < 6:
        li = Iteam + NonIteam
    else:
        li = Iteam[:6]
    if len(li) < 6:
        return li
    else:
        return li[:6]

def spliting(row):
    li =[]
    date = row.split(",")
    li.append(date[-1])
    year = date[0].split("at")
    li.append(year[-1])
    against = year[0].split("vs")
    li.append(against[-1])

    return li
def get_profile_ref(profile_ref, player_name):
    if len(profile_ref) == 0:
        return ''
    return "<ref>[" + profile_ref + " " + player_name + " Profile]</ref>"

def Batting_role(batting):
    if batting == "Right hand bat":
        return "కుడిచేతి"
    elif batting == "Left hand bat":
        return "ఎడమచేతి"
    else:
        return batting

def getData(row):
	

	batting = Batting_role(row['Batting Style'].values[0])
	team = row['Teams'].values[0]
	if team != 'nan':
		team = ast.literal_eval(row['Teams'].values[0])
	teams_of_player = teams(team,row['Nationality'].values[0])
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
	profile_ref = ast.literal_eval(row['References'].values[0])
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
		'Batting_Style':batting,
		'info_batting_style':row['Batting Style'].values[0],
		'Bowling_Style':row['Bowling Style'].values[0],
		'Height':row['Height'].values[0],
		'Jersey_Number':row['Jersey_Number'].values[0],
		'Gender':row['Gender'].values[0],
		'Playing_Role':row['Playing Role'].values[0],
		'Teams':teams_of_player,
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
		"AWARDS" :AWARDS,
		'profile_ref':profile_ref[0]


	}

	return data

def main():
	file_loader = FileSystemLoader('./template')
	env = Environment(loader=file_loader)
	template = env.get_template('template.j2')
	
	glob = {'get_profile_ref':get_profile_ref }
	# func_dict = {
    #     "get_profile_ref": get_profile_ref
    # }
	template.globals.update(glob)
    # template.globals.update(func_dict)
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
	# fobj = open('infoandoverview.text', 'w', encoding='utf-8')
	# fobj.write(tewiki+'\n')	
	with open('infoandoverview.txt', 'w', encoding='utf-8') as fobj:
		# row = moviesDF.head(12).tail(1)
		row = moviesDF.loc[moviesDF['Cricinfo_id']==253802]
		text = template.render(getData(row))
		player_name = row["Full Name"].values[0]
	# print(player_name)
	# x = ast.literal_eval(player_name)
	# print(type(x))
	# print(x.keys())
	# for key,vale in x.items():
	# 	print(key)
	# writePage(player_name, text, fobj)
		fobj.write(template.render(getData(row)))
   
	# fobj.write('</mediawiki>')
	# fobj.close()

if __name__ == '__main__':
	main()