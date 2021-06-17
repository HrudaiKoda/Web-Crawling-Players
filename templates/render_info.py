import pickle
from jinja2 import Environment, FileSystemLoader
from google.transliteration import transliterate_text
from googletrans import Translator
from google_trans_new import google_translator  
# from translate import Translator
translator = Translator()
translit = google_translator()

# from anuvaad import Anuvaad
# telugu = Anuvaad('english-telugu')
from deeptranslit import DeepTranslit
trans = DeepTranslit('telugu').transliterate

from genXML import tewiki, writePage

import ast
countries = []

def concate_birth(date):
    if len(date) == 1:
        return date[0]
    elif len(date) == 0:
        return "nan"
    else:
        li = ','.join(date)
        return li.rstrip()
def get_role(role):
    role_map = {
        "Bowler": "బౌలర్",
        "Allrounder": "ఆల్ రౌండర్",
        "Batter": "బ్యాట్స్‌మన్‌",
        "Opening batter": "ఓపెనింగ్ బ్యాట్స్‌మన్‌",
        "Wicketkeeper batter": "వికెట్ కీపర్ బ్యాట్స్‌మన్‌",
        "Top order batter": "టాప్ ఆర్డర్ బ్యాట్స్‌మన్‌",
        "Middle order batter": "మిడిల్ ఆర్డర్ బ్యాట్స్‌మన్",
        "Wicketkeeper": "వికెట్ కీపర్",
        "Bowling allrounder": "బౌలింగ్ ఆల్ రౌండర్",
        "Batting allrounder": "బ్యాటింగ్ ఆల్ రౌండర్"
    }
    if not role in role_map.keys():
        return role
    return role_map[role]

def get_trophy_name(description):
    trophy_translations = {
        "Basil D'Oliveira": "బాసిల్ డి'ఒలివెరా", 
        'World Cup': 'ప్రపంచ కప్', 
        'ICC World Test Champ': 'ఐసిసి ప్రపంచ టెస్ట్ ఛాంపియన్‌షిప్', 
        'Frank Worrell Trophy': 'ఫ్రాంక్ వొరెల్ ట్రోఫీ', 
        'Border-Gavaskar': 'బోర్డర్-గవాస్కర్ ట్రోఫీ', 
        "Men's T20 World Cup": 'టీ20 ప్రపంచ కప్', 
        'The Ashes': 'ది యాషెస్', 
        'World Cup Qualifier': 'ప్రపంచ కప్ క్వాలిఫైయర్', 
        'Chappell-Hadlee': 'చాపెల్-హాడ్లీ', 
        'Trans-Tasman Trophy': 'ట్రాన్స్-టాస్మాన్ ట్రోఫీ', 
        'WCL Championship': 'ప్రపంచ క్రికెట్ లీగ్ ఛాంపియన్‌షిప్', 
        'ICC Champions Trophy': 'ఐసిసి ఛాంపియన్స్ ట్రోఫీ', 
        'The Wisden Trophy': 'ది విస్డెన్ ట్రోఫీ', 
        'Asia Cup': 'ఆసియా కప్'       
    }
    if not description in trophy_translations.keys():
        return getTransliteratedDescription(description)
    return trophy_translations[description]

def get_trophy_names_list(given_trophy_list):
    trophy_list = list(given_trophy_list)
    for i in range(len(trophy_list)):
        trophy_list[i] = get_trophy_name(trophy_list[i])
    return ', '.join(trophy_list)

def get_transliteration_description(description):
    try:
        current_attribute_value = description
        # anu_title = telugu.anuvaad(row.title.values[0])
        deep = trans(current_attribute_value)[0]
        description = deep['pred']
    except:
        try:
            return transliterate_text(test_text, lang_code='te')
        except:
            pass
    return description

def get_translation_description(description):
	return translit.translate(description,lang_tgt='te')

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
    final = []
    date = row.split(",")
    li.append(date[-1])
    year = date[0].split("at")
    li.append(year[-1])
    against = year[0].split("vs")
    li.append(against[-1])
    for i in li:
        final.append(i.strip())
    return final
def get_source(profile_ref,player_name):
    return profile_ref + " " + player_name + " ప్రొఫైల్"

def get_profile_ref(profile_ref, player_name):
    if len(profile_ref) == 0:
        return ''
    return " <ref>[" + profile_ref + " " + player_name + " ప్రొఫైల్]</ref> "


def Batting_role(batting):
    if batting == "Right hand bat":
        return "కుడి చేతి వాటం"
    elif batting == "Left hand bat":
        return "ఎడమ చేతి వాటం"
    else:
        return batting
def interLinks_for_place(birth_place,countries):
    date = []
    for i in birth_place:
        date.append(i.lstrip())
    for i in date:
        if i in countries:
            date.remove(i)
    if len(date) == 0:
        return "nan"
    elif len(date) == 1:
        date = get_translation_description(date)
        date = ast.literal_eval(date)
        return "[["+date[0]+"]]"
    else:
        date = get_translation_description(date)
        date = ast.literal_eval(date)
        li = ']],[['.join(date)
        return "[["+li+"]]"
def Age_translation(age):
    if (age.find('y') != -1 and age.find('d') != -1):
        age = age.replace('y'," సంవత్సరాల")
        age = age.replace('d'," రోజులు")
    elif (age.find('y') != -1):
        age = age.replace('y'," సంవత్సరాలు")
    return age

def translate_height(height):
    if (height.find('ft') != -1 and height.find('in') != -1):
        height = height.replace('ft'," అ.")
        height = height.replace('in'," అం.")
    elif (height.find('ft') != -1):
        height = height.replace('ft'," అడుగులు")
    return height

def Team_translator(teams_of_player):
	li = []
	for i in teams_of_player:
		li.append(get_translation_description(i))
	return li

def check_nulls_for_translation(word):
	if word != 'nan':
		return get_translation_description(word)
	else:
		return 'nan'
def check_nulls_for_transliteration(word):
	if word != 'nan':
		return get_transliteration_description(word)
	else:
		return 'nan'
def getData(row,countries):
	
# transliteration and translation
	
	birth_date = row['Birth_Date'].values[0]
	if birth_date != 'nan':
		birth_date = ast.literal_eval(row['Birth_Date'].values[0])
		birth_date = concate_birth(birth_date)
	birth_date = check_nulls_for_translation(birth_date)
	bith_overview = birth_date.split(",")
	if (bith_overview[0].find('0') != -1):
		bith_overview[0] = bith_overview[0].replace('0','')


	Birth_Place = row['Birth_Place'].values[0]
	if Birth_Place != 'nan':
		Birth_Place = ast.literal_eval(row['Birth_Place'].values[0])
		Birth_Place = interLinks_for_place(Birth_Place,countries)
		# if Birth_Place != 'nan':
		# 	Birth_Place = get_translation_description(Birth_Place)
		# 	Birth_Place = ast.literal_eval(Birth_Place)
	
	team = row['Teams'].values[0]
	if team != 'nan':
		team = ast.literal_eval(row['Teams'].values[0])
		teams_of_player = teams(team,row['Nationality'].values[0])
		teams_of_player = get_translation_description(teams_of_player)
		teams_of_player = ast.literal_eval(teams_of_player)
		
	
	tropies = row["Major trophies"].values[0]
	if tropies != 'nan':
		tropies = ast.literal_eval(row["Major trophies"].values[0])
	AWARDS = row["Awards_telugu"].values[0]
	if AWARDS != 'nan':
		AWARDS = ast.literal_eval(row["Awards_telugu"].values[0])
		
		# AWARDS = Team_translator(AWARDS)

	records = row["Records_telugu"].values[0]
	if records != 'nan':
		records = ast.literal_eval(row["Records_telugu"].values[0])
		# print(recordss)
	# 	# records = Team_translator(records)

	Test_Matches_debut = spliting(row['Test Matches_debut'].values[0])
	ODI_Matches_debut= spliting(row['ODI Matches_debut'].values[0])
	T20I_Matches_debut = spliting(row['T20I Matches_debut'].values[0])
	Test_Matches_last_appearance = spliting(row['Test Matches_last_appearance'].values[0])
	ODI_Matches_last_appearance = spliting(row['ODI Matches_last_appearance'].values[0])
	T20I_Matches_last_appearance = spliting(row['T20I Matches_last_appearance'].values[0])
	profile_ref = ast.literal_eval(row['References'].values[0])
# ##############################
# transliteration and translation
# natinality (translation)
	
# bathing in overview
	batting = Batting_role(row['Batting Style'].values[0])
# debuts
	data = {
		#{%- macro info(title, id, year, genre, actors, duration, country, original_title) -%}
		'Full_Name':get_transliteration_description(row['Full Name'].values[0]),
		'Player_Name':get_transliteration_description(row['Player_Name'].values[0]),
		'Nationality':get_translation_description(row['Nationality'].values[0]).strip(),
		'Born':check_nulls_for_translation(birth_date),
		'Birth_place':Birth_Place,
		'Born_ov':bith_overview,
		'age':Age_translation(row['Age'].values[0]),
		'Died':check_nulls_for_translation(row['Died'].values[0]),
		'Relations':row['Relations'].values[0],
		'career_span':row['career_span'].values[0],
		'Batting_Style':batting,
		# 'info_batting_style':row['Batting Style'].values[0],
		'Bowling_Style':check_nulls_for_transliteration(row['Bowling Style'].values[0]),
		'Height':Age_translation(row['Height'].values[0]),
		'Jersey_Number':row['Jersey_Number'].values[0],
		'Gender':row['Gender'].values[0],
		'Playing_Role':get_role(row['Playing Role'].values[0]),
		'Teams':teams_of_player,
		'testdebutdate':check_nulls_for_translation(Test_Matches_debut[1]),
		'testdebutyear':Test_Matches_debut[0],
		'testdebutagainst':check_nulls_for_translation(Test_Matches_debut[-1]),
		'odidebutdate':check_nulls_for_translation(ODI_Matches_debut[1]),
		'odidebutyear':ODI_Matches_debut[0],
		'odidebutagainst':check_nulls_for_translation(ODI_Matches_debut[-1]),
		'T20Idebutdate':check_nulls_for_translation(T20I_Matches_debut[1]),
		'T20Idebutyear':T20I_Matches_debut[0],
		'T20Idebutagainst':check_nulls_for_translation(T20I_Matches_debut[-1]),
		'lasttestdate':check_nulls_for_translation(Test_Matches_last_appearance[1]),
		'lasttestyear':Test_Matches_last_appearance[0],
		'lasttestagainst':check_nulls_for_translation(Test_Matches_last_appearance[-1]),
		'lastodidate':check_nulls_for_translation(ODI_Matches_last_appearance[1]),
		'lastodiyear':ODI_Matches_last_appearance[0],
		'lastodiagainst':check_nulls_for_translation(ODI_Matches_last_appearance[-1]),
		'lastT20Idate':check_nulls_for_translation(T20I_Matches_last_appearance[1]),
		'lastT20Iyear':T20I_Matches_last_appearance[0],
		'lastT20Iagainst':check_nulls_for_translation(T20I_Matches_last_appearance[-1]),
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
	
	glob = {'get_profile_ref':get_profile_ref,'get_source':get_source,'get_trophy_names_list':get_trophy_names_list,'get_trophy_name':get_trophy_name }
	# func_dict = {
    #     "get_profile_ref": get_profile_ref
    # }
	template.globals.update(glob)
    # template.globals.update(func_dict)
	moviesDF =pickle.load(open('./data/pickle.pkl', 'rb'))
	moviesDF.fillna(value="nan", inplace=True)
	# ids = moviesDF.Cricinfo_id.tolist()
	nations = list(set(moviesDF.Nationality.tolist()))
	countries = nations
	
	# print(countries)
	# ids =ids[3:4] #remove this to generate articles for all movies
	
	# Initiate the file object
	# fobj = open('movies.xml', 'w',encoding="utf-8")
	# fobj.write(tewiki+'\n')
	# primary_text = 'నవంబర్ 05, 1988'
	# x = gs.translate(primary_text, 'te')
	# print(x)
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
		text = template.render(getData(row,countries))
		player_name = row["Full Name"].values[0]
	# print(player_name)
	# x = ast.literal_eval(player_name)
	# print(type(x))
	# print(x.keys())
	# for key,vale in x.items():
	# 	print(key)
	# writePage(player_name, text, fobj)
		fobj.write(text)
   
	# fobj.write('</mediawiki>')
	# fobj.close()

if __name__ == '__main__':
	main()