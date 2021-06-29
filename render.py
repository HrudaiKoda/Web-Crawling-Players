import pickle
import pandas
from genXML import tewiki, writePage

infobox_and_overviews, personal_lives, professional_lives, statistics, records_and_awards, categories = {}, {}, {}, {}, {}, {}

with open('./templates/infobox_and_overviews.pkl', 'rb') as f:
    infobox_and_overviews = pickle.load(f)
with open('./templates/personal_lives.pkl', 'rb') as f:
    personal_lives = pickle.load(f)
with open('./templates/professional_lives.pkl', 'rb') as f:
    professional_lives = pickle.load(f)
with open('./templates/statistics.pkl', 'rb') as f:
    statistics = pickle.load(f)
with open('./templates/records_and_awards.pkl', 'rb') as f:
    records_and_awards = pickle.load(f)
with open('./templates/categories.pkl', 'rb') as f:
    categories = pickle.load(f)
    
with open('./data_collection/data/final_cricket_players_DF.pkl', 'rb') as f:
    cricket_players_DF = pickle.load(f)
    ids = cricket_players_DF.Cricinfo_id.tolist()
    with open('cricket_players.xml', 'w') as fobj:
        fobj.write(tewiki + '\n')
        for _id in ids:
            sp = '\n\n'
            row = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id']==_id]
            template_string = infobox_and_overviews[_id] + sp + personal_lives[_id] + sp + professional_lives[_id] + sp + statistics[_id] + sp + records_and_awards[_id] + sp + categories[_id]
            writePage(row.Player_Name.values[0], template_string, fobj)
        fobj.write('</mediawiki>')