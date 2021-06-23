import pickle
from jinja2 import Environment, FileSystemLoader
from deep_translator import GoogleTranslator

from google.transliteration import transliterate_word, transliterate_text
import ast
from googletrans import Translator
from google_trans_new import google_translator  
# from translate import Translator
translator = google_translator()
from deeptranslit import DeepTranslit
trans = DeepTranslit('telugu').transliterate
import pandas as pd
from genXML import tewiki, writePage
import translators as ts

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
        "Batter": "[[బ్యాట్స్‌మన్]]‌",
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
        'World Cup': '[[ప్రపంచ కప్]]', 
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
        'Asia Cup': 'ఆసియా కప్',
		"ICC Women's World Cu" : 'ఐసిసి ఉమెన్స్ ప్రపంచ కప్'     
    }
    if not description in trophy_translations.keys():
        return get_transliteration_description(description)
    return trophy_translations[description]

def get_trophy_names_list(given_trophy_list):
    trophy_list = list(given_trophy_list)
    for i in range(len(trophy_list)):
        trophy_list[i] = get_trophy_name(trophy_list[i])
    return ', '.join(trophy_list)

def get_transliteration_description(description):
    try:
        current_attribute_value = description
        deep = trans(current_attribute_value)[0]
        description = deep['pred']
    except:
        try:
            return transliterate_text(test_text, lang_code='te')
        except:
            pass
    return description

def get_translation_description(description):
    # global translator
    # if isinstance(description, str) and not is_valid_string(description):
    #     return description
    try:
        # print('1')
        return translator.translate(description, lang_src='en', lang_tgt='te')
    except:
        try:
            # print('2')
            return ts.google(query_text=description, from_language='en', to_language='te')
        except:
            try:
                # print('3')
                return GoogleTranslator(source='en', target='te').translate(text=description)
            except:
                return description

def get_nation(nationality):
	return get_translation_description(nationality).strip()

def teams6(tea,Nationality):
    Iteam = []
    NonIteam = []
    li = []
    for i in tea:
        if Nationality in i:
            Iteam.append(i)
        else:
            NonIteam.append(i)
    if len(Iteam) < 7:
        li = Iteam + NonIteam
    else:
        li = Iteam[:6]
    if len(li) < 7:
        return li
    else:
        return li[:6]



def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

def get_teams_string(teams_list,Nationality):
    if not is_valid_string(teams_list):
        return ''
    actual_list = ast.literal_eval(teams_list)
    actual_list = teams6(actual_list,Nationality)
    capitals = {
        'Super 3s': 'సూపర్ ౩స్', 'SC': 'ఎస్.సీ.', 'Glamorgan 2nd': 'గ్లమోర్గన్ 2న్ద్', 
        'HBS': 'హెచ్.బీ.ఎస్.', 'BCCSL': 'బీ.సీ.సీ.ఎస్.ఎల్.', 'Leicestershire 2nd': 'లీసెస్టర్షైర్ 2న్ద్', 
        'CH': 'సీ.హెచ్.', 'ECB': 'ఇ.సీ.బీ.', 'C': 'సీ.', 'Warwickshire 2nd': 'వార్విక్షైర్ 2న్ద్', 
        'UWI': 'యూ.డబల్యూ.ఐ.', 'PINT': 'పి.ఐ.ఎన్.టి.', 'Surrey 2nd': 'సర్రే 2న్ద్', 
        'NZCPA': 'ఎన్.జీ.సీ.పి.ఏ.', 'Lancashire 2nd': 'లాంక్షైర్ 2న్ద్', 
        'Essex 2nd': 'ఎస్సెక్స్ 2న్ద్', 'BCB': 'బీ.సీ.బీ.', '1': '1', 
        'Somerset 2nd': 'సోమర్సెట్ 2న్ద్', 'DVS': 'డి.వీ.ఎస్.', 'XI': 'XI', 
        'Kent 2nd': 'కెంట్ 2న్ద్', "Men's 1": "మెన్'స్ 1", 'KNCB': 'కె.ఎన్.సీ.బీ.', 
        'CA': 'సీ.ఏ.', 'MCA': 'ఎం.సీ.ఏ.', 'VII': 'VII', 'Patriots 1': 'పేట్రియాట్స్ 1', '19': '19', 
        'AJ': 'ఏ.జె.', 'BCA': 'బీ.సీ.ఏ.', 'HCC': 'హెచ్.సీ.సీ.', 'PCA': 'పి.సీ.ఏ.', 'TN': 'టి.ఎన్.', 
        'P': 'పి.', 'UCB-BCB': 'యూ.సీ.బీ.-బీ.సీ.బీ.', 'RR': 'ఆర్.ఆర్.', 'Sussex 2nd': 'సస్సెక్స్ 2న్ద్', 
        'MAF': 'ఎం.ఏ.ఎఫ్.', 'ICBT': 'ఐ.సీ.బీ.టి.', 'DS': 'డి.ఎస్.', 'World-XI': 'వరల్డ్-XI', 'ICL': 'ఐ.సీ.ఎల్.', 
        'Worcestershire 2nd': 'వోర్సెస్టర్షైర్ 2న్ద్', 'XII': 'XII', 'DH': 'డి.హెచ్.', 'VRA': 'వీ.ఆర్.ఏ.', 
        'ICC': 'ఐసీసీ', 'Under-17': 'అండర్ -17', 'VOC': 'వీ.ఓ.సీ.', 'NCA': 'ఎన్.సీ.ఏ.', 
        'MCCU': 'ఎం.సీ.సీ.యూ.', 'IV': 'IV', 'MV': 'ఎం.వీ.', 'Durham 2nd': 'డర్హామ్ 2న్ద్', 'B': 'బీ', 
        'RCA': 'ఆర్.సీ.ఏ.', 'KSCA': 'కె.ఎస్.సీ.ఏ.', 'Northern 2nd': 'నార్తర్న్ 2న్ద్', 'WICB': 'డబల్యూ.ఐ.సీ.బీ.', 
        'FATA': 'ఎఫ్.ఏ.టి.ఏ.', 'DY': 'డి.వై.', 'TNCA': 'టి.ఎన్.సీ.ఏ.', 'NCU': 'ఎన్.సీ.యూ.', 'S': 'ఎస్.', 
        'CPL': 'సీ.పి.ఎల్.', 'YMCA': 'వై.ఎం.సీ.ఏ.', 'Yorkshire 2nd': 'యార్క్షైర్ 2న్ద్', 'T20': 'టి20', 'PJ': 'పి.జె.', 
        'Patriots 2': 'పేట్రియాట్స్ 2', 'UCCE': 'యూ.సీ.సీ.ఇ.', 'Middlesex 2nd': 'మిడిల్‌సెక్స్ 2న్ద్', 'Under-23': 'అండర్-23', 
        'D.A.V': 'డి.ఏ.వీ.', 'HDG': 'హెచ్.డి.జీ.', 'CC': 'సీ.సీ.', 'MAS': 'ఎం.ఏ.ఎస్.', 'ACB': 'ఏ.సీ.బీ.', 'UAE': 'యూ.ఏ.ఇ.', 
        'Under 19': 'అండర్ 19', '2': '2', 'MC': 'ఎం.సీ.', 'AJK': 'ఏ.జె.కె.', 'CI': 'సీ.ఐ.', 'TUKS': 'టి.యూ.కె.ఎస్.', 
        'Pakhtunkhwa 2nd': 'పఖ్తున్ఖ్వా 2న్ద్', 'Sindh 2nd': 'సింధ్ 2న్ద్', 'DOHS': 'డి.ఓ.హెచ్.ఎస్.', 'TUTI': 'టి.యూ.టి.ఐ.', 
        'Gloucestershire 2nd': 'గ్లౌసెస్టర్షైర్ 2న్ద్', 'Hampshire 2nd': 'హాంప్‌షైర్ 2న్ద్', 'D': 'డి.', 'Derbyshire 2nd': 'డెర్బీషైర్ 2న్ద్', 
        'MCCU 2nd': 'ఎం.సీ.సీ.యూ. 2న్ద్', 'A': 'ఏ.', 'VB': 'వీ.బీ.', 'Nottinghamshire 2nd': 'నాటింగ్హామ్షైర్ 2న్ద్', 
        'Northamptonshire 2nd': 'నార్తాంప్టన్షైర్ 2న్ద్', 'KZKC': 'కె.జీ.కె.సీ.', 'DJ': 'డి.జె.', 
        'Under-11s': 'అండర్ -11స్', 'Under-22s': 'అండర్ -22స్', 'Under-17s': 'అండర్ -17స్', 'Under': 'అండర్', 
        'Under-15s': 'అండర్ -15స్', 'Under-25s': 'అండర్ -25స్', 'Under-20s': 'అండర్ -20స్', 'Under-21s': 'అండర్ -21స్', 
        'Under-13s': 'అండర్ -13స్', 'Under-14s': 'అండర్ -14స్', 'Under-18s': 'అండర్ -18స్', 'Under-24s': 'అండర్ -24స్', 
        'Under-19s': 'అండర్ -19స్', 'Under-16s': 'అండర్ -16స్', 'Under-23s': 'అండర్ -23స్' 
    }
    translated_output = ""
    twos = [ke for ke in capitals.keys() if len(ke.split(" ")) == 2]
    ones = [ke for ke in capitals.keys() if len(ke.split(" ")) == 1]
    try:
        for j in range(len(actual_list)):
            # print("Actual team name", actual_list[j])
            tokenized = actual_list[j].split(" ")
            for i in range(len(tokenized)-1):
                cur = tokenized[i] + " " + tokenized[i+1]
                if cur in twos:
                    t = capitals[cur].split(" ")
                    tokenized[i] = t[0]
                    tokenized[i+1] = t[1]
            for i in range(len(tokenized)):
                if tokenized[i] in ones:
                    tokenized[i] = capitals[tokenized[i]]
            actual_list[j] = ' '.join(tokenized)
            # print("Updated team name", actual_list[j])
        translated_output = get_transliteration_description(
            ', '.join(actual_list))      
        return translated_output
    except Exception as e:
        print("Level 2", e)
        try:
            translated_output = get_translation_description(actual_list)
            if ']]' in translated_output:
                translated_output = translated_output.replace(']]', ']')
            actual_list = list(ast.literal_eval(translated_output))
            return ', '.join(actual_list)
        except Exception as f:
            print("Level 3", f)
            try:
                translated_output = get_translation_description(
                    ', '.join(actual_list))
                return translated_output
            except Exception as g:
                print("Final level", g)
                return ', '.join(actual_list)

def get_awards(teams_list):
    if not is_valid_string(teams_list):
        return ''
    actual_list = ast.literal_eval(teams_list)
    capitals = {
        'OBE':'ఓ.బీ.ఇ.','july':"జూలై", 'Year':'ఇయర్','year':'ఇయర్','on':'ఆన్','Dec':'డిసెంబర్', 'the':'ది','The':"ది", 'MBE':'ఎం.బీ.ఇ.', 'SASSSA':'ఎస్.ఏ.ఎస్.ఎస్.ఎస్.ఏ.', 
	'SHIELD':'ఎస్.హెచ్.ఐ.ఇ.ఎల్.డి.', 'ECB':'ఇ.సీ.బీ.', 'SACOS':'ఎస్.ఏ.సీ.ఓ.ఎస్.', 'N.C.C':'ఎన్.సీ.సీ.', 
	'MdeS':'ఎం.డి.ఇ.ఎస్.', 'NtlB':'ఎన్.టి.ఎల్.బీ.', '(ICC':'(ఐ.సీ.సీ.', 'ICC':'ఐ.సీ.సీ.', 'HS':'హెచ్.ఎస్.', 
	'(ET':'(ఇ.టి.', 'SA':'ఎస్.ఏ.', 'BHS':'బీ.హెచ్.ఎస్.', 'UNISA':'యూ.ఎన్.ఐ.ఎస్.ఏ.', 'HH':'హెచ్.హెచ్.', 
	'UOFS':'యూ.ఓ.ఎఫ్.ఎస్.', 'u-19s':'అండర్ -19స్', 'LG':'ఎల్.జీ.', 'WP':'డబల్యూ.పి.', 'MR':'ఎం.ఆర్.', 
	'R':'ఆర్.', 'AM':'ఏ.ఎం.', 'UAE':'యూ.ఏ.ఇ.', 'FC':'ఎఫ్.సీ.', 'CWS':'సీ.డబల్యూ.ఎస్.', 'B':'బీ.', 
	'RAU':'ఆర్.ఏ.యూ.', 'CBC':'సీ.బీ.సీ.', '(HS':'(హెచ్.ఎస్.', 'XI':'XI', 'SACD':'ఎస్.ఏ.సీ.డి.', 'EG':'ఇ.జీ.', 
	'(EP/WP/Bdr/Ess/WAus/SA':'(ఇ.పి./డబల్యూ.పి./బీ.డి.ఆర్./ఇ.ఎస్.ఎస్./డబల్యూ.ఏ.యూ.ఎస్./ఎస్.ఏ.', 
	'WPB':'డబల్యూ.పి.బీ.', 'UWC':'యూ.డబల్యూ.సీ.', 'Tvl':'టి.వీ.ఎల్.', 'UPE':'యూ.పి.ఇ.', 'ET':'ఇ.టి.', 
	'CBE':'సీ.బీ.ఇ.', '(GW':'(జీ.డబల్యూ.', 'SHEFFIELD':'ఎస్.హెచ్.ఇ.ఎఫ్.ఎఫ్.ఐ.ఇ.ఎల్.డి.', 'SACS':'ఎస్.ఏ.సీ.ఎస్.', 
	'(FA':'(ఎఫ్.ఏ.', 'SASA':'ఎస్.ఏ.ఎస్.ఏ.', 'FA':'ఎఫ్.ఏ.', ' v ':' వర్సెస్ ', 'Under-19s':'అండర్ -19స్', 
	'Under':'అండర్', 'EL':'ఇ.ఎల్.', 'BBC':'బీ.బీ.సీ.', 'FR':'', 'GO':'ఎఫ్.ఆర్.', 'MTN':'ఎం.టి.ఎన్.', 'PCA':'పి.సీ.ఏ.', 
	'S.F.':'ఎస్.ఎఫ్.', 'PE':'పి.ఇ.', 'SAARC':'ఎస్.ఏ.ఏ.ఆర్.సీ.', 'GW':'జీ.డబల్యూ.', 'OFS':'ఓ.ఎఫ్.ఎస్.', 'ODI':'ఓ.డి.ఐ.', 
	'Surrey':'సర్రే', 'Under-17s':'అండర్ -17స్', 'Derbyshire':'డెర్బీషైర్', 'A':'ఏ.', 'KS':'కె.ఎస్.', 'S':'ఎస్.', 
	'Lancashire':'లాంక్షైర్', 'Leicestershire':'లీసెస్టర్షైర్', 'NT':'ఎన్.టి.', 'SRdeS':'ఎస్.ఆర్.డి.ఇ.ఎస్.', 
	'T20I':'టి20ఐ', 'GRADE':'జీ.ఆర్.ఏ.డి.ఇ.', 'NBC':'ఎన్.బీ.సీ.', 'I':'ఐ.', 'EP':'ఇ.పి.', 'CC':'సీ.సీ.', 'DR':'డి.ఆర్.', 'St':'సెయింట్' 
    }
    translated_output = ""
    twos = [ke for ke in capitals.keys() if len(ke.split(" ")) == 2]
    ones = [ke for ke in capitals.keys() if len(ke.split(" ")) == 1]
    try:
        for j in range(len(actual_list)):
            # print("Actual team name", actual_list[j])
            tokenized = actual_list[j].split(" ")
            for i in range(len(tokenized)-1):
                cur = tokenized[i] + " " + tokenized[i+1]
                if cur in twos:
                    t = capitals[cur].split(" ")
                    tokenized[i] = t[0]
                    tokenized[i+1] = t[1]
            for i in range(len(tokenized)):
                if tokenized[i] in ones:
                    tokenized[i] = capitals[tokenized[i]]
            actual_list[j] = ' '.join(tokenized)
            # print("Updated team name", actual_list[j])
        translated_output = get_transliteration_description(
            ', '.join(actual_list))      
        return translated_output
    except Exception as e:
        print("Level 2", e)
        try:
            translated_output = get_translation_description(actual_list)
            if ']]' in translated_output:
                translated_output = translated_output.replace(']]', ']')
            actual_list = list(ast.literal_eval(translated_output))
            return ', '.join(actual_list)
        except Exception as f:
            print("Level 3", f)
            try:
                translated_output = get_translation_description(
                    ', '.join(actual_list))
                return translated_output
            except Exception as g:
                print("Final level", g)
                return ', '.join(actual_list)

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
    # if not is_valid_string(birth_place):
    #     return ''
    date = []
    place = []
    # birth_place = ast.literal_eval(birth_place)
    for i in birth_place:
        date.append(i.strip())
    for i in date:
        if i in countries:
            date.remove(i)
    for i in date:
        place.append(get_translation_description(i))
    if len(place) == 0:
        return "nan"
    elif len(place) == 1:
        # date = getTranslatedDescription(date)
        # date = ast.literal_eval(date)
        return "[["+place[0]+"]]"
    else:
        # date = getTranslatedDescription(date)
        # date = ast.literal_eval(date)
        li = ']],[['.join(place)
        return "[["+li+"]]"

def Age_translation(age):
    if (age.find('y') != -1 and age.find('d') != -1):
        age = age.replace('y'," సంవత్సరాల")
        age = age.replace('d'," రోజులు")
    elif (age.find('y') != -1):
        age = age.replace('y'," సంవత్సరాలు")
    return age

def translate_height(height):
    # if not is_valid_string(height):
    #     return ''
    if (height.find('ft') != -1 and height.find('in') != -1):
        height = height.replace('ft',"")
        height = height.replace('in',"")
        height = height.split(' ')
    elif(height.find('ft') != -1):
        height = height.replace('ft',"")
        height = list(height)
        
    
    return height
		
def translate_death(row):
    # if not is_valid_string(row):
    #     return ''
    if ', (' in row:
        deadth = row.split(", (")
        if 'aged' in deadth[1]:
            deadth[1] = deadth[1].replace('aged','(వయస్సు :')
            if (deadth[1].find('y') != -1 and deadth[1].find('d') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాల")
                deadth[1] = deadth[1].replace('d'," రోజులు")
            elif (deadth[1].find('y') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాలు")
            deadth[0] = get_transliteration_description(deadth[0]).strip()
        return ''.join(deadth)
    elif ' (' in row:
        deadth = row.split(" (")
        if 'aged' in deadth[1]:
            deadth[1] = deadth[1].replace('aged','(వయస్సు :')
            if (deadth[1].find('y') != -1 and deadth[1].find('d') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాల")
                deadth[1] = deadth[1].replace('d'," రోజులు")
            elif (deadth[1].find('y') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాలు")
            deadth[0] = get_transliteration_description(deadth[0]).strip()
        return ''.join(deadth)
    elif '(aged null)' in row:
        deadth = row.replace("(aged null)","")
        return get_transliteration_description(deadth)
    else:
        return get_transliteration_description(row)
# def Team_translator(teams_of_player):
# 	li = []
# 	for i in teams_of_player:
# 		li.append(get_translation_description(i))
# 	return li
def conv(t):
    t = ast.literal_eval(t)
    t = get_translation_description(t)
    return ast.literal_eval(t)

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

	# death_date = row['Death_Date'].values[0]
	# if death_date != 'nan':
    # print(birth_date)
	# 	death_date = ast.literal_eval(row['Death_Date'].values[0])
	# 	death_date = concate_birth(death_date)
	# death_date = check_nulls_for_translation(death_date)

	Birth_Place = row['Birth_Place'].values[0]
	if Birth_Place != 'nan':
		Birth_Place = ast.literal_eval(row['Birth_Place'].values[0])
		Birth_Place = interLinks_for_place(Birth_Place,countries)
	deadth = row['Died'].values[0]	
	if deadth != 'nan':
		deadth = translate_death(row['Died'].values[0])
	# Death_Place = row['Death_Place'].values[0]
	# if Death_Place != 'nan':
	# 	Death_Place = ast.literal_eval(row['Death_Place'].values[0])
	# 	# Death_Place = interLinks_for_place(Death_Place,countries)


	# team = row['Teams'].values[0]
	# if team != 'nan':
	# 	team = ast.literal_eval(team)
	# 	teams_of_player = teams(team,row['Nationality'].values[0])
	# 	teams_of_player = get_translation_description(teams_of_player)
	# 	if (teams_of_player.find(']]') != -1):
	# 		teams_of_player = teams_of_player.replace(']]',"']")
	# 	teams_of_player = ast.literal_eval(teams_of_player)
	print(birth_date)
	
	tropies = row["Major trophies"].values[0]
	if tropies != 'nan':
		tropies = ast.literal_eval(row["Major trophies"].values[0])
	
	AWARDS = row["AWARDS"].values[0]
	if AWARDS != 'nan':
		AWARDS = get_awards(AWARDS)

	# records = row["Records_telugu"].values[0]
	# if records != 'nan':
	# 	records = ast.literal_eval(row["Records_telugu"].values[0])
	
	Test_Matches_debut = spliting(row['Test Matches_debut'].values[0])
	ODI_Matches_debut= spliting(row['ODI Matches_debut'].values[0])
	T20I_Matches_debut = spliting(row['T20I Matches_debut'].values[0])
	Test_Matches_last_appearance = spliting(row['Test Matches_last_appearance'].values[0])
	ODI_Matches_last_appearance = spliting(row['ODI Matches_last_appearance'].values[0])
	T20I_Matches_last_appearance = spliting(row['T20I Matches_last_appearance'].values[0])
	profile_ref = ast.literal_eval(row['References'].values[0])

	batting = Batting_role(row['Batting Style'].values[0])
# debuts
	data = {
		'Full_Name':get_transliteration_description(row['Full Name'].values[0]),
		'Player_Name':get_transliteration_description(row['Player_Name'].values[0]),
		'Nationality':row['Nationality'].values[0].strip(),
		'Born':birth_date,
		'Birth_place':Birth_Place,
		'Born_ov':bith_overview,
		'age':Age_translation(row['Age'].values[0]),
		'Died':deadth,
		'Relations':row['Relations'].values[0],
		'career_span':row['career_span'].values[0],
		'Batting_Style':check_nulls_for_transliteration(row['Batting Style'].values[0]),
		'Bowling_Style':check_nulls_for_transliteration(row['Bowling Style'].values[0]),
		'Height':translate_height(row['Height'].values[0]),
		'Jersey_Number':row['Jersey_Number'].values[0],
		'Gender':row['Gender'].values[0],
		'Playing_Role':get_role(row['Playing Role'].values[0]),
		'Teams':row['Teams'].values[0],
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
		# 'Records':records,
		"AWARDS" :AWARDS,
		'profile_ref':profile_ref[0]


	}

	return data

def main():
	file_loader = FileSystemLoader('./template')
	env = Environment(loader=file_loader)
	template = env.get_template('template.j2')
	
	glob = {'get_profile_ref':get_profile_ref,'get_source':get_source,'get_trophy_names_list':get_trophy_names_list,'get_trophy_name':get_trophy_name,'conv':conv,'get_teams_string':get_teams_string,'get_nation':get_nation }
	template.globals.update(glob)
	moviesDF =pickle.load(open('./data/pickle.pkl', 'rb'))
	moviesDF.fillna(value="nan", inplace=True)
	ids = moviesDF.Cricinfo_id.tolist()
	nations = list(set(moviesDF.Nationality.tolist()))
	countries = nations
	# li = []
	# for i in countries:
	# 	print(type(i))
	# 	i = ast.literal_eval(i)
	# 	print(type(i))
		# li.append(i[-1])
	# print(li)
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
		row = moviesDF.loc[moviesDF['Cricinfo_id']==53747]
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