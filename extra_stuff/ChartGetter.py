import billboard
import json

date = "1972-12-21"
year = '1993'
fetch=True

chart = billboard.ChartData('hot-100', date)
print(chart)
print(chart[0].title, chart[0].artist)