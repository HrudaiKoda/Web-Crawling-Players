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

bat_stat_order = {
    "Mat": 1,
    "Inns": 2,
    "NO": 5,
    "Runs": 3,
    "HS": 4,
    "Ave": 6,
    "100s": 9,
    "50s": 10,
    "Ct": 13,
    "St": 14,
    "BF": 8,
    "SR": 7,
    "4s": 11,
    "6s": 12
}

bowl_stat_order = {
    "Mat": 1,
    "Inns": 2,
    "Balls": 3,
    "Runs": 4,
    "Wkts": 5,
    "BBI": 6,
    "BBM": 7,
    "Ave": 8,
    "Econ": 9,
    "SR": 10,
    "4w": 11,
    "5w": 12,
    "10w": 13
}

translated_names = {
    'rn': "పరుగులు",
    'bta': "సగటు బ్యాటింగ్ స్కోరు", 
    'st': "స్టంపింగ్స్", 
    'fw': "ఐదు వికెట్ మ్యాచ్‌లు", 
    'mt': "మ్యాచ్‌లు", 
    'bbi': "ఉత్తమ బౌలింగ్ ఇన్నింగ్స్", 
    'hs': "అత్యధిక స్కోరు", 
    'wk': "వికెట్లు", 
    'ct': "క్యాచ్‌లు", 
    'bwa': "సగటు బౌలింగ్ స్కోరు", 
    'sp': "వ్యవధి", 
    "Mat": "మ్యాచ్‌లు",
    "Inns": "ఇన్నింగ్స్",
    "NO": "నాట్-అవుట్స్",
    "Runs": "పరుగులు",
    "HS": "అత్యధిక స్కోరు",
    "Ave": "సగటు బ్యాటింగ్ స్కోరు",
    "Avg": "సగటు బ్యాటింగ్ స్కోరు",
    "100s": "శతకాలు",
    "50s": "అర్ధ శతకాలు",
    "Ct": "క్యాచ్‌లు",
    "St": "స్టంపింగ్స్",
    "BF": "ఎదురుకున్న బంతులు",
    "SR": "స్ట్రైక్ రేట్",
    "0s": "జీరోలు",
    "4s": "ఫోర్లు",
    "6s": "సిక్సలు",
    "Balls": "బంతులు",
    "Wkts": "వికెట్లు",
    "BBI": "ఉత్తమ బౌలింగ్ ఇన్నింగ్స్",
    "BBM": "ఉత్తమ బౌలింగ్ మ్యాచ్",
    "Econ": "ఎకానమీ",
    "4w": "నాలుగు వికెట్ మ్యాచ్‌లు",
    "5w": "ఐదు వికెట్ మ్యాచ్‌లు",
    "10w": "పది వికెట్ మ్యాచ్‌లు",
    "Span": "వ్యవధి",
    "Test": "టెస్ట్",
    "ODI": "వన్డే ఇంటర్నేషనల్‌",
    "T20": "టీ20",
    "T20I": "అంతర్జాతీయ టీ20",
    "FC": "ఫస్ట్ క్లాస్",
    "List A": "లిస్ట్ ఏ"
}    

def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
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
    if isinstance(description, str) and not is_valid_string(description):
        return description
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

def get_trophy_name(description):
    if not is_valid_string(description):
        return ''
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

def get_nationality(nation):
    nation = nation.strip()
    nations = {
        'Pakistan': 'పాకిస్తాన్', 
        'Japan': 'జపాన్', 
        'Canada': 'కెనడా', 
        'India': 'భారతదేశం', 
        'Belgium': 'బెల్జియం', 
        'P.N.G.': 'పాపువా న్యూ గిని', 
        'Oman': 'ఒమన్', 
        'Austria': 'ఆస్ట్రియా', 
        'West Indies': 'వెస్ట్ ఇండీస్', 
        'Kuwait': 'కువైట్', 
        'E&C Africa': 'ఇ & సి ఆఫ్రికా', 
        'Bermuda': 'బెర్ముడా', 
        'Fiji': 'ఫిజి', 
        'Chile': 'చిలీ', 
        'Denmark': 'డెన్మార్క్', 
        'Malaysia': 'మలేషియా', 
        'Bangladesh': 'బంగ్లాదేశ్', 
        'Germany': 'జర్మనీ', 
        'U.A.E.': 'యునైటెడ్ అరబ్ ఎమిరేట్స్', 
        'Hong Kong': 'హాంగ్ కొంగ', 
        'Malta': 'మాల్టా',
        'Zimbabwe': 'జింబాబ్వే', 
        'Scotland': 'స్కాట్లాండ్', 
        'Singapore': 'సింగపూర్', 
        'Sri Lanka': 'శ్రీలంక', 
        'England': 'ఇంగ్లాండ్', 
        'Gibraltar': 'గిబ్రాల్టర్', 
        'Argentina': 'అర్జెంటీనా', 
        'Uganda': 'ఉగాండా', 
        'Italy': 'ఇటలీ', 
        'Kenya': 'కెన్యా', 
        'Nepal': 'నేపాల్', 
        'Netherlands': 'నెదర్లాండ్స్', 
        'South Africa': 'దక్షిణ ఆఫ్రికా', 
        'Ireland': 'ఐర్లాండ్', 
        'U.S.A.': 'యునైటెడ్ స్టేట్స్ ఆఫ్ అమెరికా', 
        'Afghanistan': 'ఆఫ్ఘనిస్తాన్', 
        'Cayman Is': 'కేమెన్ ఐలాండ్స్', 
        'New Zealand': 'న్యూజీలాండ్', 
        'Namibia': 'నమీబియా', 
        'Australia': 'ఆస్ట్రేలియా'
    }
    if not nation in nations.keys():
        return ''
    return nations[nation]


def get_trophy_names_list(given_trophy_list):
    if not is_valid_string(given_trophy_list):
        return ''
    trophy_list = list(given_trophy_list)
    for i in range(len(trophy_list)):
        if trophy_list[i] == 'World Cup':
            trophy_list[i] = '[[' + get_trophy_name(trophy_list[i]) + ']]'
        else:
            trophy_list[i] = get_trophy_name(trophy_list[i])
    return ', '.join(trophy_list)

def get_matches_ref(all_ref, player_name):
    if not is_valid_string(all_ref):
        return ''
    required_ref = [r for r in all_ref if "matches" in r]
    if len(required_ref) == 0:
        return ''
    return "<ref>[" + required_ref[0] + " " + player_name.strip() + " మ్యాచ్‌లు]</ref>"
    
def get_stats_ref(all_ref, player_name):
    if not is_valid_string(all_ref):
        return ''
    required_ref = [r for r in all_ref if "stats" in r]
    if len(required_ref) == 0:
        return ''
    return "<ref>[" + required_ref[0] + " " + player_name.strip() + " గణాంకాలు]</ref>"
    
def stat_value(attribute_name, attribute_value):
    # print(attribute_name, attribute_value)
    if str(attribute_value) == "" or str(attribute_value) == "nan" or attribute_value == None:
        # print(attribute_name, attribute_value, '1')
        return "-"
    if "hs" in attribute_name.lower() or "bbi" in attribute_name.lower() or "BBM" in attribute_name or "span" in attribute_name.lower() or attribute_name == 'sp':
        return attribute_value
    if int(float(attribute_value)) < 0:
        # print(attribute_name, attribute_value, '2')
        return "-"
    return attribute_value

def bat_comparator(a, b):
    global bat_stat_order
    if bat_stat_order[a] > bat_stat_order[b]:
        return 1
    return -1
    
def get_bat_atts_sorted(bat_stats_list):
    return sorted(bat_stats_list, key=cmp_to_key(bat_comparator))

def bowl_comparator(a, b):
    global bowl_stat_order
    if bowl_stat_order[a] > bowl_stat_order[b]:
        return 1
    return -1
    
def get_bowl_atts_sorted(bowl_stats_list):
    return sorted(bowl_stats_list, key=cmp_to_key(bowl_comparator))   
    
def print_names(li):
    return (li)

def get_teams_string(teams_list):
    if not is_valid_string(teams_list):
        return ''
    actual_list = ast.literal_eval(teams_list)
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
        translated_output = getTransliteratedDescription(
            ', '.join(actual_list))      
        return translated_output
    except Exception as e:
        print("Level 2", e)
        try:
            translated_output = getTranslatedDescription(actual_list)
            if ']]' in translated_output:
                translated_output = translated_output.replace(']]', ']')
            actual_list = list(ast.literal_eval(translated_output))
            return ', '.join(actual_list)
        except Exception as f:
            print("Level 3", f)
            try:
                translated_output = getTranslatedDescription(
                    ', '.join(actual_list))
                return translated_output
            except Exception as g:
                print("Final level", g)
                return ', '.join(actual_list)

def get_role(role):
    if not is_valid_string(role):
        return ''
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
    
def shuffle_list(given_list):
    result = list(given_list)
    random.shuffle(result)
    return result


def batting_description_func(first_word, gender_pronoun_2, num1, num2):
    if num1 <= 0 and num2 <= 0:
        return ''
    if num1 > 0 and num2 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు స్కోరు ' + str(num1) + ', స్ట్రైక్ రేట్ ' + str(num2) + '. ')
    elif num1 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు స్కోరు ' + str(num1) + '. ')
    return (first_word + ' ' + gender_pronoun_2 + ' స్ట్రైక్ రేట్ ' + str(num2) + '. ')


def bowling_description_func(first_word, gender_pronoun_2, num1, num2):
    if num1 <= 0 and num2 <= 0:
        return ''
    if num1 > 0 and num2 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు బౌలింగ్ స్కోరు ' + str(num1) + ', ఎకానమీ రేట్ ' + str(num2) + '. ')
    elif num1 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు బౌలింగ్ స్కోరు ' + str(num1) + '. ')
    return (first_word + ' ' + gender_pronoun_2 + ' ఎకానమీ రేట్ ' + str(num2) + '. ')


def opening_sentence(first_word, player_name, num1, num2, has_played):
    if num1 <= 0 and num2 <= 0:
        return ''
    if num1 > 0 and num2 > 0:
        return (first_word + ' ' + player_name + ' ' + str(num1) + ' మ్యాచ్‌లు, ' + str(num2) + ' ఇన్నింగ్స్‌లలో ' + has_played + '. ')
    elif num1 > 0:
        return (first_word + ' ' + player_name + ' ' + str(num1) + ' మ్యాచ్‌లు ' + has_played + '. ')
    return (first_word + ' ' + player_name + ' ' + str(num2) + ' ఇన్నింగ్స్‌లలో ' + has_played + '. ')


def batting_sent1(gender_pronoun_1, sum_batting_100s, sum_batting_50s, has_done):
    if sum_batting_100s <= 0 and sum_batting_50s <= 0:
        return ''
    if sum_batting_100s > 0 and sum_batting_50s > 0:
        return ('అన్ని ఫార్మాట్లు కలిపి ' + gender_pronoun_1 + ' ' + str(sum_batting_100s) + ' శతకాలు, ' + str(sum_batting_50s) + ' అర్ధ శతకాలు ' + has_done + '. ')
    elif sum_batting_100s > 0:
        return ('అన్ని ఫార్మాట్లు కలిపి ' + gender_pronoun_1 + ' ' + str(sum_batting_100s) + ' శతకాలు ' + has_done + '. ')
    return ('అన్ని ఫార్మాట్లు కలిపి ' + gender_pronoun_1 + ' ' + str(sum_batting_50s) + ' అర్ధ శతకాలు ' + has_done + '. ')


def bowling_sent1(gender_pronoun_1, sum_bowling_balls, has_done, sum_wickets, has_taken):
    if sum_bowling_balls <= 0 and sum_wickets <= 0:
        return ''
    if sum_bowling_balls > 0 and sum_wickets > 0:
        return ('తన కెరీర్ లో, ' + gender_pronoun_1 + ' మొత్తం ' + str(sum_bowling_balls) + ' బంతులు (' + str(sum_bowling_balls//6) + ' ఓవర్లు) బౌలింగ్ చేసి, ' + str(sum_wickets) + ' వికెట్లు ' + has_taken + '. ')
    elif sum_bowling_balls > 0:
        return ('తన కెరీర్ లో, ' + gender_pronoun_1 + ' మొత్తం ' + str(sum_bowling_balls) + ' బంతులు (' + str(sum_bowling_balls//6) + ' ఓవర్లు) బౌలింగ్ ' + has_done + '. ')
    return ('తన కెరీర్ లో ' + str(sum_wickets) + ' వికెట్లు ' + has_taken + '. ')


def bowling_sent2(gender_pronoun_2, gender_pronoun_1, bowling_10w_test, bowling_10w_FC, has_taken):
    if bowling_10w_test <= 0 and bowling_10w_FC <= 0:
        return ''
    if bowling_10w_test > 0 and bowling_10w_FC > 0:
        return (gender_pronoun_2 + ' కెరీర్లో, ' + gender_pronoun_1 + ' ' + str(bowling_10w_test) + ' టెస్ట్ మ్యాచ్లలో, ' + str(bowling_10w_FC) + ' ఫస్ట్ క్లాస్ మ్యాచ్లలో 10 వికెట్లు ' + has_taken + '. ')
    elif bowling_10w_test > 0:
        return (gender_pronoun_2 + ' కెరీర్లో, ' + gender_pronoun_1 + ' ' + str(bowling_10w_test) + ' టెస్ట్ మ్యాచ్లలో 10 వికెట్లు ' + has_taken + '. ')
    return (gender_pronoun_2 + ' కెరీర్లో, ' + gender_pronoun_1 + ' ' + str(bowling_10w_FC) + ' ఫస్ట్ క్లాస్ మ్యాచ్లలో 10 వికెట్లు ' + has_taken + '. ')

def get_translation(word, prefix_string):
    global translated_names
    if not is_valid_string(word):
        return ''
    if not word in translated_names.keys():
        return getTranslatedDescription(word)
    if word == "SR":
        if prefix_string == 'Batting_':
            return translated_names[word]
        return "బౌలింగ్ స్ట్రైక్ రేట్"
    if word == "Ave":
        if prefix_string == 'Batting_':
            return translated_names[word]
        return "సగటు బౌలింగ్ స్కోరు"
    return translated_names[word]

def null_check(given_list, given_att):
    for element in given_list:
        if '_' + element + '_' in given_att:
            return True
    return False

def can_be_considered_1(attributes, prop_name, row, curr_att):
    req_attrs = [a for a in attributes if '_' + prop_name + '_' in a]
    req_list = [a for a in req_attrs if (isinstance(row[a], str) and is_valid_string(row[a])) or ((not isinstance(row[a], str)) and stat_value(a, row[a]) != "-")]
    valids_count = len(req_list)
    return valids_count != 0

def can_be_considered_2(attributes, prop_name, row, curr_att, other_list):
    req_attrs = [a for a in attributes if prop_name in a and null_check(other_list, a)]
    req_list = [a for a in req_attrs if (isinstance(row[a], str) and is_valid_string(row[a])) or ((not isinstance(row[a], str)) and stat_value(a, row[a]) != "-")]
    valids_count = len(req_list)
    return valids_count != 0


def get_batting_info(row):
    global all_attributes
    bat_attributes = [att for att in all_attributes if "Batting_" in att and (
        not "_Ct" in att) and (not "_St" in att)]
    batting_format_names = []
    batting_stat_names = []
    batting_details = {}
    # print(row['Batting_T20_Mat'])
    
    for att in bat_attributes:
        curr_att = att.split('_')
        # print(curr_att)
        if can_be_considered_1(bat_attributes, curr_att[1], row, curr_att):
            batting_format_names.append(curr_att[1])
    for att in bat_attributes:
        curr_att = att.split('_')
        # print(curr_att)
        if can_be_considered_2(bat_attributes, curr_att[2], row, curr_att, batting_format_names):
            batting_stat_names.append(curr_att[2])

    batting_format_names = list(set(batting_format_names))
    batting_stat_names = get_bat_atts_sorted(list(set(batting_stat_names)))

    for format_name in batting_format_names:
        for stat_name in batting_stat_names:
            attribute_name = "Batting_" + format_name + "_" + stat_name
            batting_details[attribute_name] = row[attribute_name]
    return batting_format_names, batting_stat_names, batting_details


def get_bowling_info(row):
    global all_attributes
    bowl_attributes = [att for att in all_attributes if "Bowling_" in att]
    bowling_format_names = []
    bowling_stat_names = []
    bowling_details = {}

    for att in bowl_attributes:
        curr_att = att.split('_')
        if can_be_considered_1(bowl_attributes, curr_att[1], row, curr_att):
            bowling_format_names.append(curr_att[1])
    for att in bowl_attributes:
        curr_att = att.split('_')            
        if can_be_considered_2(bowl_attributes, curr_att[2], row, curr_att, bowling_format_names):
            bowling_stat_names.append(curr_att[2])

    bowling_format_names = list(set(bowling_format_names))
    bowling_stat_names = get_bowl_atts_sorted(list(set(bowling_stat_names)))

    for format_name in bowling_format_names:
        for stat_name in bowling_stat_names:
            if stat_name == "10w" and not format_name in ["Test", "FC"]:
                continue
            attribute_name = "Bowling_" + format_name + "_" + stat_name
            bowling_details[attribute_name] = row[attribute_name]
    return bowling_format_names, bowling_stat_names, bowling_details


def get_fielding_info(row):
    global all_attributes
    field_attributes = [att for att in all_attributes if "Batting_" in att and (
        "_Ct" in att or "_St" in att or "Mat" in att or "Inns" in att)]
    fielding_format_names = []
    fielding_stat_names = []
    fielding_details = {}

    for att in field_attributes:
        curr_att = att.split('_')
        if can_be_considered_1(field_attributes, curr_att[1], row, curr_att):
            fielding_format_names.append(curr_att[1])
    for att in field_attributes:
        curr_att = att.split('_')            
        if can_be_considered_2(field_attributes, curr_att[2], row, curr_att, fielding_format_names):
            fielding_stat_names.append(curr_att[2])

    fielding_format_names = list(set(fielding_format_names))
    fielding_stat_names = get_bat_atts_sorted(list(set(fielding_stat_names)))

    for format_name in fielding_format_names:
        for stat_name in fielding_stat_names:
            attribute_name = "Batting_" + format_name + "_" + stat_name
            fielding_details[attribute_name] = row[attribute_name]
    return fielding_format_names, fielding_stat_names, fielding_details


def can_consider_trophy_stat(stat_name, all_trophies):
    return len([ke for ke in all_trophies.keys() if stat_name in all_trophies[ke].keys() and is_valid_string(all_trophies[ke][stat_name])]) != 0


def get_trophy_info(row):
    global all_attributes
    if not is_valid_string(row['Major_Trophies']):
        return [], [], {}
    all_trophies = ast.literal_eval(row['Major_Trophies'])
    if len(all_trophies) == 0:
        return [], [], {}
    trophy_names = [name for name in all_trophies.keys()
                                                       if len(all_trophies[name]) > 0]
    trophy_stat_names = []
    if len(trophy_names) == 0:
        return [], [], {}
    for ke in all_trophies[trophy_names[0]].keys():
        if can_consider_trophy_stat(ke, all_trophies):
            trophy_stat_names.append(ke)
    trophy_details = {}
    for key1 in all_trophies.keys():
        if key1 in trophy_names:
            trophy_details[key1] = {}
        else:
            continue
        for key2 in all_trophies[key1].keys():
            if key2 in trophy_stat_names:
                trophy_details[key1][key2] = all_trophies[key1][key2]
    # for i in range(len(trophy_names)):
    #     trophy_names[i] = getTransliteratedDescription(trophy_names[i])
    trophy_stat_names = [t_stat for t_stat in trophy_stat_names if not t_stat in ['tt', 'pr', 'hn', 'bbad']]
    return trophy_names, trophy_stat_names, trophy_details


def get_description_sums(row):
    global all_attributes

    bat_match_attrs = [
        att for att in all_attributes if "Batting_" in att and "Mat" in att]
    sum_batting_matches = sum([row[att]
                              for att in bat_match_attrs if row[att] > 0])

    bat_inns_attrs = [
        att for att in all_attributes if "Batting_" in att and "Inns" in att]
    sum_batting_innings = sum([row[att]
                              for att in bat_inns_attrs if row[att] > 0])

    bat_runs_attrs = [
        att for att in all_attributes if "Batting_" in att and "Runs" in att]
    sum_batting_runs = sum([row[att]
                           for att in bat_runs_attrs if row[att] > 0])

    bat_100s_attrs = [
        att for att in all_attributes if "Batting_" in att and "100s" in att]
    sum_batting_100s = sum([row[att]
                           for att in bat_100s_attrs if row[att] > 0])

    bat_50s_attrs = [
        att for att in all_attributes if "Batting_" in att and "50s" in att]
    sum_batting_50s = sum([row[att] for att in bat_50s_attrs if row[att] > 0])

    field_catch_attrs = [
        att for att in all_attributes if "Batting_" in att and "Ct" in att]
    sum_catches = sum([row[att] for att in field_catch_attrs if row[att] > 0])

    field_stump_attrs = [
        att for att in all_attributes if "Batting_" in att and "St" in att]
    sum_stumpings = sum([row[att]
                        for att in field_stump_attrs if row[att] > 0])

    sum_dismissals = sum_catches + sum_stumpings

    bowl_mat_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Mat" in att]
    sum_bowling_matches = sum([row[att]
                              for att in bowl_mat_attrs if row[att] > 0])

    bowl_inns_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Inns" in att]
    sum_bowling_innings = sum([row[att]
                              for att in bowl_inns_attrs if row[att] > 0])

    bowl_balls_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Balls" in att]
    sum_bowling_balls = sum([row[att]
                            for att in bowl_balls_attrs if row[att] > 0])

    bowl_wkt_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Wkts" in att]
    sum_wickets = sum([row[att] for att in bowl_wkt_attrs if row[att] > 0])

    return sum_batting_matches, sum_batting_innings, sum_batting_runs, sum_batting_100s, sum_batting_50s, sum_dismissals, sum_catches, sum_stumpings, sum_bowling_matches, sum_bowling_innings, sum_bowling_balls, sum_wickets


def get_start_year(span):
    if not is_valid_string(span):
        return -1
    try:
        break_up = span.split('-')
        return int(break_up[0])
    except:
        return -1


def did_retire(span):
    if not is_valid_string(span):
        return False
    try:
        break_up = span.split('-')
        return int(break_up[1]) < 2021
    except:
        return False
    
def get_debut_string(deb):
    # print(deb)
    if not is_valid_string(deb):
        return ''
    deb = deb.replace("vs", "versus")
    deb = deb.replace("Vs", "versus")
    deb = deb.replace("vS", "versus")
    deb = deb.replace("VS", "versus")
    occ = deb.find(" at ")
    if occ == -1:
        return getTransliteratedDescription(deb)
    deb = deb[:occ] + ', ' + deb[occ:]
    occ = deb.find(" at ")
    occ2 = deb.find("-")
    if occ2 == -1:
        occ2 = len(deb)
    curr_sub = deb[occ:occ2]
    # print(curr_sub)
    tokens = curr_sub.split(' ')
    tokens.append('lo ')
    deb = deb.replace(curr_sub, ' '.join(tokens[2:]))
    partition = deb.find('lo ')
    partition += 3
    return getTransliteratedDescription(deb[:partition]) + getTranslatedDescription(deb[partition:])


def getData(row):
    batting_format_names, batting_stat_names, batting_details = get_batting_info(row)
    bowling_format_names, bowling_stat_names, bowling_details = get_bowling_info(row)
    fielding_format_names, fielding_stat_names, fielding_details = get_fielding_info(row)
    trophy_names, trophy_stat_names, trophy_details = get_trophy_info(row)
    sum_batting_matches, sum_batting_innings, sum_batting_runs, sum_batting_100s, sum_batting_50s, sum_dismissals, sum_catches, sum_stumpings, sum_bowling_matches, sum_bowling_innings, sum_bowling_balls, sum_wickets = get_description_sums(row)
    data = {
        # {%- macro early_career(player_name, career_start_year, first_class_debut, listA_debut, T20_debut, T20I_debut, ODI_debut, test_debut) -%}
        'player_name': getTransliteratedDescription(row['Player_Name']).strip(),
        'gender': row['Gender'],
        'career_start_year': get_start_year(row['career_span']),
        'first_class_debut': row['FC Matches_debut'],
        'listA_debut': row['List A Matches_debut'],
        'T20_debut': row['T20 Matches_debut'],
        'T20I_debut': row['T20I Matches_debut'],
        'ODI_debut': row['ODI Matches_debut'],
        'test_debut': row['Test Matches_debut'],
        
        # {%- macro career_intro(player_name, player_role, nationality, teams, jersey_number, has_retired) -%}
        'player_role': row['Playing Role'],
        'nationality': get_nationality(row['Nationality']),
        'teams': row['Teams'],
        'jersey_number': row['Jersey_Number'],
        'has_retired': did_retire(row['career_span']),
        
        # {%- macro batting_description(player_name, sum_batting_matches, sum_batting_innings, sum_batting_runs, sum_batting_100s, 
        #                sum_batting_50s, test_batting_average, test_batting_strike_rate, ODI_batting_average, 
        #                ODI_batting_strike_rate, T20I_batting_average, T20I_batting_strike_rate) -%}
        
        'sum_batting_matches': sum_batting_matches,
        'sum_batting_innings': sum_batting_innings,
        'sum_batting_runs': sum_batting_runs, 
        'sum_batting_100s': sum_batting_100s, 
        'sum_batting_50s': sum_batting_50s,
        'test_batting_average': row['Batting_Test_Ave'],
        'test_batting_strike_rate': row['Batting_Test_SR'],
        'ODI_batting_average': row['Batting_ODI_Ave'],
        'ODI_batting_strike_rate': row['Batting_ODI_SR'],
        'T20I_batting_average': row['Batting_T20I_Ave'],
        'T20I_batting_strike_rate': row['Batting_T20I_SR'],
        
        # {%- macro fielding_description(sum_dismissals, sum_catches, sum_stumpings, is_wicketkeeper) -%}
        'sum_dismissals': sum_dismissals,
        'sum_catches': sum_catches,
        'sum_stumpings': sum_stumpings,
        
		# {%- macro bowling_description(player_name, sum_bowling_matches, sum_bowling_innings, sum_bowling_balls, sum_wickets, test_bowling_average,
		#                         test_bowling_economy, ODI_bowling_average, ODI_bowling_economy, T20I_bowling_average, T20I_bowling_economy,
		#                         bowling_10w_test, bowling_10w_FC) -%}
  
		'sum_bowling_matches': sum_bowling_matches,
  		'sum_bowling_innings': sum_bowling_innings, 
    	'sum_bowling_balls': sum_bowling_balls, 
     	'sum_wickets': sum_wickets,
        'test_bowling_average': row['Bowling_Test_Ave'],
        'test_bowling_economy': row['Bowling_Test_Econ'],
        'ODI_bowling_average': row['Bowling_ODI_Ave'],
        'ODI_bowling_economy': row['Bowling_ODI_Econ'],
        'T20I_bowling_average': row['Bowling_T20I_Ave'],
        'T20I_bowling_economy': row['Bowling_T20I_Econ'],
        'bowling_10w_test': row['Bowling_Test_10w'],
        'bowling_10w_FC': row['Bowling_FC_10w'],
        
        # {%- macro trophy_description(player_name, major_trophy_and_championship_names) -%}
        'major_trophy_and_championship_names': trophy_names,
        
        # Batting table
        'batting_format_names': batting_format_names,
        'batting_stat_names': batting_stat_names,
        'batting_details': batting_details,
        
        # Bowling table
        'bowling_format_names': bowling_format_names,
        'bowling_stat_names': bowling_stat_names,
        'bowling_details': bowling_details,
                
        # Fielding table
        'fielding_format_names': fielding_format_names,
        'fielding_stat_names': fielding_stat_names,
        'fielding_details': fielding_details,
                
        # Trophy table
        'trophy_names': trophy_names,
        'trophy_stat_names': trophy_stat_names, 
        'trophy_details': trophy_details,
        
        # References
        'all_ref': ast.literal_eval(row['References'])
	}
    
    return data

def main():
    global all_attributes
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template('life.j2')
    
    func_dict = {
        "stat_value": stat_value,
        "is_valid_string": is_valid_string,
        "shuffle_list": shuffle_list,
        "batting_description_func": batting_description_func,
        "bowling_description_func": bowling_description_func,
        "opening_sentence": opening_sentence,
        "batting_sent1": batting_sent1,
        "bowling_sent1": bowling_sent1,
        "bowling_sent2": bowling_sent2,
        "print_names": print_names,
        "get_teams_string": get_teams_string,
        "get_translation": get_translation,
        "get_matches_ref": get_matches_ref,
        "get_stats_ref": get_stats_ref,
        "getTransliteratedDescription": getTransliteratedDescription,
        "get_role": get_role,
        "get_debut_string": get_debut_string,
        "get_trophy_name": get_trophy_name,
        "get_trophy_names_list": get_trophy_names_list
    }
    template.globals.update(func_dict)
    
    with open('../data_collection/data/final_cricket_players_DF.pkl', 'rb') as f:
        cricket_players_DF = pickle.load(f)
        cricket_players_DF.fillna(value="nan", inplace=True)
        ids = cricket_players_DF.Cricinfo_id.tolist()
        all_attributes = cricket_players_DF.columns.tolist()
        ids = [54950]
        with open('life.txt', 'w') as fobj:
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
