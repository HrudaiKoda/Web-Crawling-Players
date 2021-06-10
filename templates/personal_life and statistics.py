from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np

def list_str(val):
    pr = str(val)
    p = pr[1:-1]
    p = p.replace("'","")
    return p
def nan_check(x):
    if(x == -1):
        return "-"
    else:
        return x
def check(tag_name,a,b,c):
    if(a == -1 and b == -1 and c == -1 ):
        em = ""
        return em
    else:
        a = nan_check(a)
        b = nan_check(b)
        c = nan_check(c)
        val = "| " +str(tag_name)+ " || " + str(a) + " || " + str(b) + " || " + str(c) + " |"
        return val

func_dict = {
    "check": check,
    "list_str":list_str
}

def render(template):
    a = pd.read_csv("final.csv")
    head = list(a.columns)
    val = dict(a.iloc[5014].replace(np.nan ,"nan"))
    env = Environment(loader=FileSystemLoader("./"))
    jinja_template = env.get_template(template)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render(val)
    return template_string

if __name__ == "__main__":
    print(render(template="personal_life and statistics.j2"))