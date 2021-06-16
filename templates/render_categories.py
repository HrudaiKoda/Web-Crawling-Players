import pickle
import random
import ast
from jinja2 import Environment, FileSystemLoader
import translators as ts
import pandas as pd
from deeptranslit import DeepTranslit
from functools import cmp_to_key
from deep_translator import GoogleTranslator
from google_trans_new import google_translator
from google.transliteration import transliterate_word, transliterate_text

translator = google_translator()
trans = DeepTranslit('telugu').transliterate
all_attributes = []
famous_countries = {
    'India': 'భారతీయ', 
    'Australia': 'ఆస్ట్రేలియా', 
    'England': 'ఇంగ్లాండు', 
    'West Indies': 'వెస్ట్‌ఇండీస్', 
    'Pakistan': 'పాకిస్తాన్', 
    'South Africa': 'దక్షిణాఫ్రికా', 
    'Sri Lanka': 'శ్రీలంక' 
}

translated_names = {
    "Span": "వ్యవధి",
    "Test": "టెస్ట్",
    "ODI": "వన్డే ఇంటర్నేషనల్‌",
    "T20": "టీ20",
    "T20I": "అంతర్జాతీయ టీ20",
    "FC": "ఫస్ట్ క్లాస్",
    "List A": "లిస్ట్ ఏ"
}    

def is_valid_string(attribute_value):
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

def getTransliteratedDescription(description):
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

def getTranslatedDescription(description):
    global translator
    if not is_valid_string(description):
        return description
    try:
        return translator.translate(description, lang_src='en', lang_tgt='te')
    except:
        try:
            return ts.google(query_text=description, from_language='en', to_language='te')
        except:
            try:
                return GoogleTranslator(source='en', target='te').translate(text=description)
            except:
                return description
            
def get_year(given_date):
    if not is_valid_string(given_date):
        return -1
    given_date = ast.literal_eval(given_date)
    if len(given_date) != 2:
        return -1
    try:
        return int(given_date[-1][:5])
    except:
        return -1
    
def get_country_player(nationality, gender):
    global famous_countries
    country_string = getTranslatedDescription(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా క్రికెట్ క్రీడాకారులు" + "]]\n"
    return "[[వర్గం:" + country_string + " క్రికెట్ క్రీడాకారులు" + "]]\n"

def get_country_test_details(nationality, played_test, gender):
    global famous_countries
    if not played_test:
        return ''
    country_string = getTranslatedDescription(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా టెస్ట్ క్రికెట్ క్రీడాకారులు" + "]]\n"
    return "[[వర్గం:" + country_string + " టెస్ట్ క్రికెట్ క్రీడాకారులు" + "]]\n"
    
def get_country_odi_details(nationality, played_ODI, gender):
    global famous_countries
    if not played_ODI:
        return ''
    country_string = getTranslatedDescription(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా వన్డే క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:వన్డే క్రికెట్ క్రీడాకారులు]]\n"
    return "[[వర్గం:" + country_string + " వన్డే క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:వన్డే క్రికెట్ క్రీడాకారులు]]\n"

def get_country_t20_details(nationality, played_t20, gender):
    global famous_countries
    if not played_t20:
        return ''
    t20_f = 'ట్వంటీ-20'
    if nationality != 'India':
        t20_f = 'టీ20'
    country_string = getTranslatedDescription(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా " + t20_f + " క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:ట్వంటీ-20 క్రికెటర్లు]]\n"
    return "[[వర్గం:" + country_string + " " + t20_f + " క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:ట్వంటీ-20 క్రికెటర్లు]]\n"

def get_wk_category(player_role):
    if not player_role.startswith('W'):
        return ''
    return "[[వర్గం:వికెట్ కీపర్లు]]\n"

def getData(row):
    data = {
        #{%- macro get_categories_list(player_role, birth_year, death_year, nationality, gender, played_ODI, played_test, played_t20) -%}
        'birth_year': get_year(row['Birth_Date']),
        'death_year': get_year(row['Death_Date']),
        'nationality': row['Nationality'],
        'gender': row['Gender'],
        'played_ODI' : row['Batting_ODI_Mat'] > 0 or row['Bowling_ODI_Mat'] > 0, 
        'played_test': row['Batting_Test_Mat'] > 0 or row['Bowling_Test_Mat'] > 0, 
        'played_t20': row['Batting_T20I_Mat'] > 0 or row['Bowling_T20I_Mat'] > 0 or row['Batting_T20_Mat'] > 0 or row['Bowling_T20_Mat'] > 0,
        'player_role': row['Playing Role']
	}
    return data

def main():
    global all_attributes
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template('categories.j2')
    
    func_dict = {        
        "get_country_player": get_country_player,
        "get_country_test_details": get_country_test_details,
        "get_country_odi_details": get_country_odi_details,
        "get_country_t20_details": get_country_t20_details,
        "get_wk_category": get_wk_category
    }
    template.globals.update(func_dict)
    
    with open('final_cricket_players_DF.pkl', 'rb') as f:
        cricket_players_DF = pickle.load(f)
        cricket_players_DF.fillna(value="nan", inplace=True)
        ids = cricket_players_DF.Cricinfo_id.tolist()
        all_attributes = cricket_players_DF.columns.tolist()
        ids = [253802]
        with open('categories.txt', 'w') as fobj:
            for i, cricketer_id in enumerate(ids):
                required_player = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id']==cricketer_id]
                for j, row in required_player.iterrows():
                    # print(row)
                    va = template.render(getData(row))
                    fobj.write(va)
                # fobj.write(text)
				# writePage(title, text, fobj)		
				# print(i, title)
				# print(text, '\n')
			# fobj.write('</mediawiki>')

if __name__ == '__main__':
	main()
