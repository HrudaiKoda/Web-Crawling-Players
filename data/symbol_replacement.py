import pandas as pd
import sweetviz as sv
b = pd.read_csv("final_cricket_players.csv")
b = b.replace(to_replace="-",value="")
b = b.replace(to_replace="[]",value="")
b = b.replace(to_replace="{}",value="")

report = sv.analyze(b, pairwise_analysis='off')
report.show_html()