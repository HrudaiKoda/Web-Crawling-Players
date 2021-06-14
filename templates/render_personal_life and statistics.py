from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
import ast 

def conv(t):
    return ast.literal_eval(t)
def list_str(val):
    pr = str(val)
    p = pr[1:-1]
    p = p.replace("'","")
    return p
def nan_check(x):
    if(x == -1 or x == "nan"):
        return "-"
    else:
        return x
def drop_row(dataset,e):
    print(dataset)
    print(e)
    row_drop = list()
    for i in range(15):
        d = dataset[e*i:e*i+e]
        p = set(d)
        print(d)
        if(len(p) == 1 and "-" in p):
            row_drop.append(i)
    return row_drop

def head_filter(l_1 , l_2):
    fin_l =list()
    for j in range(len(l_2)):
        if(j not in l_1):
            fin_l.append(l_2[j])
    return fin_l
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
    "drop_row":drop_row
}

def render(template):
    a = pd.read_csv("final_cricket_players.csv")
    head = list(a.columns)
    val = a.iloc[5014].replace(np.nan ,"nan")
    val = dict(val.fillna("nan"))
    env = Environment(loader=FileSystemLoader("./"))
    jinja_template = env.get_template(template)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render(val)
    return template_string

if __name__ == "__main__":
    print(render(template="personal_life and statistics.j2"))
