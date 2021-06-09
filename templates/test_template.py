# place this file in the same dir of template file
# specify template name in main
# This works if template has the naming convention similar to dataset column Titles. 
# To change dataset row change iloc index in render 
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np

def render(template):
    a = pd.read_csv("cricket_players.csv")
    head = list(a.columns)
    val = dict(a.iloc[10].replace(np.nan ,"nan"))
    env = Environment(loader=FileSystemLoader("./"))
    jinja_template = env.get_template(template)
    template_string = jinja_template.render(val)
    return template_string

if __name__ == "__main__":
    print(render(template="template.j2"))