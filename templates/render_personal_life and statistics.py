from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
import ast 
#from deeptranslit import DeepTranslit
#trans = DeepTranslit('telugu')
from google.transliteration import transliterate_word , transliterate_text
from google_trans_new import google_translator
translator = google_translator()


def translate(var):
    res = list()
    for i in range(len(var)):
        if(var[i] != "nan"):
            if(i == 1):
                re = transliterate_text(list_str(var[i],0),lang_code="te")
                
            elif(i == 4):
                relation =str()
                rel = conv(var[i])
                for i in range(len(rel)):
                    try:
                        relation = relation + str(rel[i][0]) + str(rel[i][1])
                    except:
                        relation = relation + str(rel[i][0])
                re = translator.translate(relation,lang_tgt="te",lang_src="en")
            else:
                re = translator.translate(var[i],lang_tgt="te",lang_src="en")
            
            res.append(re)
        else:
            res.append(var[i])
    return res
def conv(t):
    literal = ast.literal_eval(t)
    return literal
def list_str(val,check_year):
    pr = str(val)
    
    p = pr.replace("[","")
    p = p.replace("]","")
    p = p.replace("'","")
    if(check_year == 1):
        p = p.replace("Y"," సంవత్సరాల")
        p = p.replace("D"," రోజులు")
        print(p)
    return p
def nan_check(x):
    if(x == -1 or x == "nan"):
        return "-"
    else:
        return x
def drop_row(dataset,e):
    row_drop = list()
    for i in range(15):
        d = dataset[e*i:e*i+e]
        p = set(d)
        if(len(p) == 1 and "-" in p):
            row_drop.append(i)
    return row_drop

def head_filter(l_1 , l_2):
    fin_l =list()
    for j in range(len(l_2)):
        if(j not in l_1):
            fin_l.append(l_2[j])
    return fin_l
def change_abbr(h):
    alpha= {
    "A":"ఏ",      
    "B":"బీ",
    "C":"సీ",  
    "D":"డి",
    "E":"ఇ",
    "F":"ఎఫ్",
    "G":"జీ",
    "H":"హెచ్",
    "I":"ఐ",
    "J":"జె",       
    "K":"కె",
    "L":"ఎల్",
    "M":"ఎం",
    "N":"ఎన్",
    "O":"ఓ",
    "P":"పి",
    "Q":"క్యూ",
    "R":"ఆర్",   
    "S":"ఎస్",
    "T":"టి",
    "U":"యూ",
    "V":"వీ",
    "W":"డబల్యూ",
    "X":"ఎక్స",
    "Y":"వై",
    "Z":"జీ"
    }
    n = ""
    for i in range(len(h)):
        print(h)
        if(ord(h[i]) >= 65 and ord(h[i]) <= 90):
            n = n + alpha[h[i].upper()] +"."
        else:
            n = n+ h[i]
    return n
def table_check(data):
    one = 0
    two = 0
    three = 0
    threshold = int(len(data)/3)
    for j in range(len(data)):
        data[j] = nan_check(data[j])
        if(j%3 == 0 and data[j] == "-"):
            one += 1
        if(j%3 == 1 and data[j] == "-"):
            two += 1
        if(j%3 == 2 and data[j] == "-"):
            three += 1
    li = [one,two,three]
    drop = list()
    data_1 = data
    for a in range(3):
        if(li[a] == threshold):
            drop.append(a+1)
            del data_1[a::3]
    return [data_1,drop]

def check(tag_name,a,b,c):
    if(a == -1 and b == -1 and c == -1 ):
        em = "-"
        return em
    else:
        a = nan_check(a)
        b = nan_check(b)
        c = nan_check(c)
        val = "| " +str(tag_name)+ " || " + str(a) + " || " + str(b) + " || " + str(c) + " |"
        return val
func_dict = {
    "check": check,
    "list_str":list_str,
    "nan_check" :nan_check,
    "table_check":table_check,
    "conv":conv,
    "head_filter":head_filter,
    "drop_row":drop_row,
    "translate":translate,
    "change_abbr":change_abbr
}

def render(template):
    a = pd.read_csv("final_cricket_players.csv")
    head = list(a.columns)
    val = a.iloc[5].replace(np.nan ,"nan")
    val = dict(val.fillna("nan"))
    env = Environment(loader=FileSystemLoader("./"))
    jinja_template = env.get_template(template)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render(val)
    return template_string

if __name__ == "__main__":
    print(render(template="personal_life.j2"))

    print(render(template="template.j2"))


